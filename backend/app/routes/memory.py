from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from ..services.embedding_service import EmbeddingService
from ..vector.pg import PGVectorStore
from ..vector.qdrant import QdrantVectorStore
from ..vector.memory import InMemoryVectorStore
from ..utils.settings import settings

router = APIRouter()

class MemoryItem(BaseModel):
    id: int
    key: str
    value: str


def _get_vector_store():
    if settings.vector_backend == "pgvector":
        return PGVectorStore()
    if settings.vector_backend == "qdrant":
        return QdrantVectorStore()
    return InMemoryVectorStore()

@router.post("/store")
async def store(item: MemoryItem):
    emb = EmbeddingService()
    vs = _get_vector_store()
    payload = emb.embed_texts([
        ("memory", {"id": item.id, "title": item.key, "content": item.value})
    ])
    vs.upsert(payload)
    return {"status": "ok"}
