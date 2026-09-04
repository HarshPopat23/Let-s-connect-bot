from __future__ import annotations

import asyncio
import contextlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    with contextlib.suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8")

from ollm.config import Settings
from ollm.logging_config import configure_logging
from ollm.services import Services


async def _index() -> None:
    settings = Settings()
    configure_logging(settings.log_level)
    services = Services.create(settings)
    try:
        await services.state.initialize()
        count = await services.rag.reindex()
        print(f"Indexed {count} chunks. Knowledge version: {services.rag.version}")
    finally:
        await services.close()


async def _ask(question: str) -> None:
    settings = Settings()
    configure_logging(settings.log_level)
    services = Services.create(settings)
    try:
        await services.rag.initialize()
        result = await services.rag.answer(question)
        print(result.answer)
        print(f"\nModel: {result.model}. Tier: {result.tier.value}. Cached: {result.cached}")
    finally:
        await services.close()


async def _check() -> None:
    settings = Settings()
    services = Services.create(settings)
    try:
        await services.state.initialize()
        available = sorted(await services.ollama.list_models())
        qdrant_ready = await services.vector_store.exists()
        print(f"Ollama models: {', '.join(available) or 'none'}")
        print(f"Qdrant collection ready: {qdrant_ready}")
        print(f"Knowledge directory: {settings.knowledge_directory}")
    finally:
        await services.close()


def index_main() -> None:
    asyncio.run(_index())


def ask_main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: ollm-ask "How do I make my first contribution?"')
    asyncio.run(_ask(" ".join(sys.argv[1:])))


def check_main() -> None:
    asyncio.run(_check())
