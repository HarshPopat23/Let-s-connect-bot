---
title: OLLM Maintainer-Priority Open Source Contributor Questions and Answers
description: Maintainer-first open-source guidance prioritizing Juan Cruz Viotti's responses, supported by practical perspectives from other contributors.
knowledge_base: OLLM
community: OSS | Let's Connect
content_type: question_answer
source_priority:
  primary: Juan Cruz Viotti
  secondary: Other experienced contributors from the collected response set
audience:
  - new open source contributors
  - students
  - GSoC and LFX applicants
  - community mentors
topics:
  - project selection
  - issue discovery
  - pull requests
  - maintainer communication
  - community participation
  - proposals
  - GSoC
  - LFX
  - contributor etiquette
language: English
version: 2.0
last_updated: 2026-09-12
---

# OLLM Maintainer-Priority Open Source Contributor Questions and Answers

## About this knowledge file

This file converts practical advice collected from open-source contributors and maintainers into structured questions and answers. Juan Cruz Viotti's answers are treated as the primary perspective because they reflect direct maintainer experience. Other contributors' responses are used as supporting guidance when they add practical steps or reinforce the maintainer perspective.

## Source-priority policy

Each answer begins with a maintainer-first perspective derived from Juan Cruz Viotti's response. The remaining guidance expands that position into practical actions for newcomers. When contributor opinions conflict, the maintainer-first position is preferred while still noting that individual repositories may use different workflows.

Every project has its own governance and contribution process. Before acting on any answer, read the project's `README.md`, `CONTRIBUTING.md`, code of conduct, issue templates, pull-request templates, and communication guidelines. Project-specific rules always take priority over general advice.

## 1. How should I choose the best open-source project to contribute to?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Start with software that you already use or are actively trying to use. When an upstream bug or limitation blocks your real work, contributing the fix can be faster and more valuable than filing an issue and waiting. Real usage gives you authentic context and naturally leads to meaningful contributions.

The best project is therefore usually one that you genuinely care about, use in practice, can understand or are motivated to learn, and whose community is active enough to review contributions. Do not select a project only because it has fewer contributors. A quiet repository may offer less competition, but it may also have inactive maintainers, delayed reviews, or no clear future direction.

A strong selection process considers the following factors:

1. **Personal interest or real usage:** Projects you already use are excellent choices. Real usage helps you understand the project's purpose, notice limitations, and contribute changes that solve genuine problems.
2. **Technical fit:** Familiarity with the project's language or framework lowers the initial learning barrier. You do not need to know the entire stack, but you should be able and willing to learn it.
3. **Community activity:** Check whether maintainers respond to issues, review pull requests, publish releases, and participate in public communication channels.
4. **Project value:** Prefer work that remains useful even if you are not selected for GSoC, LFX, or another program. The contribution should improve your skills and create real value for users.
5. **Newcomer support:** Look for clear documentation, contribution guidelines, public discussions, meetings, and respectful feedback.
6. **Review responsiveness:** A highly active project can still be approachable if maintainers provide timely and constructive reviews.

Crowd size is a secondary factor. You can stand out in a popular project through thoughtful research, reliable execution, clear communication, and meaningful contributions. A less crowded project is useful only when it is healthy and actively maintained.

### Practical selection checklist

- Use the project or complete its introductory tutorial.
- Read its roadmap, documentation, governance, and contribution guide.
- Inspect issue responses, recent pull-request reviews, releases, and discussions.
- Join its public communication channel or community meeting.
- Identify whether its goals match your interests and career direction.
- Confirm that you would still value the experience without a stipend or selection.

### Key principle

Choose for interest, usefulness, technical growth, and community health. Do not choose only for low competition.

## 2. How should I find the best issue to work on, and should I use AI?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** The strongest issues often come from trying to use the project and discovering something that blocks you. In that situation, the issue may not exist yet because you found a real problem that nobody previously noticed or reported.

Start manually and through real usage so that you understand the project before allowing AI to assist you. Browse issues labeled `good first issue`, `help wanted`, `documentation`, or `bug`, but do not assume a label guarantees that an issue is simple or still relevant.

The best issue is one that you can reproduce, understand, and complete within a reasonable scope. Review recent merged pull requests to learn what maintainers currently prioritize, what testing they expect, and how contributors communicate.

