.PHONY: install test lint services models index run up logs down check

install:
	python3 -m venv .venv
	.venv/bin/pip install -e ".[dev]"

test:
	.venv/bin/pytest -q

lint:
	.venv/bin/ruff check .

services:
	docker compose up -d ollama qdrant

models:
	docker compose --profile setup run --rm model-init

index:
	docker compose --profile setup run --rm index

run:
	.venv/bin/ollm

up:
	docker compose up -d ollama qdrant bot

logs:
	docker compose logs -f bot

down:
	docker compose down

check:
	docker compose run --rm bot ollm-check

