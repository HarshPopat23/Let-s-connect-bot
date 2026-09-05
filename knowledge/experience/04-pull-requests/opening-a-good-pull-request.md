---
title: Opening a Good Pull Request, Start to Finish
category: pull-requests
source_url: https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
updated: 2026-09-05
---

# What a pull request actually is

A pull request is a request you send asking the project to add your changes into their code. It shows the exact lines you changed, lets people leave comments on specific lines, and only gets combined into the main project once someone with the right permission approves it and clicks merge. Opening one does not mean it will be accepted; it starts a conversation, not a guarantee.

# Small pull requests get merged faster, and here is why

Keep each pull request focused on doing exactly one thing. A study of real code review data at Cisco found that reviewers get noticeably worse at spotting problems once a single change goes past roughly 200 to 400 lines; past that point, people skim instead of actually reading carefully, and mistakes slip through. A smaller, single-purpose pull request is easier for a tired, busy maintainer to review properly, gets a faster answer, and is far less likely to get stuck in an argument, since a huge change touching five unrelated things means all five have to be agreed on before any of them can be merged. If you notice your change growing to cover several unrelated things, it is almost always better to split it into several smaller pull requests instead of one large one.

# What a draft pull request is, and why to use one

GitHub lets you open a pull request as a **draft** instead of a normal one. A draft cannot be merged yet, and it does not automatically ask anyone to review it, which makes it a safe way to save and share work that is still in progress. When your change is actually finished and you want real feedback, you click the button labeled **Ready for review**, and only then does GitHub treat it like a normal pull request and notify reviewers.

# Opening your first pull request: the basic steps

Make sure your local copy of the main branch is fully up to date first, then create a brand-new branch from it, make your actual code changes there, save them as one or more commits, and push that branch up to GitHub. On GitHub, you will then see a button offering to open a pull request from that branch. Give it a clear title and a description explaining what changed and why, and open it as a draft first if it is not fully finished yet.

# The full process, if you are using AI to help you

If you are using AI tools to help you work through this, here is a complete sequence that fits together well, start to finish:

**Step one: find issues.** Use the methods already covered for finding issues (testing the product yourself as a real user, or asking AI to suggest a list).

**Step two: find a genuinely meaningful, unclaimed issue.** From your list, keep only the issues where nobody has already been assigned, and where no pull request already exists trying to fix it. Working on something already being handled by someone else wastes both your time and theirs.

**Step three: pick the one that matters most.** From what is left, look for the issue that could make a real difference to the project, something that is blocking other work, or is clearly a stated priority. Do not just guess this from the outside; actually ask the maintainer whether this particular issue matters to them right now, before spending hours on it.

**Step four: build a clean draft pull request.** As you work, hold yourself to three rules: leave no dead code behind (no unused variables, no commented-out old attempts left in place), do not repeat work that already exists elsewhere in the project (look for an existing component or function to reuse instead of writing your own new version of the same thing), and build your branch starting from the current, up-to-date main branch, not an old copy sitting on your computer for weeks.

**Step five: submit it as a draft.** This lets you save your progress and get early comments without formally asking anyone to review it yet.

**Step six: review your own diff before asking anyone else to.** Open your own pull request's changed-files view on GitHub and go through it line by line, asking yourself "why is this line actually here" for every single one. You can genuinely ask an AI tool to do this same pass with you and challenge your own reasoning; it often catches things a second look would have caught anyway.

**Step seven: mark it ready for review.** Once you are satisfied with your own answers to "why," click **Ready for review** so the maintainer is actually notified and knows it is time to look at it.

# The maintainer is not reviewing my pull request. What now?

This is one of the most common worries a new contributor has, and it is rarely personal. Most maintainers on open-source projects are volunteers who also have their own full-time jobs, and review happens whenever they can find the time, which is not always quickly.

A few things genuinely help. If the project has a community chat, such as Slack or Discord, you can politely share a direct hyperlink to your pull request there to get more eyes on it; check the README first, since some projects specifically welcome this and others prefer you not to. While you are waiting, do not just sit idle: keep exploring the codebase for other real bugs, open more issues as you find them, or even go explore a different project that uses the same technology, so the waiting time is not wasted.

If a full month passes with genuinely no response and no sign that the maintainers are active at all, it is reasonable to consider putting your energy into a different project instead. One simple way to check whether a project is actually active, before you commit time to it or while you wait: open the repository's **Commits** page and look at when the very last commit was made. A commit from a few days or weeks ago is a good sign people are still working on it. A last commit from a year or more ago is a strong signal the project may be slow, unmaintained, or effectively abandoned.
