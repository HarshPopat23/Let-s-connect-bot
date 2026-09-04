---
title: Practical Git and GitHub Workflow for Contributors
category: workflow
source_url: https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project
updated: 2026-09-04
---

# Prepare the repository

Fork the repository when you do not have write access, then clone your fork. Configure the original repository as the upstream remote.

Typical commands are:

    git clone https://github.com/YOUR-NAME/PROJECT.git
    cd PROJECT
    git remote add upstream https://github.com/ORIGINAL-OWNER/PROJECT.git
    git remote -v

Before new work, update the default branch according to the project's policy:

    git switch main
    git fetch upstream
    git rebase upstream/main
    git push origin main

Some projects prefer merge instead of rebase. Follow CONTRIBUTING and do not rewrite shared branch history.

# Use one focused branch

Create a branch from the current upstream default branch:

    git switch -c fix/short-description

Keep one logical change per branch. Avoid unrelated formatting, dependency updates or refactors. Small focused diffs are easier to test, review and revert.

# Commit responsibly

Inspect changes before staging:

    git status
    git diff
    git add path/to/intended-file
    git diff --staged
    git commit -s -m "fix: concise description"

Use `-s` only when the project requires Developer Certificate of Origin sign-off. Some projects use conventional commits, imperative subjects, issue prefixes or no fixed format. The project guide is authoritative.

Never commit `.env`, tokens, private keys, personal data, large generated output or editor files. If a secret is committed, removing the line is not enough because Git preserves history. Revoke the secret immediately and follow the host's secret-removal process.

# Update a branch during review

Fetch upstream and use the project's preferred update method. Rebase can produce a clean history but rewrites commit identifiers; avoid it when maintainers request additive commits or when others share the branch. Force-push only your own branch and use the safer form:

    git push --force-with-lease origin fix/short-description

Never force-push the upstream default branch.

# Recover safely

Use `git status`, `git diff`, `git log --oneline --decorate --graph` and `git reflog` to understand state before destructive actions. If uncertain, create a backup branch and ask for help. Do not copy random reset commands without understanding which commits and uncommitted files they affect.

