---
title: Python Decorator
categories: programming
tags:
  - python
---

Python decorators are a syntactic sugar.
They appear declarative and are used in that manner, yet they're actually imperatively executed.
I believe this mismatch in mental model is a primary source of confusion when it comes to writing decorators.

**Say it with me**: decorators declaratively configure python code but they are executed imperatively.
If you write decorators that cannot be declaratively applied, such as relying on sequencing or pre-existing state, you
might be in for a bad time.
The decorator syntax is very much streamlined and abstracted away for the end user.
But writers are required to know how the engine works under the hood and it's not the prettiest thing.

## Desugaring

```python
def wraps(func):
  # Technically should return a callable
  return func

@wraps
def foo():
  ...

# Equivalent without syntactic sugar
foo = wraps(foo)
```

A decorator is a function that wraps another function.
It receives the wrapped function in as the parameter.

Here's something unintuitive you can also do, now that you've seen the desugaring:

```python
def wraps(func):
    return 'hello world'

@wraps
def foo():
    ...

# Equivalent without sugar
foo = wraps(foo)

# But wait, func isn't used in wraps
assert foo = 'hello world'
```

I can't think of a reason to decorate a function but not return a function.
We know this is possible in python, knowing the syntactic sugar behind it.
But this breaks the mental model behind decorators.

## Decorators With Parameters

Wait you say, how do you pass parameters to the decorator itself?
`lru_cache()` lets you specify the size of the cache.

This is where it's crucial to understanding the desugaring if one hopes to wrap their mind around this:

```python
def lru_cache(maxsize=128, typed=False):
    '''Outer most function, name of the decorator. Provides closure for decorator parameters.'''
    cache = {}

    def decorating_wrapper(func):
        '''Same as parameterless decorators. Notice the input is always func'''

        def actual_lru_cache(*args):
            '''Wrapped function, what the user will actually end up invoking.

            This is where we use decorator parameters at runtime.
            '''

            result = cache.get(args):
            if not result:
                cache[args] = result = func(*args)
            if size > maxsize:
                # lru eviction logic, using parameterize value
                ...

            return result

        return actual_lru_cache(func)
    return decorating_wrapper

@lru_cache(max_size=8)
def foo():
    ...

# same as
decorating_wrapper = lru_cache(10)
foo = decorating_wrapper(foo)

# one-liner
foo = lru_cache(10)(foo)
```

Basically you have an additional layer of abstraction.
You could follow this logic as deep as you want, with more wrapped functions.
It's devolves into a series of nested functions, where the decorator syntax and sugar is restricted to the _i=1_ iteration.

## When To Use Decorators

There are two use cases for decorators:

- wrapping a function, a function-level context manager
- declaratively registering functions

In general, decorators are good choice if they are agnostic to the underlying function.
They're good for working wtih function objects, such as registering callbacks or mapping which function maps to which conditional.

### Wrapping A Function

Decorators have a strong use case for transparently wrapping a function to bookend its execution with more code.
`lru_cache` or uwsgi tween handlers are good.
They act similarly as a context manager that wraps the entire function body.
In place of `yield`, the wrapped function is invoked.
For a HTTP tween, this can be used to measure timings or to tag a add meta data to request and response.

### Declaratively Registering Function

It can be in declarative configuration pattern.
This is used by flask to register endpoints.
The alternative would be call a registration function imperatively, after the request handler was defined.

Pytest uses decorators for parametrizing tests.
This declares a list of test cases to be run (which is really just registration into pytest).
The test runner uses this input to expand to multiple tests cases.
