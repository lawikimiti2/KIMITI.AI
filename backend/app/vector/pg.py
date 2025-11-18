from __future__ import annotations
from typing import List, Tuple, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..models.models import Document, Memory
from ..db.session import SessionLocal

class PGVectorStore:
    def __init__(self, session: Optional[Session] = None):
        self.session = session or SessionLocal()

    def upsert(self, items: List[Tuple[str, List[float], dict]]):
        for kind, emb, meta in items:
            if kind == "document":
                doc = self.session.query(Document).get(meta["id"])  # type: ignore
                if doc:
                    doc.embedding = emb
            elif kind == "memory":
                mem = self.session.query(Memory).get(meta["id"])  # type: ignore
                if mem:
                    mem.embedding = emb
        self.session.commit()

    def search(self, query: List[float], top_k: int = 5, filter: Optional[dict] = None) -> List[dict]:
        # Search documents and memory; return combined results
        results: List[dict] = []
        q = text("""
            SELECT id, title, content, 1 - (embedding <=> :q) AS score, 'document' AS kind
            FROM documents
            WHERE embedding IS NOT NULL
            ORDER BY embedding <-> :q
            LIMIT :k
        """)
        for row in self.session.execute(q, {"q": query, "k": top_k}).mappings():
            results.append({"kind": row["kind"], "id": row["id"], "score": float(row["score"]), "content": row["content"], "title": row["title"]})

        q2 = text("""
            SELECT id, key, value, 1 - (embedding <=> :q) AS score, 'memory' AS kind
            FROM memory
            WHERE embedding IS NOT NULL
            ORDER BY embedding <-> :q
            LIMIT :k
        """)
        for row in self.session.execute(q2, {"q": query, "k": top_k}).mappings():
            results.append({"kind": row["kind"], "id": row["id"], "score": float(row["score"]), "content": row["value"], "title": row["key"]})

        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]
