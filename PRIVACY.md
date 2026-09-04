# Privacy Notice

OLLM processes a Telegram numeric user ID and question to provide an answer. It stores the user ID with a daily aggregate question count. It caches generated answers keyed by a one-way hash of the normalized question and records optional useful or needs-improvement feedback.

The default application logs operational errors and numeric user IDs when processing fails. It does not intentionally log full question text.

The raw WhatsApp export and VCF contacts supplied during development are not part of this repository, Docker image or vector index. The knowledge base contains only rewritten, anonymized general guidance and public links.

Users must not send credentials, private repository content, personal data, confidential conversations or undisclosed vulnerabilities to OLLM.

SQLite data persists in the `bot_data` Docker volume. Administrators should define a retention and deletion process before public deployment. Cached answers expire logically after the configured time, though expired records may remain until a later cache lookup or maintenance operation.

Telegram independently processes messages under its own terms. A self-hosted OLLM deployment sends retrieved context only to the local Ollama instance and does not call a hosted language-model API.

