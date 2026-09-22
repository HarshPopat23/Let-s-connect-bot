from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from ollm.config import Settings
from ollm.discord_bot import (
    FeedbackView,
    OLLMDiscordBot,
    format_for_discord,
    split_discord_text,
)


def test_split_discord_text_short() -> None:
    assert split_discord_text("hello world") == ["hello world"]


def test_split_discord_text_long() -> None:
    long_text = ("Discord RAG bot test. " * 200).strip()
    parts = split_discord_text(long_text, limit=200)
    assert len(parts) > 1
    assert all(len(p) <= 200 for p in parts)
    assert " ".join(parts).replace("  ", " ") == long_text


def test_format_for_discord_strips_citations() -> None:
    raw = "Here is the guidance [1] regarding pull requests [2]."
    cleaned = format_for_discord(raw)
    assert cleaned == "Here is the guidance regarding pull requests."


def test_discord_bot_registers_commands() -> None:
    settings = Settings(discord_bot_token="fake_token", discord_guild_id="123456789")
    mock_rag = MagicMock()
    mock_state = MagicMock()

    bot = OLLMDiscordBot(settings, mock_rag, mock_state)
    commands = {cmd.name for cmd in bot.tree.get_commands()}

    expected = {"ask", "about", "sources", "privacy", "help", "status", "reindex"}
    assert expected.issubset(commands)


@pytest.mark.asyncio
async def test_feedback_view_records_feedback() -> None:
    mock_state = MagicMock()
    mock_state.add_feedback = AsyncMock()

    view = FeedbackView(state=mock_state, cache_key="test_cache_key_12345", user_id=999)
    interaction = MagicMock()
    interaction.user.id = 999
    interaction.response = MagicMock()
    interaction.response.edit_message = AsyncMock()
    interaction.followup = MagicMock()
    interaction.followup.send = AsyncMock()

    await view._handle_feedback(interaction, "useful")

    mock_state.add_feedback.assert_awaited_once_with(999, "test_cache_key_12345"[:20], "useful")
    interaction.response.edit_message.assert_awaited_once()
