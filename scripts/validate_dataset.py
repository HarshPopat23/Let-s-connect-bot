#!/usr/bin/env python3
"""Validate count, uniqueness, privacy, and situation-only guarantees."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

from build_dataset import SOURCE_CATALOG

ROOT = Path(__file__).resolve().parents[1]
JSONL = ROOT / "dataset" / "situations.jsonl"
CATALOG = ROOT / "dataset" / "catalog.csv"
SITUATION_FILES = sorted((ROOT / "knowledge").glob("*/*/situations.md"))
ID = re.compile(r"^OSS-\d{2}-\d{3}$")
CATEGORY = re.compile(r"^\d{2}-[a-z0-9-]+$")
PHONE = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def fail(message: str) -> None:
    raise SystemExit(f"Validation failed: {message}")


def main() -> None:
    records = [json.loads(line) for line in JSONL.read_text(encoding="utf-8").splitlines()]
    if len(records) != 2500:
        fail(f"expected 2500 records, found {len(records)}")
    if len(SITUATION_FILES) != 50:
        fail(f"expected 50 Markdown files, found {len(SITUATION_FILES)}")

    ids = [str(record.get("id", "")) for record in records]
    situations = [str(record.get("situation", "")) for record in records]
    if any(not ID.fullmatch(item) for item in ids):
        fail("one or more IDs do not match OSS-NN-NNN")
    if len(ids) != len(set(ids)):
        fail("duplicate IDs found")
    if len(situations) != len(set(situations)):
        fail("duplicate situation text found")

    counts = Counter(str(record["category"]) for record in records)
    if set(counts.values()) != {50}:
        fail(f"every category must contain 50 situations: {dict(counts)}")

    required_keys = {
        "id",
        "group",
        "category",
        "title",
        "journey_stage",
        "difficulty",
        "applicable_roles",
        "situation",
        "chat_informed",
        "source_keys",
        "source_urls",
    }
    allowed_stages = {
        "discover",
        "learn",
        "contribute",
        "collaborate",
        "grow",
        "lead",
        "maintain",
        "sustain",
        "program",
        "ecosystem",
    }
    allowed_difficulties = {"beginner", "intermediate", "advanced"}
    forbidden_keys = {"answer", "solution", "recommendation", "next_step"}
    for record in records:
        if set(record) != required_keys:
            fail(f"schema field mismatch in {record.get('id', 'unknown')}")
        if forbidden_keys.intersection(record):
            fail(f"answer-like field found in {record['id']}")
        if not CATEGORY.fullmatch(str(record["category"])):
            fail(f"invalid category in {record['id']}")
        if not CATEGORY.fullmatch(str(record["group"])):
            fail(f"invalid group in {record['id']}")
        if record["journey_stage"] not in allowed_stages:
            fail(f"invalid journey stage in {record['id']}")
        if record["difficulty"] not in allowed_difficulties:
            fail(f"invalid difficulty in {record['id']}")
        source_keys = record.get("source_keys", [])
        if not source_keys or any(key not in SOURCE_CATALOG for key in source_keys):
            fail(f"unknown or missing source key in {record['id']}")
        expected_urls = [SOURCE_CATALOG[key][1] for key in source_keys]
        if record.get("source_urls") != expected_urls:
            fail(f"source URL mismatch in {record['id']}")
        if any(not str(url).startswith("https://") for url in record["source_urls"]):
            fail(f"non-HTTPS source URL in {record['id']}")
        if not record.get("applicable_roles"):
            fail(f"missing applicable roles in {record['id']}")
        situation = str(record["situation"])
        if "http://" in situation or "https://" in situation:
            fail(f"URL embedded in situation text: {record['id']}")
        if EMAIL.search(situation) or PHONE.search(situation):
            fail(f"possible personal contact data in {record['id']}")
        if "whatsapp" in situation.casefold() or "participant_" in situation.casefold():
            fail(f"raw-chat marker found in {record['id']}")

    for path in SITUATION_FILES:
        bullets = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("- OSS-"))
        if bullets != 50:
            fail(f"{path.relative_to(ROOT)} contains {bullets} situations")

    with CATALOG.open(encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    if len(csv_rows) != len(records):
        fail("CSV and JSONL row counts differ")

    forbidden_names = {"chat.txt", "contacts.vcf"}
    if any(path.name.casefold() in forbidden_names for path in ROOT.rglob("*")):
        fail("forbidden private chat or contacts file found")

    forbidden_in_data = {".env", "chat.txt", "contacts.vcf"}
    for search_dir in [ROOT / "dataset", ROOT / "knowledge", ROOT / "docs"]:
        if search_dir.exists() and any(path.name.casefold() in forbidden_in_data for path in search_dir.rglob("*")):
            fail("forbidden private or secret file found in public dataset/knowledge/docs directories")

    print(
        f"Validated {len(records)} unique situations in {len(SITUATION_FILES)} categories; "
        "no answer fields or personal contact data detected."
    )


if __name__ == "__main__":
    main()
