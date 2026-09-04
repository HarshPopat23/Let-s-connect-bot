from ollm.config import Settings
from ollm.models import ModelTier
from ollm.router import ModelRouter


def settings() -> Settings:
    return Settings(
        _env_file=None,
        model_easy="qwen3:4b",
        model_standard="mistral:7b-instruct",
        model_complex="mistral-nemo:12b",
    )


def test_short_definition_uses_easy_model() -> None:
    router = ModelRouter(settings())
    selection = router.select("What is a pull request?", {"qwen3:4b"})
    assert selection.tier is ModelTier.EASY
    assert selection.selected_model == "qwen3:4b"


def test_normal_guidance_uses_standard_model() -> None:
    router = ModelRouter(settings())
    question = "My pull request has had no response for two weeks. What should I do next?"
    selection = router.select(question, {"mistral:7b-instruct"})
    assert selection.tier is ModelTier.STANDARD


def test_security_question_uses_complex_model() -> None:
    router = ModelRouter(settings())
    selection = router.select(
        "How should I privately report this security vulnerability?",
        {"mistral-nemo:12b"},
    )
    assert selection.tier is ModelTier.COMPLEX


def test_missing_complex_model_falls_back() -> None:
    router = ModelRouter(settings())
    selection = router.select(
        "Compare the architecture and security tradeoffs of these designs.",
        {"mistral:7b-instruct"},
    )
    assert selection.tier is ModelTier.COMPLEX
    assert selection.selected_model == "mistral:7b-instruct"
    assert selection.used_fallback
