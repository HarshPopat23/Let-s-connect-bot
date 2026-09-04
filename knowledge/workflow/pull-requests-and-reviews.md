---
title: Pull Requests, Review and Merge Etiquette
category: workflow
source_url: https://docs.github.com/pull-requests/reference/pull-request-reviews
updated: 2026-09-04
---

# A pull request is a technical conversation

The purpose of a pull request is to propose a change for review, not to announce finished work. Review can identify design constraints, compatibility risks and maintenance costs that were not visible from the issue.

# Write a reviewable pull request

Keep the diff focused. Explain the problem and why the change is needed. Link the approved issue or design. Describe the approach, user-visible effects, tests, documentation and any unresolved risks. Do not claim testing you did not perform.

Use a draft when design feedback is needed early or checks are incomplete. A draft reduces confusion but does not excuse an unexplained diff.

# Respond to review

Read the whole review before editing. Group related changes, run tests again and reply with what changed. If a suggestion is unclear, ask what scenario the reviewer is protecting.

Disagreement is acceptable. State the requirement, evidence and tradeoff without becoming defensive. A maintainer may choose a different design because they carry long-term responsibility.

Do not resolve another person's conversation merely to make the interface look complete. Let the reviewer confirm when appropriate.

# Review someone else's work

First understand the issue and repository rules. Test the change when possible. Separate blocking correctness problems from optional suggestions. Explain why a concern matters and offer a concrete example.

Use language such as "Could this fail when the value is empty?" rather than personal judgments. Mark minor optional comments clearly. Avoid flooding a new contributor with many style comments that automated tools should handle.

Non-maintainers can provide useful feedback, but should not imply that their approval authorizes merge. GitHub reviews allow comments, approvals and change requests; permissions and repository rules determine which reviews are binding.

# Merge is not guaranteed

A correct patch may not merge because the feature is out of scope, duplicates planned work, increases maintenance cost, breaks compatibility or lacks a willing long-term owner. Closure is not permission to reopen the same proposal repeatedly.

