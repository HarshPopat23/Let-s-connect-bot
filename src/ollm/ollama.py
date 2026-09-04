from __future__ import annotations

import logging
from collections.abc import Sequence

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(self, base_url: str, timeout_seconds: float = 180) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout_seconds),
        )

    async def close(self) -> None:
        await self._client.aclose()

    @retry(
        retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def list_models(self) -> set[str]:
        try:
            response = await self._client.get("/api/tags")
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OllamaError(f"Could not list Ollama models: {exc}") from exc
        result: set[str] = set()
        for item in response.json().get("models", []):
            name = item.get("model") or item.get("name")
            if name:
                result.add(str(name))
        return result

    @retry(
        retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def embed(self, texts: Sequence[str], model: str) -> list[list[float]]:
        if not texts:
            return []
        try:
            response = await self._client.post(
                "/api/embed",
                json={"model": model, "input": list(texts), "truncate": True},
            )
            response.raise_for_status()
            embeddings = response.json().get("embeddings")
            if not embeddings or len(embeddings) != len(texts):
                raise OllamaError("Ollama returned an unexpected embedding response")
            return embeddings
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:500]
            raise OllamaError(f"Embedding request failed: {detail}") from exc
        except httpx.HTTPError as exc:
            raise OllamaError(f"Embedding request failed: {exc}") from exc

    @retry(
        retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(2),
        reraise=True,
    )
    async def chat(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
    ) -> str:
        try:
            response = await self._client.post(
                "/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "stream": False,
                    "think": False,
                    "options": {"temperature": temperature},
                    "keep_alive": "10m",
                },
            )
            response.raise_for_status()
            content = response.json().get("message", {}).get("content", "").strip()
            if not content:
                raise OllamaError("Ollama returned an empty answer")
            return content
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:500]
            raise OllamaError(f"Chat request failed for {model}: {detail}") from exc
        except httpx.HTTPError as exc:
            raise OllamaError(f"Chat request failed for {model}: {exc}") from exc
