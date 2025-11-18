from __future__ import annotations
from typing import List, Tuple, Optional

class VectorStore:
    def upsert(self, items: List[Tuple[str, List[float], dict]]):
        raise NotImplementedError

    def search(self, query: List[float], top_k: int = 5, filter: Optional[dict] = None) -> List[dict]:
        raise NotImplementedError
