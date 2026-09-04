from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ModelTier(StrEnum):
    EASY = "easy"
    STANDARD = "standard"
    COMPLEX = "complex"


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    chunk_id: str
    title: str
    section: str
    text: str
    source_path: str
    source_url: str
    category: str
    updated: str = ""


@dataclass(frozen=True, slots=True)
class SearchHit:
    chunk_id: str
    title: str
    section: str
    text: str
    source_path: str
    source_url: str
    category: str
    score: float


@dataclass(frozen=True, slots=True)
class ModelSelection:
    tier: ModelTier
    requested_model: str
    selected_model: str
    reason: str
    used_fallback: bool = False


@dataclass(slots=True)
class AnswerResult:
    answer: str
    sources: list[SearchHit] = field(default_factory=list)
    model: str = "retrieval-only"
    tier: ModelTier = ModelTier.EASY
    cached: bool = False
    cache_key: str = ""
