---
title: Git log For Merge Commit
categories: [programming]
tags: [git, scripting]
---

Merge commits are unique objects in git.
Beyond normal commit stuff, they have multiple parents.

`git log` has special arguments that can be used to change how merge commits are displayed.
A commonly known one is `--first-parent` , which ignores the second parent branch.
For many workflows where changes are merged to `master` , this lets you traverse the `master` branch lineage.

However, I'm here to talk about this [section of the doc][1] `-m` , `-c` , and `--cc` .
These are the useful when it comes to viewing the diff (patch) of a merge commit.

[1]: https://git-scm.com/docs/git-log#Documentation/git-log.txt--c

## Default behaviour

By default, `git log -p` will not attempt to show a diff for a merge.
It's a merge, what more do you need to know?

`git show` handles merge commits intelligently and uses the `--cc` flag.
This explains why `git show` behaves differently to `git log` .

## `-m`

The first flag, `-m` , will show the `git diff` between the commit and parents.
"Parents" is intentionally plural: diffs for each file changed in each commit will be shown.
That is, the diff hunks are entirely denormalized.

This can be thought of as a `git diff @^1..@` **unioned** with `git diff @^2..@` .
The changes in each file will be displayed. If a file is changed in both parents, then that file will have 2 diffs
shown for it.

## `-c`

The `-c` flag has a little more smarts than `-m` .
It shows a combined diff for a file, as is the result of the merge.
And it only shows files that are modified from both parents.
i.e. an **intersection** of the file sets.

The reasoning is that files changed only on one parent branch are trivially fast-forwarded.
This option is useful for seeing how git merged files and viewing the consequences of that.

## `--cc`

This option is weird in that it's a long option, unlike the previous two.
But it seems like it was meant to be " `-c` but  more".
This is the smartest of the bunch.
It's what `git show` will use when used on a merge commit.

Like `-c` only files that are in the common set of all parents are candidates.
Then the "uninteresting" hunks are filtered out, leaving only the hunks that resulted in merge conflicts.
So this option shows all the conflict resolutions.
Since those times are the where most common mistakes are introduced, this option quickly becomes handy.
