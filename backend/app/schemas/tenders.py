from pydantic import BaseModel, Field
from typing import List, Optional, Any

class TenderUploadResponse(BaseModel):
    document_id: int
    title: Optional[str]

class TenderExtractRequest(BaseModel):
    document_id: int

class BoqItem(BaseModel):
    item: str
    quantity: float
    unit: str
    rate: float

class TenderExtractResponse(BaseModel):
    tender_id: int
    summary: str
    boq: List[BoqItem] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)

class TenderGenerateProposalRequest(BaseModel):
    tender_id: int

class TenderResponse(BaseModel):
    id: int
    document_id: int
    summary: Optional[str]
    boq: List[Any] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
