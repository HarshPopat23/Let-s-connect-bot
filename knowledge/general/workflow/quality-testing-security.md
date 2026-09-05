---
title: Contribution Quality, Testing and Security Checklist
category: workflow
source_url: https://bestpractices.coreinfrastructure.org/en/criteria/0
updated: 2026-09-04
---

# Before changing code

Reproduce the current behavior and identify the supported versions. Read nearby tests and interfaces. Confirm the desired behavior with an issue or specification when it is ambiguous.

# During implementation

Make the smallest coherent change. Preserve backward compatibility unless a breaking change is approved. Handle invalid input and failure paths. Avoid logging secrets, personal data or full credentials. Follow existing error-handling and concurrency patterns.

# Test evidence

Add a regression test that fails without the fix when practical. Run the documented unit, integration, formatting and linting commands. Test the exact user scenario and important edge cases. Record commands and meaningful results in the pull request.

Do not weaken or delete a test merely to make checks green unless the expected behavior officially changed. Do not claim that all tests pass if you ran only a subset.

# Dependency and generated changes

Explain new dependencies, licenses and maintenance implications. Commit lock files or generated output only according to project policy. Review dependency changes for unexpected transitive packages and security advisories.

# Security reports

Read SECURITY.md before reporting. Vulnerabilities often require private disclosure so maintainers can investigate and coordinate a release. Include reproduction details privately and avoid accessing data that is not yours.

# Final self-review

Review the complete diff as a reviewer would. Remove debug code and unrelated edits. Confirm documentation, changelog and release-note requirements. Check that names, messages and comments explain intent rather than restating code.
