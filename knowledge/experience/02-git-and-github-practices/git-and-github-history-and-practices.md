---
title: The History of Git and GitHub, and the Commands You Will Actually Use
category: git-and-github-practices
source_url: https://git-scm.com/book/en/v2/Getting-Started-A-Short-History-of-Git
updated: 2026-09-05
---

# Where Git came from

Git was not built as a general-purpose product. It was built in an emergency. From 2002 onward, the Linux kernel project (the core of the Linux operating system) used a paid tool called BitKeeper to track changes to its code. BitKeeper's company let kernel developers use it for free, but under strict rules. In 2005, a kernel developer named Andrew Tridgell wrote a small tool that peeked at how BitKeeper worked behind the scenes, without permission. BitKeeper's company said this broke the rules of their free license, and took away free access for every kernel developer at once. Thousands of people suddenly had no tool to keep working with.

Linus Torvalds, the person who created Linux itself, decided to write a replacement tool himself instead of waiting on anyone else. His first saved version of this new tool, which he named Git, was made on April 7, 2005. In about ten days it was already good enough to manage its own code, and within two months the entire Linux kernel was being built using it. Torvalds wanted it to be fast even on a huge project, to work without needing one central computer in charge, to never quietly lose or corrupt someone's work, and to handle thousands of people working on their own separate copies at once without chaos. Git still behaves the way it does today because of these original goals.

# Where GitHub came from

Git and GitHub are two different things, and mixing them up is one of the most common confusions for someone new. Git is the tool described above. It lives entirely on your own computer and knows nothing about websites, accounts, or anything called a "pull request." GitHub is a company's website built on top of Git, founded by Tom Preston-Werner, Chris Wanstrath and PJ Hyett (with Scott Chacon helping early on), and opened to the public in April 2008. What GitHub added was a place to store copies of Git projects online and a set of social features on top: a way to propose changes for review (a pull request), a way to report problems (an issue), and a way to make your own copy of someone else's project (a fork). GitLab and Bitbucket are other companies offering a similar website on top of the same Git tool. When you run `git commit`, you are only talking to Git on your own machine. When you open a pull request, you are talking to GitHub's website, which itself is just using Git behind the scenes to move code between different copies of a project.

# The words "local" and "remote," explained simply

Almost everything below depends on this one idea, so it is worth being explicit about it.

**Local** means the copy of the project sitting on your own computer, in a folder, that only you can see until you choose to share it.

**Remote** means a copy of the project that lives somewhere else, almost always on a server such as GitHub, that other people can also see and download.

When you make a change, you are editing your local copy first. Nothing you do reaches anyone else until you deliberately send it to a remote copy, using a command like `git push`. The reverse is also true: changes other people make on the remote copy do not appear on your computer automatically, you have to deliberately ask for them, using a command like `git fetch` or `git pull`. Almost every mistake a new contributor makes with Git comes down to forgetting that local and remote can be, and often are, out of sync with each other.

A few more basic words you will see constantly: your **working directory** is simply the actual files on disk that you open and edit in your editor. The **staging area** (sometimes called the index) is a waiting area where you place the specific changes you are about to save, using `git add`, before you actually save them with `git commit`. A **commit** is a saved snapshot of your project at one point in time, with a message describing what changed. A **branch** is just a name pointing at one specific commit and its history, letting several separate lines of work exist in the same project without interfering with each other. **HEAD** is Git's name for "the commit you are currently looking at right now."

# Your first real workflow, start to finish

A brand-new contributor's very first sequence, combining setup with an actual change, usually looks like this:

    git clone https://github.com/YOUR-NAME/PROJECT.git
    cd PROJECT
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"
    git add path/to/changed-file
    git commit -s -m "fix: concise description of the change"
    git push origin your-branch-name

`git clone` downloads a full copy of a remote project onto your computer for the first time; after this, that folder is your local copy. `git config --global` tells Git your name and email so every commit you make anywhere on your computer is labeled as coming from you; you only need to run this once per computer, not once per project. `git add` moves your changed file into the staging area described above. `git commit -s -m "..."` saves a snapshot of everything in the staging area, with the `-m` message describing what you did. The `-s` flag additionally adds a line to the commit called a Developer Certificate of Origin sign-off, which is a short statement that you have the right to contribute this code; only add `-s` when a project's rules actually require it (see this knowledge base's licensing and DCO guidance for what that means). Finally, `git push` uploads your new commit from your local copy to the remote copy on GitHub, which is the step that actually lets anyone else see your work.

# Commands you will reach for constantly

Checking what has changed before you save it as a commit:

    git status                          # a plain-English summary: what's staged, what's changed but not staged, what's brand new
    git diff                            # shows the exact lines changed, for changes not yet staged
    git diff --cached                   # shows the exact lines changed, for changes already staged (also written --staged)
    git diff HEAD                       # shows every change since your last commit, staged or not

