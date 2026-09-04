---
title: Pull request CI failures
group: 04-pull-requests
category: 21-pull-request-ci-failures
journey_stage: contribute
scenario_count: 50
content_type: situations-only
chat_informed: true
source_keys:
  - github-actions
  - github-prs
---

# Pull request CI failures

This file contains situations only. It intentionally provides no answers or recommended actions.

## Beginner situations

- OSS-21-001: Investigating a required check that fails only in CI, while the contributor cannot access protected CI logs.
- OSS-21-002: Distinguishing a flaky test from a regression caused by the patch, while secrets are intentionally unavailable to forked workflows.
- OSS-21-003: Understanding why a workflow did not start for a forked pull request, while reruns produce different failing tests.
- OSS-21-004: Rerunning a failed job without hiding the original failure, while the contributor cannot access protected CI logs.
- OSS-21-005: Debugging a matrix build that fails on one platform, while secrets are intentionally unavailable to forked workflows.
- OSS-21-006: Updating a branch after required status checks become outdated, while reruns produce different failing tests.
- OSS-21-007: Handling a test timeout with no useful failure message, while the contributor cannot access protected CI logs.
- OSS-21-008: Comparing logs from successful and failed workflow runs, while secrets are intentionally unavailable to forked workflows.
- OSS-21-009: Requesting approval for a workflow run from an external fork, while reruns produce different failing tests.
- OSS-21-010: Investigating a check that passes locally with cached dependencies, while the contributor cannot access protected CI logs.
- OSS-21-011: Investigating a required check that fails only in CI, while the failure also appears on unrelated pull requests.
- OSS-21-012: Distinguishing a flaky test from a regression caused by the patch, while the workflow uses a different toolchain version than local setup.
- OSS-21-013: Understanding why a workflow did not start for a forked pull request, while the branch protection rule references a renamed check.
- OSS-21-014: Rerunning a failed job without hiding the original failure, while the failure also appears on unrelated pull requests.
- OSS-21-015: Debugging a matrix build that fails on one platform, while the workflow uses a different toolchain version than local setup.
- OSS-21-016: Updating a branch after required status checks become outdated, while the branch protection rule references a renamed check.
- OSS-21-017: Handling a test timeout with no useful failure message, while the failure also appears on unrelated pull requests.
- OSS-21-018: Comparing logs from successful and failed workflow runs, while the workflow uses a different toolchain version than local setup.
- OSS-21-019: Requesting approval for a workflow run from an external fork, while the branch protection rule references a renamed check.
- OSS-21-020: Investigating a check that passes locally with cached dependencies, while the failure also appears on unrelated pull requests.

## Intermediate situations

- OSS-21-021: Investigating a required check that fails only in CI, while secrets are intentionally unavailable to forked workflows.
- OSS-21-022: Distinguishing a flaky test from a regression caused by the patch, while reruns produce different failing tests.
- OSS-21-023: Understanding why a workflow did not start for a forked pull request, while the contributor cannot access protected CI logs.
- OSS-21-024: Rerunning a failed job without hiding the original failure, while secrets are intentionally unavailable to forked workflows.
- OSS-21-025: Debugging a matrix build that fails on one platform, while reruns produce different failing tests.
- OSS-21-026: Updating a branch after required status checks become outdated, while the contributor cannot access protected CI logs.
- OSS-21-027: Handling a test timeout with no useful failure message, while secrets are intentionally unavailable to forked workflows.
- OSS-21-028: Comparing logs from successful and failed workflow runs, while reruns produce different failing tests.
- OSS-21-029: Requesting approval for a workflow run from an external fork, while the contributor cannot access protected CI logs.
- OSS-21-030: Investigating a check that passes locally with cached dependencies, while secrets are intentionally unavailable to forked workflows.
- OSS-21-031: Investigating a required check that fails only in CI, while the workflow uses a different toolchain version than local setup.
- OSS-21-032: Distinguishing a flaky test from a regression caused by the patch, while the branch protection rule references a renamed check.
- OSS-21-033: Understanding why a workflow did not start for a forked pull request, while the failure also appears on unrelated pull requests.
- OSS-21-034: Rerunning a failed job without hiding the original failure, while the workflow uses a different toolchain version than local setup.
- OSS-21-035: Debugging a matrix build that fails on one platform, while the branch protection rule references a renamed check.
- OSS-21-036: Updating a branch after required status checks become outdated, while the failure also appears on unrelated pull requests.
- OSS-21-037: Handling a test timeout with no useful failure message, while the workflow uses a different toolchain version than local setup.
- OSS-21-038: Comparing logs from successful and failed workflow runs, while the branch protection rule references a renamed check.
- OSS-21-039: Requesting approval for a workflow run from an external fork, while the failure also appears on unrelated pull requests.
- OSS-21-040: Investigating a check that passes locally with cached dependencies, while the workflow uses a different toolchain version than local setup.

## Advanced situations

- OSS-21-041: Investigating a required check that fails only in CI, while reruns produce different failing tests.
- OSS-21-042: Distinguishing a flaky test from a regression caused by the patch, while the contributor cannot access protected CI logs.
- OSS-21-043: Understanding why a workflow did not start for a forked pull request, while secrets are intentionally unavailable to forked workflows.
- OSS-21-044: Rerunning a failed job without hiding the original failure, while reruns produce different failing tests.
- OSS-21-045: Debugging a matrix build that fails on one platform, while the contributor cannot access protected CI logs.
- OSS-21-046: Updating a branch after required status checks become outdated, while secrets are intentionally unavailable to forked workflows.
- OSS-21-047: Handling a test timeout with no useful failure message, while reruns produce different failing tests.
- OSS-21-048: Comparing logs from successful and failed workflow runs, while the contributor cannot access protected CI logs.
- OSS-21-049: Requesting approval for a workflow run from an external fork, while secrets are intentionally unavailable to forked workflows.
- OSS-21-050: Investigating a check that passes locally with cached dependencies, while reruns produce different failing tests.
