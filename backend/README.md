# Backend Service

FastAPI-based backend for the RAG-Based Coding Assistant.

## Submodules
- `ingestion/`: Document loaders, code-aware parsers, and chunking pipeline.
- `indexing/`: Inverted index (TF-IDF) and dense vector index (FAISS) builders.
- `retrieval/`: Lexical, semantic, and hybrid retrieval search algorithms.
- `generation/`: Grounded LLM prompt builder and structured response generator.
- `eval/`: Retrieval evaluation metrics (Precision, Recall, F1, Precision@K, MAP, MRR).
- `api.py`: FastAPI server exposing `/health`, `/ingest`, `/query`, and `/eval` endpoints.
# 1. Activate the Python virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run the FastAPI server with Uvicorn
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
