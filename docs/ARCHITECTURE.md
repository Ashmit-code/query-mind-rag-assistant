# Architecture

Query Mind is organized as a compact full-stack application with a Python FastAPI backend and a React frontend.

## Request flow

1. The frontend sends a user question to the backend API.
2. The backend ingests or retrieves source chunks from the knowledge store.
3. Retrieval runs in hybrid mode: lexical TF-IDF + dense vector search.
4. The generator builds a grounded prompt and calls Ollama locally.
5. The response is rendered in the frontend with source context and code formatting.

## Backend modules

- `backend/api.py`: FastAPI routes and orchestration layer
- `backend/ingestion/`: parsing, chunking, and document loading
- `backend/indexing/`: TF-IDF and Qdrant indexing logic
- `backend/retrieval/`: search and ranking code
- `backend/generation/`: prompt construction and LLM integration
- `backend/tests/`: regression tests for the RAG pipeline

## Data flow

- `data/raw/` contains source documents used for indexing
- `data/processed/` is the chunked and normalized corpus
- Local Qdrant persistence stores embeddings and metadata
- `backend/requirements.txt` defines the Python runtime dependencies

## Frontend

The frontend is a Vite React application that handles chat UX, retrieval mode selection, code rendering, and source panels. It communicates with the API over HTTP.

## Operational notes

- The project defaults to local development with a local Qdrant path and local Ollama host.
- Production deployments can use a remote Qdrant cluster and environment-based configuration.
- The repo intentionally keeps operational configuration in `.env` and example settings in `.env.example`.
