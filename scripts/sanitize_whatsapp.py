#!/usr/bin/env python3
"""Create privacy-redacted review candidates from a WhatsApp text export.

This output is not safe to index automatically. Human review is mandatory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

MESSAGE_START = re.compile(
    r"^(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s+"
    r"(?P<time>\d{1,2}:\d{2}(?:\s*[ap]m)?)\s+-\s+"
    r"(?P<sender>[^:]+):\s?(?P<body>.*)$",
    re.IGNORECASE,
)
PHONE = re.compile(r"(?<!\d)(?:\+?\d[\d\s()-]{7,}\d)(?!\d)")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
WHATSAPP_MENTION = re.compile(r"@\u2068.*?\u2069")

KEYWORDS = {
    "open source",
    "opensource",
    "contribut",
    "pull request",
    " pr ",
    "issue",
    "maintainer",
    "mentor",
    "review",
    "github",
    "git ",
    "gsoc",
    "lfx",
    "outreachy",
    "cncf",
    "kubernetes",
    "kubeflow",
    "codebase",
    "proposal",
    "documentation",
    "testing",
    "license",
}

SYSTEM_PHRASES = {
    "joined using a group link",
    "was added",
    "requested to join",
    "changed the group",
    "left",
    "pinned a message",
    "this message was deleted",
    "<media omitted>",
}


@dataclass
class Message:
    date: str
    time: str
    sender: str
    body: str


def parse_export(text: str) -> list[Message]:
    messages: list[Message] = []
    current: Message | None = None
    for line in text.splitlines():
        match = MESSAGE_START.match(line)
        if match:
            if current:
                messages.append(current)
            current = Message(**match.groupdict())
        elif current:
            current.body += "\n" + line
    if current:
        messages.append(current)
    return messages


def redact(text: str) -> str:
    text = WHATSAPP_MENTION.sub("[mention removed]", text)
    text = EMAIL.sub("[email removed]", text)
    text = PHONE.sub("[phone removed]", text)
    return text.strip()


def participant_id(sender: str, salt: str) -> str:
    digest = hashlib.sha256(f"{salt}|{sender}".encode()).hexdigest()[:12]
    return f"participant_{digest}"


def relevant(body: str) -> bool:
    lowered = f" {body.casefold()} "
    return any(keyword in lowered for keyword in KEYWORDS)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--salt",
        required=True,
        help="Private one-time value used to create non-reversible participant labels",
    )
    args = parser.parse_args()

    messages = parse_export(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    kept = 0
    with args.output.open("w", encoding="utf-8") as destination:
        for message in messages:
            body = redact(message.body)
            lowered = body.casefold()
            if not relevant(body) or any(phrase in lowered for phrase in SYSTEM_PHRASES):
                continue
            record = {
                "date": message.date,
                "participant": participant_id(message.sender, args.salt),
                "candidate_text": body,
                "review_status": "manual_review_required",
            }
            destination.write(json.dumps(record, ensure_ascii=False) + "\n")
            kept += 1
    print(f"Wrote {kept} redacted review candidates to {args.output}")
    print("Do not index this file. Rewrite approved insights as general Markdown guidance.")


if __name__ == "__main__":
    main()
