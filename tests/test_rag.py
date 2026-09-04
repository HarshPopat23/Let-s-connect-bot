from pathlib import Path

import pytest

from ollm.config import Settings
from ollm.models import SearchHit
from ollm.rag import RAGService
from ollm.state import SQLiteState


class FakeOllama:
    def __init__(self) -> None:
        self.chat_calls = 0

    async def embed(self, texts, model):
        del model
        return [[0.1, 0.2, 0.3] for _ in texts]

    async def list_models(self):
        return {"qwen3:4b", "mistral:7b-instruct", "mistral-nemo:12b"}

    async def chat(self, model, system_prompt, user_prompt, temperature):
        del model, system_prompt, user_prompt, temperature
        self.chat_calls += 1
        return "Read the contributor guide before choosing work [1]."


class FakeVectorStore:
    def __init__(self, hits):
        self.hits = hits

    async def search(self, query_vector, limit, score_threshold):
        del query_vector, limit, score_threshold
        return self.hits


def make_settings(tmp_path: Path) -> Settings:
    return Settings(
        _env_file=None,
        knowledge_directory=tmp_path,
        state_database=tmp_path / "state.sqlite3",
    )


@pytest.mark.asyncio
async def test_refuses_when_retrieval_has_no_evidence(tmp_path: Path) -> None:
    state = SQLiteState(tmp_path / "state.sqlite3")
    await state.initialize()
    rag = RAGService(make_settings(tmp_path), FakeOllama(), FakeVectorStore([]), state)
    rag._knowledge_version = "test"
    result = await rag.answer("Will this unknown project select me?")
    assert "could not find enough reliable information" in result.answer
    assert result.model == "retrieval-only"


@pytest.mark.asyncio
async def test_grounded_answer_has_source_and_cache(tmp_path: Path) -> None:
    state = SQLiteState(tmp_path / "state.sqlite3")
    await state.initialize()
    hit = SearchHit(
        chunk_id="1",
        title="Official Guide",
        section="Start",
        text="Read CONTRIBUTING before selecting an issue.",
        source_path="guide.md",
        source_url="https://example.test/guide",
        category="workflow",
        score=0.9,
    )
    ollama = FakeOllama()
    rag = RAGService(make_settings(tmp_path), ollama, FakeVectorStore([hit]), state)
    rag._knowledge_version = "test"
    first = await rag.answer("How do I start contributing to this project?")
    second = await rag.answer("How do I start contributing to this project?")
    assert "https://example.test/guide" in first.answer
    assert second.cached
    assert ollama.chat_calls == 1
