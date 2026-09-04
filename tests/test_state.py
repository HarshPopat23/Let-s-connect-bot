from pathlib import Path

import pytest

from ollm.state import SQLiteState


@pytest.mark.asyncio
async def test_daily_quota_is_enforced(tmp_path: Path) -> None:
    state = SQLiteState(tmp_path / "state.sqlite3")
    await state.initialize()
    assert await state.consume_daily_quota(123, 2) == (True, 1)
    assert await state.consume_daily_quota(123, 2) == (True, 0)
    assert await state.consume_daily_quota(123, 2) == (False, 0)


@pytest.mark.asyncio
async def test_cache_round_trip(tmp_path: Path) -> None:
    state = SQLiteState(tmp_path / "state.sqlite3")
    await state.initialize()
    key = state.cache_key("What is OSS?", "v1")
    await state.set_cache(key, {"answer": "Open source"}, ttl_seconds=60)
    assert await state.get_cache(key) == {"answer": "Open source"}
    assert key == state.cache_key("  what IS oss? ", "v1")
