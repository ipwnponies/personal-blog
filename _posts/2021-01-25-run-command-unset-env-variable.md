---
title: Running Commands With Environment Variable
categories: programming
tags:
  - shell scripting
---

Environment variables are essentially global variables, when it comes to the shell.
In spawned child processes, environment variables are not propagated by default unless you `export` them.

This scoping is common in many programming languages.
Exporting an environment variable would be like referencing a `nonlocal` variable in `Python`:
you can access a variable from higher up in the process hierarchy.
However, existing processes are unaffected, including those that share a common process ancestry.

## Running A Command With An Env Var

There are a few ways to run a command with a set environment variable:

```sh
# bash syntax
FOO=1 command

# Using subshell scoping
(FOO=1; command)

# Using env command, which behaves like a subshell
env FOO=1 command
```

The `bash` syntax is the fastest as it doesn't involve a subshell invocation.
`fish` 3.0 shell recently introduce this, due to popular request.

Using `bash` subshell allows you to mutate a new, temporary environment.
It is thrown away so you can use `set -x` to set a value.
This subshell syntax is bash-only, the fish shell does not have this syntactic sugar.

The `env` command know show to interpret the env var syntax.
Since it's a command, it is shell-agnostic.
In fact, this is how you set env var for the `fish` shell.
This isn't useful for `bash`, since it's functionally equivalent but involves a subprocess invocation.

## Running A Command Without An Env Var

This is an extremely rare occurrence.
I've only needed to do this once, in the 12+ years I've worked with shell scripts.
If you need the absence of a variable, the shell script can be improved to understand a null sentinel value.
If your environment is setting this variable needlessly, you should fix the environment inheritance.

However, if you find yourself in this situation, we can use `env`.
Basically, you want to create a subshell, `unset` the variable, then run the command.
`env -u` allows this, just like it allows for setting a variable in the first place.
