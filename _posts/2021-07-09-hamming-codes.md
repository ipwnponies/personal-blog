---
title: Hamming Codes
categories: math
tags:
  - computer science
  - algorithm
---

Hamming codes are an error-correcting code.
The upgrade from a parity check is that it is capable of detecting and correcting errors.
It scales quite well, requiring only `log(N)` parity bits.
With large enough data blocks, overhead is minimized.

This [youtube video] from _3Blue1Brown_ does a very good job of explaining it.
His approach builds it up from first principles, and makes Hamming Codes almost seems like the intuitive conclusion.

[youtube video]: https://www.youtube.com/watch?v=X8jsijhllIA

We'll try to follow the same iterative evolution.

## Goal

Depending on the medium, bits of data can be corrupted and flipped.
Detection and correction is crucial to avoiding the cascade of errors within the system.

Some systems are more prone and less tolerant to errors than others.
This is exacerbated by the quantity of data and transmission medium.

We are looking to detect and correct errors in a block of data.
If we cannot correct the data, we can still retry transmission.

## Parity Check

Parity check is a bit that is used to enforce even parity,
The value of this bit is set such that the entire data block has an even number of 1-bits (even parity).
This works out to be an XOR operation across the whole block.

When you receive a block of data, you can detect if the integrity of the block is intact.
This is a very simple computation.

Parity is only able to detect an error within the block, it doesn't know which bit is wrong.
This lacks error correction.
Just as dangerous, 2 errors will be masked, as the parity computation will remain correct by coincidence.

It scales `O(1)`, only requiring a single parity bit for as many blocks as you want to be the atomic unit.
A single parity bit is perfect if the errors are rare and retrying is trivial.

### Parity Check - Detection

To detect which bit contains the error, you are required to limit the breadth of the data to a single bit.
If the parity is incorrect, you know exactly which bit has an error.

For a single bit of data, the even parity bit would be the same value as the data bit.
For a block of data, the parity block is essentially a duplicate data block!

This scales `O(N)` and has a 50% overhead.

### Parity Check - Correction

Now that we can detect which bit has an error, we can tackle correcting it.
Assuming the parity bit is error-free, we simply use the parity value.
But we can't make this assumption because the parity bit is also susceptible to errors.
It's just looks like more data to the transmission medium!

It's impossible to know whether the parity bit or data bit contains the error...
What do?

Add another parity bit!
This redundancy will give us a best-of-3 consensus on the correct data value.
This scales still scales `O(n)`, with a 66% overhead.

While this overhead is hard to swallow, it's mandatory.
If you have:
-N parity bits

- detected which bit the discrepancy lies at
- ultimately cannot decide whether the parity or data bit is the correct one
  What's the point?
  You're in the same position as the simply parity check across the whole block.

Note, we just described a Hamming Code special case, Hamming(3,1).

## Hamming Code

Having described Hamming(3,1), we will begin to work on generalizing the Hamming Code algorithm.

### Making Parity Bit Do More Work

We have the upper bound of `3*O(N))`.
How do we bring this down?
We need to make each parity bit cover more than a single data bit.
Our constraint is that we still need to be able to pinpoint which exact bit has an error.

### Parity Ranges

Assume 4 data bits, where we want to use 3 or less parity bits.
What if we have make the first parity bit cover bits 0-1, second parity bit covers bit 1-2, and third parity bit
covers bits 2-3?
With this overlapping coverage scheme, it's possible to narrow down errors to a bit.
i.e. If the error is in bit 0, only the first parity bit will be incorrect.
If in bit 1, then both first and second parity bits.

We've reduced the parity bit space requirement by 1.
What's the math behind this?
It's because the parity bits cover **interval ranges** of size 2.
For N elements, there are N-1 intervals.

How do we save more?
Can we make the size of the intervals larger, to 3?
Sure, for 5 bits, this looks like:
parity bit | range coverage
-|-
0 | 0,1,2
1 | 1,2,3
2 | 2,3,4

