from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ..services.learn_service import LearnService

router = APIRouter()


class ReindexItem(BaseModel):
    id: int
    kind: str = "document"  # document | memory
    title: str | None = None
    content: str


class ReindexRequest(BaseModel):
    items: List[ReindexItem]


@router.post("/reindex")
async def reindex(req: ReindexRequest):
    svc = LearnService()
    payload: List[Dict[str, Any]] = []
    for it in req.items:
        payload.append(
            {
                "id": it.id,
                "kind": it.kind,
                "title": it.title,
                "content": it.content,
            }
        )
    svc.reindex(payload)
    return {"indexed": len(payload)}


@router.post("/retrain")
async def retrain():
    # Placeholder: hook Kubeflow or a training pipeline here
    return {"status": "accepted"}

