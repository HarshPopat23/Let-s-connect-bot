#!/usr/bin/env python3
"""Build the OLLM situation-only Markdown and JSONL dataset."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

from dataset_specs import CATEGORIES

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
DATASET = ROOT / "dataset"

SOURCE_CATALOG = {
    "github-contributing": (
        "GitHub Docs: Contributing to open source",
        "https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-open-source",
    ),
    "github-project": (
        "GitHub Docs: Contributing to a project",
        "https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project",
    ),
    "github-issues": (
        "GitHub Docs: Issues",
        "https://docs.github.com/en/issues",
    ),
    "github-prs": (
        "GitHub Docs: Pull requests",
        "https://docs.github.com/en/pull-requests",
    ),
    "github-reviews": (
        "GitHub Docs: Reviewing proposed changes",
        "https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request",
    ),
    "github-actions": (
        "GitHub Docs: GitHub Actions",
        "https://docs.github.com/en/actions",
    ),
    "github-actions-security": (
        "GitHub Docs: Secure use reference",
        "https://docs.github.com/en/actions/reference/security/secure-use",
    ),
    "github-repository-security": (
        "GitHub Docs: Repository security and analysis",
        "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository",
    ),
    "github-releases": (
        "GitHub Docs: About releases",
        "https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases",
    ),
    "git-reference": (
        "Git: Reference",
        "https://git-scm.com/docs",
    ),
    "open-source-guide": (
        "Open Source Guides: How to contribute",
        "https://opensource.guide/how-to-contribute/",
    ),
    "welcoming-communities": (
        "Open Source Guides: Building welcoming communities",
        "https://opensource.guide/building-community/",
    ),
    "maintainer-guide": (
        "Open Source Guides: Best practices for maintainers",
        "https://opensource.guide/best-practices/",
    ),
    "governance-guide": (
        "Open Source Guides: Leadership and governance",
        "https://opensource.guide/leadership-and-governance/",
    ),
    "legal-guide": (
        "Open Source Guides: The legal side of open source",
        "https://opensource.guide/legal/",
    ),
    "choose-license": (
        "Choose an open source license",
        "https://choosealicense.com/",
    ),
    "contributor-covenant": (
        "Contributor Covenant 2.1",
        "https://www.contributor-covenant.org/version/2/1/code_of_conduct/",
    ),
    "dco": (
        "Developer Certificate of Origin",
        "https://developercertificate.org/",
    ),
    "cncf-getting-started": (
        "CNCF Contributors: Getting started",
        "https://contribute.cncf.io/contributors/getting-started/",
    ),
    "cncf-governance": (
        "CNCF Governance",
        "https://contribute.cncf.io/community/governance/",
    ),
    "cncf-security": (
        "CNCF project security guidelines",
        "https://contribute.cncf.io/projects/best-practices/security/",
    ),
    "kubernetes-contribute": (
        "Kubernetes: Contribute",
        "https://kubernetes.io/docs/contribute/",
    ),
    "kubernetes-review": (
        "Kubernetes: Reviewing pull requests",
        "https://kubernetes.io/docs/contribute/review/reviewing-prs/",
    ),
    "kubernetes-localization": (
        "Kubernetes: Localizing documentation",
        "https://kubernetes.io/docs/contribute/localization/",
    ),
    "kubeflow-contributing": (
        "Kubeflow: Contributing",
        "https://www.kubeflow.org/docs/about/contributing/",
    ),
    "gsoc-guide": (
        "Google Summer of Code guides",
        "https://developers.google.com/open-source/gsoc/resources/guide",
    ),
    "gsoc-ai": (
        "Google Summer of Code AI guidance",
        "https://developers.google.com/open-source/gsoc/resources/ai_guidance",
    ),
    "lfx-guide": (
        "LFX Mentorship mentee guide",
        "https://docs.linuxfoundation.org/lfx/mentorship/mentee-guide",
    ),
    "outreachy-guide": (
        "Outreachy applicant guide",
        "https://www.outreachy.org/docs/applicant/",
    ),
    "openssf-baseline": (
        "OpenSSF Project Security Baseline",
        "https://baseline.openssf.org/",
    ),
}

GROUP_RANGES = (
    (1, 5, "01-getting-started"),
    (6, 10, "02-git-and-github-practices"),
    (11, 16, "03-issues"),
    (17, 23, "04-pull-requests"),
    (24, 27, "05-quality-documentation-and-inclusion"),
    (28, 31, "06-community-and-collaboration"),
    (32, 35, "07-security-privacy-and-legal"),
    (36, 39, "08-programs-and-ecosystems"),
    (40, 45, "09-growth-governance-and-sustainability"),
    (46, 50, "10-advanced-engineering-and-project-lifecycle"),
)


def group_for(category_number: int) -> str:
    for first, last, group in GROUP_RANGES:
        if first <= category_number <= last:
            return group
    raise ValueError(f"No knowledge group for category {category_number}")


def sentence(focus: str, complication: str) -> str:
    text = f"{focus[:1].upper()}{focus[1:]}, while {complication}."
    return " ".join(text.split())


def build() -> list[dict[str, object]]:
    if KNOWLEDGE.exists():
        shutil.rmtree(KNOWLEDGE)
    KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    DATASET.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    index_rows: list[tuple[int, str, str, str, str]] = []

    for category_number, category in enumerate(CATEGORIES, start=1):
        group = group_for(category_number)
        folder = KNOWLEDGE / group / category["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        category_records: list[dict[str, object]] = []
        for round_number in range(5):
            difficulty = ("beginner", "beginner", "intermediate", "intermediate", "advanced")[
                round_number
            ]
            for focus_number, focus in enumerate(category["focuses"]):
                local_number = round_number * len(category["focuses"]) + focus_number + 1
                complication = category["complications"][
                    (focus_number * 2 + round_number) % len(category["complications"])
                ]
                situation = sentence(focus, complication)
                record = {
                    "id": f"OSS-{category_number:02d}-{local_number:03d}",
                    "group": group,
                    "category": category["slug"],
                    "title": category["title"],
                    "journey_stage": category["stage"],
                    "difficulty": difficulty,
                    "applicable_roles": category["roles"],
                    "situation": situation,
                    "chat_informed": category["chat_informed"],
                    "source_keys": category["sources"],
                    "source_urls": [SOURCE_CATALOG[key][1] for key in category["sources"]],
                }
                records.append(record)
                category_records.append(record)

        lines = [
            "---",
            f"title: {category['title']}",
            f"group: {group}",
            f"category: {category['slug']}",
            f"journey_stage: {category['stage']}",
            f"scenario_count: {len(category_records)}",
            "content_type: situations-only",
            f"chat_informed: {str(category['chat_informed']).lower()}",
            "source_keys:",
            *[f"  - {key}" for key in category["sources"]],
            "---",
            "",
            f"# {category['title']}",
            "",
            "This file contains situations only. It intentionally provides no answers or recommended actions.",
            "",
        ]
        for level in ("beginner", "intermediate", "advanced"):
            lines.extend([f"## {level.title()} situations", ""])
            for record in category_records:
                if record["difficulty"] == level:
                    lines.append(f"- {record['id']}: {record['situation']}")
            lines.append("")
        (folder / "situations.md").write_text("\n".join(lines), encoding="utf-8")
        index_rows.append((category_number, category["title"], group, category["slug"], len(category_records)))

    with (DATASET / "situations.jsonl").open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    with (DATASET / "catalog.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        csv_fields = [
            "id",
            "group",
            "category",
            "journey_stage",
            "difficulty",
            "applicable_roles",
            "situation",
            "chat_informed",
        ]
        writer.writerow(csv_fields)
        for record in records:
            row = []
            for key in csv_fields:
                value = record[key]
                row.append(" | ".join(value) if isinstance(value, list) else value)
            writer.writerow(row)

    index_lines = [
        "# Situation category index",
        "",
        f"Total categories: {len(index_rows)}",
        "",
        f"Total situations: {len(records)}",
        "",
        "| Number | Category | Group | Folder | Situations |",
        "| ---: | --- | --- | --- | ---: |",
    ]
    index_lines.extend(
        f"| {number} | {title} | `{group}` | `knowledge/{group}/{slug}/situations.md` | {count} |"
        for number, title, group, slug, count in index_rows
    )
    (ROOT / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    digest = hashlib.sha256((DATASET / "situations.jsonl").read_bytes()).hexdigest()
    stats = {
        "categories": len(index_rows),
        "groups": len(GROUP_RANGES),
        "situations": len(records),
        "markdown_files": len(index_rows),
        "chat_informed_categories": sum(bool(c["chat_informed"]) for c in CATEGORIES),
        "sha256_situations_jsonl": digest,
    }
    (DATASET / "stats.json").write_text(
        json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return records


if __name__ == "__main__":
    built = build()
    print(f"Built {len(built)} situations across {len(CATEGORIES)} categories")
