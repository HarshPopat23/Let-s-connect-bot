from __future__ import annotations

import hashlib
import re
import uuid
from pathlib import Path

import yaml

from ollm.models import DocumentChunk

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


class KnowledgeError(RuntimeError):
    pass


def _parse_markdown(path: Path) -> tuple[dict[str, object], str]:
    raw = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(raw)
    if not match:
        raise KnowledgeError(f"Knowledge file has no YAML front matter: {path}")
    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        raise KnowledgeError(f"Invalid YAML front matter: {path}")
    body = raw[match.end() :].strip()
    return metadata, body


def _sections(body: str, default_title: str) -> list[tuple[str, str]]:
    matches = list(HEADING.finditer(body))
    if not matches:
        return [(default_title, body)]
    result: list[tuple[str, str]] = []
    preface = body[: matches[0].start()].strip()
    if preface:
        result.append((default_title, preface))
    heading_hierarchy: dict[int, str] = {}
    for index, match in enumerate(matches):
        level = len(match.group(1))
        heading_text = match.group(2).strip()
        heading_hierarchy[level] = heading_text
        for d in list(heading_hierarchy.keys()):
            if d > level:
                del heading_hierarchy[d]
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        text = body[start:end].strip()
        if level <= 2:
            effective_heading = heading_text
        else:
            parent = heading_hierarchy.get(2) or heading_hierarchy.get(1) or default_title
            if parent and parent != heading_text:
                effective_heading = f"{parent} - {heading_text}"
            else:
                effective_heading = heading_text
        if text:
            result.append((effective_heading, text))
    return result


def _split_text(text: str, max_characters: int = 1800, overlap: int = 220) -> list[str]:
    if len(text) <= max_characters:
        return [text]
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip()
        if current and len(candidate) > max_characters:
            chunks.append(current)
            tail = current[-overlap:].lstrip()
            current = f"{tail}\n\n{paragraph}".strip()
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def load_knowledge(directory: Path) -> list[DocumentChunk]:
    if not directory.exists():
        raise KnowledgeError(f"Knowledge directory does not exist: {directory}")
    chunks: list[DocumentChunk] = []
    for path in sorted(directory.rglob("*.md")):
        metadata, body = _parse_markdown(path)
        if metadata.get("index", True) is False or metadata.get("content_type") == "situations-only":
            continue
        title = str(metadata.get("title") or path.stem.replace("-", " ").title())
        source_url = str(metadata.get("source_url") or "")
        category = str(metadata.get("category") or path.parent.name)
        updated = str(metadata.get("updated") or "")
        relative = path.relative_to(directory).as_posix()
        for section, section_text in _sections(body, title):
            for part_number, part in enumerate(_split_text(section_text), start=1):
                identity = f"{relative}|{section}|{part_number}|{part}"
                chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, identity))
                chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        title=title,
                        section=section,
                        text=part,
                        source_path=relative,
                        source_url=source_url,
                        category=category,
                        updated=updated,
                    )
                )
    if not chunks:
        raise KnowledgeError("No indexable Markdown knowledge was found")
    return chunks


def knowledge_version(chunks: list[DocumentChunk]) -> str:
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk.chunk_id.encode())
    return digest.hexdigest()[:16]
