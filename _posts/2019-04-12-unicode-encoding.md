---
title: Unicode Encodings
categories:
- programming
tags:
- localization
---

[Unicode] is an industry standard for representing text in many languages.
Before unicode, [ASCII] was typically used to encode text into bits.

# Encodings

What is encoding and why do we need it?
Abstract concepts like characters need to be translated to real-world, physical things.
For text, this means mapping characters to a bits.
While this is arbitrary, it's consistent and standards exist.
This is what allows programs to write text files that can be read by another program.

[Unicode]: https://en.wikipedia.org/wiki/Unicode
[ASCII]: https://en.wikipedia.org/wiki/ASCII

A simple, ELI5 example:

    A => 00, B => 01, etc.
    ABBA => 00010100

# Unicode

As the internet connected more peoples of the world, ASCII was insufficient to represent non-latin based languages.
Unicode was an encoding that allowed for more than 128 characters (7-bit ASCII).

It's designed to be extensible, so that new characters can be continue to be added to it.
We've already seen this in action, with emojis becoming unicode characters.
Try explaining what that is to someone 27 years ago (1991) and why it deserves to be a character encoded into a
universal character set.

# UTF-8, UTF-16, UTF-32

These are the implementation of Unicode.
This is important to remember, they are different implementations with trade-offs but all share the same end-goal of
being able to encode unicode characters.

The number doesn't denote any hierarchy or size limitations.

See this [StackOverflow] answer for more details.

[StackOverflow]: https://stackoverflow.com/a/496374

## UTF-8

UTF-8 uses 1-4 bytes and is variable width.
It's directly compatible with ASCII.
A file containing only ASCII characters should (in theory) be encoded the same for both ASCII and UTF-8.
Therefore it is also small and compact.

If you need to use non-ASCII characters, then UTF-8 might represent it in 2-4 bytes.
Due to the backwards compatibility with ASCII, much of the lower bytes cannot be used, so more bytes will be used to
represent characters.

This is the most common encoding, by far.
It's because the prevalence of latin-based languages (English) on the internet that allows optimizing for this case;
the more unicode that is ASCII, the more efficient the UTF-8 is in size.

## UTF-16

UTF-16 uses 2-4 bytes.
By encoding a minimum of 2 bytes, it can represent 65k characters, which likely covers 99% of current languages in-use.
If needed, additional bytes can e used.

Think of this as ASCII with a little bit more wiggle room than 128 characters.

This is the default encoding on Windows machines.

## UTF-32

UTF-32 use 4 bytes and is fixed-width.
This makes it easy to do string manipulation.

The disadvantage is that every character is exactly 4 bytes and text is bloated.

This is seldom used.
