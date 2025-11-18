from __future__ import annotations
from typing import List, Tuple
from ..llm.clients import EmbeddingClient

class EmbeddingService:
    def __init__(self):
        self.client = EmbeddingClient()

    def embed_texts(self, pairs: List[Tuple[str, dict]]) -> List[Tuple[str, List[float], dict]]:
        texts = [meta.get("content", "") for _, meta in pairs]
        vectors = self.client.embed(texts)
        out = []
        for (kind, meta), vec in zip(pairs, vectors):
            out.append((kind, vec, meta))
        return out
