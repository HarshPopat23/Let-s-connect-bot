# Telegram Bot Setup

1. Open the verified `@BotFather` account in Telegram.
2. Send `/newbot` and choose the display name OLLM.
3. Choose an available username ending in `bot`, such as `ollm_contributor_bot`.
4. Copy the token into `TELEGRAM_BOT_TOKEN` in `.env`.
5. Use `/setdescription`, `/setabouttext` and `/setuserpic` to add community branding.
6. Add the bot to the required group if group questions are needed.

The code answers all text in private chat. In groups it answers only `/ask question`, which avoids processing normal conversation. The bot does not need administrator permission for this behavior.

Keep privacy mode enabled unless you intentionally implement group-message ingestion. OLLM does not need access to all group messages.

If a token is exposed, revoke it through BotFather immediately and replace the value in `.env`.

