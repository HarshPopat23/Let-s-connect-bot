from __future__ import annotations

import logging
import os
import re
import tempfile
from collections.abc import Sequence
from pathlib import Path

import httpx
from fastembed import TextEmbedding
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

# Ensure writable cache directory for HuggingFace and FastEmbed on Render/Linux
_DEFAULT_CACHE_DIR = Path(tempfile.gettempdir()) / "fastembed_cache"
_DEFAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("HF_HOME", str(_DEFAULT_CACHE_DIR / "hf"))
os.environ.setdefault("FASTEMBED_CACHE_PATH", str(_DEFAULT_CACHE_DIR))
os.environ.setdefault("XDG_CACHE_HOME", str(_DEFAULT_CACHE_DIR))
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        timeout_seconds: float = 180,
        api_key: str = "",
        embedding_provider: str = "auto",
        fastembed_model: str = "BAAI/bge-small-en-v1.5",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key.strip()
        self.is_groq = bool(self.api_key)
        self.embedding_provider = embedding_provider
        self._fastembed_model_name = fastembed_model
        self._fastembed_instance: TextEmbedding | None = None

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=httpx.Timeout(timeout_seconds),
        )

    def _get_fastembed(self) -> TextEmbedding:
        if self._fastembed_instance is None:
            cache_path = str(_DEFAULT_CACHE_DIR)
            self._fastembed_instance = TextEmbedding(
                model_name=self._fastembed_model_name,
                cache_dir=cache_path,
            )
        return self._fastembed_instance

    async def close(self) -> None:
        await self._client.aclose()

    @retry(
        retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def list_models(self) -> set[str]:
        if self.is_groq:
            try:
                response = await self._client.get("/models")
                response.raise_for_status()
                return {m["id"] for m in response.json().get("data", []) if "id" in m}
            except Exception as exc:
                logger.warning("Could not fetch Groq models dynamically: %s", exc)
                return {
                    "qwen/qwen3.6-27b",
                    "qwen/qwen3.8-27b",
                    "openai/gpt-oss-120b",
                    "openai/gpt-oss-20b",
                    "groq/compound",
                }

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

        use_fastembed = (
            self.embedding_provider == "fastembed"
            or (self.embedding_provider == "auto" and self.is_groq)
        )

        if use_fastembed:
            fe = self._get_fastembed()
            embeddings = list(fe.embed(list(texts)))
            return [emb.tolist() for emb in embeddings]

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
        if self.is_groq:
            try:
                response = await self._client.post(
                    "/chat/completions",
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        "temperature": temperature,
                        "max_tokens": 1024,
                    },
                )
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                # Clean reasoning/thinking tags if model outputs <think>...</think>
                content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
                return content
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:500]
                raise OllamaError(f"Groq chat request failed for {model}: {detail}") from exc
            except httpx.HTTPError as exc:
                raise OllamaError(f"Groq chat request failed for {model}: {exc}") from exc

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
