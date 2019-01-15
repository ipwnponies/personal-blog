# Introduction
Neovim was taking a long time to start up but only on my laptop.
Like 2 seconds long.
This didn't happen on a shared aws dev box, which led me to thinking this was maybe hardware
or OS filesystem caching issue.
Here's what I did to debug and get to the bottom of the mystery.

# Profiling vim
The first step was to sanity check how slow this was.
```
time nvim -c quit
        2.30 real         1.21 user         0.79 sys
```
The user time is 1.2 seconds.
Wow, that's pretty slow startup time.

Let's profile `neovim` itself to see if this is caused by a slow plugin.
This can be done with the `--startuptime` argument, which outputs profiling timings:
```
vim --startuptime output.log
cat output.log

times in msec
 clock   self+sourced   self:  sourced script
 clock   elapsed:              other lines

000.011  000.011: --- NVIM STARTING ---
001.012  001.000: locale set
001.795  000.783: inits 1
001.816  000.021: window checked
002.033  000.217: parsing arguments
002.418  000.385: expanding arguments
002.569  000.151: inits 2
003.064  000.495: init highlight
005.683  001.906  001.906: sourcing /Users/jngu/.config/nvim/autoload/plug.vim
020.847  003.326  003.326: sourcing /Users/jngu/.vim/bundle/vim-polyglot/ftdetect/polyglot.vim
021.343  000.041  000.041: sourcing /Users/jngu/.vim/bundle/vim-polyglot/after/ftdetect/rspec.vim
021.436  010.796  007.430: sourcing /usr/local/Cellar/neovim/0.3.1/share/nvim/runtime/filetype.vim
...
<truncated>
...
2042.010  000.131  000.131: sourcing /Users/jngu/.vim/bundle/vim-airline/autoload/airline/init.vim
2042.872  001.226  001.096: sourcing /Users/jngu/.vim/bundle/vim-airline/autoload/airline/section.vim
2043.112  2039.617  2019.833: sourcing /Users/jngu/.config/nvim/init.vim
2043.148  000.467: sourcing vimrc file(s)
...
<truncated>
...
2199.493  000.381  000.381: sourcing /Users/jngu/.vim/bundle/vim-gitgutter/autoload/gitgutter/hunk.vim
2200.435  019.790: first screen update
2200.437  000.002: --- NVIM STARTED ---
```
The first column shows the elasped time (from start) and the second column shows the incremental time.
Sourcing my `init.vim` takes 2.04 seconds, out of the total running time of 2.20 seconds.

# Debugging vimrc
The next step is narrow down what in my `init.vim` is causing the slowness.
It's possible I have too much crap in my vimrc and it's taking forever to load on a cold cache.

Vim has some profiling functions for plugin authors to use:
```vim
:profile start debug_vimrc.log
:profile! file */<plugin>/*
```
This can be used to dive deeper into a specific plugin's behaviour to a great granularity.

But in my case, I found the issue by _binary-search-and-comment-out_ my vimrc.
And narrowed it down to these lines:
```vim
   if has('nvim') && has('ttyin') && has('ttyout')
       if exists("$VIRTUAL_ENV")
           " Skip the activated virtualenv, which probably doesn't have neovim package
           let g:python3_host_prog = system("type -ap python3 | head -n2 | tail -n1")[:-2]
           let g:python_host_prog = system("type -ap python2 | head -n2 | tail -n1")[:-2]
       else
           let g:python3_host_prog = system("command -v python3")[:-2]
           let g:python_host_prog = system("command -v python2")[:-2]
       endif
   endif
```
This snippet is used for selecting the python virtualenv that has `neovim` package installed.
It uses `system()`, which runs a command in a new subshell.

Hmm... that can't be the problem, right? Let's test it.
```
time fish -c exit
        1.03 real         0.52 user         0.36 sys
```
Huh, that's 0.5 seconds to spawn a new shell and we're calling it twice here.

# Debugging Fish startup
`fish` has the debug flag `-d`, which prints debugging trace to `stderr`.
There several levels of debug verbosity so I iterated through it incrementally, to avoid reading through noisy logs.
```fish
fish -d 3 -c exit 2>&1 | ts -i '%.S' | sort -n -k 1
```
This will spawn a `fish` shell and immediately exit, print debug information to `stdout` (instead of `stderr`).
The output goes to `ts` from `moreutils`, which appends a timestamp to every line.
Then we sort it by the duration.

```
<truncated>
...
00.000225 <3> fish: Created job 3 from command 'status --is-interactive' with pgrp -2
00.000397 <2> fish: determine_config_directory_paths() results:
00.990492 <3> fish: Created job 5 from command 'set PATH (brew --prefix coreutils)/libexec/gnubin $PATH' with pgrp -2
```

# The Fix
So it seems the command `set PATH (brew --prefix coreutils)/libexec/gnubin $PATH` is the culprit.
More precisely, the call to `brew --prefix coreutils` via command substitution.
```
time brew --prefix coreutils
        1.42 real         0.55 user         0.41 sys
```
The entire cost of creating a new subshell was on this `brew` call.
Since the brew installation path doesn't change often, the workaround is to statically hardcoded the path.
This is much prefered to paying the cost of subshell startup.
```fish
set PATH /usr/local/opt/coreutils/libexec/gnubin $PATH
```

And with that small change, we've fix shell and `nvim` start up times.
```
time nvim -c quit
        0.30 real         0.18 user         0.06 sys
```
