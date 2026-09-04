#!/usr/bin/env python3
"""Search the situation catalogue without generating answers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="", help="Words to match in situation text")
    parser.add_argument("--group", default="", help="Exact major knowledge-group folder name")
    parser.add_argument("--category", default="", help="Exact category folder name")
    parser.add_argument(
        "--difficulty",
        choices=["beginner", "intermediate", "advanced"],
        default="",
    )
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    terms = [term.casefold() for term in args.query.split() if term]
    matches = []
    path = ROOT / "dataset" / "situations.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if args.group and record["group"] != args.group:
            continue
        if args.category and record["category"] != args.category:
            continue
        if args.difficulty and record["difficulty"] != args.difficulty:
            continue
        haystack = f"{record['title']} {record['situation']}".casefold()
        if terms and not all(re.search(rf"\b{re.escape(term)}\b", haystack) for term in terms):
            continue
        matches.append(record)
        if len(matches) >= max(args.limit, 0):
            break

    for record in matches:
        print(
            f"{record['id']} | {record['group']} | {record['category']} | "
            f"{record['difficulty']}"
        )
        print(record["situation"])
        print()
    print(f"Matches shown: {len(matches)}")


if __name__ == "__main__":
    main()
