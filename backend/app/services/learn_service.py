from __future__ import annotations
from ..llm.clients import EmbeddingClient
from ..vector.pg import PGVectorStore
from ..vector.qdrant import QdrantVectorStore
from ..vector.memory import InMemoryVectorStore
from ..utils.settings import settings

class LearnService:
    def __init__(self):
        self.embed = EmbeddingClient()
        if settings.vector_backend == "pgvector":
            self.vs = PGVectorStore()
        elif settings.vector_backend == "qdrant":
            self.vs = QdrantVectorStore()
        else:
            self.vs = InMemoryVectorStore()

    def reindex(self, items):
        vectors = self.embed.embed([i["content"] for i in items])
        payload = []
        for item, vec in zip(items, vectors):
            payload.append((item.get("kind", "document"), vec, item))
        self.vs.upsert(payload)
