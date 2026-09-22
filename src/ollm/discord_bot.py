from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from ollm.config import Settings
from ollm.rag import RAGService
from ollm.state import SQLiteState

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

_CITATION_MARKER = re.compile(r"\s?\[\d+\]")

GREETINGS = {
    "hi",
    "hii",
    "hiii",
    "hello",
    "helloo",
    "hey",
    "heyy",
    "namaste",
    "good morning",
    "good afternoon",
    "good evening",
    "yo",
    "hola",
}

GREETING_MESSAGE = (
    "Hello! 👋 I'm **OLLM**, your open-source contributor guide for **OSS Let's Connect**.\n\n"
    "I'm here to help you navigate your open-source journey! You can ask me things like:\n"
    "• *How do I choose my first open-source project?*\n"
    "• *What is OSS Let's Connect and when are the meetings?*\n"
    "• *How do I create a pull request on GitHub?*\n"
    "• *What are GSoC, LFX, and Outreachy?*\n"
    "• *How should I ask a maintainer for help?*\n\n"
    "Feel free to ask any question using `/ask <question>`!"
)


def format_for_discord(text: str) -> str:
    """Format answer text for Discord rendering."""
    text = _CITATION_MARKER.sub("", text)
    return text.strip()


def split_discord_text(text: str, limit: int = 1900) -> list[str]:
    """Split text into chunks under Discord's 2000 character limit."""
    if len(text) <= limit:
        return [text]
    parts: list[str] = []
    remaining = text
    while len(remaining) > limit:
        split_at = remaining.rfind("\n", 0, limit)
        if split_at < limit // 2:
            split_at = remaining.rfind(" ", 0, limit)
        if split_at < limit // 2:
            split_at = limit
        parts.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()
    if remaining:
        parts.append(remaining)
    return parts


