# OLLM Architecture

OLLM is a retrieval-augmented Telegram assistant that runs without a paid language-model API.

## Request flow

1. A user sends a direct message or uses `/ask` in a group.
2. The bot validates chat access, length and the daily quota.
3. A normalized question and knowledge version form the cache key.
4. Ollama creates the query embedding with `nomic-embed-text`.
5. Qdrant returns the most relevant curated knowledge chunks above the score threshold.
6. The rule-based router selects an easy, standard or complex local model.
7. Ollama receives the question, retrieved context and strict grounding instructions.
8. OLLM appends verified source links outside the model output and sends the answer.
9. The answer is cached in SQLite and optional feedback is recorded.

## Trust boundaries

Telegram supplies untrusted user input. Markdown files are curated but are still presented to the model as reference data, not instructions. The prompt tells the model to ignore embedded instructions. The model cannot call shell commands, GitHub or Telegram tools.

Qdrant is bound only to localhost on the host. The Telegram token remains in `.env` and is not committed. Raw chats and contacts are never copied into the image or knowledge directory.

## Components

`bot.py` contains Telegram commands and group behavior.

`rag.py` performs retrieval, grounded generation and source attachment.

`router.py` chooses models without spending an extra model inference.

`knowledge.py` parses front matter, sections and deterministic chunks.

`vector_store.py` manages the Qdrant collection.

`state.py` provides SQLite caching, limits, feedback and metadata.

`ollama.py` is the local chat and embedding client.

## Why long polling

The default deployment uses Telegram long polling. It does not require a public domain, TLS certificate or inbound application port, which is convenient for one free Oracle VM. A webhook can be added later when horizontal scaling is required. Telegram permits either polling or webhooks, not both simultaneously.

## Scaling boundary

One CPU-only free VM is appropriate for an initial community bot with strict limits and caching. Local generation is serialized by available compute and can be slow under concurrent load. The first scaling steps are stronger caching, smaller models, a request queue and separate Ollama hardware. Multiple bot workers require coordinated update handling and a shared rate-limit/cache database.

