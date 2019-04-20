---
title: PyPy and JIT Compiling
categories:
- programming
tags:
- python
- compiler
- optimization
---

I've been hearing about `PyPy` for a while now and how it's 8-17 times faster than `CPython`.
I finally sat down and spent some time to read up on this.

# What is PyPy

The default and most common interpreter is `CPython`. It's the one that's shipped with python installations.
It's called "C" because it's written in `C`.
Very badly named but it is what it is.

`PyPY` is a alternative python interpreter.
It, too, is named because of the language it's written in, `Python`.

It's a popular alternative interpreter that's started development to solve the performance issues with data science
libraries, like `matplotlib` and `numpy`.

# How Can It Be Faster Than CPython

## Language the Compiler is Written in Doesn't Matter

`CPython` is written in `C`, then compiled to machine-code.
The machine code executable then runs and interprets the python source code.

`PyPy` is written `Python` (not actually but close enough for our discussion) and produces a machine-code executable.
The executable then runs and interprets the source code.

Do you see a difference?
The language the compiler is written in doesn't matter because the compiler is the product.
Sure, it might take you a minute to compile `CPython` and 10 minutes for `PyPy` but that doesn't matter during runtime.

## Runtime Differences

The difference in performance comes during runtime.
`CPython` reads python source and produces byte code.
This is just a form that's more easily parsed by the runtime.
Code is parsed into an Abstract Syntax Tree, functions are references, constants can be inlined, etc.
It's a very light layer of processing.
After this, the source code is interpreted as the user executes programs.

`PyPy` also produces byte code.
The difference is a Just-In-Time (JIT) compiler.
During runtime, it's continually analyzing access patterns and optimizing.
Maybe there's a conditional that's always being called and can be speed up with inlining,
to reduce accesses (I don't really know compiler theory, bear with me).
The gist is that it's using source code + runtime data to determine optimizations.
