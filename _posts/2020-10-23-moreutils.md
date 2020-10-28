---
title: moreutils
categories: programming
tags:
  - unix
  - scripting
  - cli
---

`moreutils` is a suite of tools that I feel every unix user should be aware of.
These tools are not essential tools but having them in your toolbox is what can make you 10x.
When you inevitably encounter a situation that these tool solve, you could instead choose to spend a few days rigging
together a bunch of jank tools and coming up with clumsy "good-enough" solution.

[moreutils]: https://joeyh.name/code/moreutils/

As we go through these tools, I'll provide example use cases as well as how one would naively attempt to solve the
problem without them.

**Note**, I'm only going to cover the tools for which I can personally present a compelling use case.

## chronic

`chronic <CMD>` wraps your command and doesn't print output, unless the command fails.
Failure is non-zero exit code.

### chronic - use case

The reason we don't enable verbose logging (besides performance) is that it generates a lot to noise.
This noise serves no purpose when things are hunky-dory.

Only when the command fails, do we care about any output.
And we care about it a lot.

### chronic - what you would do

Without `chronic`, your choices are:

- Enable verbose logging during investigation period, wait for the issue to reproduce, then revert the verbosity.
- Always enable verbose logging, use other tooling to manage noise.

Replicating this tool is trivial for any adhoc command: save the output to a file and `rm log` if it succeeds.
Any more effort and you're reinventing `chronic`.

## ifne

`echo hello world | ifne <CMD>` conditionally runs the wrapped command if stdin is not empty.

### ifne - use case

This is meant to interface to a command that is not programmed to handle empty stdin.
i.e. Run this command only if there's input to run on.
These programs can hang as they wait patiently for input.

Or sometimes the program has expensive startup costs that can be skipped altogether.
i.e. network calls for initialization that will be wasted.

Albeit this class of programs is rare, it's nice that to have this conditional logic piece.

### ifne - what you would do

There aren't a lot of programs like this.
But when you encounter them, you often end up writing a shell script that involves several steps:

1. First command outputs to a intermediate file.
1. Use shell scripting to check status code.
   - If the exit code is 0, then the command passed and likely has output.
     Execute second command, feeding it the input file.
   - If the exit code is non-zero, then the command failed and likely doesn't have output.
     Skip over the next command.
     Don't even invoke it.

So it's not about providing a benefit, it's a way to write more fluid and self-descriptive commands.

## parallel

`echo 1 2 3 | parallel <CMD> {}` is an alternative to `xargs`.
Most people know `xargs` but learning to use it can be a bit of challenge.
`parallel` is an alternative that feels the same to a user but with improved underlying implementation.

