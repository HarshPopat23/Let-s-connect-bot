#!/usr/bin/env python3
"""Print aggregate open-source theme counts without emitting chat content."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

MESSAGE_START = re.compile(
    r"^\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}(?:\s*[ap]m)?\s+-\s+[^:]+:\s?(.*)$",
    re.IGNORECASE,
)

THEMES = {
    "issues": r"\b(issue|bug|feature request|assign|good first issue)\b",
    "pull_requests": r"\b(pr|pull request|merge|review|approval|changes requested)\b",
    "git_and_github": r"\b(git|github|fork|clone|branch|commit|rebase|conflict)\b",
    "maintainer_communication": r"\b(maintainer|mentor|reply|response|follow.?up|slack|discord|meeting)\b",
    "programs": r"\b(gsoc|lfx|outreachy|mentorship|proposal|selection)\b",
    "project_discovery": r"\b(project|organization|repository|repo|codebase)\b",
    "testing_and_ci": r"\b(test|testing|ci|workflow|check|lint|build|pipeline)\b",
    "responsible_ai": r"\b(ai|llm|chatgpt|copilot|generated)\b",
    "documentation": r"\b(documentation|docs|readme|guide|tutorial)\b",
    "career_and_learning": r"\b(resume|career|internship|learn|learning|skill|job)\b",
    "question_like": r"(\?|\bhow\b|\bwhat\b|\bwhy\b|\bshould\b|\bcan\b|\bwhere\b|\bwhen\b)",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("export", type=Path, help="Local WhatsApp text export")
    args = parser.parse_args()
    counts: Counter[str] = Counter()
    message_count = 0
    current = ""

    def count_message(body: str) -> None:
        nonlocal message_count
        if not body:
            return
        message_count += 1
        lowered = body.casefold()
        for name, pattern in THEMES.items():
            if re.search(pattern, lowered):
                counts[name] += 1

    with args.export.open(encoding="utf-8") as handle:
        for line in handle:
            match = MESSAGE_START.match(line)
            if match:
                count_message(current)
                current = match.group(1)
            elif current:
                current += " " + line.strip()
    count_message(current)

    result = {
        "messages_analyzed": message_count,
        "overlapping_theme_counts": dict(sorted(counts.items())),
        "privacy": "Aggregate counts only. No message, sender, date, or contact value is emitted.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
