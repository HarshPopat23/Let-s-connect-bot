from __future__ import annotations

import logging

import discord
from discord import app_commands

from ollm.bot import split_telegram_text
from ollm.config import Settings
from ollm.rag import RAGService
from ollm.state import SQLiteState

logger = logging.getLogger(__name__)

DISCORD_MESSAGE_LIMIT = 1900


class DiscordOLLMBot:
    def __init__(self, settings: Settings, rag: RAGService, state: SQLiteState) -> None:
        self.settings = settings
        self.rag = rag
        self.state = state

    def build(self) -> discord.Client:
        intents = discord.Intents.default()
        intents.message_content = False
        client = discord.Client(intents=intents)
        tree = app_commands.CommandTree(client)

        @tree.command(name="ask", description="Ask an open-source contribution question")
        @app_commands.describe(question="What do you want to ask OLLM?")
        async def ask(interaction: discord.Interaction, question: str) -> None:
            await self._answer(interaction, question)

        @client.event
        async def on_ready() -> None:
            guild = discord.Object(id=self.settings.discord_guild_id) if self.settings.discord_guild_id else None
            try:
                if guild:
                    tree.copy_global_to(guild=guild)
                    await tree.sync(guild=guild)
                else:
                    await tree.sync()
                logger.info("Discord slash commands synced")
            except Exception as exc:
                logger.error("Failed to sync Discord slash commands: %s", exc, exc_info=True)
            try:
                await self.rag.initialize()
                logger.info("OLLM initialized with knowledge version %s", self.rag.version)
            except Exception as exc:
                logger.error(
                    "RAG initialization failed at startup (bot remains online): %s",
                    exc,
                    exc_info=True,
                )
            logger.info("Discord bot logged in as %s", client.user)

        return client

    async def _answer(self, interaction: discord.Interaction, question: str) -> None:
        question = " ".join(question.strip().split())
        if not question:
            await interaction.response.send_message("Please include a question.", ephemeral=True)
            return
        if len(question) > self.settings.max_question_characters:
            await interaction.response.send_message(
                f"Please shorten the question to {self.settings.max_question_characters} characters.",
                ephemeral=True,
            )
            return

        allowed, remaining = await self.state.consume_daily_quota(
            interaction.user.id, self.settings.daily_question_limit
        )
        if not allowed:
            await interaction.response.send_message(
                "You have reached today's question limit. Try again after midnight UTC, "
                "or ask the community if the question is urgent.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            result = await self.rag.answer(question)
        except Exception:
            logger.exception("Question processing failed for discord_user_id=%s", interaction.user.id)
            await interaction.followup.send(
                "OLLM could not process that question. The knowledge service may be "
                "temporarily unavailable. Please try again later.",
                ephemeral=True,
            )
            return

        footer = f"\n\n_Model tier: {result.tier.value}. Questions remaining today: {remaining}._"
        parts = split_telegram_text(result.answer + footer, limit=DISCORD_MESSAGE_LIMIT)
        for part in parts:
            await interaction.followup.send(part, ephemeral=True)
