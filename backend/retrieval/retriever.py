"""
Retrieval and Ranking Engine for Information Retrieval.
Combines Lexical (TF-IDF with code-aware tokenization) and Dense Semantic (Qdrant).
Includes calibrated score thresholds and automatic DuckDuckGo web search fallback.
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

from backend.ingestion.chunker import Chunk, load_saved_chunks
from backend.indexing.tfidf_index import get_tfidf_index, build_and_save_tfidf
from backend.indexing.qdrant_index import get_qdrant_index
from backend.retrieval.web_search import search_web, format_web_context

logger = logging.getLogger(__name__)

# Calibrated minimum relevance thresholds for local retrieval
RELEVANCE_THRESHOLDS: Dict[str, float] = {
    "tfidf": 0.06,
    "semantic": 0.45,
    "hybrid": 0.32,
}


class RetrievalResult(BaseModel):
    chunk_id: str
    doc_id: str
    score: float
    rank: int
    source: str
    filename: str
    section: str
    language: str
    topic: str
    text: str
    has_code: bool


class UnifiedSearchResult(BaseModel):
    query: str
    mode: str
    source_type: str  # 'local', 'web', or 'none'
    local_results: List[RetrievalResult] = []
    web_results: List[Dict[str, str]] = []
    formatted_context: str = ""
    max_score: float = 0.0


def ensure_indices_ready(
    index_dir: str | Path = "data/indices",
    chunks_path: str | Path = "data/processed/chunks.json",
):
    """
    Ensures TF-IDF and Qdrant are loaded/indexed.
    """
    tfidf_idx = get_tfidf_index()
    qdrant_idx = get_qdrant_index()

    chunks = []
    if tfidf_idx.vectorizer is None:
        if not tfidf_idx.load(index_dir):
            chunks = load_saved_chunks(chunks_path)
            if chunks:
                logger.info(f"Building TF-IDF index from {len(chunks)} chunks...")
                tfidf_idx.build(chunks)
                tfidf_idx.save(index_dir)

    if qdrant_idx.count() == 0:
        if not chunks:
            chunks = load_saved_chunks(chunks_path)
        if chunks:
            logger.info(f"Indexing {len(chunks)} chunks in Qdrant...")
            qdrant_idx.index_chunks(chunks)


def retrieve_local(
    query: str,
    mode: str = "hybrid",
    top_k: int = 5,
    alpha: float = 0.5,
    index_dir: str | Path = "data/indices",
) -> List[RetrievalResult]:
    """
    Searches local knowledge base using TF-IDF, Qdrant semantic, or Hybrid.
    """
    ensure_indices_ready(index_dir=index_dir)
    tfidf_idx = get_tfidf_index()
    qdrant_idx = get_qdrant_index()

    mode = mode.lower().strip()

    if mode == "tfidf":
        if tfidf_idx.vectorizer is None:
            return []
        raw = tfidf_idx.search(query, top_k=top_k)
        return [
            RetrievalResult(
                chunk_id=c.chunk_id,
                doc_id=c.doc_id,
                score=round(float(score), 4),
                rank=i + 1,
                source=c.source,
                filename=c.filename,
                section=c.section,
                language=c.language,
                topic=c.topic,
                text=c.text,
                has_code=c.has_code,
            )
            for i, (c, score) in enumerate(raw)
        ]

    elif mode in ["semantic", "dense"]:
        raw = qdrant_idx.search(query, top_k=top_k)
        return [
            RetrievalResult(
                chunk_id=c.chunk_id,
                doc_id=c.doc_id,
                score=round(float(score), 4),
                rank=i + 1,
                source=c.source,
                filename=c.filename,
                section=c.section,
                language=c.language,
                topic=c.topic,
                text=c.text,
                has_code=c.has_code,
            )
            for i, (c, score) in enumerate(raw)
        ]

    elif mode == "hybrid":
        fetch_k = max(top_k * 3, 10)
        tfidf_matches = tfidf_idx.search(query, top_k=fetch_k) if tfidf_idx.vectorizer else []
        dense_matches = qdrant_idx.search(query, top_k=fetch_k)

        tfidf_scores = {c.chunk_id: s for c, s in tfidf_matches}
        dense_scores = {c.chunk_id: s for c, s in dense_matches}

        chunks_map: Dict[str, Chunk] = {}
        for c, _ in tfidf_matches:
            chunks_map[c.chunk_id] = c
        for c, _ in dense_matches:
            chunks_map[c.chunk_id] = c

        all_ids = set(tfidf_scores.keys()) | set(dense_scores.keys())
        hybrid_scores: Dict[str, float] = {}

        for cid in all_ids:
            s_lex = tfidf_scores.get(cid, 0.0)
            s_sem = dense_scores.get(cid, 0.0)
            # Calibrated combination
            combined = alpha * s_lex + (1.0 - alpha) * s_sem
            if s_lex > 0.10 and s_sem > 0.35:
                combined += 0.05  # agreement boost
            hybrid_scores[cid] = combined

        sorted_cids = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for i, (cid, score) in enumerate(sorted_cids):
            c = chunks_map[cid]
            results.append(
                RetrievalResult(
                    chunk_id=c.chunk_id,
                    doc_id=c.doc_id,
                    score=round(float(score), 4),
                    rank=i + 1,
                    source=c.source,
                    filename=c.filename,
                    section=c.section,
                    language=c.language,
                    topic=c.topic,
                    text=c.text,
                    has_code=c.has_code,
                )
            )
        return results
    else:
        raise ValueError(f"Unknown retrieval mode: {mode}. Must be 'tfidf', 'semantic', or 'hybrid'.")


def retrieve_with_fallback(
    query: str,
    mode: str = "hybrid",
    top_k: int = 5,
    allow_web_fallback: bool = True,
) -> UnifiedSearchResult:
    """
    Main retrieval pipeline:
    1. Retrieve local knowledge base chunks.
    2. Check if top score meets RELEVANCE_THRESHOLDS.
    3. If relevance passes, returns local results.
    4. If relevance fails and fallback enabled, queries DuckDuckGo.
    """
    local_results = retrieve_local(query=query, mode=mode, top_k=top_k)
    threshold = RELEVANCE_THRESHOLDS.get(mode, 0.30)
    max_score = max([r.score for r in local_results], default=0.0)

    # Check if local results meet confidence threshold
    if local_results and max_score >= threshold:
        context_parts = []
        for r in local_results:
            source_tag = f"[{r.filename} - {r.section}]" if r.section else f"[{r.filename}]"
            context_parts.append(f"{source_tag}\n{r.text}")
        formatted_context = "\n\n---\n\n".join(context_parts)

        return UnifiedSearchResult(
            query=query,
            mode=mode,
            source_type="local",
            local_results=local_results,
            formatted_context=formatted_context,
            max_score=max_score,
        )

    # Fallback to DuckDuckGo web search
    if allow_web_fallback:
        logger.info(
            f"Local retrieval score ({max_score:.4f} < {threshold}) below threshold for '{query}'. "
            f"Invoking DuckDuckGo web search fallback..."
        )
        web_res = search_web(query, max_results=4)
        if web_res:
            formatted_web = format_web_context(web_res)
            return UnifiedSearchResult(
                query=query,
                mode=mode,
                source_type="web",
                local_results=[],
                web_results=web_res,
                formatted_context=formatted_web,
                max_score=max_score,
            )

    return UnifiedSearchResult(
        query=query,
        mode=mode,
        source_type="none",
        local_results=[],
        web_results=[],
        formatted_context="",
        max_score=max_score,
    )
