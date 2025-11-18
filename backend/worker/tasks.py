from __future__ import annotations
from .celery_app import celery_app
from app.services.learn_service import LearnService

@celery_app.task
def reindex_items(items: list[dict]):
    svc = LearnService()
    svc.reindex(items)
    return {"count": len(items)}
