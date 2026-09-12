from __future__ import annotations

import logging
from dataclasses import asdict

from ollm.config import Settings
from ollm.knowledge import knowledge_version, load_knowledge
from ollm.models import AnswerResult, ModelTier, SearchHit
from ollm.ollama import OllamaClient
from ollm.router import ModelRouter
from ollm.state import SQLiteState
from ollm.vector_store import VectorStore

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are OLLM, the open-source contributor guide and mentor for OSS Let's Connect.

Answer as a helpful, experienced open-source contributor and reviewer.

Guidelines:
1. When Knowledge Context is supplied, prioritize it for facts about OSS Let's Connect community details, programs, mentors, events, and guidelines.
2. Synthesize the provided knowledge context with your general open-source, Git, GitHub, and software engineering knowledge to give a comprehensive, practical, and helpful answer.
3. If no specific knowledge context is available, provide standard open-source best practices, explain concepts clearly, and guide the user on where to find project-specific details (such as CONTRIBUTING.md or community channels).
4. Never guarantee that a pull request will merge or that someone will be selected for competitive programs (GSoC, LFX, Outreachy).
5. Prefer meaningful work, understanding, testing, and respectful communication.
6. Do not cite sources with bracketed numbers like [1] or [2], and do not add a "Sources" section (sources are handled separately).
7. Keep the answer concise and well-formatted for Telegram. Do not use "#" headings or double asterisks "**". Use simple bullet points or single asterisks *word* for emphasis.
"""


class RAGService:
    def __init__(
        self,
        settings: Settings,
        ollama: OllamaClient,
        vector_store: VectorStore,
        state: SQLiteState,
    ) -> None:
        self.settings = settings
        self.ollama = ollama
        self.vector_store = vector_store
        self.state = state
        self.router = ModelRouter(settings)
        self._knowledge_version = "unknown"

    @property
    def version(self) -> str:
        return self._knowledge_version

    async def initialize(self) -> None:
        await self.state.initialize()
        chunks = load_knowledge(self.settings.knowledge_directory)
        local_version = knowledge_version(chunks)
        indexed_version = await self.state.get_metadata("knowledge_version")
        collection_exists = await self.vector_store.exists()
        if (
            self.settings.reindex_on_start
            or not collection_exists
            or (indexed_version is not None and indexed_version != local_version)
        ):
            await self.reindex(chunks=chunks)
        else:
            self._knowledge_version = local_version
            if indexed_version is None:
                await self.state.set_metadata("knowledge_version", local_version)

    async def reindex(self, chunks=None) -> int:
        chunks = chunks or load_knowledge(self.settings.knowledge_directory)
        if not chunks:
            raise RuntimeError("The knowledge directory contains no indexable documents")
        sample = await self.ollama.embed(["Open source contribution knowledge"])
        await self.vector_store.recreate(vector_size=len(sample[0]))
        batch_size = 12
        import gc
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start : start + batch_size]
            inputs = [f"{item.title}\n{item.section}\n{item.text}" for item in batch]
            vectors = await self.ollama.embed(inputs)
            await self.vector_store.upsert(batch, vectors)
            del batch, inputs, vectors
            gc.collect()
        self._knowledge_version = knowledge_version(chunks)
        await self.state.set_metadata("knowledge_version", self._knowledge_version)
        await self.state.set_metadata("knowledge_chunk_count", str(len(chunks)))
        logger.info("Indexed %s knowledge chunks", len(chunks))
        gc.collect()
        return len(chunks)

    async def answer(self, question: str) -> AnswerResult:
        question = " ".join(question.strip().split())
        if not question:
            raise ValueError("Question is empty")
        cache_key = self.state.cache_key(question, self._knowledge_version)
        cached = await self.state.get_cache(cache_key)
        if cached:
            return self._from_cache(cached, cache_key)

        query_vector = (await self.ollama.embed([question]))[0]
        hits = await self.vector_store.search(
            query_vector,
            limit=self.settings.retrieval_limit,
            score_threshold=self.settings.retrieval_score_threshold,
        )

        available_models = await self.ollama.list_models()
        selection = self.router.select(question, available_models)

        if hits:
            context = self._build_context(hits)
            user_prompt = f"Question:\n{question}\n\nKnowledge context:\n{context}"
        else:
            user_prompt = (
                f"Question:\n{question}\n\n"
                "Please provide a helpful, practical, and encouraging answer based on open-source and software development best practices."
            )

        answer = await self.ollama.chat(
            model=selection.selected_model,
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=self.settings.answer_temperature,
        )
        result = AnswerResult(
            answer=answer,
            sources=hits,
            model=selection.selected_model,
            tier=selection.tier,
            cache_key=cache_key,
        )
        await self._cache_result(result)
        return result

    def _build_context(self, hits: list[SearchHit]) -> str:
        blocks: list[str] = []
        used = 0
        for index, hit in enumerate(hits, start=1):
            block = (
                f"[{index}] {hit.title} | {hit.section}\n"
                f"Source URL: {hit.source_url or 'Internal curated community guidance'}\n"
                f"{hit.text}"
            )
            if blocks and used + len(block) > self.settings.max_context_characters:
                break
            blocks.append(block)
            used += len(block)
        return "\n\n".join(blocks)

    async def _cache_result(self, result: AnswerResult) -> None:
        await self.state.set_cache(
            result.cache_key,
            {
                "answer": result.answer,
                "sources": [asdict(item) for item in result.sources],
                "model": result.model,
                "tier": result.tier.value,
            },
            self.settings.cache_ttl_seconds,
        )

    @staticmethod
    def _from_cache(payload: dict, cache_key: str) -> AnswerResult:
        sources = [SearchHit(**item) for item in payload.get("sources", [])]
        return AnswerResult(
            answer=str(payload["answer"]),
            sources=sources,
            model=str(payload.get("model", "cached")),
            tier=ModelTier(payload.get("tier", ModelTier.EASY.value)),
            cached=True,
            cache_key=cache_key,
        )
