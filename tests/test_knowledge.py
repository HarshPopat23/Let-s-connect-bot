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


def test_nested_subheading_inherits_parent(tmp_path: Path) -> None:
    (tmp_path / "faq.md").write_text(
        """---
title: Maintainer FAQ
category: admin
---

# FAQ

## 1. How do I start?

### Answer

Start with tools you use.

### Checklist

Step 1 and step 2.
""",
        encoding="utf-8",
    )
    chunks = load_knowledge(tmp_path)
    assert len(chunks) == 2
    assert chunks[0].section == "1. How do I start? - Answer"
    assert "Start with tools you use." in chunks[0].text
    assert chunks[1].section == "1. How do I start? - Checklist"
    assert "Step 1 and step 2." in chunks[1].text


