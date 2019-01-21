---
title: stdio Buffering
---
# What is line buffering
Programs can choose to buffer IO for performance.
Reading/writing large chunks at once is more efficient than reading/writing single characters.
For interactive input, it's often desirable to remove line buffering, so that data can stream in realtime.
Many programs will change line buffering behaviour, depending on whether the input or output is interactive (tty).

But sometimes, programs are not written well.
So we want a solution to avoid line-buffering.

# stdbuf
`stdbuf` comes standard on linux systems.
it allows modifying the input/output stream buffering behaviour.

The following example has a program generating infinite output, piped to `grep` (further piped to `cat` to force grep
into non-tty mode).
Note that `grep` has `--line-buffered` argument for enabling line buffering, instead of block-buffering.
```fish
fish -c 'while echo hi; sleep 0.5; end' | grep -Pi --color=auto 'hi' | cat
fish -c 'while echo hi; sleep 0.5; end' | stdbuf -output=0 grep -Pi --color=auto 'hi' | cat
```

The first command will hang and buffer, which will make it seems like the `grep` command isn't finding anything.
When `ctrl-c`, `stdout` is flushed and all the results are dumped on the screen.

The second command uses `stdbuf` with output set to unbuffered, which will print the output immediately.
The buffering amount can also be manually set to a value of how many bytes to output.

# Alternatives
`unbuffer` is a tool that wraps `expect`.
`expect` creates a pseudo-tty that it uses to watch for prompts and automate macros via stdin.
`unbuffer` is specific use-case of `expect`, where there are no rules to match and react, it's only used to set up the
psuedo-tty.
This tricks the pipeline into line-buffering mode.
