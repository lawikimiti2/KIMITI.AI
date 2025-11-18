from __future__ import annotations
from typing import List, Tuple, Optional

class InMemoryVectorStore:
    def __init__(self):
        self.items: List[Tuple[str, List[float], dict]] = []

    def upsert(self, items: List[Tuple[str, List[float], dict]]):
        # replace by id
        ids = {meta["id"] for _, _, meta in items}
        self.items = [row for row in self.items if row[2].get("id") not in ids]
        self.items.extend(items)

    def search(self, query: List[float], top_k: int = 5, filter: Optional[dict] = None) -> List[dict]:
        def cos(a: List[float], b: List[float]) -> float:
            import math
            dot = sum(x*y for x, y in zip(a, b))
            na = math.sqrt(sum(x*x for x in a)) or 1.0
            nb = math.sqrt(sum(y*y for y in b)) or 1.0
            return dot / (na * nb)

        rows = []
        for kind, emb, meta in self.items:
            if filter and not all(meta.get(k) == v for k, v in filter.items()):
                continue
            rows.append({
                "kind": kind,
                "id": meta.get("id"),
                "score": cos(query, emb),
                "content": meta.get("content"),
                "title": meta.get("title"),
            })
        rows.sort(key=lambda r: r["score"], reverse=True)
        return rows[:top_k]
