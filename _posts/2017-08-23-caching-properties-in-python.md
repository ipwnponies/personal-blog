---
title: Caching Properties in Python
---
# What are cached properties and why do I care?
A cached property is a mechanism that allows for storing the result of a function call, so that
future calls return the cached value and avoid computation costs. If the function is expensive, this
can save on time and API calls.

# How is this done?
You can certainly implement a naive solution yourself.
```python
cached_value = None
def foo():
    if cached_value:
        return cached
```

There are exisitng packages that can do this and with more functionality. Let's talk about these.

## cached-property
[`cached-property`](https://github.com/pydanny/cached-property) is a python package that pulled out
the caching functionality from django.

### When to use
`cached-property` should be used if you need to cache the result of a function call that does not
take parameters (at least changing parameters). It is good for functions that are slow-changing but
changing, nonetheless. This will give you singleton-ish behaviour. It has support for threading, a
way to invalidate the cache, and TTL settings.

### How to use
```python
from cached_property import cached_property

@cached_property
def get_user_preference():
  # Super expensive query to get user preference
  pass
```
User preferences are slow changing but is accessed frequently. A common coding paradigm is to store
a local copy after making the expensive call. This introduces code noise because you'll have an
extra local variable, or you would need to modify the function call like [above](#how-is-this-done).
Using `cached-property` takes care of all these details.

We can invalidate the cache every 5 minutes, which means that user preferences are stale for a
maximum of 5 minutes. To refresh, it's the same function call but returns a different result because
the function is non-deterministic (changes over time depending on the data on backend).

## functools.lru_cache
Python 3.2 introduces `functools.lru_cache` decorator that will allows you cache function calls,
limiting the cache size using an [LRU cache](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_Recently_Used_.28LRU.29).

### When to use
`functools.lru_cache` should be used when you need to cache the results of a deterministic function
call for memoization purposes. Think the classic fibonnaci sequence, this is the perfect use case.

### How to use
```python
from functools import lru_cache
@lru_cache(maxsize=1000)
def fibonacci(n):
  if n == 0 or n == 1:
    return 1
  else:
    return fibonacci(n-1) + fibonacci(n-2)
```
If we run `fibonacci(100)`, we will recurse and cache the results for `0 < n < 100`. Any subsequent
function call within that range will return the cached result instead of recursing.
