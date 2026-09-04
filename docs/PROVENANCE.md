# Provenance and chat-analysis record

## Community-chat analysis

The supplied OSS Let's Connect export contained 21,936 lines. The aggregate-only parser identified 16,980 messages without printing message text, senders, dates, or contact values. It was then processed through a privacy-redacting relevance filter before qualitative review.

The filter produced 2,093 review candidates. These candidates were not copied into this repository and were not automatically treated as true guidance.

Approximate recurring-theme counts from the narrower sanitized review set were:

| Theme | Matching messages |
| --- | ---: |
| Question-like messages | 761 |
| GSoC, LFX, Outreachy, and mentorship programs | 627 |
| Pull requests, reviews, and merges | 356 |
| Project discovery, repositories, and codebases | 288 |
| Git and GitHub | 244 |
| Maintainer communication, replies, and meetings | 232 |
| Issues and assignment | 176 |
| AI-assisted contribution | 96 |
| Career and learning | 93 |
| Testing and CI | 82 |
| Documentation | 63 |

Additional signals included proposal applications, newcomer onboarding, reviewer roles, codebase understanding, assignment, setup, debugging, no-response cases, conflicts, conduct, licensing, and security.

Counts overlap because one message can match several themes. They describe the source conversation, not the final dataset distribution.

## Transformation rules

- Do not quote messages directly.
- Do not retain participant names or stable pseudonyms.
- Do not retain phone numbers, emails, dates, or contact records.
- Do not preserve private anecdotes that could identify a participant.
- Do not convert unverified chat claims into facts.
- Rewrite only recurring patterns as general situations.
- Add public-source-informed situations for missing lifecycle areas.
- Keep situations separate from answers.

## Gap expansion

The chat strongly represented early contributor questions and program applications. Official sources were used to expand underrepresented areas such as governance, releases, security disclosure, accessibility, localization, dependency supply chains, project succession, reviewer responsibilities, and maintainer sustainability.

## Excluded files

The raw WhatsApp export and supplied VCF contact file are deliberately absent from this repository and its generated dataset.
