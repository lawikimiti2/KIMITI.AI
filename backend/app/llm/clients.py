from __future__ import annotations
from typing import List, Optional
import os
import requests

from ..utils.settings import settings

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


class ChatClient:
    def __init__(self):
        self.provider = settings.llm_provider
        if self.provider in {"openai", "vllm"}:
            if OpenAI is None:
                raise RuntimeError("openai package not installed")
            base_url = settings.openai_base_url or settings.inference_base_url
            api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY", "none")
            self.client = OpenAI(base_url=base_url, api_key=api_key)
            self.model = settings.openai_model or settings.inference_model
        elif self.provider == "ollama":
            self.base_url = settings.inference_base_url or "http://localhost:11434"
            self.model = settings.inference_model or "llama3"
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate(self, system: str, user: str) -> str:
        if self.provider in {"openai", "vllm"}:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=0.2,
            )
            return resp.choices[0].message.content or ""
        elif self.provider == "ollama":
            r = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    "stream": False,
                },
                timeout=120,
            )
            r.raise_for_status()
            data = r.json()
            return data.get("message", {}).get("content", "")
        else:
            raise ValueError("Unsupported provider")


class EmbeddingClient:
    def __init__(self):
        self.provider = settings.embedding_provider or settings.llm_provider
        if self.provider in {"openai", "vllm"}:
            if OpenAI is None:
                raise RuntimeError("openai package not installed")
            base_url = settings.openai_base_url or settings.inference_base_url
            api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY", "none")
            self.client = OpenAI(base_url=base_url, api_key=api_key)
            self.model = settings.embedding_model
        elif self.provider == "ollama":
            self.base_url = settings.inference_base_url or "http://localhost:11434"
            self.model = settings.inference_model or "mxbai-embed-large"
        elif self.provider == "memory":  # deterministic local fallback
            self.model = "memory"
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}")

    def embed(self, texts: List[str]) -> List[List[float]]:
        if self.provider in {"openai", "vllm"}:
            resp = self.client.embeddings.create(model=self.model, input=texts)
            return [d.embedding for d in resp.data]
        elif self.provider == "ollama":
            r = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "input": texts},
                timeout=120,
            )
            r.raise_for_status()
            data = r.json()
            # ollama can return {embeddings: [[...], ...]}
            if isinstance(data, dict) and "embeddings" in data:
                return data["embeddings"]
            if isinstance(data, list) and data and "embedding" in data[0]:
                return [row["embedding"] for row in data]
            raise RuntimeError("Unexpected embedding response from Ollama")
        elif self.provider == "memory":
            return [self._hash_embed(t) for t in texts]
        else:
            raise ValueError("Unsupported provider")

    def _hash_embed(self, text: str, dim: int = 384) -> List[float]:
        # very simple deterministic embedding for local tests
        import math

        vec = [0.0] * dim
        for i, ch in enumerate(text.encode("utf-8")):
            vec[i % dim] += (ch % 13) / 13.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]
