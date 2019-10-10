---
title: Margins Vs. Padding
categories:
- programming
tags:
- web
- css
---

Both margins and padding can help to achieve the whitespace separation between elements.
You can generally get the design you want with either but there will be strange interactions in the UI if you don't
understand the distinction between the two.

This [`stackoverflow` post][1] succinctly demonstrates the distinction.
Every element has margins, borders, paddings, and the content.
Often these are zero width (invisible).

[1]: https://stackoverflow.com/a/2189462

For the sake of understanding margins and padding, assume that there is always a non-zero border.
It begins to make sense when to use which.

# Focusable Area

Padding will increase the size of the border hitbox.
Everything inside the borders will be clickable.
Imagine if we emulated a `button` element but using a `div`.

Increasing the margin will not increase the size of the button.
Increasing the padding will.

Between two consecutive elements with no margins or borders, the effective padding is:

    padding = paddingA + paddingB

# Collapsible Whitespace

Visualize stacking elements on top of one another, where the border serves as the hit box.
Margins increase the space between the boxes.

Margins collapse into each other.
This is a **very, very** important concept, one that can have unexpected consequences if not taken into consideration.
Margins should be viewed as the invariant contract of how much space is guaranteed around the hit box.
Between two consecutive elements, the effective margin is:

    max(marginA, marginB)
