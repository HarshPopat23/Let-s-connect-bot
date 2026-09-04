#!/usr/bin/env sh
set -eu

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env. Add TELEGRAM_BOT_TOKEN, then run this script again."
  exit 1
fi

if ! grep -Eq '^TELEGRAM_BOT_TOKEN=.+$' .env; then
  echo "TELEGRAM_BOT_TOKEN is empty in .env."
  exit 1
fi

docker compose up -d ollama qdrant
docker compose --profile setup run --rm model-init
docker compose --profile setup run --rm index
docker compose up -d --build bot
docker compose ps

