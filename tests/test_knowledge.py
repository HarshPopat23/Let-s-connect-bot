from pathlib import Path

import pytest

from ollm.knowledge import KnowledgeError, knowledge_version, load_knowledge


def test_loads_front_matter_and_sections(tmp_path: Path) -> None:
    document = tmp_path / "guide.md"
    document.write_text(
        """---
title: Test Guide
category: test
source_url: https://example.test/guide
updated: 2026-09-04
---

# First section

Useful contributor guidance.

# Second section

More guidance.
""",
        encoding="utf-8",
    )
    chunks = load_knowledge(tmp_path)
    assert len(chunks) == 2
    assert chunks[0].title == "Test Guide"
    assert chunks[0].source_url == "https://example.test/guide"
    assert knowledge_version(chunks) == knowledge_version(load_knowledge(tmp_path))


def test_rejects_document_without_front_matter(tmp_path: Path) -> None:
    (tmp_path / "bad.md").write_text("# Missing metadata", encoding="utf-8")
    with pytest.raises(KnowledgeError):
        load_knowledge(tmp_path)


def test_skips_situations_only_and_unindexed_documents(tmp_path: Path) -> None:
    (tmp_path / "situations.md").write_text(
        """---
title: Situations Catalogue
category: test
content_type: situations-only
---

# Situations

- Some situation
""",
        encoding="utf-8",
    )
    (tmp_path / "ignored.md").write_text(
        """---
title: Ignored Guide
index: false
---

# Content
""",
        encoding="utf-8",
    )
    (tmp_path / "valid.md").write_text(
        """---
title: Valid Guide
category: test
source_url: https://example.test/valid
---

# Valid Section

Valid indexable content.
""",
        encoding="utf-8",
    )
    chunks = load_knowledge(tmp_path)
    assert len(chunks) == 1
    assert chunks[0].title == "Valid Guide"


