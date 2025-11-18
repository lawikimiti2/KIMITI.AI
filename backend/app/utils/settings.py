from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pydantic import Field, TypeAdapter
import json
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Core
    environment: str = os.getenv("ENVIRONMENT", "development")
    CORS_ALLOW_ORIGINS: List[str] = Field(default=["*"])

    @staticmethod
    def _parse_list(value: object) -> List[str]:
        if isinstance(value, list):
            return [str(x) for x in value]
        if isinstance(value, str):
            s = value.strip()
            try:
                parsed = json.loads(s)
                return TypeAdapter(List[str]).validate_python(parsed)
            except (json.JSONDecodeError, TypeError, ValueError):
                # Fallback: comma-separated values
                parts = [p.strip() for p in s.split(",") if p.strip()]
                return parts or ["*"]
        return ["*"]

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@db:5432/kimiti",
    )

    # Vector backend: pgvector | qdrant | memory
    vector_backend: str = os.getenv("VECTOR_BACKEND", "pgvector")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://qdrant:6333")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")

    # LLM provider: openai | ollama | vllm | hf
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_base_url: Optional[str] = os.getenv("OPENAI_BASE_URL")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Embeddings
    embedding_provider: Optional[str] = (
        os.getenv("EMBEDDING_PROVIDER")
        or os.getenv("LLM_PROVIDER", "openai")
    )
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "text-embedding-3-small",
    )

    # Ollama/vLLM
    # e.g. http://localhost:11434 for Ollama
    inference_base_url: Optional[str] = os.getenv("INFERENCE_BASE_URL")
    inference_model: Optional[str] = os.getenv("INFERENCE_MODEL")

    # Celery / Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", redis_url)
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", redis_url)

    # Storage
    data_dir: str = os.getenv("DATA_DIR", "./data")
    dvc_enabled: bool = os.getenv("DVC_ENABLED", "false").lower() == "true"

settings = Settings()
