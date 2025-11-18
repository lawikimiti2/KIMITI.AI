from __future__ import annotations
import pdfplumber
from typing import BinaryIO

def extract_pdf(file: BinaryIO) -> str:
    text = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)
