from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models.models import Document, Tender
from ..schemas.tenders import (
    TenderUploadResponse, TenderExtractRequest, TenderExtractResponse,
    TenderGenerateProposalRequest, TenderResponse,
)
from ..parsers.pdf import extract_pdf
from ..parsers.word import extract_docx
from ..parsers.excel import extract_xlsx
from ..services.tender_service import TenderService
from ..services.embedding_service import EmbeddingService
from ..utils.settings import settings
from ..vector.pg import PGVectorStore
from ..vector.qdrant import QdrantVectorStore
from ..vector.memory import InMemoryVectorStore

router = APIRouter()

def _get_vector_store():
    if settings.vector_backend == "pgvector":
        return PGVectorStore()
    if settings.vector_backend == "qdrant":
        return QdrantVectorStore()
    return InMemoryVectorStore()

@router.post("/upload", response_model=TenderUploadResponse)
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.filename.endswith(".pdf"):
        content = extract_pdf(file.file)
    elif file.filename.endswith(".docx"):
        content = extract_docx(file.file)
    elif file.filename.endswith(".xlsx"):
        content = extract_xlsx(file.file)
    else:
        content = (await file.read()).decode("utf-8", errors="ignore")

    doc = Document(doc_type="tender", title=file.filename, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Embed & index
    emb = EmbeddingService()
    vs = _get_vector_store()
    payload = emb.embed_texts([( "document", {"id": doc.id, "title": doc.title, "content": content} )])
    vs.upsert(payload)

    return TenderUploadResponse(document_id=doc.id, title=doc.title)

@router.post("/extract", response_model=TenderExtractResponse)
async def extract(req: TenderExtractRequest, db: Session = Depends(get_db)):
    doc = db.query(Document).get(req.document_id)  # type: ignore
    if not doc:
        raise HTTPException(404, "Document not found")
    svc = TenderService()
    summary = svc.summarize(doc.content or "")
    boq = svc.parse_boq(doc.content or "")
    risks = svc.analyze_risks(doc.content or "")

    tender = Tender(document_id=doc.id, summary=summary, boq=boq, risks=risks)
    db.add(tender)
    db.commit()
    db.refresh(tender)

    return TenderExtractResponse(tender_id=tender.id, summary=summary, boq=boq, risks=risks)

@router.post("/generate-proposal")
async def generate_proposal(req: TenderGenerateProposalRequest, db: Session = Depends(get_db)):
    tender = db.query(Tender).get(req.tender_id)  # type: ignore
    if not tender:
        raise HTTPException(404, "Tender not found")
    svc = TenderService()
    content = svc.proposal(tender.summary or "")
    return {"proposal": content}

@router.get("/{id}", response_model=TenderResponse)
async def get_tender(id: int, db: Session = Depends(get_db)):
    tender = db.query(Tender).get(id)  # type: ignore
    if not tender:
        raise HTTPException(404, "Tender not found")
    return TenderResponse(
        id=tender.id,
        document_id=tender.document_id,
        summary=tender.summary,
        boq=tender.boq or [],
        risks=tender.risks or [],
    )
