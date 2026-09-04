---
title: Responsible AI Use in Open-Source Contribution
category: safety
source_url: https://developers.google.com/open-source/gsoc/resources/ai_guidance
updated: 2026-09-04
---

# Responsibility cannot be delegated

The contributor is responsible for every issue, proposal, line of code, test and claim they submit. If you cannot explain generated work, do not submit it. Follow the project's current AI policy and disclose use when required.

# Good uses

Use AI to explain unfamiliar terms, identify likely entry points, summarize selected code, brainstorm edge cases, interpret compiler errors, create candidate test outlines, compare documented alternatives and improve clarity after you write the substance.

Validate with repository search, documentation, tests, specifications and human review. Prefer narrow questions with supplied context over asking an AI system to solve an entire issue.

# Harmful uses

Do not mass-generate issues, typo pull requests, superficial reviews, generic proposals or comments. Do not submit invented APIs, fake benchmarks, fabricated experience or code copied from unknown training sources without license review.

Do not paste private code, security reports, credentials, personal data or confidential conversations into external AI services. Check organizational policy before sharing any repository context.

# A practical verification method

First reproduce and explain the problem yourself. Ask AI for hypotheses or relevant files. Verify each claim in the code. Write or understand a failing test. Compare at least one alternative. Run required checks. Review the final diff without AI and prepare to explain every decision.

# OLLM limitations

OLLM retrieves curated documents and uses a local model, but it can still misunderstand context. Its answer is guidance, not project authorization. Verify project-specific rules at the linked source and ask maintainers when evidence is incomplete.