Increasing the interval range decreases the required parity bits by 1 each time.
This is still `O(N)` and is not significant enough.

### Addressing

The problem with intervals is that is subdividing the group uniformly.
No matter the interval size chosen, it's still scaling by `O(N)`.
No, we need some addressing scheme that reduces the search space.
Each additional bit further cutting down the search space some more.
Like half as much... for searching... binary search?

The first parity interval covers the first half of the bits.
The second interval covers a quarter of the half.
But it can also cover a quarter of the other half.
These two bits already let us uniquely address and search 4 bits.

These parity bits end up representing binary addresses:
the most significant bit (MSB) is 0 for the first half of range and 1 for the second half.

This is the gist of a generalized Hamming Code approach.
Each parity bit handles parity for the addresses they cover, which are addresses where the Nth position is set for the
Nth parity bit.

### Data Block

For 3 parity bits, we can encode 2^3 == 8 addresses.
The parity bits are located at 001, 010, and 100.
The 000 bit is unused.
This leaves 4 bits of data in Hamming(7,4).

| Address | Purpose                                                  |
| ------- | -------------------------------------------------------- |
| 000     | Unused                                                   |
| 001     | Parity bit for addresses matching 001 mask. Call this A  |
| 010     | Parity bit for addresses matching 010 mask. Call this B  |
| 011     | Data bit, indexed by A + B                               |
| 100     | Parity bit for addresses matching 100 mask. Call this C. |
| 101     | Data bit, indexed by A + C                               |
| 110     | Data bit, indexed by B + C                               |
| 111     | Data bit, indexed by A + B + C                           |

From the table, we can see how the data bits are uniquely indexed and covered by the parity bits.

### Efficiency

For N parity bits, we can encode 2^N addresses.
The zeroth bit is unused (except in [Extended Hamming](#extended-hamming)).
This provides 2^N - 1 - N number of data bits.

| Number of parity bits | Block size | Data bits | Hamming() | Efficiency |
| --------------------- | ---------- | --------- | --------- | ---------- |
| 2                     | 3          | 1         | (3,1)     | 33%        |
| 3                     | 7          | 4         | (7,4)     | 57%        |
| 4                     | 15         | 11        | (15,11)   | 73         |
| 5                     | 31         | 26        | (31,26)   | 84         |
| 6                     | 63         | 57        | (63,57)   | 90         |

At 8 bits of parity, the block size is 255 bits and 97% load efficiency.

## Extended Hamming

There is an unused bit, 000, that is used in _Extended Hamming Code_.
It is a parity bit for the whole block.

What does this information give us?
A single error would result in odd parity.
But we can already detect this with the existing parity bits.

What about two errors?
With two errors, the parity bits will detect errors but unfortunately resolve to the wrong location of error.
This is because the Hamming Code can only perform corrections for a single error.
How can the Hamming code differentiate between 1 or 2 errors?

The parity bit on the whole block will give odd parity for a single error and even parity for 2 errors!
That is, if the parity bits detect an error but the block parity bit is already even, we know there are 2 errors.
And knowing the data is incorrect and irrecoverable, we drop it and request for a resend.

This single bit in Extended Hamming effectively allows us to tolerate 2 errors, even though we can only correct 1.

## Conclusion

This was a very fun topic to learn.
I highly suggested watching the video, it's extremely elegant explanation.

There is a [math/logic puzzle][puzzle] about a king and 1000 bottles of wine, one of which is poisoned.
The king can use rats or tasters to test the wine bottles.
How many tasters do we need?

[puzzle]: https://mathoverflow.net/q/59939

The solution is `log(N)` if we turn this into a Hamming Code problem.
Where each rat tastes half the bottles of wine in an overlapping fashion.
The ones that die (parity bit) will denote the address of the poisoned bottle.

This video elegantly demonstrates the evolution and thought process questioning that brought about the next innovation.
