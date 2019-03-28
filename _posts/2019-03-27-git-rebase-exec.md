---
title: Exec a command for each git commit
categories:
- programming
tags:
- git
---

Ever wanted to `git bisect` but not actually bisect?
As in, you just want to run a command but on every commit.

Turns out, the answer is in `git rebase`.
When rebasing interactively, you can append an "exec" command that will automatically execute in between each rebased commit.

```text
pick 1111111 Refactor one thing
exec time make test
pick 2222222 Add new feature
exec time make test
pick 3333333 Refactor another thing
exec time make test

# Rebase 000000..333333 onto 000000 (3 command(s))
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# x, exec = run command (the rest of the line) using shell
# d, drop = remove commit
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out
```

In this illustrative example, we've decided to run `time make test` on each of our commits, to test for test performance
regressions.

Neato!
