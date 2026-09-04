from __future__ import annotations

from dataclasses import dataclass

from ollm.config import Settings
from ollm.ollama import OllamaClient
from ollm.rag import RAGService
from ollm.state import SQLiteState
from ollm.vector_store import VectorStore


@dataclass(slots=True)
class Services:
    settings: Settings
    ollama: OllamaClient
    vector_store: VectorStore
    state: SQLiteState
    rag: RAGService

    @classmethod
    def create(cls, settings: Settings) -> Services:
        ollama = OllamaClient(settings.ollama_base_url, settings.ollama_timeout_seconds)
        vector_store = VectorStore(
            settings.qdrant_url,
            settings.qdrant_collection,
            settings.qdrant_api_key,
        )
        state = SQLiteState(settings.state_database)
        rag = RAGService(settings, ollama, vector_store, state)
        return cls(settings, ollama, vector_store, state, rag)

    async def close(self) -> None:
        await self.ollama.close()
        await self.vector_store.close()
