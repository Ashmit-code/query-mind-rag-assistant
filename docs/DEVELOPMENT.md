# Development Guide

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
Copy-Item .env.example .env
```

## Backend commands

```powershell
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
python -m pytest backend/tests/test_rag_pipeline.py -v
```

## Frontend commands

```powershell
npm install --prefix frontend
npm run dev --prefix frontend
npm run build --prefix frontend
```

## Useful checks

- API docs: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`
- App UI: `http://localhost:5173`

## Re-indexing and troubleshooting

- If local vector state is stale, clear the generated data directories and re-ingest source documents.
- Confirm Ollama is running and the target model is available before generating answers.
- Verify `.env` values match the local machine if using custom network or remote Qdrant settings.
