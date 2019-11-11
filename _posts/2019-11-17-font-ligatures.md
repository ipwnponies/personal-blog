---
title: Font Ligatures
categories:
- programming
tags:
- font
- editor
---

Font ligatures are a typography concept, where adjacent characters can be interpreted as a different glyph altogether.
A common example in handwriting is `>=`.

## Kerning

Kerning is used to manipulate the spacing between characters for a proportional font.
A good example is with capital "AV":
there's lots of spacing in between that can be removed and [still look fine][2].

[2]: https://en.wikipedia.org/wiki/Kerning#/media/File:Kerning_EN.svg

With other combinations though, the characters can collide, such as with "fi".
Removing kerning makes the spacing uneven.
In this situation, ligatures can be used to [replace the character pairs][3] and preserve kerning.

[3]: https://graphicdesign.stackexchange.com/a/78914

## Monospace Font

Ligatures are not restricted to proportional fonts, like kerning.
Ligatures are a more general concept of detecting and rendering character pairs differently.

This makes it useful for monospace fonts and programming.
Since ligatures are only an visual representation, they are still the two original characters.
A ligature can designed to maintain the constant width, such that the two monospace characters have a corresponding
ligature that is two character-widths.

In my view, this makes it a "killer app":
use monospace font for the grid-like layout of code but have the ability to have kerning or symbols be rendered.
And it's implemented at the font level as opposed to the editor.

## Browser and Editor Support

Web browsers support this with [`font-variant-ligatures`][1] CSS property.
It has many different sets of ligatures to apply.

[1]: https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-ligatures

With `Electron` applications, this can be injected by applying custom CSS styling.

Some terminals support font ligatures, such as iTerm2.

Many modern apps support ligatures.
But it seems to not be evenly applied or enabled by default.
maybe this is because it's a newer typographical concept that is only beginning to reach mainstream.
