---
title: Python Generators
categories: programming
tags:
  - python
  - lesson
  - concurrency
---

Python generators are an advanced concept that don't see a lot of use in application programming.
It's relegated to the domain of frameworks or libraries that support concurrency.

## Basic Generator

A generator is defined if a function definition contains the `yield` statement.
This expression tells Python that the function does not execute to completion and will _yield_ execution at some point.

```python
def give_candy():
  """Hand out candy to trick-or-treaters."""
  for i in bucket_of_candies():
    yield i

  return 'Success, handed out all the candies'

def dump_all_candy_to_one_kid():
  return bucket_of_candies()

type(give_candy)    # Function
type(give_candy())  # Generator

type(dump_all_candy_to_one_kid)    # Function
type(dump_all_candy_to_one_kid())  # List
```

In this example, `give_candy()` is a generator.
It doesn't immediately return, it yields iterative values before finally returning.

### Motivation For Generators

By pausing and resuming execution, generators are able to be more memory efficient when generating large result sets.
A random number generator will be able to generate infinite random numbers with low overhead.

A regular function would need to finish execution (generating infinite numbers) before it can return.
As you can imagine, no computer in existence can finish generating "infinite" numbers and such a function would
eventually run out of memory.

It needs to be stated that generators are not a performance optimization.
They are a different paradigm of programming.
This will become more relevant later, when we discuss coroutines.

## Using Generators

Once you have a generator, you need a way to pull values from it.
Generators are `Iterators` and implement the `__next__()` function.
You can iterate through values using a `for` loop or comprehensions.

To get a single value, you use `next()`.

```python
def give_candy():
  for i in candies():
    yield i

generator = give_candy()
candy = next(generator)

for i in generator:
  hand_out(i)
```

## Coroutines

So the above shows 90% of interactions involving generators.
They're performant iterators.
But this greatly discounts the ability to write coroutines.

What are [coroutines]?
Coroutines are subroutines that allow for multi-tasking.
Similar to threads, you can run multiple coroutines concurrently, progressing each coroutine at arbitrary paces.
Threads are to the OS, what coroutines are to a language runtime:

- the OS decides which threads to run and preempt. Concurrency synchronization constructs orchestrate ordering.
- the language runtime decides which coroutine to run. Coroutine constructs (yield) allow for orchestration.

[coroutines]: https://en.wikipedia.org/wiki/Coroutine

Think of coroutines as a "passing a ball back-and-forth":

1. The caller will invoke a coroutine and sit back
1. The coroutine will run until it hits a `yield`, then hand back control to the caller
1. The caller will continue execution before passing back to the coroutine ([`send`][send] or `next`).
1. Repeat until completed.
   This [stackoverflow post][stack-overflow-passing-back-forth] has a good trivial example to illustrate.

[send]: https://docs.python.org/3.9/reference/expressions.html?highlight=expression#generator.send
[stack-overflow-passing-back-forth]: https://stackoverflow.com/a/19302700

### Why Coroutines

Coroutines are a concurrency technique.
It's very similar to event-driven programming and is very efficient for IO bound operations.

Instead of using threads or processes, which use system resources in terms of memory and OS process/thread limits,
coroutines are much lighter weight.
They rely and constrain the programmers to write programs within this framework.
This makes async programming harder to write and port, compared to simply multi-threading everything instead.
