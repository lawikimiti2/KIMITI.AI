from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from .base import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    doc_type = Column(String(50), index=True)
    title = Column(String(255))
    content = Column(Text)
    meta = Column("metadata", JSONB, default=dict)
    embedding = Column(Vector(1536), nullable=True)

class Tender(Base):
    __tablename__ = "tenders"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    summary = Column(Text)
    boq = Column(JSONB, default=list)
    risks = Column(JSONB, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    document = relationship("Document")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), index=True)
    role = Column(String(16))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    chat_message_id = Column(Integer, ForeignKey("chat_messages.id"))
    correction = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Memory(Base):
    __tablename__ = "memory"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), index=True)
    value = Column(Text)
    meta = Column("metadata", JSONB, default=dict)
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
