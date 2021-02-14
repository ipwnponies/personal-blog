---
title: Bracketed Paste Mode
categories: programming
tags:
  - unix
---

[Bracketed Paste Mode][1] is a feature of terminals, which is used for signalling extra information to programs.
By adding markers to wrap the text payload, a program can identify that an incoming series of characters is through a
"paste" action and not key input.

[1]: https://cirw.in/blog/bracketed-paste

## How Does It Work

[ANSI escape codes][ansi] are used to delimit pasted text.
The start marker is `\e[200~` and the end marker is `\e[201~`.
The use of ANSI escape codes is similarly used to embed formatting information, such as colour or font styling.
It's almost like stenography.

[ansi]: https://en.wikipedia.org/wiki/ANSI_escape_code

When the user executes a paste action, the terminal is the program that reacts to perform the action.
It knows that a "paste" command was invoked and to wrap the clipboard contents with the escape codes.
This new payload is forwarded to the program.

[xterm] started this and many terminals are beginning to support this.
ITerm2 has a setting that must be enabled.

[xterm]: http://www.xfree86.org/current/ctlseqs.html#Bracketed%20Paste%20Mode

## Program Support

If the terminal supports this mode, it will insert these escape codes.
How the program wishes to use the payload is up to it.
If it's not supported, you might see the raw codes.

If supported, the program will use this as a signal that the input was non-interactive.
This knowledge allows it to behave differently, like how processes might change behaviour for non-tty input.
Examples include consuming the payload in batch, instead of key-by-key.

Neovim supports this by default.
It automatically toggles the `paste` setting before inserting the content.
`paste` disables auto-indentation and other plugin rules.
This is faster and preserves formatting.
It leaves `paste` mode after the paste is completed.

`fish` shell supports this.
This is "safe paste" mode, where newlines are preserved with `fish`'s multiline mode.
Normally receiving a newline from the terminal is ambiguous and taken to be the same as return key.
This causes multiline paste to execute line by line.
Multiline mode is great for safe behaviour and avoids executing invalid shell commands, like a paste of English text.

## Summary

Bracketed paste is great.
But it feels like a workaround, because there's only one channel to send information (stdout).
Unix programs are very opaque in this regard.
This makes it hard for a terminal to convey when it is simply forwarding user key input or when it wants to send
it's own data.
ANSI escape codes feel largely like a hack as well.
But the constraint means that you don't have tight coupling and we're able to use any terminal or program we'd like.
