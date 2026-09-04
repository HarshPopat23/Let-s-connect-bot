# Deploy OLLM on Oracle Cloud Free Tier

Oracle availability and Always Free capacity vary by region. Verify the current Oracle terms before deployment. A card may be required for account verification even when using eligible free resources.

## Recommended instance

Choose an Always Free eligible Ubuntu ARM compute shape with as much allowed memory as available. Select the home region carefully. A CPU-only instance can run the small model but responses will be slower than a GPU service.

Open SSH port 22 only to your own IP when practical. Long polling means OLLM does not need a public web port. Do not expose ports 6333 or 11434 in the cloud security list.

## Install Docker

Follow Docker's current Ubuntu installation instructions. Add your user to the Docker group only if you understand the local privilege implications. Confirm:

    docker version
    docker compose version

## Deploy

Clone your OLLM repository and enter it:

    git clone YOUR_REPOSITORY_URL.git
    cd OLLM
    cp .env.example .env
    nano .env

Set `TELEGRAM_BOT_TOKEN` and your numeric `ADMIN_USER_IDS`. Leave API key fields empty for the local deployment.

Start Ollama and Qdrant:

    docker compose up -d ollama qdrant

Download local models. The complex model is optional on a constrained server:

    docker compose --profile setup run --rm model-init

If storage or memory is limited, set `MODEL_COMPLEX=mistral:7b-instruct` before running model initialization.

Build the knowledge index and start the bot:

    docker compose --profile setup run --rm index
    docker compose up -d --build bot
    docker compose logs -f bot

## Security

The Compose file binds Ollama and Qdrant host ports to `127.0.0.1`. Do not change them to public bindings. Protect `.env`, keep Ubuntu and Docker updated, disable password SSH login after confirming key access and configure backups.

## Resource limitations

Model downloads require several gigabytes of disk. The complex model requires more memory and can be slow. Start with `qwen3:4b` and `mistral:7b-instruct`, observe memory with `docker stats`, and add the complex model only if the instance remains stable.

