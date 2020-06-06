---
title: Euclid's Algorithm for Calculating Greatest Common Divisor
categories:
- programming
tags:
- math
---

The greatest common divisor between two numbers is the largest common factor of either numbers.
e.g. 8 is the GCD between 16 and 24.

[Euclid's Algorithm][1] is an intuitive method for calculating the GCD, using only the modulo operator.

[1]: https://en.wikipedia.org/wiki/Greatest_common_divisor#Euclid's_algorithm

```math
gcd(a,0) = a
gcd(a,b) = gcd(b, a mod b)
```

## gcd(a,0)

`gcd(a,0)` is not intuitive but makes mathematical sense.
In layman's terms, it says the "greatest common divisor between a number and 0 is the number itself".
This makes little sense, as `0` cannot be a divisor.

What is more accurate is the "greatest common divisor between a number and 1 is 1".

We must ignore the layman's term for interpreting `gcd(a,0)`.
It should simply be used as the base case when using defining the recurrent relation.
Look at the the value of `b` from previous `gcd`, it's `a mod b`.

If `a mod b == 0`, then the gcd is `a`.

## gcd(a,b) = gcd(b, a mod b)

If `b` divides evenly into `a` (`a` mod `b` == 0):

- `b` is a factor of `a`
- `b` is a factor of itself, by definition
- `b` is the greatest common divisor

If `b` does not divide evenly, then there is a remainder.
If we can find the GCD between the remainder and `b`, then that will also be a divisor for `a`.

Eventually, the remainder will be 0 (found divisor) or 1 (divides into everything).

## Intuitive Summary

The intuition that I've been trying to wrap my mind around is that we are iteratively trying to find a the division
between divisor and remainder.
If we find a "remainder" for which a divisor is a multiple, and the quotient is a multiple of the divisor, then this
"remainder" is a factor of the  quotient.

This [visual][2] is what made it really click.
We keep slicing a rectangle and iterate on the remainder.
Do this until we find a value that evenly divides for all.
1 is the guaranteed common divisor.

[2]: https://en.wikipedia.org/wiki/File:The_Great_Common_Divisor_of_62_and_36_is_2.ogv
