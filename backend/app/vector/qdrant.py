from __future__ import annotations
from typing import List, Tuple, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from ..utils.settings import settings

class QdrantVectorStore:
    def __init__(self, collection: str = "kimiti_docs"):
        self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
        self.collection = collection
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.client.get_collection(self.collection)
        except Exception:
            self.client.recreate_collection(
                collection_name=self.collection,
                vectors_config=qm.VectorParams(size=1536, distance=qm.Distance.COSINE),
            )

    def upsert(self, items: List[Tuple[str, List[float], dict]]):
        points: List[qm.PointStruct] = []
        for kind, emb, meta in items:
            payload = {"kind": kind, **meta}
            points.append(qm.PointStruct(id=payload.get("id"), vector=emb, payload=payload))
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, query: List[float], top_k: int = 5, filter: Optional[dict] = None) -> List[dict]:
        flt = None
        if filter:
            must = [qm.FieldCondition(key=k, match=qm.MatchValue(value=v)) for k, v in filter.items()]
            flt = qm.Filter(must=must)
        res = self.client.search(collection_name=self.collection, query_vector=query, limit=top_k, query_filter=flt)
        return [
            {"kind": p.payload.get("kind"), "id": p.payload.get("id"), "score": float(p.score), "content": p.payload.get("content"), "title": p.payload.get("title")}
            for p in res
        ]
