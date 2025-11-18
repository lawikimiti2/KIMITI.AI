from __future__ import annotations
from typing import BinaryIO
from docx import Document
from io import BytesIO

def extract_docx(file: BinaryIO) -> str:
    data = file.read()
    doc = Document(BytesIO(data))
    parts = []
    for para in doc.paragraphs:
        parts.append(para.text)
    return "\n".join(parts)
