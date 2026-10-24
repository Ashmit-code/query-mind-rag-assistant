"""
FastAPI REST API Server for Query Mind.
Endpoints:
- Ingestion (data/raw scan, file upload, URL download)
- Hybrid Retrieval & Answer Generation (TF-IDF + Qdrant + Ollama + DuckDuckGo fallback)
- Ollama & Knowledge Base Status
"""

import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

load_dotenv(dotenv_path=ROOT_DIR / ".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("query-mind-api")

from backend.ingestion.loader import load_directory, load_file
from backend.ingestion.chunker import process_and_save_chunks, load_saved_chunks
from backend.indexing.tfidf_index import get_tfidf_index, build_and_save_tfidf
from backend.indexing.qdrant_index import get_qdrant_index
from backend.retrieval.retriever import (
    retrieve_with_fallback,
    retrieve_local,
    ensure_indices_ready,
    UnifiedSearchResult,
    RetrievalResult,
)
from backend.generation.generator import generate_answer, GeneratedResponse

app = FastAPI(
    title="QUERY MIND Coding Assistant API",
    description="Information Retrieval RAG system with TF-IDF, Qdrant Vector Search, Ollama LLM, and Web Fallback.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Pydantic Schemas ────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    query: str = Field(..., description="User query or coding question")
    mode: str = Field(default="hybrid", description="Retrieval mode: 'hybrid', 'semantic', or 'tfidf'")
    top_k: int = Field(default=5, ge=1, le=20)
    allow_web_fallback: bool = Field(default=True, description="Enable DuckDuckGo fallback when local score is low")
    ollama_model: Optional[str] = Field(default=None, description="Target Ollama model name")


class IngestResponse(BaseModel):
    status: str
    documents_loaded: int
    chunks_created: int
    indices_updated: bool


class UrlIngestRequest(BaseModel):
    url: str = Field(..., description="Public URL of text/markdown/code file")


# ─── Startup Hook ────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup_event():
    """Ensure TF-IDF and Qdrant indices are initialized on startup."""
    try:
        index_dir = ROOT_DIR / "data/indices"
        chunks_path = ROOT_DIR / "data/processed/chunks.json"
        ensure_indices_ready(index_dir=index_dir, chunks_path=chunks_path)
    except Exception as e:
        logger.warning(f"Startup notice: Index loading deferred ({e})")


# ─── Health & Knowledge Base Stats ───────────────────────────────────────────

@app.get("/health", tags=["System"])
def health_check():
    qdrant = get_qdrant_index()
    tfidf = get_tfidf_index()
    return {
        "status": "ok",
        "service": "querymind",
        "qdrant_mode": "cloud" if qdrant.url else "local",
        "qdrant_points": qdrant.count(),
        "tfidf_ready": tfidf.vectorizer is not None,
    }


@app.get("/knowledge/stats", tags=["System"])
def knowledge_stats():
    qdrant = get_qdrant_index()
    tfidf = get_tfidf_index()
    raw_dir = ROOT_DIR / "data/raw"
    raw_docs = len(list(raw_dir.rglob("*.*"))) if raw_dir.exists() else 0

    return {
        "raw_files": raw_docs,
        "qdrant_points": qdrant.count(),
        "tfidf_terms": len(tfidf.vectorizer.vocabulary_) if tfidf.vectorizer else 0,
        "qdrant_target": qdrant.url or "local storage",
    }


# ─── Ingestion Endpoints ──────────────────────────────────────────────────────

def _reindex_all_chunks(chunks):
    """Rebuilds TF-IDF in-memory and indexes all chunks in Qdrant."""
    index_dir = ROOT_DIR / "data/indices"
    build_and_save_tfidf(chunks, index_dir)
    qdrant_idx = get_qdrant_index()
    qdrant_idx.clear()
    qdrant_idx.index_chunks(chunks)


@app.post("/ingest", response_model=IngestResponse, tags=["Ingestion"])
def ingest_documents():
    """Ingests all files in data/raw and updates TF-IDF and Qdrant."""
    raw_dir = ROOT_DIR / "data/raw"
    processed_file = ROOT_DIR / "data/processed/chunks.json"

    docs = load_directory(raw_dir)
    if not docs:
        raise HTTPException(status_code=400, detail="No valid raw documents found in data/raw.")

    chunks = process_and_save_chunks(docs, processed_file)
    _reindex_all_chunks(chunks)

    return IngestResponse(
        status="success",
        documents_loaded=len(docs),
        chunks_created=len(chunks),
        indices_updated=True,
    )


@app.post("/ingest/file", response_model=IngestResponse, tags=["Ingestion"])
async def ingest_file(file: UploadFile = File(...)):
    """Uploads a document and re-indexes the entire knowledge base."""
    allowed_exts = {
        ".md", ".markdown", ".txt", ".py", ".js", ".ts", ".pdf",
        ".java", ".cpp", ".cc", ".cxx", ".c", ".h", ".hpp",
        ".html", ".htm", ".css"
    }
    suffix = Path(file.filename or "upload.txt").suffix.lower()
    if suffix not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Allowed: {', '.join(sorted(allowed_exts))}",
        )

    upload_dir = ROOT_DIR / "data/raw/uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    save_path = upload_dir / (file.filename or f"upload{suffix}")

    try:
        with open(save_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    raw_dir = ROOT_DIR / "data/raw"
    processed_file = ROOT_DIR / "data/processed/chunks.json"
    docs = load_directory(raw_dir)
    chunks = process_and_save_chunks(docs, processed_file)
    _reindex_all_chunks(chunks)

    return IngestResponse(
        status="success",
        documents_loaded=len(docs),
        chunks_created=len(chunks),
        indices_updated=True,
    )


@app.post("/ingest/url", response_model=IngestResponse, tags=["Ingestion"])
def ingest_url(req: UrlIngestRequest):
    """Downloads a document from a URL and updates indices."""
    import requests as http_req

    url = req.url.strip()
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")

    try:
        resp = http_req.get(url, timeout=30, headers={"User-Agent": "QueryMind/2.0"})
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")

    url_path = url.split("?")[0].rstrip("/")
    filename = url_path.split("/")[-1] or "downloaded_doc"
    if "." not in filename:
        filename += ".md"

    upload_dir = ROOT_DIR / "data/raw/uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    save_path = upload_dir / filename

    try:
        save_path.write_bytes(resp.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    raw_dir = ROOT_DIR / "data/raw"
    processed_file = ROOT_DIR / "data/processed/chunks.json"
    docs = load_directory(raw_dir)
    chunks = process_and_save_chunks(docs, processed_file)
    _reindex_all_chunks(chunks)

    return IngestResponse(
        status="success",
        documents_loaded=len(docs),
        chunks_created=len(chunks),
        indices_updated=True,
    )


# ─── Query & Generation Pipeline ──────────────────────────────────────────────

@app.post("/query", response_model=GeneratedResponse, tags=["Pipeline"])
def query_pipeline(req: QueryRequest):
    """
    Full RAG pipeline:
    1. Hybrid retrieval (TF-IDF + Qdrant)
    2. Score threshold check & DuckDuckGo fallback if score is low
    3. Grounded Markdown generation via Ollama (or deterministic extractor)
    """
    clean_query = req.query.strip()
    if not clean_query:
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")

    try:
        search_res = retrieve_with_fallback(
            query=clean_query,
            mode=req.mode,
            top_k=req.top_k,
            allow_web_fallback=req.allow_web_fallback,
        )
        answer = generate_answer(
            search_result=search_res,
            model_name=req.ollama_model,
        )
        return answer
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/retrieve", response_model=UnifiedSearchResult, tags=["Pipeline"])
def retrieve_only(req: QueryRequest):
    """Retrieval-only endpoint for debugging and inspection."""
    clean_query = req.query.strip()
    if not clean_query:
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")

    return retrieve_with_fallback(
        query=clean_query,
        mode=req.mode,
        top_k=req.top_k,
        allow_web_fallback=req.allow_web_fallback,
    )


# ─── Ollama Service Endpoints ─────────────────────────────────────────────────


@app.get("/ollama/status", tags=["Ollama"])
def ollama_status():
    """Checks whether local Ollama is active."""
    import requests as http_req
    try:
        resp = http_req.get("http://localhost:11434/api/tags", timeout=3)
        if resp.status_code == 200:
            return {"running": True, "message": "Ollama is running"}
        return {"running": False, "message": f"Ollama HTTP {resp.status_code}"}
    except Exception as e:
        return {"running": False, "message": f"Ollama unreachable: {str(e)}"}


@app.get("/ollama/models", tags=["Ollama"])
def ollama_models():
    """Lists installed models available in Ollama."""
    import requests as http_req
    try:
        resp = http_req.get("http://localhost:11434/api/tags", timeout=5)
        if resp.status_code != 200:
            return {"models": [], "error": f"Ollama HTTP {resp.status_code}"}
        data = resp.json()
        models = [m.get("name", "") for m in data.get("models", [])]
        return {"models": models}
    except Exception as e:
        return {"models": [], "error": str(e)}
