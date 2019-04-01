---
title: Python on Windows
categories:
- programming
tags:
- python
- windows
---

Normally, all my programming work is done in a unix environment.
All my tools and knowledge is heavily centered in the unix/ubuntu world.
Even on a Windows machine, I'm still using Windows Subsystem for Linux (WSL).

Sometimes I work on OSX, which is BSD-based.
The only issues I have are BSD commands that masquerade but are entirely different beasts than gnu counter-parts.
I have decided that it's simplest to install the gnu variants (sed, time, ps) through HomeBrew and not have to think
about it.

But today, we're going to talk about native Windows.
I had to test a python script and see how it behaved in a windows environment, to know what limitations of support we
could declare.

# Virtualenvs

So the first thing I do is create a virtualenv and install the requirements.
I figured that there may be some libraries that have binaries for Windows and I would need to install those for it to
work outside of WSL.

```cmd
python.exe -m virtualenv windows_venv

ls .\windows_venv\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       2018-08-30     21:58                Include
d-----       2019-03-31     02:05                Lib
d-----       2019-03-31     02:05                lib
d-----       2019-03-31     02:06                Scripts
-a----       2018-06-27     04:11          30189 LICENSE.txt

```

Woah, wut?
There's two "lib" directories.
That's weird, I thought Windows was case-insensitive.

Why yes, it is. And yes, it doesn't handle this well at all.

# Fix

The [fix] looks odd and silly but it's a workaround to restore the invariant that is now "varianting".

[fix]: https://stackoverflow.com/a/54297075

```cmd
move .\windows_venv\Lib rmthis
move .\rmthis\site-packages\ .\windows_venv\lib
rmdir rmthis
fsutil.exe file setCaseSensitiveInfo .\windows_venv\ disable
```

First you make the directories unique once more.
Otherwise the `move` operations get super-confused at why you are moving a file into the same destination.
The contents of the two directories are merged back in.
Then case-sensitivity option is disabled on the venv dir.
