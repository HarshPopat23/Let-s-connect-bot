from ollm.bot import split_telegram_text


def test_short_text_is_unchanged() -> None:
    assert split_telegram_text("short") == ["short"]


def test_long_text_is_split_within_limit() -> None:
    text = ("A useful open source sentence. " * 300).strip()
    parts = split_telegram_text(text, limit=200)
    assert len(parts) > 1
    assert all(len(part) <= 200 for part in parts)
    assert " ".join(parts).replace("  ", " ") == text
