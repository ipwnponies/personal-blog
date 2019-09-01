---
title: Windows Terminal
categories:
- programming
tags:
- terminal
- windows
---

Microsoft is working on a [better terminal][1], which will improve the WSL experience.
It's available if you install the Windows 10 May 1903 update.
This update is not deployed by default and can be obtained by going to Windows Update and opting in.

[1]: https://github.com/microsoft/terminal

So far, it's been pretty solid.
I don't think I have a strong opinion regarding terminals.
Or that I ask too much of one.
But all the existing solutions (cmd.exe, wsltty, conemu) have kinda sucked in different ways.

All I ask is for a terminal that can display powerline, can scale the display dynamically and accurately, and doesn't
scroll like ass.
I don't program terminal emulators so maybe these requirements are actually big asks.
But as a user, they seem like reasonable and minimal acceptance criteria.

Oh well, let's move on to how to configure `Windows Terminal`.

# profiles.json

Configurations are stored in `profiles.json`, in roaming app data (syncs across devices).

**Protip**: Editing the settings opens in `notepad` by default (that might just be because it's my default app for
.json files).
You can find the file by viewing recent files in *File Explorer* and opening it with your editor of choice.

The following snippet are notable keys to change:

```json
{
    ...
    "commandline" : "wsl.exe -d Legacy",
    "fontFace" : "Ubuntu Mono",
    "startingDirectory" : "\\\\wsl$\\Legacy\\home\\ipwnponies",
    ...
},
```

## `commandline`

`commandline` doesn't seem to take arguments well, from my experience.
I attempted to launch `fish` through `wsl/bash` via `wsl.exe ~ -d Legacy /usr/bin/fish` but that was no go.

Turns out I've been rolling a 2-year old hacky workaround, launching `wsl.exe` with `bash -c '/usr/bin/fish'` as the command.
This was a `WSL` limitation that restricted the shell to `bash`.
Well, that was [fixed long ago][2] and now we can properly `chsh` to the `fish` shell.

[2]: https://github.com/Microsoft/WSL/issues/2199#issuecomment-307430802

## `fontFace`

I changed the font `Consolas` to my preferred font of `Ubuntu Mono`.
More specifically, the *powerline*-patched variant.
And this is where I ran into my first bug, caused by [fonts with long names][3].

[3]: https://github.com/microsoft/terminal/issues/602

There's a 32 character limit and terminal will crash while trying to load the font.
This is annoying for me because I use `Powerline` fonts, specifically [*Ubuntu Mono derivative Powerline*][4].
Without powerline fonts, my powerline-enabled `fish` shell looks like garbage, with blocks and random characters.

[4]: https://github.com/powerline/fonts/tree/master/UbuntuMono

## `startingDirectory`

The default starting directory is `%USERPROFILE%` (`/c/Users/ipwnponies/`) but we want to use `/home/ipwnponies`.

The `Windows Terminal` only accepts windows paths and is not `wsl`-aware.
We will need to use the `wsl` network share `\\wsl$\`.
This share holds the mounts to all the distributions that are installed.

# Impressions

My initial impression is pretty good. It has the following advantages over its competitors:

- Configurable with json, instead of of unintuitive gui like `conemu`
- Drawing fonts with aliasing, unlike `cmd.exe`
- Tabbed windows, unlike `wsltty`

I'll keep playing with it but I'm hoping it becomes a high quality terminal for `WSL`, akin to `iTerm2` on `OSX`.
