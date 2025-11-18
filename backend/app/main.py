from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils.settings import settings
from .routes import tenders, chat, business, train, memory

app = FastAPI(title="Kimiti AI Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tenders.router, prefix="/api/tenders", tags=["tenders"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(business.router, prefix="/api/business", tags=["business"])
app.include_router(train.router, prefix="/api/learn", tags=["learn"])
app.include_router(memory.router, prefix="/api/memory", tags=["memory"])

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
