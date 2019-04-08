---
title: Cross-compiling to ARM
categories:
- programming
tags:
- compile
- arm
---

I've been trying to make my C.H.I.P. into a headless server, for running scripts.
It's low power and quiet (no fan) so it's a perfect use case.
It's like an IoT device but an actual computer.

# Motivation

## Benefit to Using Precompiled Binaries

Before this, I would usually install prepackaged packages.
It's the most typical use case, I need to install a program on Ubuntu or Windows and for x86 or x64.
I'd take a hunch and say this covers 90% of all installs that the majority of users experience.

Using precompiled, packaged binaries takes all the guesswork out of build configuration options.
One person makes the effort to compile and distribute the binaries.
There's no meaningful work being done with each individual compiling the same source code for the same system architectures.

## Compiling From Source

When you use an OS or architecture combination that is not popular, there may not exist a packaged binary.
You would need to compile from source (and maybe be the first to provide binary!).

Compiling from source is tedious as it requires you to set up a development environment, with the toolchain required to build.
You're basically following the same steps as a developer would.

This is what I did and was successful.
But I quickly found out that these small chips are not powerful enough to quickly compile.
It took me >1 hour to compile `cmake` and >20 minute to compile `fish` shell.

# Why Compiling Code Takes Forever

Compiling a set of source code from scratch can take a long time.
C header files can contain a ton of directives and templates.
And a lot of the macros can be conditional.

Every file that imports the same header, may need to reprocess the header, in case it changes.
For a common header, it can be referenced dozens of times in the include dependency chain of a single object file.

## Optimizations

The use of [precompiled headers] can speed up compilation times.
Just like source code, the headers can be compiled into intermediate files, precompiled headers.
If the headers are static, the existing precompiled header can be used to speed things up.
Many toolchains will include precompiled headers for known libraries.

[precompiled headers]: https://en.wikipedia.org/wiki/Precompiled_header

[Include guards] can be used to prevent recursive includes and minimize needed disk IO.

[include guards]: https://en.wikipedia.org/wiki/Include_guard

# Cross-Compiling

## Installing a Cross-Compiler

Install the `gcc-arm-linux-gnueabihf` compiler.
This compiler will compile down to ARM instruction code, instead of x64 or x86.

## Generate Makefile

Then configure the project to use your compiler.

With autotools:

```sh
 ./configure --build x86_64-pc-linux-gnu --host arm-linux-gnueabihf
```

With cmake:

```sh
cmake -D CMAKE_C_COMPILER=/usr/bin/arm-linux-gnueabihf-gcc -D CMAKE_CXX_COMPILER=/usr/bin/arm-linux-gnueabihf-g++ .
```

<!-- markdownlint-disable MD026 -->

## Profit!

<!-- markdownlint-enable -->

Not really.
I failed real hard at getting anything to compile.
I compiled both `cmake` and `fish shell` natively on C.H.I.P. and want to cross-compile them, to illustrate how much
faster it can be.

At this point, I was hit many roadblocks.
I have a weak understanding of how `cmake` and `autotools` works, so look at the following anecdote from this perspective.

I think that there isn't a set interface for cross-compiling and it's up to each project to build support when they're
setting up `configure` and `CMakeList.txt` files.
This can mean that some projects won't cross-compile, unless you want to manually dive in the build configuration and
fix it to do so.
Even after setting the C and C++ compiler, What I noticed was that some libraries were still being built for x64.
The linker puked when trying to link these libraries with arm libraries.

I gave up at this point.
While it would be good to learn to cross-compile, there's a steep learning curve and lots of terminology and tooling
that's a requisite.

So my adventure in cross-compiling was a crapshoot.
Maybe I'll try this again in the future.
Next time, I'll read more general articles about cross-compiling to raspberry pi.
I would like to confirm my hypothesis that it requires the project to support cross-compiling (no hardcoded architecture
or configurations).