Useful manual methods include:

- Running the project locally and following its tutorials.
- Using the product as a real user and recording failures or confusing behavior.
- Reading open issues, discussions, roadmaps, and recent pull requests.
- Searching the codebase for `TODO`, `FIXME`, deprecated code, missing tests, and documentation gaps.
- Asking maintainers which tasks are useful and appropriately scoped.

AI is useful after you have gathered project context. It can summarize an issue, explain unfamiliar code, locate potentially relevant files, compare candidate issues, suggest test cases, or help interpret a stack trace. It should not blindly select an issue or declare that something is a bug.

Before committing to an issue:

1. Reproduce the reported behavior locally.
2. Check whether the issue is still valid on the latest branch.
3. Search open and closed issues, pull requests, discussions, and recent commits.
4. Read the complete issue discussion for hidden requirements.
5. Estimate whether you understand the expected result and affected components.
6. Follow the project's assignment or claiming policy.

### Key principle

Use manual investigation to establish truth. Use AI to accelerate understanding, not to replace verification.

## 3. What should I do if someone else starts working on an issue that I opened or planned to solve?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** If someone else completes the work first, that is a positive outcome because the issue is solved. The objective is not personal ownership. Use the saved time to investigate the next useful problem.

Do not turn the situation into a competition. The project's goal is to solve the problem, not to guarantee ownership of work to the person who first noticed it. Check the repository's contribution rules because projects handle assignment differently.

If you have not started implementation, allow the other contributor to proceed and choose another useful task. You can still review their pull request, share reproduction steps, suggest test cases, or provide technical context.

If you have already completed meaningful work, leave one calm public comment explaining your current progress. Ask whether collaboration would be useful. Do not post angry messages, open a competing pull request merely to race, or pressure maintainers to choose you.

If the other contributor becomes inactive, wait for the project's stated inactivity period. Then ask publicly whether you may continue the work. Some communities reassign stale issues; others accept the first complete and correct implementation.

If the competing work is clearly spam or does not address the issue, do not attack the contributor. Report the technical problem factually and let maintainers decide.

### Recommended response

- Acknowledge the other contributor respectfully.
- Share any useful research or reproduction details.
- Offer to collaborate or review.
- Continue with another task if collaboration is unnecessary.
- Ask maintainers only when project policy or ownership is unclear.

### Key principle

Optimize for the issue being solved and the project improving, not for personal ownership.

## 4. Should I assign myself to every unassigned issue that I might be able to solve?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Assignment is often an anti-pattern in open source. It comes largely from company-oriented project management, while distributed volunteer projects frequently work better when contributors simply produce useful work and nobody can reserve tasks indefinitely.

No. Claiming many issues without immediate capacity blocks other contributors and reduces trust. In some open-source projects, self-assignment itself is discouraged because assignment can create the false impression that nobody else may work on the task.

First read the project's workflow. Some projects require a maintainer to assign issues, some allow an `/assign` command, and some prefer contributors to submit working pull requests without formal assignment.

If self-assignment is allowed, take one issue at a time. A second issue may be reasonable only when the first is waiting on review and you have clearly demonstrated that you can complete both. Never reserve tasks simply to increase visibility or prevent others from contributing.

Before claiming an issue:

- Confirm that you can reproduce or understand it.
- Research the expected scope.
- Check whether another contributor has announced work.
- Make sure you can begin soon and provide progress updates.
- Release the issue if you become unavailable.

