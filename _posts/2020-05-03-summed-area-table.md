---
title: Summed Area Table
categories:
- programming
tags:
- algorithms
---

A [summed area table][1] is a handy data structure for calculating summed area in a matrix.
It is a pre-computation table that allows for O(1) area sums.

An area sum is the summation of values around a point in a matrix.
It's very useful for computer vision, which helps with fast computations for image editing:

- anti-aliasing
- compression
- image restoration
- scaling
- sampling
- image recognition and feature extraction

These image editing techniques require many reads to get surrounding pixel values.
A pre-computed table allows for combining disparate values into values that can relative to one another. allowing for
constant time computation.
For example, to read 3x3 square would naively require reading 9 pixels but a summed area table allows reading 4 corner values.
For even larger squares, such as 8x8, this is still only 4 corner values instead of 64 pixels.

## Generating Summed Area Table

The general idea is to calculate the sum of all values from (0,0) to (i, j).
This can be done by building on top of previously calculated values for (i-1, j), (i, j -1), and (i-1, j-1).
This is a dynamic programming technique.
This [blog post][2] has really good illustrations that demonstrate visually what is going on.

```plaintext
A B
C D

summed_area[D] = summed_area[B] + summed_area[C] - summed_area[A] + value[D]

Rearranging, to retrieve value at D
value[D] = summed_area[D] - summed_area[B] - summed_area[C] + summed_area[A]

A B C
D E F
G H I

To get sum area for 2x2 at I (E, F, H, I)
2x2_area[I] = summed_area[I] - summed_area[C] - summed_area[G] + summed_area[A]

Note that the values used are exclusive, because we are removing their contribution from the summed area.
```

To make it easier to handle edge cases, consider that out of bounds values for i and j are considered 0.
Use the typical techniques of handling these boundary edge cases.
Either:

- Add `if i == 0` conditional logic
- Add dummy row `1 == -1` with values of 0

[1]: https://en.wikipedia.org/wiki/Summed-area_table
[2]: https://computersciencesource.wordpress.com/2010/09/03/computer-vision-the-integral-image/
