---
title: How to Write a Strong GSoC or LFX Proposal
category: how-to-write-the-best-gsoc-or-lfx-proposal
source_url: https://google.github.io/gsocguides/student/writing-a-proposal
updated: 2026-09-05
---

# Prove you can already do the work, before you even apply

The strongest proposals do not open by describing skills in general. They open by showing real, already-merged work on that exact project: a short list of pull requests you already got merged, and issues you already reported, ideally with the actual PR numbers linked. This matters far more than any paragraph describing your abilities, because it is proof instead of a claim. If you have not contributed to the project yet, that is the very first thing to go fix, well before you start writing the proposal itself.

# The overall shape a strong proposal usually takes

Different organizations format this differently, but a proposal that covers the following, in roughly this order, is hard to argue with:

- who you are, and your relevant background
- your existing contributions to this specific project, with links
- a short abstract explaining the problem the project solves and what you plan to improve
- a clear list of expected outcomes, written as concrete deliverables
- one or two real "qualification tasks," explained in detail (see below, this is the most important section)
- a table connecting each outcome to the problem it fixes and your proposed solution
- a week-by-week timeline with a midterm checkpoint
- ideas for what could come after this specific program, to show longer-term thinking
- your honest availability for the program period
- a statement that you intend to keep contributing after the program ends
- a short, genuine explanation of why you specifically are a good fit
- a references section linking every external resource, algorithm, or documentation page you relied on

# Qualification tasks are the single most important section, and they need real code

Do not just describe, in words, a feature you would like to build. Pick one or two small, real, currently-unsolved problems in the project's actual codebase, and work through an actual solution as part of the proposal itself. This means showing:

- the current buggy or missing behavior, described precisely
- an actual code snippet showing your proposed fix or new logic, not just a description of it
- a plain-language, step-by-step explanation of how that code works
- ideally, a short "before" and "after" comparison, so a mentor can immediately see the difference your change makes

This single section proves competence far more convincingly than any list of past skills, because a mentor can read your actual reasoning and actual code, on their actual project, before they have even accepted you.

# Explain the why behind every decision, not just the what

Whenever your proposal involves choosing between two possible approaches, write out the reasoning for your choice explicitly, instead of only naming the one you picked. For example, if two different algorithms could both solve a problem, do not just say "I will use algorithm A." Explain what algorithm B would have looked like too, and give the concrete reason A fits this specific situation better, for example because it makes detecting a certain kind of error simpler, or because it naturally fits the data structure the project already uses. A mentor reading this can tell the difference between someone who understood the tradeoff and someone who picked the first idea that came to mind.

# Always include a real timeline, with a midterm checkpoint in the middle

Break the whole program into clear phases, ideally week by week, starting from the community bonding period and ending at final submission. Make sure there is an explicit midterm evaluation point roughly halfway through, with a clearly stated, realistic subset of your outcomes marked as done by that point. This shows a mentor you have actually thought about pacing and about which parts of the work naturally come first, not just what the finished result should eventually look like.

# Show commitment beyond just the program itself

State your honest, specific availability for the program period, for example how many hours per week you can realistically give, and mention clearly if you have conflicting commitments such as exams during that time. Separately, say plainly that you intend to keep contributing to the project after the program formally ends. Mentors are choosing who to invest real time in, and a contributor who is honestly planning to stick around is a safer investment than someone who reads as only interested in the program itself.

# Cite every source you actually used

Anywhere you reference a specific algorithm, an external library's behavior, or another project's documentation, add it to a references section at the end with the actual link. This does two things: it lets a mentor quickly verify your technical reasoning against the real source, and it shows the proposal is grounded in real research rather than guesswork.

# End with something honestly yours

A short closing statement about why open source specifically matters to you, in your own plain words rather than generic phrases, is worth including. Mentors read a great many proposals; a short, specific, honest reason for why you care lands better than a polished but generic closing line.

# A few do's and don'ts worth remembering

**Ask the maintainer how long your proposal should be, before you write it.** Different organizations expect very different lengths, and some have a hard maximum. Ask first instead of guessing and writing far more than anyone will actually read.

**Use simple language throughout.** A proposal full of unnecessarily complicated words does not make you look more capable; it just makes it harder for a busy mentor to read quickly.

**Send it to the maintainer for review before your final submission**, if the program's timeline allows this. A mentor's early feedback on a draft is far more useful to you than only finding out something was wrong after you have already submitted it.

**Do not overload it with exact file paths and function names.** Avoid writing things like "this exists in this exact file, inside this exact function" over and over. A little bit of this, to show you actually explored the codebase, is fine; a proposal that reads like a directory listing is not.

**Do not repeat the same point again and again in different words.** If you already said something clearly once, trust that it landed, and move on to your next point instead of restating it.

**Do not make it too long or boring.** Remember that a real human being, usually one with many other proposals to read, is the one reading yours. Being clear and reasonably short respects their time far more than being exhaustive.

# Real examples worth reading

Reading a full, real proposal that actually got accepted is often more useful than any list of tips. Two complete examples, one written for GSoC and one written for LFX Mentorship, are shared publicly here for exactly this reason:

- GSoC proposal example: https://docs.google.com/document/d/1KRmWBUlNVxKfen5NnzUrY-PVE340xm1c40fK5zda7Ck/edit?usp=sharing
- LFX Mentorship proposal example: https://docs.google.com/document/d/1t3ZxFLM2yhg4AVGmnB0KkXGgciZlAYhrGqOHlxTvfc0/edit?usp=sharing
