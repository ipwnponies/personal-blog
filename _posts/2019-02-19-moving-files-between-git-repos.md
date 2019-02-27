---
title: Migrating files from one git repo to another
category:
  - programming
tag:
  - git
---

# Problem

When I first started writing greasemonkey scripts, I just checked them into my dotfiles because I didn't want to bother
creating a new repo to house them.
I've finally decided they need their own repo and history.
And it will be cleaner for users to install the scripts (imagine if I told you to install scripts from my dotfiles!?)
Now we need to figure out how to migrate them over properly.

# Why Not Just Copy

The most direct and naive solution is to simply `cp` the files over and call it a day.
But this would forfeit all the valuable history for these files.
I've already made use of the history when I implemented a feature, reverted, and then forgot I did it the first when I
tried implementing it a second time.
Fear not, git has a way to do anything.

The proper way to handle this is to get a file's complete history as a set of patches.
Then apply these patches to the new repo as independent commits.
Since the author date is metadata that is preserved, it will appear as if I made these commits way in the past,
even before the repo came into existence.
Such is the magic of git.

# How To

I followed the steps from this [stackoverflow post](https://stackoverflow.com/a/11426261):

## First Step, Collecting the Commits

```sh
git log --pretty=email --patch-with-stat --reverse --full-index --binary -- path/to/file_or_folder > patch
```

`git log` is used to show git history.
You can specify multiple files.

`--pretty=email` sets the format to an email patch format that can be consumed by `git am`.

`--patch-with-stat` is used to output the patch, with file system information.
File system information includes the permission changes, symlinks, owners, etc.

`--reverse` will output the commits patch file in ascending chronological order.
By default, git log outputs results in reverse chronological order because the most common use case for SCM is to view
recent changes first.

`--full-index` lists the full file names, not just the shortened name. I really don't know if this matters 100%.

`--binary` outputs patch information for binary files. `git log` will skip outputting binary files in the patch.

## Second Step, Applying the Patch to the New Repo

```sh
git am --committer-date-is-author-date <patch
```

This command is `git apply` but works on a series of patches.
`am` stands for "apply mail".

When `--committer-date-is-author-date` is set, the commit date will be set to the commit's author date.
By default, git would set the commit date to the current datetime,
since you're basically just creating new git commits in the new repo.

The author date is intended for house keeping, to preserve information such as when the original author wrote the
code vs. when the repo owner merged the pull request into master (via squash or rebase).
It's possible for PRs to be merged months or years later and knowing the real date vs. what the intent was when originally
written provides much useful context.
This information is not preserved because git uses the commit time as part of the SHA generation.
It's important to note that you lose this bit of metadata information in the migration process.