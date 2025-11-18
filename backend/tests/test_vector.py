from __future__ import annotations
from app.vector.memory import InMemoryVectorStore

def test_memory_vector_store_search():
    vs = InMemoryVectorStore()
    vec = [0.0] * 4
    vec[0] = 1.0
    vs.upsert([
        ("memory", vec, {"id": 1, "title": "A", "content": "alpha"}),
        ("memory", [0.0,1.0,0.0,0.0], {"id": 2, "title": "B", "content": "beta"}),
    ])
    res = vs.search([1.0,0.0,0.0,0.0], top_k=1)
    assert res[0]["id"] == 1