class FeedbackView(discord.ui.View):
    def __init__(
        self, state: SQLiteState, cache_key: str, user_id: int, timeout: float = 300
    ) -> None:
        super().__init__(timeout=timeout)
        self.state = state
        self.cache_key = cache_key
        self.user_id = user_id

    @discord.ui.button(label="Useful", style=discord.ButtonStyle.success, emoji="👍")
    async def useful(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self._handle_feedback(interaction, "useful")

    @discord.ui.button(
        label="Needs improvement", style=discord.ButtonStyle.secondary, emoji="👎"
    )
    async def poor(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self._handle_feedback(interaction, "poor")

    async def _handle_feedback(self, interaction: discord.Interaction, rating: str) -> None:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "Only the person who asked can provide feedback.", ephemeral=True
            )
            return
        await self.state.add_feedback(interaction.user.id, self.cache_key[:20], rating)
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        label = (
            "Feedback recorded: Useful 👍"
            if rating == "useful"
            else "Feedback recorded: Needs improvement 👎"
        )
        try:
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(label, ephemeral=True)
        except Exception as exc:
            logger.warning("Could not acknowledge feedback button: %s", exc)


class OLLMDiscordBot(commands.Bot):
    def __init__(self, settings: Settings, rag: RAGService, state: SQLiteState) -> None:
        intents = discord.Intents.default()
        # Do not request privileged intents like message_content so the bot connects
        # smoothly without requiring manual intent toggles in the Discord Developer Portal.
        super().__init__(command_prefix="!", intents=intents)
        self.settings = settings
        self.rag = rag
        self.state = state
        self._register_slash_commands()

    def _register_slash_commands(self) -> None:
        @self.tree.command(
            name="ask",
            description="Ask OLLM an open-source contribution question",
        )
        @app_commands.describe(question="Your question about open source, GSoC, GitHub, etc.")
        async def ask_command(interaction: discord.Interaction, question: str) -> None:
            await self._handle_ask_interaction(interaction, question)

        @self.tree.command(
            name="about",
            description="About OSS Let's Connect",
        )
        async def about_command(interaction: discord.Interaction) -> None:
            text = (
                "**OSS Let's Connect** helps newcomers learn open source, make meaningful "
                "contributions, collaborate respectfully and grow toward mentorship and "
                "maintainership. The community values collaboration over competition, "
                "welcomes beginner questions and prioritizes consistency and understanding.\n\n"
                "🌐 Website: https://oss-website-navy.vercel.app/\n"
                "🐙 GitHub: https://github.com/OSSConnect"
            )
            await interaction.response.send_message(text)

        @self.tree.command(
            name="sources",
            description="See how OLLM answers are grounded",
        )
        async def sources_command(interaction: discord.Interaction) -> None:
            text = (
                "**OLLM Sources & Grounding**\n"
                "OLLM retrieves curated Markdown documents before answering. Its sources include "
                "official GitHub documentation, Open Source Guides, GSoC, LFX Mentorship, "
                "Outreachy, CNCF, Kubernetes, Contributor Covenant, OpenSSF and community guidance. "
                "Each answer is strictly grounded in these verified sources."
            )
            await interaction.response.send_message(text)

        @self.tree.command(
            name="privacy",
            description="Understand stored data and privacy",
        )
        async def privacy_command(interaction: discord.Interaction) -> None:
            text = (
                "**OLLM Privacy Information**\n"
                "OLLM stores your Discord user ID and daily question count for quota limits. "
                "It caches generated answers and records optional useful or not useful feedback. "
                "It does not store personal contact information.\n"
                "⚠️ *Do not send passwords, API tokens, private repository keys or sensitive personal data.*"
            )
            await interaction.response.send_message(text)

        @self.tree.command(
            name="help",
            description="How to use OLLM",
        )
        async def help_command(interaction: discord.Interaction) -> None:
            text = (
                "**OLLM Commands**\n"
                "• `/ask <question>` - Ask OLLM any open-source question\n"
                "• `/about` - Learn about OSS Let's Connect\n"
                "• `/sources` - See how answers are grounded\n"
                "• `/privacy` - Understand stored data\n"
                "• `/status` - Service status (administrators)\n\n"
                "💡 *Tip: For a useful answer, include the project name, repository or issue link, "
                "what you tried, the expected result and what actually happened.*"
            )
            await interaction.response.send_message(text)

        @self.tree.command(
            name="status",
            description="Service status for administrators",
        )
        async def status_command(interaction: discord.Interaction) -> None:
            if not self._is_admin(interaction.user.id):
                await interaction.response.send_message(
                    "This command is only available to administrators.", ephemeral=True
                )
                return
            models = sorted(await self.rag.ollama.list_models())
            stats = await self.state.statistics()
            chunk_count = await self.state.get_metadata("knowledge_chunk_count") or "unknown"
            text = (
                "📊 **OLLM Status**\n"
                f"• Knowledge version: `{self.rag.version}`\n"
                f"• Indexed chunks: `{chunk_count}`\n"
                f"• Models: {', '.join(f'`{m}`' for m in models) or 'none'}\n"
                f"• Users: `{stats['users']}`\n"
                f"• Questions: `{stats['questions']}`\n"
                f"• Cached answers: `{stats['cached_answers']}`\n"
                f"• Feedback records: `{stats['feedback']}`"
            )
            await interaction.response.send_message(text, ephemeral=True)

        @self.tree.command(
            name="reindex",
            description="Rebuild the knowledge index (administrators)",
        )
        async def reindex_command(interaction: discord.Interaction) -> None:
            if not self._is_admin(interaction.user.id):
                await interaction.response.send_message(
                    "This command is only available to administrators.", ephemeral=True
                )
                return
            await interaction.response.defer(thinking=True, ephemeral=True)
            count = await self.rag.reindex()
            await interaction.followup.send(
                f"Knowledge index rebuilt successfully with `{count}` chunks.", ephemeral=True
            )

    def _is_admin(self, user_id: int) -> bool:
        return user_id in self.settings.admin_user_ids

    async def setup_hook(self) -> None:
        if self.settings.discord_guild_id:
            try:
                guild_obj = discord.Object(id=self.settings.discord_guild_id)
                self.tree.copy_global_to(guild=guild_obj)
                synced = await self.tree.sync(guild=guild_obj)
                logger.info(
                    "Synced %d Discord slash commands to guild %d",
                    len(synced),
                    self.settings.discord_guild_id,
                )
            except Exception as exc:
                logger.warning(
                    "Failed to sync commands to guild %d: %s",
                    self.settings.discord_guild_id,
                    exc,
                )
        try:
            global_synced = await self.tree.sync()
            logger.info("Synced %d global Discord slash commands", len(global_synced))
        except Exception as exc:
            logger.warning("Failed to sync global Discord slash commands: %s", exc)

    async def on_ready(self) -> None:
        logger.info(
            "Logged in to Discord as %s (ID: %s)",
            self.user,
            self.user.id if self.user else "unknown",
        )

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        # Only handle DMs here, not @mentions in a public channel: a DM is naturally
        # private to the asker, but a public-channel reply cannot be made ephemeral,
        # so answering there would leak the asker's question and answer to everyone.
        # Use /ask in a server channel for a private reply instead.
        is_dm = isinstance(message.channel, discord.DMChannel)

        if is_dm:
            clean_text = message.content
            if self.user:
                clean_text = clean_text.replace(f"<@{self.user.id}>", "").replace(
                    f"<@!{self.user.id}>", ""
                )
            clean_text = clean_text.strip()
            if clean_text:
                await self._handle_ask_message(message, clean_text)
                return

        await self.process_commands(message)

    async def _handle_ask_interaction(
        self, interaction: discord.Interaction, question: str
    ) -> None:
        if len(question) > self.settings.max_question_characters:
            await interaction.response.send_message(
                f"Please shorten the question to {self.settings.max_question_characters} characters.",
                ephemeral=True,
            )
            return

        normalized_q = re.sub(r"[^a-zA-Z\s]", "", question).strip().lower()
        if normalized_q in GREETINGS:
            await interaction.response.send_message(GREETING_MESSAGE)
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

        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            result = await self.rag.answer(question)
        except Exception:
            logger.exception(
                "Question processing failed in Discord for user_id=%s", interaction.user.id
            )
            await interaction.followup.send(
                "OLLM could not process that question. The local model or knowledge service "
                "may be temporarily unavailable. Please try again later.",
                ephemeral=True,
            )
            return

        footer = f"\n\n*Model tier: {result.tier.value} | Questions remaining today: {remaining}*"
        formatted = format_for_discord(result.answer) + footer
        parts = split_discord_text(formatted)

        for part in parts[:-1]:
            await interaction.followup.send(part, ephemeral=True)

        view = FeedbackView(self.state, result.cache_key, interaction.user.id)
        await interaction.followup.send(parts[-1], view=view, ephemeral=True)

    async def _handle_ask_message(self, message: discord.Message, question: str) -> None:
        if len(question) > self.settings.max_question_characters:
            await message.reply(
                f"Please shorten the question to {self.settings.max_question_characters} characters."
            )
            return

        normalized_q = re.sub(r"[^a-zA-Z\s]", "", question).strip().lower()
        if normalized_q in GREETINGS:
            await message.reply(GREETING_MESSAGE)
            return

        allowed, remaining = await self.state.consume_daily_quota(
            message.author.id, self.settings.daily_question_limit
        )
        if not allowed:
            await message.reply(
                "You have reached today's question limit. Try again after midnight UTC, "
                "or ask the community if the question is urgent."
            )
            return

        async with message.channel.typing():
            try:
                result = await self.rag.answer(question)
            except Exception:
                logger.exception(
                    "Question processing failed in Discord for user_id=%s", message.author.id
                )
                await message.reply(
                    "OLLM could not process that question. The local model or knowledge service "
                    "may be temporarily unavailable. Please try again later."
                )
                return

            footer = f"\n\n*Model tier: {result.tier.value} | Questions remaining today: {remaining}*"
            formatted = format_for_discord(result.answer) + footer
            parts = split_discord_text(formatted)

            for part in parts[:-1]:
                await message.channel.send(part)

            view = FeedbackView(self.state, result.cache_key, message.author.id)
            await message.reply(parts[-1], view=view)


class DiscordOLLMBot:
    """Compatibility wrapper for Discord standalone entrypoint."""

    def __init__(self, settings: Settings, rag: RAGService, state: SQLiteState) -> None:
        self.bot = OLLMDiscordBot(settings, rag, state)

    def build(self) -> OLLMDiscordBot:
        return self.bot
