---
title: "Building a NES Emulator - Part 2"
categories:
- programming
- building a nes emulator
tags:
- python
- hardware
- math
---

This [article][1] helped to illustrate the understanding I've put into this article.

[1]: www.righto.com/2012/12/the-6502-overflow-flag-explained.html

# Signed Number Representations

In working on this emulator, I've finally began to understand the purpose of 1's and 2's complements.
They are both number systems used to represent negative numbers with bits.

## Ones-Complement

1's complement is simply flipping all the bits.
In hardware, this is very easy to do with an XOR operation.

## Twos-Complement

2's complement is 1's complement + 1.
2's complement is very useful because it allows for subtraction using the exact same bitwise adding operations.
Like arithmetics, you can "add" negative numbers, instead of implementing an independent and separate subtraction operator.
All that changes is how you choose to interpret the results.

```text
0x0F + 0x90 = 0x9F  # Bitwise operation
15 + 144 = 159      # Unsigned addition
15 + (-97) = (-82)  # 2's complement
```

This bears repeating:
the bitwise operations are **literally the same**, it's the interpretation (2's complement) that changes the values.

I'll repeat that again:
the adding operation is literally the same for addition (with unsigned values) as it is with subtraction (with 2's complement).

### How It Works

The example above makes it seems like sorcery but it's quite mundane explanation for how this works.
Some key observations:

- 2's complement is an arbitrary system. There's no mathematic bearing or law of nature that brought it to existence.
- Due to bit width and wrap around, you can add the max unsignd value and it will overflow back to the same value.
  i.e. For 8-bits, adding 256 to any number will result in the same number. Think of this like musical octave.

```text
M - N
M - N + 256                 # Adding 256 (octave) doesn't change the value
M + (-N + 256)              # Algebra rearranging
M + 2's complement of N     # Oh hey, we're back to regular addition, if we "reinterpret" the meaning of -N == (256 - N)
```

This is the example that made it all click for me.
2's complement wasn't randomly discovered by stroke of genius.
It was chosen by definition because it substituted subtraction of two positive numbers and replaced it with addition of
2's complement (addition of a negative number).

So there's no magic here, it was deliberately chosen so that we can use addition for subtraction, as long as we
interpret negative numbers using 2's complement.

# Overflow

Overflow and Carry flags on the 6502 was unnecessarily confusing.
But this was because I was not thinking like a hardware engineer.
They are the same exact same concept but for signed and unsigned addition, respectively.
If you're doing **signed addition**, only the **overflow** flag is relevant.
If you're using **unsigned addition**, only the **carry** flag is useful.

The reason for two separate flags is that the 6502 uses the same physical logic gates for addition instruction.
Whether you're trying to do signed or unsigned addition is irrelevant, they're implemented by the same hardware.
What changes is which flag you should be looking at to interpret your results.
Adding an additional, redundant-ish status flag is the trade-off between adding a separate hardware component for signed
vs. unsigned addition.

I want to highlight this again: **only one** of overflow or carry flags are useful at any one time and it depends on
whether you intended for signed or unsigned operation.
