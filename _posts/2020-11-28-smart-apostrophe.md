---
title: Smart Apostrophe
categories: technology
tags:
  - font
  - unicode
---

[Smart apostrophes/curved quotes][wiki] are... interesting.
There are over [30 characters][code point table] that are considered quotation marks in Unicode.
The most well-known are the quotation mark (_"_, \&quot;) and apostrophe (_'_, \&apos;).
These are the characters available in ASCII.

[wiki]: https://en.wikipedia.org/wiki/Quotation_mark#Curved_quotes_within_and_across_applications
[code point table]: https://en.wikipedia.org/wiki/Quotation_mark#unicode_quote_table

## Word Processors

Word processors have been transforming the quotation mark into their respective stylized unicode characters for presentation.
For example, when you wrap a word with quotes, most word processors will do all the smarts necessary to determine that
you intend to surround with open and close quotes, respectively.
As a user, I appreciate that I don't have to differentiate, as the use case is consistent and it seems unnecessarily
pedantic to require the user to do so manually.
But I can see why typographers would be less than ecstatic about magic handling or misconceptions resulting not
understanding these are distinct characters.

## Applescript

This bit me when writing a script in [Applescript][applescript].
Applescript uses curly quotes for string literals.
It makes the least amount of sense, even typographers would probably agree that this is not the starting place they
would choose, for a hill to die on.
It's literally for the scripting language, it doesn't even need to be smart quotes.
We just need delimiters for string literals and, by convention, we chose double quotes.

[applescript]: ./2019-02-15-applescript.md#os-menulet
