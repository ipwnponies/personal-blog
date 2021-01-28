---
title: Finding Hard Or Soft Symlinks
categories: programming
tags:
  - unix
  - shell scripting
---

When you have a symlink, it's trivial to use `ls` or `realink` to resolve what files it points to.
When you have a hardlink, you don't even need resolution.

What happens if you have a canonical source file and you're trying to find who references it?
Turns out it's not so simple.
You have to use `find` to scour the filesystem and do file node comparison.

```sh
find -L /search-dir/ -samefile /dir/target-file
```

The use case that I encountered was with `brew` and finding out if `fish` shell completions were installed.
The `brew` formulae installs files in the brew location and uses symlinks to install it onto the system.
I was debugging why I was missing `docker-compose` completions and trying to diagnose if it was not part of
installation steps.
