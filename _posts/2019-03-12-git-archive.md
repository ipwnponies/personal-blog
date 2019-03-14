---
title: Git Archive on SHA
categories:
- programming
tags:
- git
- security
---

What do you do when you want a file in a git repo?
In GitHub, you would view the raw file and save that to disk.
You can clone the repo, get the files you need, and then clean up.

This all sounds real roundabout.
Good thing there's lesser-known `git` commands to help us out.

# Git Archive

`git archive` does exactly what we want.
You give it a repository, a ref, and the paths of the files to get.
The output is dumped to stdout, unless you specify the `--output` option to write to tarball.

```sh
git archive --remote=host.com:repo master fileA fileB | tar xf -
```

`git archive` is basically `wget` for a `git` repository.

# Security

Here's a gotcha: you can't specify a commit ID (sha) with git archive.
The reasoning is actually pretty good in this [stackoverflow post][stack].

[stack]: https://stackoverflow.com/a/26135822

Git repos can have dangling objects that have yet to be garbage collected away.
This includes sensitive secrets that have been removed from the repository proper but still exist on disk.
Normally, you're only able to interact with the remote through clone or fetch (git receive-pack) which only "knows
about" non-dangling objects.
Git archive could have bypassed this interface, if shas were allowed.

The workaround is to give that commit a tag, which probably makes sense for most use cases.
i.e. You want to get a few files for a particular release or branch, not an arbitrary commit.
If you truly wanted an arbitrary commit, clone the repo then.
