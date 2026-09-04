from __future__ import annotations

import logging
from collections.abc import Sequence

from qdrant_client import AsyncQdrantClient, models

from ollm.models import DocumentChunk, SearchHit

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self, url: str, collection: str, api_key: str = "") -> None:
        self.collection = collection
        self.client = AsyncQdrantClient(url=url, api_key=api_key or None, timeout=60)

    async def close(self) -> None:
        await self.client.close()

    async def exists(self) -> bool:
        return await self.client.collection_exists(self.collection)

    async def recreate(self, vector_size: int) -> None:
        if await self.exists():
            await self.client.delete_collection(self.collection)
        await self.client.create_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )

    async def upsert(
        self,
        chunks: Sequence[DocumentChunk],
        vectors: Sequence[Sequence[float]],
    ) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("Chunk and vector counts differ")
        points = [
            models.PointStruct(
                id=chunk.chunk_id,
                vector=list(vector),
                payload={
                    "title": chunk.title,
                    "section": chunk.section,
                    "text": chunk.text,
                    "source_path": chunk.source_path,
                    "source_url": chunk.source_url,
                    "category": chunk.category,
                    "updated": chunk.updated,
                },
            )
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]
        await self.client.upsert(collection_name=self.collection, points=points, wait=True)

    async def search(
        self,
        query_vector: Sequence[float],
        limit: int,
        score_threshold: float,
    ) -> list[SearchHit]:
        response = await self.client.query_points(
            collection_name=self.collection,
            query=list(query_vector),
            with_payload=True,
            limit=limit,
            score_threshold=score_threshold,
        )
        hits: list[SearchHit] = []
        for point in response.points:
            payload = point.payload or {}
            hits.append(
                SearchHit(
                    chunk_id=str(point.id),
                    title=str(payload.get("title", "Knowledge source")),
                    section=str(payload.get("section", "")),
                    text=str(payload.get("text", "")),
                    source_path=str(payload.get("source_path", "")),
                    source_url=str(payload.get("source_url", "")),
                    category=str(payload.get("category", "")),
                    score=float(point.score),
                )
            )
        return hits
