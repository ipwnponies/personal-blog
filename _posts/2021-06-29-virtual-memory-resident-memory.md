---
title: Virtual Vs. Resident Memory
categories: technology
tags:
  - profiling
  - unix
  - windows
  - performance
---

Whenever I've needed to look at how much memory a process is using, I'm never actually sure what value to use.
There's resident memory, virtual memory, swap memory, ...
It can be overwhelming when in the context of looking at computer resource usage and all the other values flying around.

I read this [*stackoverflow* post][1], which concisely explained this.

[1]: https://stackoverflow.com/questions/7880784/what-is-rss-and-vsz-in-linux-memory-management

## Virtual Memory

This one is easiest to explain.
Virtual memory is all the memory a process can access.

This includes:

- in-memory
- swap memory
- shared libraries
- allocated memory

Theoretically, this is limited by how many bits are used for addressing.
For a 32-bit system, this is 4 gigabytes.
For 64, this is 16 exabytes.

Practically, a process requests memory allocation until the OS tells it to bugger off.
This is when your system calls for memory allocation fail.

You should view virtual memory as the theoretical ceiling of memory usage.
While you should not ignore it, you can rest easier knowing that the OS is going to swap out any unused memory and
recover physical memory.
This is a reason that Chrome can seem to use a lot of memory, it's just loading a bunch of libraries and caching things
in memory.
Much of it is actually swapped out.

## Resident Memory

Resident memory is how much real, physical memory the process is currently using.

Note that this includes shared libraries, with no deduping.
Terminating the process will not necessarily recover the resident memory amount.

You should view this as the working memory footprint.
Lowering this value will allow you to fit more processes on the same system.
If you're experience performance issues, you'll likely see that the resident memory used is high.
The OS is soon left hard choices to make, with respect to swapping.
It starts targeting things you are actually using, in a failing game of juggling resources and thrashing.

## Example

Taken from the [post][1]:

```ignore
ProcessFoo

Virtual memory
500 K binary
2500 K shared libs
200 k heap allocation

Resident Memory, what is actually loaded at this moment
400 K binary
1000 K shared lib
100 k heap allocation
```

The virtual memory is the sum of the full values.
If you did not have smart systems for managing resources, you'd naively load everything into memory,
which would be `500 + 2500 + 200 = 3200 K`.

The resident memory is smaller, at `400 + 1000 + 100 = 1500 K`.
