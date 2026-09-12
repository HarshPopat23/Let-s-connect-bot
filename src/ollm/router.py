from __future__ import annotations

import re

from ollm.config import Settings
from ollm.models import ModelSelection, ModelTier


class ModelRouter:
    """Select a local model without spending another model call on classification."""

    COMPLEX_TERMS = {
        "architecture",
        "design proposal",
        "security",
        "vulnerability",
        "license compatibility",
        "legal",
        "maintainer conflict",
        "rejected",
        "proposal review",
        "debug",
        "root cause",
        "migration",
        "governance",
        "compare",
        "strategy",
        "roadmap",
    }
    EASY_PREFIXES = (
        "what is ",
        "what are ",
        "define ",
        "meaning of ",
        "where is ",
        "how to start",
        "how do i start",
        "link for ",
        "who can ",
    )

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def classify(self, question: str) -> tuple[ModelTier, str]:
        normalized = " ".join(question.lower().split())
        words = re.findall(r"[a-z0-9+#.-]+", normalized)
        complex_matches = [term for term in self.COMPLEX_TERMS if term in normalized]

        if len(words) >= 80 or len(complex_matches) >= 2 or normalized.count("?") >= 3:
            return ModelTier.COMPLEX, "long or multi-part strategic question"
        if complex_matches:
            return ModelTier.COMPLEX, f"complex topic: {complex_matches[0]}"
        if len(words) <= 18 and normalized.startswith(self.EASY_PREFIXES):
            return ModelTier.EASY, "short factual or navigation question"
        if len(words) <= 10:
            return ModelTier.EASY, "short question"
        return ModelTier.STANDARD, "normal contributor guidance question"

    def _configured_model(self, tier: ModelTier) -> str:
        return {
            ModelTier.EASY: self.settings.model_easy,
            ModelTier.STANDARD: self.settings.model_standard,
            ModelTier.COMPLEX: self.settings.model_complex,
        }[tier]

    @staticmethod
    def _is_available(model: str, available: set[str]) -> bool:
        if model in available:
            return True
        base = model.split(":", maxsplit=1)[0]
        return any(item == base or item.startswith(f"{base}:") for item in available)

    def select(self, question: str, available: set[str]) -> ModelSelection:
        tier, reason = self.classify(question)
        requested = self._configured_model(tier)

        if not available or self._is_available(requested, available):
            return ModelSelection(tier, requested, requested, reason)

        fallback_order = {
            ModelTier.COMPLEX: [self.settings.model_standard, self.settings.model_easy],
            ModelTier.STANDARD: [self.settings.model_easy, self.settings.model_complex],
            ModelTier.EASY: [self.settings.model_standard, self.settings.model_complex],
        }[tier]
        for fallback in fallback_order:
            if self._is_available(fallback, available):
                return ModelSelection(
                    tier,
                    requested,
                    fallback,
                    f"{reason}; configured model is unavailable",
                    used_fallback=True,
                )
        return ModelSelection(tier, requested, requested, reason)

