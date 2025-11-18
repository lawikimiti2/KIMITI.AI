from __future__ import annotations
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..services.chat_service import ChatService
from ..llm.clients import EmbeddingClient
from ..vector.pg import PGVectorStore
from ..vector.qdrant import QdrantVectorStore
from ..vector.memory import InMemoryVectorStore
from ..utils.settings import settings
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models.models import Memory

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatWithContextRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    chat_message_id: int | None = None
    correction: str


def _get_vector_store():
    if settings.vector_backend == "pgvector":
        return PGVectorStore()
    if settings.vector_backend == "qdrant":
        return QdrantVectorStore()
    return InMemoryVectorStore()

@router.post("/")
async def chat(req: ChatRequest):
    svc = ChatService()
    return {"answer": svc.chat_simple(req.query)}

@router.post("/with-context")
async def chat_with_context(req: ChatWithContextRequest):
    embed = EmbeddingClient()
    vs = _get_vector_store()
    qvec = embed.embed([req.query])[0]
    hits = vs.search(qvec, top_k=5)
    context = "\n\n".join([f"{h.get('title')}: {h.get('content')}" for h in hits])
    svc = ChatService()
    return {"answer": svc.chat_with_context(req.query, context=context), "context_used": hits}

@router.post("/feedback")
async def feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    # Store correction into memory and index it for future retrieval
    mem = Memory(key="feedback", value=req.correction, meta={})
    db.add(mem)
    db.commit()
    db.refresh(mem)

    embed = EmbeddingClient()
    vs = _get_vector_store()
    payload = [("memory", {"id": mem.id, "title": mem.key, "content": mem.value})]
    vectors = embed.embed([mem.value])
    vs.upsert([(payload[0][0], vectors[0], payload[0][1])])
    return {"status": "stored", "memory_id": mem.id}
