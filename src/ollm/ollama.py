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

# Ensure thread and memory limits for ONNX/BLAS on memory-constrained hosts (e.g. Render 512MB)
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

# Ensure writable cache directory for HuggingFace and FastEmbed on Render/Linux
_DEFAULT_CACHE_DIR = Path(tempfile.gettempdir()) / "fastembed_cache"
_DEFAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("HF_HOME", str(_DEFAULT_CACHE_DIR / "hf"))
os.environ.setdefault("FASTEMBED_CACHE_PATH", str(_DEFAULT_CACHE_DIR))
os.environ.setdefault("XDG_CACHE_HOME", str(_DEFAULT_CACHE_DIR))
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")


class GroqError(RuntimeError):
    pass


# Backwards compatibility alias
OllamaError = GroqError


class GroqClient:
    def __init__(
        self,
        api_key: str = "",
        base_url: str = "https://api.groq.com/openai/v1",
        timeout_seconds: float = 60,
        fastembed_model: str = "BAAI/bge-small-en-v1.5",
        embedding_provider: str = "fastembed",
        **_kwargs: object,
    ) -> None:
        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")
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
            cache_path = os.environ.get("FASTEMBED_CACHE_PATH") or str(_DEFAULT_CACHE_DIR)
            threads = int(os.environ.get("FASTEMBED_THREADS", "1"))
            self._fastembed_instance = TextEmbedding(
                model_name=self._fastembed_model_name,
                cache_dir=cache_path,
                threads=threads,
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
        try:
            response = await self._client.get("/models")
            response.raise_for_status()
            return {m["id"] for m in response.json().get("data", []) if "id" in m}
        except Exception as exc:
            logger.warning("Could not fetch Groq models dynamically: %s", exc)
            return {
                "openai/gpt-oss-20b",
                "openai/gpt-oss-120b",
                "groq/compound-mini",
                "groq/compound",
                "qwen/qwen3.8-27b",
                "qwen/qwen3.6-27b",
            }

    async def embed(self, texts: Sequence[str], model: str = "") -> list[list[float]]:
        del model  # FastEmbed uses the configured lightweight local model
        if not texts:
            return []
        fe = self._get_fastembed()
        embeddings = list(fe.embed(list(texts)))
        return [emb.tolist() for emb in embeddings]

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
            raise GroqError(f"Groq chat request failed for {model}: {detail}") from exc
        except httpx.HTTPError as exc:
            raise GroqError(f"Groq chat request failed for {model}: {exc}") from exc


# Backwards compatibility alias
OllamaClient = GroqClient
