# Operations Guide

## Routine checks

Run `docker compose ps` and `docker compose logs --tail=200 bot`. Use `/status` from a Telegram administrator account to view installed models, indexed chunks and aggregate usage.

Run `docker compose run --rm bot ollm-check` after model or infrastructure changes.

## Updating knowledge

Pull reviewed repository changes, rebuild the index, then restart the bot only if application code changed:

    git pull --ff-only
    docker compose --profile setup run --rm index
    docker compose up -d --build bot

The index command intentionally replaces the collection. Qdrant and Ollama remain private Docker services.

## Backups

Back up the repository and Docker volumes before major upgrades. The repository is the source of truth for knowledge; the vector index can be regenerated. The SQLite volume contains limits, feedback and cached answers and can be backed up separately.

## Model changes

Pull the new model with Ollama, update `.env`, test with `ollm-ask`, then restart the bot. Changing the embedding model requires a full reindex because vectors from different models are not interchangeable.

## Failure behavior

If Ollama or Qdrant is unavailable, users receive a temporary service message and the exception is logged without question text. If retrieval finds no sufficiently relevant source, OLLM refuses to invent an answer and recommends official project documentation or a maintainer.

## Cost control

The default daily limit is ten questions per Telegram user. Identical questions use a twenty-four-hour cache. Group messages require `/ask`, preventing the bot from processing ordinary conversation. Reduce context length or use only the easy and standard models if the VM becomes slow.

