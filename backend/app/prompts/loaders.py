from __future__ import annotations
import os

BASE = os.path.join(os.path.dirname(__file__))

_CACHE = {}

def load_prompt(name: str) -> str:
    if name in _CACHE:
        return _CACHE[name]
    p = os.path.join(BASE, name)
    with open(p, "r", encoding="utf-8") as f:
        _CACHE[name] = f.read()
    return _CACHE[name]
