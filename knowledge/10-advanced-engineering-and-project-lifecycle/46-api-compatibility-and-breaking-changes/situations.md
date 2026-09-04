---
title: API compatibility and breaking changes
group: 10-advanced-engineering-and-project-lifecycle
category: 46-api-compatibility-and-breaking-changes
journey_stage: contribute
scenario_count: 50
content_type: situations-only
chat_informed: false
source_keys:
  - github-prs
  - github-releases
  - governance-guide
---

# API compatibility and breaking changes

This file contains situations only. It intentionally provides no answers or recommended actions.

## Beginner situations

- OSS-46-001: Changing a public function used by unknown downstream projects, while the project has no formal compatibility policy.
- OSS-46-002: Adding an optional field that affects serialized output, while generated clients lag behind the server implementation.
- OSS-46-003: Removing behavior already marked as deprecated, while release timelines differ across related repositories.
- OSS-46-004: Fixing a bug whose current behavior became depended upon, while the project has no formal compatibility policy.
- OSS-46-005: Renaming a configuration option across clients and documentation, while generated clients lag behind the server implementation.
- OSS-46-006: Introducing a new API version while supporting the old version, while release timelines differ across related repositories.
- OSS-46-007: Changing error types or messages used by automation, while the project has no formal compatibility policy.
- OSS-46-008: Updating a schema consumed by independently released components, while generated clients lag behind the server implementation.
- OSS-46-009: Adding validation that rejects previously accepted input, while release timelines differ across related repositories.
- OSS-46-010: Testing compatibility across language-specific client libraries, while the project has no formal compatibility policy.
- OSS-46-011: Changing a public function used by unknown downstream projects, while downstream usage is only partially visible.
- OSS-46-012: Adding an optional field that affects serialized output, while the fix improves correctness but breaks an existing workaround.
- OSS-46-013: Removing behavior already marked as deprecated, while maintainers disagree on whether the API is public.
- OSS-46-014: Fixing a bug whose current behavior became depended upon, while downstream usage is only partially visible.
- OSS-46-015: Renaming a configuration option across clients and documentation, while the fix improves correctness but breaks an existing workaround.
- OSS-46-016: Introducing a new API version while supporting the old version, while maintainers disagree on whether the API is public.
- OSS-46-017: Changing error types or messages used by automation, while downstream usage is only partially visible.
- OSS-46-018: Updating a schema consumed by independently released components, while the fix improves correctness but breaks an existing workaround.
- OSS-46-019: Adding validation that rejects previously accepted input, while maintainers disagree on whether the API is public.
- OSS-46-020: Testing compatibility across language-specific client libraries, while downstream usage is only partially visible.

## Intermediate situations

- OSS-46-021: Changing a public function used by unknown downstream projects, while generated clients lag behind the server implementation.
- OSS-46-022: Adding an optional field that affects serialized output, while release timelines differ across related repositories.
- OSS-46-023: Removing behavior already marked as deprecated, while the project has no formal compatibility policy.
- OSS-46-024: Fixing a bug whose current behavior became depended upon, while generated clients lag behind the server implementation.
- OSS-46-025: Renaming a configuration option across clients and documentation, while release timelines differ across related repositories.
- OSS-46-026: Introducing a new API version while supporting the old version, while the project has no formal compatibility policy.
- OSS-46-027: Changing error types or messages used by automation, while generated clients lag behind the server implementation.
- OSS-46-028: Updating a schema consumed by independently released components, while release timelines differ across related repositories.
- OSS-46-029: Adding validation that rejects previously accepted input, while the project has no formal compatibility policy.
- OSS-46-030: Testing compatibility across language-specific client libraries, while generated clients lag behind the server implementation.
- OSS-46-031: Changing a public function used by unknown downstream projects, while the fix improves correctness but breaks an existing workaround.
- OSS-46-032: Adding an optional field that affects serialized output, while maintainers disagree on whether the API is public.
- OSS-46-033: Removing behavior already marked as deprecated, while downstream usage is only partially visible.
- OSS-46-034: Fixing a bug whose current behavior became depended upon, while the fix improves correctness but breaks an existing workaround.
- OSS-46-035: Renaming a configuration option across clients and documentation, while maintainers disagree on whether the API is public.
- OSS-46-036: Introducing a new API version while supporting the old version, while downstream usage is only partially visible.
- OSS-46-037: Changing error types or messages used by automation, while the fix improves correctness but breaks an existing workaround.
- OSS-46-038: Updating a schema consumed by independently released components, while maintainers disagree on whether the API is public.
- OSS-46-039: Adding validation that rejects previously accepted input, while downstream usage is only partially visible.
- OSS-46-040: Testing compatibility across language-specific client libraries, while the fix improves correctness but breaks an existing workaround.

## Advanced situations

- OSS-46-041: Changing a public function used by unknown downstream projects, while release timelines differ across related repositories.
- OSS-46-042: Adding an optional field that affects serialized output, while the project has no formal compatibility policy.
- OSS-46-043: Removing behavior already marked as deprecated, while generated clients lag behind the server implementation.
- OSS-46-044: Fixing a bug whose current behavior became depended upon, while release timelines differ across related repositories.
- OSS-46-045: Renaming a configuration option across clients and documentation, while the project has no formal compatibility policy.
- OSS-46-046: Introducing a new API version while supporting the old version, while generated clients lag behind the server implementation.
- OSS-46-047: Changing error types or messages used by automation, while release timelines differ across related repositories.
- OSS-46-048: Updating a schema consumed by independently released components, while the project has no formal compatibility policy.
- OSS-46-049: Adding validation that rejects previously accepted input, while generated clients lag behind the server implementation.
- OSS-46-050: Testing compatibility across language-specific client libraries, while release timelines differ across related repositories.
