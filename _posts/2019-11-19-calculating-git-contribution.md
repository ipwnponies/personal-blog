---
title: Calculating Lines of Code Committed in a Repository
categories:
- programming
tags:
- git
- scripting
---

Recently I applied [`black` python code formatter][1] to a repository at work.
I was the one to bite the bullet and format all existing files.
I was curious to know how many files would be touched and how many lines would be changed.

[1]: https://black.readthedocs.io/en/stable/

## Determining the Percent of Files Affected

```sh
# Count number of python files
find . -name '*.py' | wc -l

# Count python files in commit
git log @ -1 --stat -- '*.py'
```

For the repository in question, it was ~75% (~300/400 files).
While writing this, I realize that quite a few of the files are possibly empty `__init__.py` files.

## Determining User Contribution in Git Repository

I used this nifty one-liner from [*StackOverflow*][2].

[2]: https://stackoverflow.com/a/7010890

```sh
# Count of commits by author
git shortlog -s -n

# List of commits by author and add/remove line counts
git log --author="ipwnponies" --pretty=tformat: --numstat --no-merges

# Cumulative summation of line change counts
git log --author="ipwnponies" --pretty=tformat: --numstat --no-merges | gawk '
    { add += $1; subs += $2; loc += $1 - $2 }
    END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }
'

# Line count changes before formatting
git log --author="ipwnponies" --pretty=tformat: --numstat --no-merges @~ | gawk '
    { add += $1; subs += $2; loc += $1 - $2 }
    END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }
'
```

I had 32412 lines of code changed, and 46979 afterwards.
This is a 45% increase in LOC changed!
