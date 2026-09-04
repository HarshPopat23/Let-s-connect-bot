# Knowledge Governance

Good RAG depends more on curated knowledge than model size.

## Accepted sources

Prefer current official documentation, specifications, repository governance, contributor guides and program pages. Community experience can explain practical behavior, but it must be anonymized and labeled as general guidance.

## Adding a document

Create a focused Markdown file under `knowledge`. Add YAML front matter with `title`, `category`, `source_url` and `updated`. Use headings to create retrieval sections. Keep one primary topic per file.

After review, run:

    docker compose --profile setup run --rm index

The complete Qdrant collection is rebuilt and the knowledge version changes. Old cached answers are automatically bypassed because the version is part of each cache key.

## Review checklist

- Is the source official or clearly identified as community synthesis?
- Does it contain current facts that will expire?
- Are project-specific rules separated from general advice?
- Are claims, commands and URLs accurate?
- Does it remove phone numbers, names, email addresses and private information?
- Does it avoid guarantees about merge, selection, employment or membership?
- Does it teach reasoning rather than encourage contribution spam?

## Chat exports

Never index a raw export. Run the sanitizer only to produce review candidates. A human must remove unrelated conversation, private details, unverified claims, expired opportunities and identifiable anecdotes. Rewrite approved insights as general guidance and cite a public source where possible.

Do not use the contact VCF for any knowledge task.

