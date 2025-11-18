Kimiti AI Platform - Backend

Overview
- FastAPI backend with pluggable vector store (pgvector/Qdrant/memory)
- Provider-agnostic LLM adapters (OpenAI, Ollama, vLLM-compatible)
- Celery worker for background jobs
- Alembic migrations, PostgreSQL with pgvector

Quick Start (Docker Compose)
1. Copy and adjust env:

```bash
cp backend/.env.example backend/.env
```

2. Build and start services:

```bash
docker compose up -d --build
```

- API: http://localhost:8000/healthz
- Frontend: http://localhost:3000
- Postgres: localhost:5432 (user/pass postgres/postgres)

Run Migrations
```bash
docker compose exec backend alembic upgrade head
```

Local Development (Windows PowerShell)
```powershell
python -m venv .venv; . .\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
setx DATABASE_URL "postgresql+psycopg://postgres:postgres@localhost:5432/kimiti"
uvicorn app.main:app --reload --app-dir backend
```

API Endpoints
- POST `/api/tenders/upload` (file upload)
- POST `/api/tenders/extract`
- POST `/api/tenders/generate-proposal`
- GET  `/api/tenders/{id}`
- POST `/api/chat`
- POST `/api/chat/with-context`
- POST `/api/chat/feedback`
- POST `/api/business/quote`
- GET  `/api/business/services`
- POST `/api/business/training`
- POST `/api/learn/reindex`
- POST `/api/learn/retrain`

Switching LLMs
- OpenAI (default): set `OPENAI_API_KEY` and `OPENAI_MODEL`
- vLLM/OpenAI-compatible: set `OPENAI_BASE_URL` to your endpoint
- Ollama: set `LLM_PROVIDER=ollama`, `INFERENCE_BASE_URL`, `INFERENCE_MODEL`

Switching Vector Stores
- `VECTOR_BACKEND=pgvector` (requires Postgres with pgvector)
- `VECTOR_BACKEND=qdrant` (requires Qdrant service)
- `VECTOR_BACKEND=memory` (development only)

Tests
```bash
cd backend
pytest -q
```
