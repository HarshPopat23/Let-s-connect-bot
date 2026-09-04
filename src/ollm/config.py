from __future__ import annotations

from pathlib import Path
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


def _csv_ints(value: str | list[int] | tuple[int, ...]) -> list[int]:
    if isinstance(value, (list, tuple)):
        return [int(item) for item in value]
    if not value.strip():
        return []
    return [int(item.strip()) for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    telegram_bot_token: str = ""
    telegram_allowed_chat_ids: Annotated[list[int], NoDecode] = Field(default_factory=list)
    admin_user_ids: Annotated[list[int], NoDecode] = Field(default_factory=list)

    ollama_base_url: str = "http://localhost:11434"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""

    embedding_model: str = "nomic-embed-text"
    model_easy: str = "qwen3:4b"
    model_standard: str = "mistral:7b-instruct"
    model_complex: str = "mistral-nemo:12b"

    qdrant_collection: str = "ollm_knowledge"
    retrieval_limit: int = Field(default=6, ge=1, le=12)
    retrieval_score_threshold: float = Field(default=0.45, ge=0, le=1)
    max_context_characters: int = Field(default=14_000, ge=2_000, le=50_000)
    answer_temperature: float = Field(default=0.15, ge=0, le=1)
    ollama_timeout_seconds: float = Field(default=180, ge=10, le=600)

    daily_question_limit: int = Field(default=10, ge=1, le=1_000)
    cache_ttl_seconds: int = Field(default=86_400, ge=60)
    max_question_characters: int = Field(default=1_200, ge=100, le=4_000)

    knowledge_directory: Path = Path("knowledge")
    state_database: Path = Path("data/ollm.sqlite3")
    reindex_on_start: bool = False
    log_level: str = "INFO"

    @field_validator("telegram_allowed_chat_ids", "admin_user_ids", mode="before")
    @classmethod
    def parse_id_lists(cls, value: object) -> list[int]:
        if value is None:
            return []
        return _csv_ints(value)  # type: ignore[arg-type]

    @field_validator("ollama_base_url", "qdrant_url")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")

    def require_bot_token(self) -> str:
        if not self.telegram_bot_token.strip():
            raise RuntimeError(
                "TELEGRAM_BOT_TOKEN is empty. Copy .env.example to .env and add the token."
            )
        return self.telegram_bot_token.strip()