Reading a project's past commits once you need context on why something is the way it is:

    git log --oneline                   # one short line per commit, easiest to scan quickly
    git log --stat                      # which files each commit touched, and how many lines
    git log -p                          # the full exact change made in every commit
    git log --graph --decorate          # a text-based picture of how branches connected, with names attached
    git log -5                          # only show the last 5 commits
    git log --author="Name"             # only commits made by one specific person
    git log --grep="pattern"            # only commits whose message contains a certain word or phrase
    git log since..until                # only commits made between two points in time (a commit, a branch name, or HEAD)
    git log -- path/to/file             # only commits that changed one specific file

Working with branches (separate lines of work) and remotes (other copies of the project elsewhere):

    git branch                          # list the branches that exist on your own computer
    git checkout -b new-branch-name     # create a brand-new branch and switch to it immediately
    git merge other-branch              # bring another branch's commits into the branch you're currently on
    git remote add name url             # give a nickname to another copy of the project somewhere else, so you can refer to it by name
    git fetch remote branch             # download a branch's commits from elsewhere, without changing anything on your own branch yet
    git pull remote                     # download and immediately combine those commits into your current branch, in one step
    git pull --rebase remote            # same as above, but replay your own commits on top afterward instead of merging (see below for what this means)
    git push remote branch              # upload your branch and its commits so other people can see them

Removing files Git isn't tracking at all, such as leftover build output:

    git clean -n                        # a dry run: only lists what WOULD be deleted, deletes nothing
    git clean -f                        # actually deletes those files, for real, with no way to undo it

Always run `-n` first to see the list before you run `-f`. There is no recycle bin here; once deleted this way, the files are gone.

# Undoing things without losing work

These three commands look similar but do very different things, and confusing them is how contributors accidentally lose work:

    git reset path/to/file              # takes one file back out of the staging area; the file's contents on disk are not touched at all
    git reset commit-id                 # moves your branch back to an earlier commit, but keeps all the actual changes as unsaved edits on disk
    git reset --hard commit-id          # moves your branch back to an earlier commit AND deletes any changes on disk that came after it

`git reset --hard` permanently throws away any uncommitted changes and any commits after the point you reset to, so only use it on commits that nobody else has already downloaded from you. If a bad commit has already been pushed, or someone else already pulled it, use `git revert commit-id` instead: this creates a brand-new commit that undoes the earlier one, without erasing or rewriting anything that already happened, which makes it safe to use even on a branch other people share. If you only want to fix the message or the contents of the single commit you just made, and have not pushed it anywhere yet, `git commit --amend` replaces that last commit in place.

# Why merge asks for a commit message and rebase does not

Say two branches have "diverged," meaning each one has commits the other does not have yet. When you run `git merge other-branch` in this situation, Git cannot just move your branch forward to catch up, because there are two separate histories to combine. Instead it creates one brand-new commit that has two parent commits instead of the usual one, called a merge commit. Because this commit does not represent a single logical change you made, Git opens a text editor with an automatically written message like `Merge branch 'other-branch' into current-branch`, which you can simply accept or edit.

