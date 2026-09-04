#!/usr/bin/env sh
set -eu

docker compose --profile setup run --rm index
