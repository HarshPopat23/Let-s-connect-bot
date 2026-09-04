# Security Policy

## Reporting a vulnerability

Do not open a public issue for suspected vulnerabilities involving token exposure, unauthorized data access, prompt injection that reveals private data, remote code execution or exposed Qdrant and Ollama services.

Contact an OSS Let's Connect organizer privately through the current community admin channel. Include the affected version, impact, reproduction steps and suggested mitigation. Do not include real secrets or access data that is not yours.

The maintainers should configure GitHub private vulnerability reporting and replace this interim contact process before public production deployment.

## Deployment requirements

- Keep `.env` out of Git.
- Bind Qdrant and Ollama to localhost or a private Docker network.
- Restrict SSH and keep the operating system and containers updated.
- Keep Telegram privacy mode enabled because OLLM does not ingest group conversations.
- Rotate a Telegram token immediately if exposed.
- Review new knowledge files for prompt injection and private information.
- Back up before upgrading Qdrant or changing embedding models.

## Supported versions

Until the first tagged release, security fixes apply only to the latest main branch.

