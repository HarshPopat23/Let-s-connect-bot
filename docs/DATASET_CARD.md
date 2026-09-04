# Dataset card

## Name

OLLM Open-Source Situation Dataset

## Purpose

Provide broad scenario coverage for an open-source contributor assistant without embedding answers inside the scenario collection.

## Version

1.0.0

## Size

- 2,500 situations
- 10 major knowledge groups
- 50 categories
- 50 Markdown topic files
- 35 chat-informed categories
- 10 journey-stage labels
- 3 difficulty labels

## Population represented

The situations cover newcomers, students, contributors, issue reporters, reviewers, maintainers, mentors, applicants, translators, designers, security researchers, release engineers, community moderators, and project leaders.

## Coverage

Coverage includes onboarding, project choice, repository reading, local setup, Git, GitHub, issues, pull requests, reviews, delays, CI, testing, documentation, accessibility, localization, communication, conduct, collaboration, responsible AI, security, privacy, supply chain, licensing, mentoring programs, CNCF ecosystems, governance, releases, careers, sustainability, APIs, performance, AI projects, infrastructure, and project migration.

## Data origin

The taxonomy combines:

- anonymized recurring themes from an OSS Let's Connect WhatsApp export
- official GitHub and Git documentation
- Open Source Guides
- CNCF, Kubernetes, and Kubeflow contributor documentation
- GSoC, LFX Mentorship, and Outreachy documentation
- Contributor Covenant, Choose a License, DCO, and OpenSSF material
- systematic edge-case expansion across roles, difficulty, and project lifecycle

No raw chat line or participant identity is included.

## Generation method

Each category has ten independently curated situation focuses and six independently curated complications. The deterministic generator combines five distinct complications with each focus, producing fifty situations per category. Human-authored category axes reduce random generic wording while systematic combination increases edge-case coverage.

## Intended uses

- intent classification
- category routing
- RAG coverage and regression testing
- benchmark prompt generation
- scenario review by experienced contributors
- discovery of missing factual guidance
- community workshop planning

## Out-of-scope uses

- factual answer retrieval
- legal conclusions
- security incident response decisions
- program-selection predictions
- automated maintainer actions
- reproducing private community conversations

## Known limitations

- Situations are synthetic generalizations and are not frequency estimates.
- Difficulty is approximate and varies by project.
- Project-specific workflows may differ.
- Combining focus and complication axes creates broad coverage but some situations may be uncommon.
- Current events and program dates are deliberately excluded from scenario text.
- The dataset is English-only.

## Maintenance

Review source links and category gaps at least every six months. Add or remove situations through `scripts/dataset_specs.py`, then rebuild and validate the generated files.
