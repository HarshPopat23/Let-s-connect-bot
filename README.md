# OLLM

OLLM is the open-source contributor Q and A bot for OSS Let's Connect. It answers Telegram questions from a curated repository using local retrieval-augmented generation. It does not require a paid language-model API.

The default system uses Telegram, Ollama, Qdrant and SQLite. Questions are embedded locally, matched against reviewed Markdown knowledge and answered by a locally hosted model. Source links are attached to every grounded answer.

## What OLLM covers

- Understanding open source and making a first contribution
- Choosing a healthy project and finding useful issues
- Git, GitHub, branches, commits, pull requests and reviews
- Communicating with maintainers and handling review delays
- Understanding large codebases without reading everything
- Documentation, testing, design and non-code contributions
- Responsible AI use and avoiding repository spam
- Licenses, CLA, DCO, privacy, secrets and security reports
- GSoC, LFX Mentorship and Outreachy preparation
- CNCF, Kubernetes and Kubeflow contribution basics
- Growing toward reviewer and maintainer responsibilities
- Presenting open-source experience accurately
- OSS Let's Connect values, activities and community behavior

## Privacy decision

The supplied WhatsApp export was used only to identify recurring questions and broad community principles. The raw export and contact VCF are not included. Phone numbers, participant identities, unrelated conversation, private anecdotes and unverified claims were deliberately excluded.

See [Knowledge Governance](docs/KNOWLEDGE_GOVERNANCE.md) and [Privacy](PRIVACY.md).

## Architecture

    Telegram question
        -> daily limit and cache
        -> local Ollama embedding
        -> Qdrant retrieval
        -> rule-based model selection
        -> local Ollama answer
        -> verified source links
        -> Telegram reply

See [Architecture](docs/ARCHITECTURE.md) and [Model Routing](docs/MODEL_ROUTING.md).

## Model priorities

| Tier | Default model | Intended questions |
| --- | --- | --- |
| Easy | `qwen3:4b` | Definitions, links and basic navigation |
| Standard | `mistral:7b-instruct` | Normal contribution and workflow guidance |
| Complex | `mistral-nemo:12b` | Architecture, security, governance and multi-part strategy |

If a selected model is unavailable, OLLM uses another installed configured model. It never silently calls a paid API.

## Fastest setup with Docker

Requirements:

- A Telegram bot token from `@BotFather`
- Docker Engine and Docker Compose
- At least 8 GB RAM for small models; more is recommended for the complex model
- Sufficient disk for Docker images and model files

Copy the configuration template:

    cp .env.example .env

Edit `.env` and set only this required value:

    TELEGRAM_BOT_TOKEN=your_token_here

Optionally set your Telegram numeric ID in `ADMIN_USER_IDS`. Leave Qdrant and hosted AI API key fields empty for a fully local deployment.

Start local services:

    docker compose up -d ollama qdrant

Download the configured models:

    docker compose --profile setup run --rm model-init

Build the knowledge index:

    docker compose --profile setup run --rm index

Start OLLM:

    docker compose up -d --build bot
    docker compose logs -f bot

Now message the bot privately, or add it to a group and use:

    /ask How should I choose my first open-source project?

## Local development without the bot container

Start Ollama and Qdrant with Docker, then create a Python environment:

    python3 -m venv .venv
    . .venv/bin/activate
    pip install -e ".[dev]"
    cp .env.example .env

For host-side commands, keep `OLLAMA_BASE_URL=http://localhost:11434`, `QDRANT_URL=http://localhost:6333`, `KNOWLEDGE_DIRECTORY=knowledge` and `STATE_DATABASE=data/ollm.sqlite3`.

Pull models from the Ollama container and index:

    docker compose --profile setup run --rm model-init
    ollm-index

Ask from the terminal:

    ollm-ask "What should I do when a maintainer does not review my PR?"

Run the bot:

    ollm

## Telegram behavior

- Private chat: every normal text message is treated as a question.
- Group chat: only `/ask question` is processed.
- Default limit: ten questions per Telegram user per UTC day.
- Repeated questions: cached for twenty-four hours.
- Feedback: users can mark an answer useful or needing improvement.
- Admin commands: `/status` and `/reindex` require `ADMIN_USER_IDS`.

See [BotFather Setup](docs/BOTFATHER_SETUP.md).

## Updating the knowledge base

Add or edit reviewed Markdown files under `knowledge`. Each file requires YAML front matter:

    ---
    title: Clear source title
    category: workflow
    source_url: https://official.example/guide
    updated: 2026-09-04
    ---

Rebuild the index:

    docker compose --profile setup run --rm index

Changing content changes the knowledge version, so old cache entries will not be reused.

## Configuration

All configuration lives in `.env`. The committed `.env.example` contains empty secret fields and safe defaults. Never commit `.env`.

Important controls include `DAILY_QUESTION_LIMIT`, `CACHE_TTL_SECONDS`, `RETRIEVAL_SCORE_THRESHOLD`, `RETRIEVAL_LIMIT`, `MAX_CONTEXT_CHARACTERS` and the three model names.

## Oracle Cloud deployment

See [Oracle Deployment](docs/DEPLOY_ORACLE.md). The default long-polling mode requires no public web endpoint. Qdrant and Ollama bind to localhost on the host and must not be publicly exposed.

## Tests

    make install
    make test
    make lint

Tests cover model routing, Markdown chunking, cache and quota state, Telegram message splitting and refusal when retrieval finds no reliable source.

## Important limitations

- A CPU-only free VM can answer slowly, especially with the complex model.
- RAG reduces hallucination but cannot eliminate it.
- Time-sensitive program details must be verified at the cited official page.
- Project-specific contributor rules override OLLM's general advice.
- OLLM cannot guarantee merge, selection, membership, payment or employment.
- OLLM is not legal or security-response advice.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [SECURITY.md](SECURITY.md). New knowledge must use authoritative sources and pass privacy review.

## License

Code is licensed under the MIT License. Individual linked sources remain under their own terms. Curated summaries should be original and should not reproduce large copyrighted passages.

