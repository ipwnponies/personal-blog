---
title: Profiling Vim Plugins
categories: programming
tags:
  - vim
  - profiling
---

I [previously posted][1] about profiling vim performance during startup.
This was useful for debugging what changes in `.vimrc` was expensive.

[1]: 2019-01-14-profiling-vim-and-fish.md

More generally, you might want to figure out which plugin is causing performance issues.
And because plugins can have adverse interactions with one another, it's not as straightforward as to add debugging in
one place.

## Profile

vim has `:profile` command, which works like a logging library.

```vim
:profile start profile.log
:profile func *
<Perform action>
:profile stop
```

This lets you dump logs to a file.
And you can use `:profile func <PATTERN>` or `:profile file <PATTERN>` to register what scripts or function names get logged.

## Log Output

```ignore
FUNCTION  airline#extensions#get_loaded_extensions()
    Defined: ~/.config/nvim/bundle/vim-airline/autoload/airline/extensions.vim line 499
Called 14 times
Total time:   0.000132
 Self time:   0.000132

count  total (s)   self (s)
   14              0.000115   return s:loaded_ext

FUNCTIONS SORTED ON TOTAL TIME
count  total (s)   self (s)  function
   17   0.369711   0.007703  airline#check_mode()
    4   0.354932   0.040761  airline#highlighter#highlight()
  212   0.225391   0.046164  airline#highlighter#exec()
  340   0.200307   0.082925  airline#highlighter#get_highlight()
...

FUNCTIONS SORTED ON SELF TIME
count  total (s)   self (s)  function
...
  340   0.200307   0.082925  airline#highlighter#get_highlight()
  212   0.225391   0.046164  airline#highlighter#exec()
    4   0.354932   0.040761  airline#highlighter#highlight()
...
```

Each function is listed and it's individual statistics are shown.
This gives you a sense of how much a plugin contributes to overall performance.

The bottom 2 sections show the total time.
The first is a list of functions in chronological ordering (total time).
This is helpful to get a sense of sequencing.
The second section shows the time a function spends.
This is useful for identify functions that are expensive.
Together, these two give you a pretty good idea to identify which is the baddie of the bunch.
