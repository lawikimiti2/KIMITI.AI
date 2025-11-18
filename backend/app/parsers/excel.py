from __future__ import annotations
from typing import BinaryIO
import openpyxl
from io import BytesIO

def extract_xlsx(file: BinaryIO) -> str:
    data = file.read()
    wb = openpyxl.load_workbook(BytesIO(data), data_only=True)
    parts = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            line = ", ".join([str(c) for c in row if c is not None])
            if line:
                parts.append(line)
    return "\n".join(parts)
