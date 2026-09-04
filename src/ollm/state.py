from __future__ import annotations

import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import aiosqlite


class SQLiteState:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    async def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.database_path) as db:
            await db.execute("PRAGMA journal_mode=WAL")
            await db.executescript(
                """
                CREATE TABLE IF NOT EXISTS answer_cache (
                    cache_key TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    expires_at INTEGER NOT NULL,
                    created_at INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS daily_usage (
                    user_id INTEGER NOT NULL,
                    usage_day TEXT NOT NULL,
                    question_count INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY (user_id, usage_day)
                );
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    cache_key TEXT NOT NULL,
                    rating TEXT NOT NULL,
                    created_at INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                """
            )
            await db.commit()

    @staticmethod
    def cache_key(question: str, knowledge_version: str) -> str:
        normalized = " ".join(question.casefold().split())
        return hashlib.sha256(f"{knowledge_version}|{normalized}".encode()).hexdigest()

    async def get_cache(self, cache_key: str) -> dict[str, Any] | None:
        now = int(time.time())
        async with aiosqlite.connect(self.database_path) as db:
            cursor = await db.execute(
                "SELECT payload FROM answer_cache WHERE cache_key = ? AND expires_at > ?",
                (cache_key, now),
            )
            row = await cursor.fetchone()
            if not row:
                await db.execute("DELETE FROM answer_cache WHERE expires_at <= ?", (now,))
                await db.commit()
                return None
            return json.loads(row[0])

    async def set_cache(self, cache_key: str, payload: dict[str, Any], ttl_seconds: int) -> None:
        now = int(time.time())
        async with aiosqlite.connect(self.database_path) as db:
            await db.execute(
                """
                INSERT INTO answer_cache(cache_key, payload, expires_at, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    payload = excluded.payload,
                    expires_at = excluded.expires_at,
                    created_at = excluded.created_at
                """,
                (cache_key, json.dumps(payload), now + ttl_seconds, now),
            )
            await db.commit()

    async def consume_daily_quota(self, user_id: int, limit: int) -> tuple[bool, int]:
        usage_day = datetime.now(UTC).date().isoformat()
        async with aiosqlite.connect(self.database_path) as db:
            await db.execute("BEGIN IMMEDIATE")
            cursor = await db.execute(
                "SELECT question_count FROM daily_usage WHERE user_id = ? AND usage_day = ?",
                (user_id, usage_day),
            )
            row = await cursor.fetchone()
            current = int(row[0]) if row else 0
            if current >= limit:
                await db.rollback()
                return False, 0
            new_count = current + 1
            await db.execute(
                """
                INSERT INTO daily_usage(user_id, usage_day, question_count)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, usage_day)
                DO UPDATE SET question_count = excluded.question_count
                """,
                (user_id, usage_day, new_count),
            )
            await db.commit()
            return True, limit - new_count

    async def add_feedback(self, user_id: int, cache_key: str, rating: str) -> None:
        async with aiosqlite.connect(self.database_path) as db:
            await db.execute(
                "INSERT INTO feedback(user_id, cache_key, rating, created_at) VALUES (?, ?, ?, ?)",
                (user_id, cache_key, rating, int(time.time())),
            )
            await db.commit()

    async def set_metadata(self, key: str, value: str) -> None:
        async with aiosqlite.connect(self.database_path) as db:
            await db.execute(
                """
                INSERT INTO metadata(key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (key, value),
            )
            await db.commit()

    async def get_metadata(self, key: str) -> str | None:
        async with aiosqlite.connect(self.database_path) as db:
            cursor = await db.execute("SELECT value FROM metadata WHERE key = ?", (key,))
            row = await cursor.fetchone()
            return str(row[0]) if row else None

    async def statistics(self) -> dict[str, int]:
        async with aiosqlite.connect(self.database_path) as db:
            cache = await (await db.execute("SELECT COUNT(*) FROM answer_cache")).fetchone()
            users = await (
                await db.execute("SELECT COUNT(DISTINCT user_id) FROM daily_usage")
            ).fetchone()
            questions = await (
                await db.execute("SELECT COALESCE(SUM(question_count), 0) FROM daily_usage")
            ).fetchone()
            feedback = await (await db.execute("SELECT COUNT(*) FROM feedback")).fetchone()
        return {
            "cached_answers": int(cache[0]),
            "users": int(users[0]),
            "questions": int(questions[0]),
            "feedback": int(feedback[0]),
        }
