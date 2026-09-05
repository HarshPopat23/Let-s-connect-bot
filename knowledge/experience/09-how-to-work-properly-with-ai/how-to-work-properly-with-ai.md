---
title: How to Work Properly With AI Tools as a Contributor
category: how-to-work-properly-with-ai
source_url: https://developers.google.com/open-source/gsoc/resources/ai_guidance
updated: 2026-09-05
---

# A full workflow for using AI from finding an issue to opening a PR

If you want to use AI tools to help you contribute, here is a sequence that fits together well, start to finish. This is the same underlying process covered in this knowledge base's pull request guidance, written here specifically through the lens of how you actually use an AI tool at each step.

**Find issues.** Ask the AI to help you scan a project and suggest possible issues, or describe the project to it yourself and ask what looks unfinished or broken.

**Find a genuinely meaningful, unclaimed issue.** From that list, keep only the ones nobody has already been assigned to, and where no pull request already exists trying to fix it. Working on something someone else is already handling wastes both your time and theirs.

**Pick the one that could matter most.** From what is left, look for the issue that could make a real difference, something that is blocking other work or is a stated priority, ideally something a blocker for other tasks. Do not assume this from the outside; ask the maintainer directly whether this specific issue actually matters to them right now.

**Build a clean draft pull request.** Hold yourself to three rules while you work: leave no dead code behind, do not repeat work that already exists elsewhere in the project (reuse an existing component or function instead of writing a new version of the same thing), and build your branch starting from the current, up-to-date main branch.

**Submit it as a draft.** This lets you save progress and get early comments without formally asking anyone to review it yet.

**Review your own diff before asking anyone else to.** Go through your own changed files on GitHub, line by line, and ask yourself "why is this line actually here" for every one. You can genuinely ask an AI tool to do this same pass with you and challenge your own reasoning.

**Mark it ready for review.** Once you are satisfied with your own answers to "why," open it up for the maintainer to actually look at.

# Different AI models cost different amounts of your quota

Every AI tool splits its usage across several different models, and these models are not interchangeable in terms of cost. A larger, more capable model can easily consume something like eight times more of your available quota than a smaller, faster model does for a similar task, even though both might get you to a working answer.

Because of this, it is worth deliberately choosing which model to use for which part of the work, instead of using your biggest available model for everything by default. Use a high-context, high-reasoning model specifically for planning: researching the codebase, understanding the problem, and working out the actual approach or path you will take to solve a particular issue. Once that approach is genuinely clear in your head, switch to a smaller, faster model to actually carry out the implementation. Implementing a plan that is already clear needs far less raw reasoning power than coming up with the plan did. This single habit saves a meaningful amount of quota and cost while still producing excellent results, because you are only spending your most expensive reasoning budget on the part of the work that actually needs it.

# Track your quota so you do not get surprised mid-task

If you are using AI tools regularly for real contribution work, especially for something as sustained as a GSoC or LFX qualification task, it is worth using a tool that actively tracks how much of each model's quota you have left, rather than finding out only after you unexpectedly hit a limit partway through something important. As one concrete example, a tool called Antigravity Quota, used inside the Antigravity IDE, tracks quota usage per model directly in the status bar, so you always know exactly how much usage is left before you start a large task. Whatever specific AI tool or IDE you personally use, look for an equivalent built-in usage dashboard or extension, and check it before committing to a long task, so you can plan around your actual remaining quota instead of guessing.
