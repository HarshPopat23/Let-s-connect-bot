---
title: Privacy, Secrets and Safe Public Collaboration
category: safety
source_url: https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning
updated: 2026-09-04
---

# Never publish secrets

Do not commit API keys, passwords, private keys, cloud credentials, session tokens, database URLs containing credentials or `.env` files. Use environment variables and committed `.env.example` placeholders.

If a secret reaches Git history, revoke or rotate it immediately. Deleting the visible line does not remove earlier commits, forks, logs or notifications.

# Protect personal and community data

Do not publish phone numbers, email addresses, private chat exports, attendance lists, resumes or personal profiles without a clear purpose and consent. Anonymization requires removing identifiers and details that can be combined to identify a person.

For community knowledge systems, convert repeated discussions into general guidance. Exclude jokes, unrelated conversations, disputes, contact lists and unverified claims. Require human review before indexing new exports.

# Share diagnostic data safely

Redact tokens, usernames, private hostnames, customer data and file paths when they reveal identity or infrastructure. Provide the smallest log excerpt that reproduces the problem.

# Vulnerabilities

Follow SECURITY.md and private reporting channels. Do not exploit systems beyond the authorization needed to confirm a report. Coordinate disclosure with maintainers.

