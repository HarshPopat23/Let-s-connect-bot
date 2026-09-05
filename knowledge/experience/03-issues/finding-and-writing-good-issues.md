---
title: Finding a Good Issue, Writing It Well, and What Happens When It Closes
category: issues
source_url: https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/closing-an-issue
updated: 2026-09-05
---

# What an "issue" actually is

An issue is just a written note attached to a project, describing one bug, one missing feature, or one question. It is not code. It is a page with a title, a longer description, and a place for people to add comments underneath. Anyone can usually read the issues on a public project, and depending on the project's settings, anyone with an account can usually open a new one too.

# How to open the Issues tab and create a new issue

On a project's GitHub page, near the top, there is a row of tabs: Code, Issues, Pull requests, and a few others. Click the one labeled **Issues**. This shows every issue that already exists for this project. To add your own, look for a green button labeled **New issue** and click it. Some projects show you a small choice of templates first (for example, "Bug report" or "Feature request"); pick whichever matches what you want to say, or choose the blank option if none fit. Then you get two boxes: a short **title** at the top, and a bigger **description** box underneath. Fill both in, then click the button to submit it (usually labeled **Submit new issue**).

# How to write an issue body that a maintainer can actually act on

A short, specific issue is far more useful than a long, vague one. Include:

- **What you expected to happen.** State the normal, correct behavior in one sentence.
- **What actually happened instead.** State the wrong behavior you saw.
- **The exact steps to make it happen again.** Numbered steps work best: "1. Open the app. 2. Click Settings. 3. Turn on dark mode." A maintainer who cannot reproduce your problem usually cannot fix it.
- **Basic environment details**, when relevant: which operating system, which browser or app version, which device.
- **A screenshot, short video, or copied error message**, if you have one. A picture of a visual bug is often worth more than a paragraph describing it.

Keep the whole thing focused on one single problem. If you notice three unrelated bugs while testing, write three separate issues instead of bundling them into one, since each will likely need a separate fix and a separate reviewer.

# Closing an issue: "completed" versus "not planned"

When a maintainer closes an issue on GitHub, they choose one of two reasons, and the difference matters:

**Closed as completed** means the problem was actually fixed, or the requested work was actually done.

**Closed as not planned** means the maintainers looked at it and deliberately decided not to do this work. This does not always mean you did anything wrong. Common reasons include: it turned out to be a duplicate of another issue already open, the behavior was actually intended and not a bug at all, or the idea does not fit where the project is currently headed. If your own reported issue gets closed as not planned, it is worth reading the maintainer's comment closely, since it usually explains why, and it is not a judgment on you personally.

# Finding a good issue to work on: two methods

## Method one: be a user first

This is the single most reliable way to find real, honest issues, and it needs no special tools. Set up the project on your own computer first, following its setup instructions. Then open it and actually use it the way a normal user would, not the way a developer skims code.

Click every single button you can find, and check whether it actually does what it is supposed to do. Turn on dark mode if the project has one, and check that every screen still looks right in it, not just the main page. Watch for small details that quietly do not match what they should logically be: for example, if there is an icon of a tree, it should probably be colored green, not some unrelated color left over from an older design. These small mismatches are real, reportable issues, and they are often the easiest ones for a new contributor to both find and later fix, because you do not need to read much code to notice that something looks or behaves wrong.

## Method two: use AI to help you search

You can ask an AI tool to read the project (or describe it yourself) and generate a list of about 30 possible issues, each labeled high, medium, or low priority. Do not start working yet. Other contributors may have had the same idea, using AI or their own testing, and some of these problems may already be filed. Open the real Issues tab first and check your AI-generated list against what already exists there, removing anything that is already reported. This usually leaves you with a shorter, more realistic list.

Even within what is left, do not automatically pick the highest-priority item. Since you are new, look for the issue that needs the smallest, most contained code change, even if it is medium or lower priority. A pull request with a small, easy-to-review diff is far more likely to get merged quickly than a large one, and it builds your track record with the project faster.

If a project already has a large backlog of existing issues instead, you can flip this around: ask AI to look through that existing list and suggest the best one for you specifically, again asking it to favor issues that need only a few lines of change, since you are still new to the project.

Between the two methods, testing the product yourself as a real user is still the better starting point, because it finds problems that genuinely exist right now, in the exact version you are looking at, instead of problems an AI is only guessing might exist.

# Once you have picked an issue

If you found the problem yourself and it is not filed yet, open it as described above, and explain clearly why it matters and what benefit fixing it gives to users, not just that you personally noticed it.

Getting assigned to work on it varies by project. Some projects let you assign yourself directly, or by commenting a specific command the project's bots understand. If self-assignment is not available, comment on the issue, mention the maintainer, and politely ask if you can work on it, then wait for their reply before starting. While you wait, you can also mention it in the project's community chat, such as Slack or Discord, if it has one; the join link is almost always posted in the project's README file. This often gets you a faster response than a comment alone.

If a maintainer eventually decides they do not want this particular fix or feature after all, they may close it as not planned, as explained above. That is a normal outcome of open-source collaboration, not a personal rejection.
