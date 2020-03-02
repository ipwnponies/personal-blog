---
title: Conditional Logic
categories:
- programming
tags:
- logic
- math
---

There a few conditional statements that we intuitively know and use daily.
However, it's easier to use and know but has been hard for me to know which is which.

I read this [short primer][1] as well as [wikipedia][2].

[1]: https://www.varsitytutors.com/hotmath/hotmath_help/topics/converse-inverse-contrapositive
[2]: https://en.wikipedia.org/wiki/Contraposition#Comparisons

## Definition

conditional | P -> Q
contrapositive | ~Q -> ~P
inverse | ~P -> ~Q
converse | Q -> P
negation | ~(P -> Q)

*Conditional* and *contrapositive* are logically equivalent to each other.
*Converse* and *inverse* are logically equivalent to each other.
*Negation* is a logical contradiction (must always be false, if conditional is valid).

## Example

Consider "if it rains, then they will cancel school".
The antecedent (P) and consequent (Q) are not logically equivalent.
i.e. "If it does not rain, they could still cancel school for other reasons".

Relationship | In English | Valid
conditional | if it rains, then they will cancel school | -
contrapositive | If they did not cancel school, it did not rain | Valid
not have possibly rained (would have automatically canceled school)
inverse | If it does not rain, then school will not be cancelled | Invalid, school was cancelled due to snow
converse | If school was cancelled school, then it rained | Invalid, school was cancelled due to snow
negation | There exists a case where it will rain but they don't cancel school | Invalid, they always cancel school

## Inverse vs. Conditional

Inverse is not the same as conditional.
Consider this conditional "if it is a cat, then it is a mammal" and the converse "if it is **not** a cat, then it is
**not** a mammal".

Inverse is equivalent to conditional IFF *P* and *Q* are *logically equivalent*.
Loosely, this means a 1:1 relationship.
i.e "If P, then Q. If not P, then it will never be Q. All paths that result in Q are caused by P".
With this strict relationship pinning, then the contrapositive is the same as the converse.