For additional perspective on why assignment can be harmful in volunteer communities, see [Do not lick the cookie](https://www.redhat.com/en/blog/dont-lick-cookie).

### Key principle

Claim only work you can actively complete, and follow the repository's policy instead of assuming assignment means ownership.

## 5. How can I start contributing if I do not know a technical stack yet?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Open-source contribution is not limited to code. A newcomer can begin through community management, content, advocacy, operations, funding, or program support while gradually improving technical skills. Maintainers often need these neglected contributions as much as, or more than, additional code.

For code contributions, begin by learning one stack well enough to build and debug small projects. You do not need to become an expert before entering open source, but immediately submitting AI-generated code to unfamiliar repositories is harmful to both you and maintainers.

A practical learning path is:

1. Choose one language or stack based on your interests.
2. Learn its basic syntax, package manager, testing tools, and debugging workflow.
3. Build two or three small projects independently.
4. Learn Git fundamentals: branches, commits, remotes, rebasing, resolving conflicts, and pull requests.
5. Select a small, active project using the same stack.
6. Run it locally, read its documentation, and make a small verified contribution.
7. Gradually move to tests, bug fixes, and deeper code changes.

You may also start with non-code contributions while developing technical skills. Valuable work includes improving documentation, testing tutorials, reproducing bugs, community moderation, event support, content creation, translation, design, advocacy, fundraising, and helping other users.

AI can explain code and concepts, but you must understand what a change does, why it belongs in that component, and how to test it. If you cannot explain your own patch, it is not ready for submission.

### Key principle

Learn by building and participating, but do not use a real project as a place to submit code you cannot understand.

## 6. If I cannot find an issue, should I use AI to generate issues or perform user testing?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Perform user testing. Even strong and mature codebases still contain legitimate simple bugs that can be discovered through careful real-world use. AI may help investigate possibilities, but actual testing establishes whether a problem exists.

Begin with user testing. Install the project, complete its tutorials, try realistic workflows, and observe broken behavior, unclear documentation, confusing interfaces, missing validation, and difficult setup steps. Problems found through genuine use are usually more valuable than generic AI suggestions because they are connected to real user experience.

AI can help brainstorm edge cases or areas worth investigating, but every suggestion must be treated as an unverified hypothesis. Never copy a generated list directly into the issue tracker.

For each possible issue:

1. Reproduce it consistently on the latest supported version.
2. Record the environment, steps, expected behavior, and actual behavior.
3. Search open and closed issues using multiple keywords.
4. Search open and merged pull requests, discussions, release notes, and recent commits.
5. Check whether the behavior is intentional or documented.
6. Confirm that no active pull request already addresses it.
7. If uncertain, ask in the project's preferred public channel before filing.
8. Open one well-researched issue rather than many speculative reports.

Telling AI not to return duplicates is not sufficient. An AI model may not have current repository state and may miss differently worded reports. Verification must happen against the live repository.

### Key principle

Use the product first. Treat AI-generated issues as research leads, never as confirmed bugs.

## 7. What should I do when I understand an issue but do not know how to implement the fix?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** First determine whether the issue is well scoped. For a clear and narrow bug, AI can be useful even to experienced engineers who are unfamiliar with the codebase. For an ambiguous issue with several possible designs, ask a maintainer because only project context may reveal the correct tradeoff.

Do not rush into coding. First determine the intended behavior, affected scope, and decision owner.

For a clear bug with known expected behavior, trace the execution path, locate the responsible code, reproduce the failure, and study related tests or previous pull requests. AI can help explain unfamiliar modules, suggest search terms, identify possible files, or propose test cases.

For an unclear feature or architectural change, ask a maintainer before implementing. Several technically valid solutions may have different compatibility, maintenance, security, or design consequences. Maintainer guidance can prevent a large patch from being rejected because it follows the wrong direction.

Use this workflow:

1. Restate the problem and expected behavior in your own words.
2. Reproduce the issue and create the smallest failing example.
3. Trace the relevant code path.
4. Read documentation, related issues, previous pull requests, and similar implementations.
5. Write a short implementation plan.
6. Confirm the plan publicly if the scope is uncertain.
7. Implement the smallest useful change.
8. Add or update tests that fail before the fix and pass afterward.
9. Run all required checks and review the diff yourself.
10. Explain the reasoning, risks, and verification in the pull request.

If the issue remains far beyond your current ability, release it honestly. Learning from the investigation is still useful, and leaving early is better than blocking the task indefinitely.

### Key principle

Use AI for explanation and exploration, maintainers for ambiguous direction, and tests for verification.

## 8. What should I do if my pull request is taking a long time to be reviewed or merged?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Long waits are normal because most maintainers are volunteers with jobs and other responsibilities. Valuable contributions can land many months or even a year after submission. Ping only when the change is genuinely needed, and recognize that a consistently inactive project may actually need more maintainers.

Long review times are normal in volunteer-maintained projects. Maintainers may have release work, security responsibilities, personal commitments, or a large review queue. A slow review does not automatically mean that your contribution is rejected.

Before following up, check your own pull request:

- Are all automated checks passing?
- Have you answered every review comment?
- Is the branch up to date?
- Is the pull request clearly described and reasonably scoped?
- Is additional documentation, testing, or a signed agreement required?
- Is the project in a release freeze or inactive period?

If everything is ready, follow the project's documented review process. One polite public follow-up after a reasonable period is acceptable. You may also raise the pull request during an appropriate community meeting, especially when you need clarification.

Do not repeatedly tag maintainers, send multiple direct messages, or post the same request across channels. Continue learning or work on another task while waiting. Some valuable pull requests take months, and occasionally much longer, to land.

If the project rarely responds to any issues or pull requests, consider whether it needs new maintainers or whether another active project would be a better place for your time.

### Key principle

Make the pull request easy to review, follow up once through the proper channel, and remain patient.

## 9. How can I determine whether an open-source project is active?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Judge activity by how maintainers respond to issues and bug reports. Mature projects may receive relatively few pull requests because the software is stable, so low commit volume alone is not evidence that a project is abandoned.

Do not judge activity using commit count alone. Mature software may require fewer code changes while still receiving responsible maintenance. The strongest indicator is whether maintainers respond to real user needs.

Review activity over several weeks or months:

- Responses to new bug reports and security concerns.
- Pull-request reviews and merges.
- Recent releases, maintenance branches, and release notes.
- Issue triage, labels, milestones, and roadmap updates.
- Public meetings, discussions, mailing lists, forums, or chat activity.
- Documentation updates and dependency maintenance.
- Evidence that maintainers explain delays or release freezes.

Red flags include many old pull requests with no response, unanswered reproducible bugs, abandoned communication channels, broken build systems, and no release or maintenance activity without explanation.

Before deciding that a project is dead, ask respectfully in its public channel. A project may be stable, temporarily paused, migrating repositories, or preparing a major release.

### Key principle

Measure responsiveness and maintenance behavior, not raw commit frequency.

## 10. How do I become an excellent contributor? Is it only about issues and pull requests?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Issues are only the tip of the iceberg. The strongest contributors deeply understand the project's purpose and vision, then identify what should happen next without waiting for every important task to be written as an issue. That judgment, combined with strong engineering, is what develops into maintainer-level responsibility.

Issues and pull requests are only visible artifacts of contribution. Excellent contributors understand the project's purpose, improve the experience of users and maintainers, and take responsibility for work that may never appear in an issue tracker.

High-value contribution includes:

- Submitting well-tested and maintainable code.
- Reporting reproducible problems with useful evidence.
- Reviewing pull requests and testing other contributors' changes.
- Improving documentation, tutorials, examples, and onboarding.
- Answering user questions and guiding newcomers respectfully.
- Participating in design discussions and roadmap planning.
- Creating demos, talks, videos, or case studies.
- Helping with releases, triage, governance, events, and community operations.
- Identifying important future work after understanding the project's vision.

Quality matters more than volume. A contributor builds trust by being consistent, receiving feedback constructively, completing commitments, communicating clearly, and helping others succeed. Maintainer-level contributors eventually identify what the project needs without waiting for every task to be written as an issue.

### Key principle

Focus on sustained project value and shared ownership, not contribution statistics.

## 11. How can I contribute during community meetings instead of remaining silent?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Ask many questions, including questions that feel basic. Community meetings often exist to open the floor for newcomers, and maintainers value sincere questions because they demonstrate interest and reveal where understanding or documentation is missing.

You do not need to be an expert to participate. Community meetings often exist specifically so contributors and users can ask questions, share progress, and understand project direction.

Before the meeting, read the agenda and prepare one useful item. During the meeting, you can:

- Ask a question about architecture, workflow, roadmap, or an unclear issue.
- Give a concise update on your current issue or pull request.
- Demonstrate a fix, prototype, test result, or newly learned concept.
- Share a user problem or usability observation.
- Propose an idea and ask whether it aligns with project priorities.
- Volunteer for a clearly defined task.
- Help another contributor by sharing relevant context.
- Take notes or add useful material to the meeting agenda.

Keep updates brief and specific: what you tried, what happened, where you are blocked, and what decision or help you need. Avoid using the meeting only to demand a review. Ask genuine questions, including basic ones, because they often reveal missing documentation that affects many newcomers.

### Example meeting update

> I reproduced issue 123 on the latest main branch and traced it to the validation layer. I see two possible approaches. Before implementing, I would like guidance on which approach matches the project's compatibility policy.

### Key principle

Participation means contributing questions, evidence, ideas, progress, or help. Expertise is not a prerequisite.

## 12. How should I write a strong GSoC, LFX, or mentorship proposal?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Research before writing. A strong proposal is concise, project-specific, and clearly written in the applicant's own voice. Reducing a proposal to its essential reasoning is harder and more valuable than producing a large volume of generic text. It must not read like unedited AI output.

A strong proposal proves that you understand the problem, the project, the users, and the work required. Attractive formatting helps readability, but technical depth, realistic planning, and demonstrated understanding matter more.

Research before writing:

- Use the project and understand the user problem.
- Read the project idea, roadmap, architecture, and related issues.
- Join community meetings and discuss expectations with mentors.
- Study relevant code, tests, previous implementations, and rejected approaches.
- Review previously selected proposals for structure, not for copying.
- Confirm the expected deliverables and evaluation criteria.

A complete proposal should contain:

1. A concise problem statement.
2. Why the problem matters to users and the project.
3. Your understanding of the current implementation.
4. A specific technical approach and alternatives considered.
5. Architecture or workflow diagrams when they improve clarity.
6. Deliverables divided into measurable milestones.
7. A realistic weekly timeline, including learning, testing, review, and buffer time.
8. Risks, dependencies, unknowns, and mitigation plans.
9. Testing, documentation, compatibility, and rollout plans.
10. Relevant experience and contributions.
11. Communication plan, availability, and other commitments.
12. Optional future work clearly separated from required deliverables.

Keep the proposal concise. Remove generic claims and paragraphs that do not prove understanding. Do not submit unedited AI-generated writing. Mentors can often recognize vague, repetitive text that lacks project-specific reasoning.

An example archive shared in the source responses is [GSoC Archive 2026](https://github.com/satwiksps/GSoC_archive_2026). Treat previous proposals as structural references only; requirements differ by organization and year.

### Key principle

Research deeply, propose specifically, plan realistically, and write concisely in your own voice.

## 13. How should I ask maintainers to review my pull request, especially after receiving no response on Slack?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** After a reasonable and appropriate review request, wait. Maintainers are busy and open-source review capacity is often underfunded. Repeated Slack messages do not create time and can make collaboration harder.

First make sure the pull request is genuinely ready for review. Resolve comments, pass automated checks, update the branch if required, and provide a concise description of the change and its verification.

Use the repository's preferred review mechanism. This may be an automatic reviewer assignment, review command, team label, public pull-request comment, mailing list, or community meeting. A short public message is usually better than a private direct message because it preserves context and allows any qualified maintainer to respond.

A useful follow-up contains:

- A statement that the pull request is ready.
- A one-sentence summary of the change.
- Confirmation that tests and checks pass.
- The specific feedback or decision you need.

If you already asked on Slack and received no response, do not keep repeating the request. Wait, continue with other useful work, or mention it once in the next appropriate meeting. If the project permits it, request review from another maintainer familiar with that code area.

### Example follow-up

> This pull request is ready for review. It fixes the reported validation failure and adds a regression test. All required checks are passing. When someone has capacity, I would appreciate feedback on the compatibility decision described in the pull-request notes.

### Key principle

Request review through the documented public process, provide useful context, and never spam maintainers.

## 14. Is there a minimum number of pull requests required for GSoC or LFX selection?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Pull-request count does not matter and can even be zero. From a maintainer's evaluation perspective, what matters is whether the applicant appears thoughtful, collaborative, capable, and genuinely understands the project.

There is no universal minimum pull-request count. Requirements can vary by organization, but selection is generally based on evidence that you understand the project, can communicate and collaborate, and are capable of completing the proposed work.

One meaningful contribution can provide stronger evidence than many trivial pull requests. Reviewers may consider:

- Understanding of the project and proposed problem.
- Quality, relevance, and maintainability of prior work.
- Ability to respond to review feedback.
- Communication quality and reliability.
- Participation in discussions and community activities.
- Technical plan, scope, timeline, and risk awareness.
- Alignment with mentors and project priorities.

Avoid creating documentation typo pull requests, artificial issue reports, or unnecessary changes merely to increase your count. This can damage trust and reduce your chance of selection.

Always read the current program and organization requirements because a specific project may request a qualification task or preliminary contribution.

### Key principle

Pull requests are evidence of collaboration and capability, not points in a selection formula.

## 15. Is open source only about GSoC and LFX? What does open source really mean?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** Open source is decentralized collaboration. People solve problems publicly so that the next engineer can build on what has already been learned. In that sense, open-source engineering contributes to a wider human foundation of shared knowledge, much like scientific publishing. GSoC and LFX are only two of many entry points.

GSoC and LFX are structured mentorship programs within a much larger open-source ecosystem. They can provide mentorship, recognition, experience, and sometimes financial support, but they are not the purpose of open source.

Open source is decentralized collaboration in which people make software, knowledge, standards, documentation, and tools available so others can study, use, improve, and build upon them under the applicable license. Each contribution can make the next person's work easier.

Open-source participation may include code, documentation, testing, design, translation, support, research, standards, governance, security, events, education, funding, or community building. Contributors gain experience with real systems, imperfect codebases, distributed teamwork, technical review, and communication across cultures and time zones.

The healthiest motivation is to solve useful problems, improve projects you care about, learn from others, and strengthen shared technical infrastructure. Mentorship programs may become outcomes of that work, but contribution should remain valuable even without selection.

### Key principle

Open source is long-term public collaboration. GSoC and LFX are opportunities within it, not its definition.

## 16. What etiquette should every new open-source contributor follow?

### Answer

**Primary maintainer perspective from Juan Cruz Viotti:** AI abuse has caused many maintainers to distrust issues and pull requests that look generated, generic, or poorly understood. Contributors should demonstrate genuine human judgment, project-specific investigation, and responsibility for every claim and code change.

Begin with the project's written rules and observe how established contributors interact. Good etiquette is not excessive formality; it is respect for other people's time, project processes, and shared goals.

### Essential etiquette

- Read `README.md`, `CONTRIBUTING.md`, the code of conduct, templates, and relevant documentation.
- Search issues, pull requests, discussions, and documentation before asking or reporting.
- Reproduce problems and provide complete technical evidence.
- Keep issues and pull requests focused on one clear objective.
- Explain what changed, why it changed, and how it was tested.
- Do not claim work you cannot actively complete.
- Do not submit spam, generated issue lists, or code you do not understand.
- Do not repeatedly tag or privately message maintainers for attention.
- Accept review feedback professionally and ask for clarification when necessary.
- Credit other contributors and collaborate instead of competing.
- Release an issue when you no longer have capacity.
- Follow the project's licensing, sign-off, security, and disclosure rules.

### Responsible use of AI

AI may assist with explanations, search, drafting, debugging, and test ideas. You remain responsible for every statement and line of code you submit. Verify the output, understand the reasoning, run the required tests, and rewrite communication in your own clear voice.

Maintainers increasingly receive large amounts of low-quality AI-generated content. Generic wording, unnecessary issues, unexplained code, invented claims, and failure to answer technical questions quickly reduce trust. The best way to stand out is to demonstrate real investigation, project-specific understanding, honest uncertainty, and human judgment.

### Beyond the basics

- Help newcomers without judging their mistakes.
- Improve documentation when repeated questions expose gaps.
- Review and test other people's contributions.
- Communicate early when blocked or unavailable.
- Understand why a component or rule exists before proposing changes.
- Focus on the learning journey and project impact rather than only stipends or titles.

### Key principle

Be useful, honest, patient, prepared, and respectful. Make maintainers' and contributors' work easier.

## Closing guidance

Successful open-source contribution is not a race to collect issues, pull requests, or program selections. It is the gradual development of technical judgment, communication, reliability, and trust. Use AI as an assistant, use project documentation as the authority, use maintainers for ambiguous decisions, and use reproducible evidence to support every contribution.

This file should be reviewed periodically because project practices, program requirements, and tooling change over time.
