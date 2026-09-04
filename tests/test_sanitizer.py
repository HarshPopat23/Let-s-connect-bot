import importlib.util
import sys
from pathlib import Path


def load_sanitizer():
    path = Path(__file__).parents[1] / "scripts" / "sanitize_whatsapp.py"
    spec = importlib.util.spec_from_file_location("sanitize_whatsapp", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_redacts_phone_email_and_mentions() -> None:
    sanitizer = load_sanitizer()
    text = "Contact +91 99999 88888 or person@example.com about open source @\u2068Name\u2069"
    redacted = sanitizer.redact(text)
    assert "99999" not in redacted
    assert "person@example.com" not in redacted
    assert "Name" not in redacted


def test_only_relevant_content_is_selected() -> None:
    sanitizer = load_sanitizer()
    assert sanitizer.relevant("How should I review a pull request?")
    assert not sanitizer.relevant("What did you have for lunch?")
