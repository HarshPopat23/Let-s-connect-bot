---
title: Practical Communication Templates for Contributors
category: workflow
source_url: https://opensource.guide/how-to-contribute/
updated: 2026-09-04
---

# Asking to work on an issue

I reproduced this on version X using these steps. The problem appears related to component Y because Z. I plan to add a regression test and make the smallest compatible fix. The contributor guide says assignment is required. May I work on it?

Adapt the message to the repository. Do not claim reproduction or understanding you do not have.

# Asking a setup question

I followed the setup instructions through step X on operating system Y. Command Z fails with this shortened error. I searched existing issues and tried A and B. Is dependency version C required, or is the documented version still supported?

# Following up on review

This pull request is ready for review. The documented checks pass, and I addressed the scope discussed in issue X. I know reviews take time. Is any information missing, or is there a more appropriate component reviewer?

Send one follow-up after a reasonable wait, not repeated daily reminders.

# Responding to review

Thank you. I updated the parser and added the empty-input regression test in the latest commit. I kept the public interface unchanged. Could you confirm whether the compatibility concern is now addressed?

# Disagreeing technically

I may be missing a project constraint. My concern with approach A is that it changes behavior for existing clients in case X. Approach B preserves that behavior but adds complexity Y. Would B be preferable, or is the breaking change intentional?

# Reporting a blocker

Progress: completed A and B. Blocker: behavior C is not specified, and the two nearby tests imply different outcomes. I need a decision on expected case D before implementing the final branch. Meanwhile, I can work on E.

# Declining or releasing an issue

I cannot complete this within the expected time. I am unassigning or asking to release it so another contributor can work on it. My investigation notes are below in case they help.