Here are some [examples](https://rudism.com/three-ways-to-script-processes-in-parallel/) to illustrate.

I feel like this is one is less useful as it doesn't fell a niche nor greatly improve another program.
Like `grep`/`rg`, `find`/`ag`, and `cat`/`bat`, the improvement is not worth the hassle of learning and deploying
another tool.

**Note**: this is referring to gnu `parallel`, there have been different programs contending for the name.

### parallel - use case

Like `xargs`, you want to execute a command multiple times with different inputs.
For example, find all `.py` files in a repo with `find`, then run the `black` formatter on them individually.

Here are [more details][parallal-vs-xargs] to explain `xargs` vs. `parallel`:

- `parallel` can run N jobs per core, whereas you need to determine the number of processes with `xargs`.
  For adhoc work, this is not a non-issue.
  But for actual parallelization, you can under/over utilize resources when switching between systems.
- `parellel` collates the output so that you can make sense of parallel jobs.
  `xargs` has notes that it's up to the program to handle collation, if using `-P`
- `parallel` can execute parallel commands in order of input (`-k`).
  `xargs` does not have such guarantees, which is a minor annoyance.
  This example, `seq 1 10 | xargs -P5 -I{} fish -c "echo {}"`, will execute 5 processes on my 4-core machine, and it can
  be demonstarted that the execution order is out of sequence.
  This means that `parallel` is maintaining a task queue.

[parallal-vs-xargs]: https://www.gnu.org/software/parallel/parallel_alternatives.html#DIFFERENCES-BETWEEN-xargs-AND-GNU-Parallel

### parallel - what you would do

Run programs in the background with `<CMD> &` and `wait` for all the programs to complete.
The huge con is that you cannot get the status code to know which invocation failed.
And the output is all interweaved, unless you handle file redirection of each invocation.

You can use `xargs -Pn <CMD>`, which will create up to 8 processes.
The output will be interwoven as well.
This is honestly "good-enough" for most use cases.

## pee

Like `tee` but for pipes.
That is, broadcast `stdout` to multiple processes and stdout.

I question the real-world practicality but if I need it, I don't want to have to think of another way to do it.

### pee - use case

If you want to perform different actions on the same input, you want the same input.
This is fine if it's a file on disk.
But if it's intermediary, such as filtered from `grep`, then you need to perform the filtering multiple times.

```sh
cat input | grep 'keyword' | pee 'sed -e s/something/else/ > first_output' 'sed -e s/something/new/ > second_output'
```

### pee - what you would do

Save the intermediary output to disk.
Then it can be passed in to multiple programs.

```sh
cat input | grep 'keyword' > intermediary-input
sed -e s/something/else/ > first_output
sed -e s/something/new/ > second_output
cat intermediary-input
rm intermediary-input
```

This is honestly not so bad.
But I guess it depends on how often you're doing this and how error prone it is to manually manage files.

## sponge

`sponge` allows for reading and writing to the same file, aka an in-place update.
When you use shell redirection to write to a file, the shell will create/truncate the file before beginning the command.
This is problematic if that file is also the source file, as it'll be truncated before it has begun reading.

### sponge - use case

Say you want to search and replace in a file:

```sh
cat source | sed "s/teh/the" > source
```

This truncates `source` before you even start reading.

```sh
cat source | sed "s/teh/the" | sponge source
```

Basically, whenever you want to edit a file in-place.
This command is not that compelling but its use will lead to self-describing code.

### sponge - what you would do

`sponge` is syntactic sugar.
Without it, you would emulate it manually:

1. Redirect output to an intermediary file.
2. Rename when command completes.

You can also use the "in-place" argument that many commands have (e.g. `sed`).

## ts

`ts` adds a timestamp to beginning to each line of a commands outputs.
This is generally very useful and easy to bolt on.
And you can easily filter it out, as the timestamp for all lines follow the same format.

### ts - use case

Most loggers will use a log format that includes the timestamp.
This tool lets retrofit a command that doesn't have this kind of logging output.
Say a script for setting a project, running tests, doing system administration.

For example, you want to rename all jpeg extensions to be consistent (`.jpg`, not `.jpeg`).

```sh
find . -type f -name '*.jpeg' -exec fish -c 'ts mv $1 (string replace ".jpeg" ".jpg")' {} \;
```

Wrapping this with `ts` will give you an audit trail for when the file renames happen.
This can be useful if the command is slow because the disk is slow or there are many files.

### ts - what you would do

If you wanted timestamp logging, you could edit the scripts to print out timestamps as a part of the program output.
Or you could add adhoc `datetime` calls inside your scripts.
While not complete, for adhoc purposes, you're often only interested in a few key timings and this is easy enough.

## vidir

Manipulate filenames with an editor.
It internally tracks and resolves the edited file to automate the `rm` or `mv` commands.

### vidir - use case

If you need to rename many files, using vim can be very handy.
This gives you access to search/replace and other editor commands.

### vidir - what you would do

Use your shell scripting skills.
This usually means you need to use shell substitutions and string manipulation to edit strings, something that shell
scripting is not well-suited for at all.

## vipe

Edit a command's stdout.
This allows for intercepting and modifying before it moves on to next process.

### vipe - use case

When parsing log files, you might only be interested in the timestamps for ERROR lines.
Sure, you could whip up some `awk` or `cut` + `grep`.
But those tools are not interactive and you can't undo/redo changes.

Instead, you can use `vipe` to edit the stream with your EDITOR of choice.
This is just text and your editor is very, very well suited for handling text transformations.
When you're done, save the file and exit.
`vipe` open the file as a temporary file, which it can then feed to the next program in the command.

### vipe - what you would do

Instead of a fluid command, you would:

1. Manually save the input to a file.
1. Edit the file.
1. `cat` the file to the next program in pipe.

This is identical to `vipe` but with a little bit of administration work.

## zrun

`zrun` will detect and replace any compressed file argument with uncompressed file counterpart.

### zrun - use case

Log files are great candidates for compression:

- text-based
- many repeating patterns (WARNING or datetime)
- large

I'm sure it's common to reduce logs to 30% of their original size.
But compressing makes it annoying to use because you need to unzip them first.
`zrun` handles this overhead by parsing the arguments for compressed files and automatically decompressing them to a
temporary file.

### zrun - what you would do

This is basically process substitution:

```sh
cat <(tar xzf foo.gz -O | cat)
```

There are `z*` versions of programs that accept compressed files: `zcat`, `zless`, etc.
The use of those would be more explicit.

## Summary

| Tool     | Description                                                  |
| -------- | ------------------------------------------------------------ |
| chronic  | Runs a command without output. Dump output if command fails. |
| combine  | Combine lines from two files using boolean operations        |
| ifne     | Run a command if stdin is non-empty                          |
| parallel | Alternative to xargs                                         |
| pee      | Broadcast stdin to multiple processes                        |
| sponge   | Read-write to the same file                                  |
| ts       | Append timestamps to stdout                                  |
| vidir    | mv or rename files using an text editor                      |
| vipe     | Edit stdin with EDITOR                                       |
| zrun     | Transparently unzip compressed files                         |

These are some of the many tools in `moreutils`.
How valuable you find each tool depends on your workflow.
These tools are revolutionary and the workarounds are easy enough to come up with.

Their value is that the workarounds can introduce much tedium, such as file redirection management and cleanup.
I personally find `ts`, `sponge`, and `vipe` to be very helpful in my toolbelt.