`git rebase other-branch` solves the same divergence differently: instead of creating a merge commit, it takes your branch's commits, sets them aside temporarily, and replays them one at a time on top of the very latest point of `other-branch`, keeping each one's own original message. No merge commit ever gets created, so the resulting history looks like one straight line instead of two histories joining. The catch is that every replayed commit gets a brand-new internal ID (its commit hash changes), which is exactly why rebase is risky on a branch someone else has already downloaded: their copy and your newly rewritten copy no longer match up at all. The safe habit most projects follow is: rebase freely on a branch that only exists on your own computer so far, and use merge (or GitHub's "squash and merge" button) once other people are already looking at or reviewing that branch.

# What a merge conflict actually is, and how to resolve it

A conflict happens when Git genuinely cannot decide, on its own, how to combine two versions of the same file, usually because both sides changed the exact same lines, or one side edited a file that the other side deleted entirely. Rather than guess and possibly get it wrong, Git pauses the merge or rebase and asks you, a human, to decide.

An unresolved conflict shows up written directly inside the affected file, looking like this:

    <<<<<<< HEAD
    your current branch's version of these lines
    =======
    the other branch's version of these lines
    >>>>>>> other-branch

Everything between the line `<<<<<<< HEAD` and the line `=======` is your own side of the disagreement. Everything between `=======` and `>>>>>>> other-branch` is the other side being brought in. Resolving the conflict means opening the file in your editor, deciding what the final correct content should actually be (which might be one side, the other side, a mix of both, or something new entirely), then deleting all three of those marker lines by hand so no trace of them remains.

The general steps to finish a conflict, once you have edited the file, are:

    git status                          # confirms which files still need resolving
    # open each conflicted file, edit out the markers, keep only the intended final result
    git add path/to/resolved-file       # tells Git you consider this one file resolved
    git commit                          # finishes the process, if this conflict happened during a merge
    git rebase --continue               # finishes the process, if this conflict happened during a rebase

During a rebase, this can pause more than once, once for every replayed commit that runs into a conflict, so you may repeat the add-and-continue step several times in a row. If you want to give up entirely and go back to exactly how things were before you started, run `git merge --abort` or `git rebase --abort`.

A few extra commands make this easier: `git diff` shows you the conflict markers with surrounding context so they're easier to read, `git log --merge` shows you the specific commits from both sides that caused the disagreement in the first place, `git checkout --ours path/to/file` or `git checkout --theirs path/to/file` lets you accept one entire side of the conflict without manually editing anything (handy for files that are auto-generated, like lockfiles), and `git mergetool` opens a visual comparison tool if your computer has one set up. Always run the project's tests again after resolving a conflict by hand. Because a human decided the final wording, it is easy to accidentally reintroduce a bug that used to be fixed, sometimes called a regression, meaning a problem that was already solved once coming back again.

# Why `git push --force` exists, and when it is safe

A plain `git push` gets rejected whenever your local branch and the matching remote branch have "diverged" from each other, meaning your local history is not simply "the remote's history, plus a few new commits on top." This happens any time you change or remove commits you had already pushed once before, which is exactly what `git rebase`, `git commit --amend`, and `git reset` all do. Git refuses the plain push here on purpose, specifically to stop you from accidentally erasing commits that currently only exist on the remote copy.

`git push --force` (sometimes shortened to `-f`) turns that protection off and makes the remote branch become an exact copy of your local branch, whatever was there before. This really is necessary after you rebase or amend a branch you had already pushed, since there is no other way to get your rewritten history onto the remote. The real danger is: if someone else pushed their own new commits to that same branch while you were working, a plain `--force` overwrites the remote and permanently deletes their commits too, with no warning shown to you at all.

    git push --force-with-lease origin your-branch-name

`--force-with-lease` adds one safety check on top: right before overwriting, it confirms the remote branch is still exactly where you last saw it. If someone else has pushed since then, it refuses to proceed instead of silently deleting their work. Use `--force-with-lease` instead of a plain `--force` as your default habit, only force-push branches that belong to you alone, and never force-push a project's shared main branch under any circumstance, no matter how sure you feel.

# Building your work on top of someone else's open pull request

Here is a real situation that comes up often: another contributor already has an open pull request (their proposed change, waiting for review) with its own branch for related work, and you want to add to it instead of doing the same work again separately. Start by commenting on their pull request to say you would like to build on it, so the original author knows what's happening and nobody duplicates effort by accident.

If the other contributor's work lives on their own fork (their personal copy of the project on GitHub), you can add that fork as a remote and create your own branch starting from theirs:

    git remote add their-username https://github.com/their-username/PROJECT.git
    git fetch their-username
    git checkout -b my-additions their-username/their-branch-name

If you would rather not add a whole new remote just for this, GitHub also lets you download any open pull request directly, using a special address it maintains automatically:

    git fetch origin pull/PR_NUMBER/head:local-branch-name
    git checkout local-branch-name

Make your changes and commit them as usual. After that, you have two options. If the other contributor turned on "Allow edits from maintainers" for their pull request and you already have the right access, you can push your commits straight onto their branch. Otherwise, push to your own fork and open a brand-new pull request, but choose their branch as the base (the branch your change will eventually be combined into) instead of the project's usual main branch. GitHub lets you pick any branch as a base, so this correctly shows everyone that your change depends on theirs. Say so plainly in your description too. Once their original pull request is finally merged, you will need to point your pull request's base back at the main branch (and possibly rebase onto it) to finish the process.

# Common Git problems new contributors hit, and the fix

You accidentally committed straight onto the main branch instead of a separate feature branch:

    git branch fix/my-change
    git reset --hard upstream/main

Only do this if nobody else has already downloaded your commits from main; this sequence saves your work onto a brand-new branch first, then moves main back to matching the official upstream copy.

A merge or rebase has stopped because of a conflict: see "What a merge conflict actually is, and how to resolve it" above for the full explanation and the exact steps.

You staged a file by mistake and do not want it in your next commit yet: `git reset path/to/file` takes it back out of the staging area without changing its actual contents at all.

Your branch has fallen behind the project's main branch, meaning other people's commits have piled up that you do not have yet: run `git fetch upstream` followed by `git rebase upstream/main` (or `git merge` instead of rebase, if the project's own contribution guide asks for that).

You find yourself in a "detached HEAD" state, usually right after checking out one specific commit or tag instead of a branch, meaning any new commit you make would not actually belong to any branch and could be lost later: immediately run `git checkout -b some-new-branch-name` to save whatever you have done onto a real branch, or run `git checkout your-original-branch` to safely step away if you have not made any changes yet.

You already pushed a branch once, and then rewrote it locally with a rebase: see "Why `git push --force` exists, and when it is safe" above; use `git push --force-with-lease origin your-branch-name`, never a plain `--force`, and never on a project's shared main branch.
