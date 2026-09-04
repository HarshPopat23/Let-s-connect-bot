# Contributing to OLLM

Thank you for helping build a trustworthy guide for open-source newcomers.

## Before starting

Search existing issues and pull requests. For a large feature or knowledge-area expansion, open an issue explaining the user need, source plan, privacy implications and proposed tests.

## Development setup

    python3 -m venv .venv
    . .venv/bin/activate
    pip install -e ".[dev]"
    cp .env.example .env
    docker compose up -d ollama qdrant

Never put a real token in a committed file.

## Code changes

- Keep pull requests focused.
- Add tests for behavior changes.
- Run `ruff check .` and `pytest -q`.
- Do not introduce a hosted paid service into the default path.
- Do not log complete questions, chat messages, tokens or personal data.
- Preserve grounded refusal when retrieval lacks reliable evidence.

## Knowledge changes

Prefer official documentation, project governance and primary sources. Write an original summary rather than copying a page. Put one clear subject in each Markdown file and include front matter.

Time-sensitive facts need an update date and wording that directs users to the official current page. Do not claim that a past GSoC or LFX organization will return.

Community-derived advice must be anonymized and rewritten as general guidance. Raw chats, phone numbers, participant names, private links, application material and contact files are prohibited.

Run `ollm-index` after knowledge changes and test at least five representative questions. Check that the returned sources actually support the answer.

## Pull request description

Explain the problem, the reason for the change, implementation, testing, security or privacy considerations and knowledge sources. Disclose meaningful AI assistance according to the repository policy and confirm that you reviewed every submitted line.

