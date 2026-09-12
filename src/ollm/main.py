from __future__ import annotations

import asyncio
import logging
import os

from telegram import BotCommand, Update
from telegram.ext import Application

from ollm.bot import OLLMBot
from ollm.config import Settings
from ollm.logging_config import configure_logging
from ollm.services import Services

logger = logging.getLogger(__name__)


async def _start_health_server(port: int) -> asyncio.Server:
    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            await reader.readline()
            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 2\r\nConnection: close\r\n\r\nOK"
            writer.write(response)
            await writer.drain()
        except Exception:
            pass
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    server = await asyncio.start_server(handle_client, "0.0.0.0", port)
    logger.info("Health check server listening on port %d", port)
    return server


def main() -> None:
    settings = Settings()
    configure_logging(settings.log_level)
    services = Services.create(settings)
    application = OLLMBot(settings, services.rag, services.state).build()
    health_server: asyncio.Server | None = None

    async def post_init(app: Application) -> None:
        nonlocal health_server
        port_env = os.environ.get("PORT")
        if port_env and port_env.isdigit():
            health_server = await _start_health_server(int(port_env))
        try:
            await app.bot.delete_webhook(drop_pending_updates=True)
            logger.info("Cleared Telegram webhook and dropped pending updates")
        except Exception as exc:
            logger.warning("Could not clear webhook: %s", exc)
        try:
            await app.bot.set_my_commands(
                [
                    BotCommand("ask", "Ask an open-source contribution question"),
                    BotCommand("about", "About OSS Let's Connect"),
                    BotCommand("sources", "How answers are grounded"),
                    BotCommand("privacy", "Data and privacy information"),
                    BotCommand("help", "How to use OLLM"),
                ]
            )
        except Exception as exc:
            logger.warning("Could not set bot commands: %s", exc)
        try:
            await services.rag.initialize()
            logger.info("OLLM initialized with knowledge version %s", services.rag.version)
        except Exception as exc:
            logger.error("RAG initialization failed at startup (bot remains online): %s", exc, exc_info=True)

    async def post_shutdown(app: Application) -> None:
        del app
        if health_server:
            health_server.close()
            await health_server.wait_closed()
        await services.close()

    application.post_init = post_init
    application.post_shutdown = post_shutdown
    application.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

