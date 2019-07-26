---
title: "Building a NES Emulator - Part 1"
categories:
- programming
- building a nes emulator
tags:
- python
- hardware
---

For hackathon, I decided to start up my life-long dream project of writing a NES emulator.
I studied computer engineering in school and the material is not exactly foreign to me.
However, I decided to lean in the software engineering side of things in my career.

I hope this project can be a relearning opportunity for me.
During school, I studied and rote-memorized the material to pass the class.
With a practical and interesting problem on-hand, let's see if I can apply myself to the academic material.

Throughout these blog series, I'm going to speak from the perspective of software/application developer trying to grok
this out as well.
I'll try to explain concepts that are entirely foreign to software developers.
Or at least give a refresher so you don't have to go back to those digital logic text books they made you buy in school.

# Why NES

The NES system has been well-documented by this point in time.
And there exists plenty of prior art, in every programming language, that I can rely on for better understanding.

# Programming Language

I'm going to use Python, the language I'm most familiar with.
I already have the development environment and tooling.
Performance is literally not going to be an issue, modern-day CPUs operate 1000s of times faster.

# Plan of Attack

The first step is to ignore the NES itself and emulate its CPU.
This is not custom hardware but the 6502, which is well-documented and easy to find reference documentation.

It was a strange realization that "emulating the NES" is equivalent to saying "emulating a macbook pro system" (e.g.
intel CPU, VGA, touchbar, etc.).
In this example, in the far future, maybe we want to emulate some touchbar games (lol) and that hardware + API have
long been deprecated.
Following this example, the first thing you want to do is ignore all other hardware and implement a x86 processor.

# Resources

The reference manual at [obelisk][1] was mentioned several times and it's a pretty clean layout.

[1]: http://obelisk.me.uk/6502/reference.html

The other page I'm using is [nesdev.com][2], which outlines the architecture of the system, as well as refresher on CPU
instruction topics.

[2]: https://nesdev.com/6502.txt

# Architecture Overview

## Registers

The 6502 has several 8-bit registers:

Register | Description
--|--
accumulator | Typically the target for "results" of operations
X index | Typically where operands ("params") are found
Y index | Similar to X but some operations exclusively use X and/or Y for different purposes
status | Bit flag with "metadata" for results of instructions
program counter | Offset to where the current execution is
stack pointer | Memory reference to the top of the stack

## Memory and Addressing

The memory bus is 16-bit, which means that it's capable of addressing up to 2^16 (65 KB) of memory.

There are 11 modes, describing how an instruction expects to get operands:

Mode | Description
--|--
Immediate | Literal values. In assembly, this is denoted with "#" prefix.
Absolute | Memory address where value is stored
Implied | No addresses needed for the instruction, instruction implies the operand. i.e. LDX loads from x register
Accumulator | No address, instruction will use accumulator register value
Indexed | Address relative to X/Y index
Indirect | Use for `JMP`, which requires 16-bit memory address. This is like absolute addressing but reads 2 bytes
Relative | Branch on condition

I'll admit, I got real bored reading this. So maybe expect this to be refined if I find errors in the future.

### Zero-page

Some of the addressing modes come with "zero-page" variants.
Memory addresses are 16-bit while the registers are processor bus is 8-bits.
It requires 2 cycles to fetch the full address.

Zero-page is an optimization that assume the most significant byte (MSB) of address is hard-coded to `0x00`.
Thus, you can reduce the time to get address to 1 cycle, 50% of original cost.
This scheme would probably be found on other processors that have mismatched word sizes for registers and memory addressing.
But those processors are probably less common.

This is very similar to variable-width Unicode (utf8/utf16), where there's cleverness for optimization purposes.
At the expense of wondering wtf is all this magic.

# Bit Operations

The first hurdle I encountered was differentiating between the `carry` and `overflow` flags.
I found this [article][3] that breaks it down very well.

[3]: http://www.righto.com/2012/12/the-6502-overflow-flag-explained.html

But I'll give you a TLDR so you can get on with your days.

## Carry vs. Overflow

Carry is used for overflow when adding unsigned integer, overflow is used for overflow when adding signed integers.
They're the same conceptually but separately implemented because **signed and unsigned arithmetic** are done with the
same operation.

They're represent different metadata for interpreting the result differently.
When you add `0x0110` and `0x1100`, the output is `0x0010`, with the `overflow=0` and `carry=1`.

Note that there is no concept of signed or unsigned integers, that's a higher-level concept: these are just bits.
It's up to the program to interpret the status flags correctly, depending on whether they wanted  as signed or unsigned arithmetic:

- If intended as signed, this is `6-4=2`, with no overflow. i.e. `assert add(6, -4) == 2 and not overflow`
- If intended as unsigned, this is `6+12=4`, with carry (worth 16). i.e. `assert add(6, 12) == 4 and carry`

The hardware operations of bitwise addition are identical, the interpretation of parameters and result are different.
It took me awhile to rack my brain around this because my brain was thinking from top-down in the abstraction stack.
At higher-level, these are two separate methods that do two separate things.
At hardware-level, these might end up looking identical and it's the interpretation of the results that matters.

## Python Bitwise-Operators

I had to brush up on my python operators a bit.

- `&` for logical `AND`, which is useful checking values of bits within an integer.
  This is how you work with bit flags, by bit-masking for target flag
- `|` for logical `OR`, which is useful for setting bit values.
  This is used for setting bit flag, without clobbering other values
- `^` for logical `XOR`. This is not used as often but it's important to recognize when you need it, for convenience.
- `bytearray` to create a mutable sequence of bytes. This is used for emulating memory space.
- `bytestring`, which are used for immutable sequence of bytes. This would be used to represent the contents of a ROM
- bytes are actually `int` and can use bitwise operators on them
- Integer literals can be specified in hex, octal, or binary formats with `0x11`, `0o21`, `0b00010001`
- Literal bytestrings can be created using `b'\x00'`.
  `\xXX` and `\000` is how you can use hex or octal string format, instead of trying memorize the decimal representation
- `ord('a') == 97` converts a single character to its Unicode value
- `int('111', 2) == 5` converts a string to base 2
- `bin(5) == '0b111'` converts an int to binary representation. A reverse of `int()`. Same with `hex()`.
