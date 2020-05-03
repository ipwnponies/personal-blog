---
title: Kadane's Algorithm
category:
- programming
tags:
- algorithm
---

[Kadane's algorithm][1] is also known as *Maximum Sum of Subarray*.
It's an algorithm for finding the contiguous subarray with the largest sum.

[1]: https://en.wikipedia.org/wiki/Maximum_subarray_problem

```plaintext
[-1, 3, -2, 5, -4, 1]
```

In this example, the subarray with the largest sum is `[3, -2, 5]`, with a sum of 6.

## Explanation

This [blog post][2] has a good layman's explanation on how the algorithm works.

[2]: https://afshinm.name/2018/06/24/why-kadane-algorithm-works/

### Brute Force

The brute force approach is to calculate the sum for all subarray permutations.
This is O(n^2), as for each N starting position, you are generating N ending position (subarrays).

### Kadane's Algorithm

Kadane's algorithm runs in O(N) time.
It uses two variables: local maxima and global maximum.

For each step, if the current element will increase the local maxima (extend current subarray):

- Update local maxima
- Update global maxima, if local maxima grows larger than it

If not, then end the current run and reset the local maxima (current subarray).

In layman's terms, it's saying:

> Will the current value extend the subarray to increase sum
> If so, extend the array
> If not, then cap that array (record if it's the largest seen so far) and begin anew
> When all done, the largest subarray will have been seen at some point

## Uses

### Max sum

You don't care about the specific details, only need to know the largest sum.
This scalar value is often useful for post-analysis or min-maxing.
You are trying to find the largest possible value, maybe to see how unoptimized something is or what the efficiency is.

For example, calculating the maximum profit for trading stock within a time period, compared to actual performance.

Or calculating the most distance covered in a minimum time window, which is more useful than instantaneous velocity.

### Largest subarray

If you're interested in the actual subarray, you'll need to modify the algorithm to store the start and end indexes for
the largest subarray.
When the global maximum is updated, capture the end index (current index) and start index.
Reset for the next subarray run, which sets that start index.
