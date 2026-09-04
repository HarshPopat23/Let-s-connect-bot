from __future__ import annotations

import logging

from telegram import BotCommand
from telegram.ext import Application

from ollm.bot import OLLMBot
from ollm.config import Settings
from ollm.logging_config import configure_logging
from ollm.services import Services

logger = logging.getLogger(__name__)


def main() -> None:
    settings = Settings()
    configure_logging(settings.log_level)
    services = Services.create(settings)
    application = OLLMBot(settings, services.rag, services.state).build()

    async def post_init(app: Application) -> None:
        await services.rag.initialize()
        await app.bot.set_my_commands(
            [
                BotCommand("ask", "Ask an open-source contribution question"),
                BotCommand("about", "About OSS Let's Connect"),
                BotCommand("sources", "How answers are grounded"),
                BotCommand("privacy", "Data and privacy information"),
                BotCommand("help", "How to use OLLM"),
            ]
        )
        logger.info("OLLM initialized with knowledge version %s", services.rag.version)

    async def post_shutdown(app: Application) -> None:
        del app
        await services.close()

    application.post_init = post_init
    application.post_shutdown = post_shutdown
    application.run_polling(drop_pending_updates=False)


if __name__ == "__main__":
    main()
