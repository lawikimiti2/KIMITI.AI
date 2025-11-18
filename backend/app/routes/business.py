from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from ..services.chat_service import ChatService

router = APIRouter()

class QuoteRequest(BaseModel):
    description: str

class TrainingRequest(BaseModel):
    topic: str

@router.get("/services")
async def services():
    return {"services": [
        {"name": "Tender Processing", "id": "tender"},
        {"name": "Document Analysis", "id": "doc"},
        {"name": "Business Automation", "id": "automation"},
        {"name": "Technical Support", "id": "support"},
        {"name": "Training Module Generation", "id": "training"},
    ]}

@router.post("/quote")
async def quote(req: QuoteRequest):
    svc = ChatService()
    prompt = f"Create a rough costed quote for: {req.description}."
    return {"quote": svc.chat_simple(prompt)}

@router.post("/training")
async def training(req: TrainingRequest):
    svc = ChatService()
    prompt = f"Generate a training module outline for: {req.topic}."
    return {"training": svc.chat_simple(prompt)}
