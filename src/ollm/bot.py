from __future__ import annotations

import logging
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ParseMode
from telegram.error import BadRequest, Conflict, NetworkError, TimedOut
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.request import HTTPXRequest

from ollm.config import Settings
from ollm.rag import RAGService
from ollm.state import SQLiteState

logger = logging.getLogger(__name__)


class OLLMBot:
    def __init__(self, settings: Settings, rag: RAGService, state: SQLiteState) -> None:
        self.settings = settings
        self.rag = rag
        self.state = state

    def build(self) -> Application:
        # Ignore inherited proxy variables by default. This prevents an unrelated host-level
        # SOCKS proxy from breaking startup or unexpectedly receiving Telegram traffic.
        request = HTTPXRequest(httpx_kwargs={"trust_env": False})
        updates_request = HTTPXRequest(
            connection_pool_size=1,
            read_timeout=35,
            httpx_kwargs={"trust_env": False},
        )
        application = (
            ApplicationBuilder()
            .token(self.settings.require_bot_token())
            .request(request)
            .get_updates_request(updates_request)
            .build()
        )
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("about", self.about))
        application.add_handler(CommandHandler("privacy", self.privacy))
        application.add_handler(CommandHandler("sources", self.sources))
        application.add_handler(CommandHandler("ask", self.ask_command))
        application.add_handler(CommandHandler("status", self.status))
        application.add_handler(CommandHandler("reindex", self.reindex))
        application.add_handler(CallbackQueryHandler(self.feedback, pattern=r"^feedback:"))
        application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, self.ask_text
            )
        )
        application.add_error_handler(self.error_handler)
        return application

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        text = (
            "Welcome to OLLM, the open-source contributor guide for OSS Let's Connect.\n\n"
            "Ask about finding a project, understanding a codebase, issues, pull requests, "
            "reviews, community communication, GSoC, LFX, Outreachy, maintainership, "
            "licensing or responsible AI use.\n\n"
            "In a private chat, send your question directly. In a group, use /ask followed "
            "by the question. OLLM uses curated sources and shows links with its answers."
        )
        await update.effective_message.reply_text(text)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        text = (
            "Commands\n"
            "/ask question - ask OLLM in a group or private chat\n"
            "/about - learn about OSS Let's Connect\n"
            "/sources - see how answers are grounded\n"
            "/privacy - understand stored data\n"
            "/status - service status for administrators\n\n"
            "For a useful answer, include the project name, repository or issue link, what "
            "you tried, the expected result and the actual result."
        )
        await update.effective_message.reply_text(text)

    async def about(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        await update.effective_message.reply_text(
            "OSS Let's Connect helps newcomers learn open source, make meaningful "
            "contributions, collaborate respectfully and grow toward mentorship and "
            "maintainership. The community values collaboration over competition, "
            "welcomes beginner questions and prioritizes consistency and understanding.\n\n"
            "Website: https://oss-website-navy.vercel.app/\n"
            "GitHub: https://github.com/OSSConnect"
        )

    async def privacy(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        await update.effective_message.reply_text(
            "OLLM stores a Telegram numeric user ID and daily question count for limits. "
            "It caches generated answers and records optional useful or not useful feedback. "
            "It does not include the raw WhatsApp export or contacts in its knowledge base. "
            "Do not send passwords, tokens, private repository content or personal data."
        )

    async def sources(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        await update.effective_message.reply_text(
            "OLLM retrieves curated Markdown documents before answering. Its sources include "
            "official GitHub documentation, Open Source Guides, GSoC, LFX Mentorship, "
            "Outreachy, CNCF, Kubernetes, Contributor Covenant, OpenSSF and community guidance. "
            "Each answer includes the most relevant source links."
        )

    async def ask_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        question = " ".join(context.args).strip()
        if not question:
            await update.effective_message.reply_text(
                "Add your question after the command. Example: /ask How do I choose my first project?"
            )
            return
        await self._answer(update, question)

    async def ask_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        await self._answer(update, update.effective_message.text or "")

    async def _answer(self, update: Update, question: str) -> None:
        message = update.effective_message
        user = update.effective_user
        chat = update.effective_chat
        if not message or not user or not chat:
            return
        if (
            self.settings.telegram_allowed_chat_ids
            and chat.id not in self.settings.telegram_allowed_chat_ids
        ):
            await message.reply_text("This bot is not enabled for this chat.")
            return
        if len(question) > self.settings.max_question_characters:
            await message.reply_text(
                f"Please shorten the question to {self.settings.max_question_characters} characters."
            )
            return

        normalized_q = re.sub(r"[^a-zA-Z\s]", "", question).strip().lower()
        if normalized_q in {
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
        }:
            greeting = (
                "Hello! 👋 I'm OLLM, your open-source contributor guide for OSS Let's Connect.\n\n"
                "I'm here to help you navigate your open-source journey! You can ask me things like:\n"
                "• *How do I choose my first open-source project?*\n"
                "• *What is OSS Let's Connect and when are the meetings?*\n"
                "• *How do I create a pull request on GitHub?*\n"
                "• *What are GSoC, LFX, and Outreachy?*\n"
                "• *How should I ask a maintainer for help?*\n\n"
                "Feel free to ask any question!"
            )
            await message.reply_text(greeting, parse_mode=ParseMode.MARKDOWN)
            return

        allowed, remaining = await self.state.consume_daily_quota(
            user.id, self.settings.daily_question_limit
        )
        if not allowed:
            await message.reply_text(
                "You have reached today's question limit. Try again after midnight UTC, "
                "or ask the community if the question is urgent."
            )
            return
        await chat.send_action(ChatAction.TYPING)
        try:
            result = await self.rag.answer(question)
        except Exception:
            logger.exception("Question processing failed for user_id=%s", user.id)
            await message.reply_text(
                "OLLM could not process that question. The local model or knowledge service "
                "may be temporarily unavailable. Please try again later."
            )
            return

        sources_block = ""
        if result.sources:
            unique_sources = []
            seen = set()
            for s in result.sources:
                key = (s.title, s.section)
                if key not in seen:
                    seen.add(key)
                    display = f"{s.title}" + (f" - *{s.section}*" if s.section else "")
                    if s.source_url:
                        unique_sources.append(f"• [{display}]({s.source_url})")
                    else:
                        unique_sources.append(f"• {display}")
                if len(unique_sources) >= 3:
                    break
            if unique_sources:
                sources_block = "\n\n*📖 Knowledge Base Sources:*\n" + "\n".join(unique_sources)

        footer = f"\n\nModel tier: {result.tier.value}. Questions remaining today: {remaining}."
        formatted = format_for_telegram(result.answer) + sources_block + footer
        parts = split_telegram_text(formatted)
        for part in parts[:-1]:
            await send_markdown(message, part, disable_web_page_preview=True)
        short_key = result.cache_key[:20]
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Useful", callback_data=f"feedback:useful:{short_key}"),
                    InlineKeyboardButton(
                        "Needs improvement", callback_data=f"feedback:poor:{short_key}"
                    ),
                ]
            ]
        )
        await send_markdown(
            message, parts[-1], reply_markup=keyboard, disable_web_page_preview=True
        )

    async def feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        query = update.callback_query
        user = update.effective_user
        if not query or not user:
            return
        await query.answer()
        _, rating, cache_key = query.data.split(":", maxsplit=2)
        await self.state.add_feedback(user.id, cache_key, rating)
        await query.edit_message_reply_markup(reply_markup=None)

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if not self._is_admin(update):
            await update.effective_message.reply_text(
                "This command is available to administrators."
            )
            return
        models = sorted(await self.rag.ollama.list_models())
        stats = await self.state.statistics()
        chunk_count = await self.state.get_metadata("knowledge_chunk_count") or "unknown"
        await update.effective_message.reply_text(
            "OLLM status\n"
            f"Knowledge version: {self.rag.version}\n"
            f"Indexed chunks: {chunk_count}\n"
            f"Models: {', '.join(models) or 'none'}\n"
            f"Users: {stats['users']}\n"
            f"Questions: {stats['questions']}\n"
            f"Cached answers: {stats['cached_answers']}\n"
            f"Feedback records: {stats['feedback']}"
        )

    async def reindex(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if not self._is_admin(update):
            await update.effective_message.reply_text(
                "This command is available to administrators."
            )
            return
        await update.effective_message.reply_text("Rebuilding the knowledge index.")
        count = await self.rag.reindex()
        await update.effective_message.reply_text(f"Knowledge index rebuilt with {count} chunks.")

    def _is_admin(self, update: Update) -> bool:
        return bool(
            update.effective_user and update.effective_user.id in self.settings.admin_user_ids
        )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        del update
        if isinstance(context.error, (Conflict, TimedOut, NetworkError)):
            logger.warning("Transient Telegram polling notice: %s", context.error)
            return
        logger.error("Unhandled Telegram update error", exc_info=context.error)


_CITATION_MARKER = re.compile(r"\s?\[\d+\]")
_HEADING_LINE = re.compile(r"^#{1,6}\s*(.+?)\s*$", re.MULTILINE)
_DOUBLE_ASTERISK_BOLD = re.compile(r"\*\*(.+?)\*\*")
_MARKDOWN_SPECIAL_CHARS = re.compile(r"[_*`\[]")


def format_for_telegram(text: str) -> str:
    """Convert model markdown into what Telegram's legacy Markdown mode can render."""
    text = _CITATION_MARKER.sub("", text)
    text = _HEADING_LINE.sub(lambda m: f"*{m.group(1)}*", text)
    text = _DOUBLE_ASTERISK_BOLD.sub(lambda m: f"*{m.group(1)}*", text)
    return text.strip()


async def send_markdown(message, text: str, **kwargs) -> None:
    """Send with Telegram Markdown rendering, falling back to plain text if it fails to parse."""
    try:
        await message.reply_text(text, parse_mode=ParseMode.MARKDOWN, **kwargs)
    except BadRequest:
        plain = _MARKDOWN_SPECIAL_CHARS.sub("", text)
        await message.reply_text(plain, **kwargs)


def split_telegram_text(text: str, limit: int = 3900) -> list[str]:
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
