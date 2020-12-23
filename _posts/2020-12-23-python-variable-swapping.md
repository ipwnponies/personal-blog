---
title: Python Variable Swapping
categories: programming
tags:
  - python
  - lesson
---

I read this [stackoverflow post][1] on python tuple swapping and decided to take some notes.

[1]: https://stackoverflow.com/a/31374778

## Swapping Variables With An Intermediary

When you want to swap the values between two variables, there are a few ways to do it.
The simplest is to introduce an intermediary variable.

```python
x = 'foo'
y = 'bar'

# Intermediary
z = x

x = y
y = z

assert x == 'bar'
assert y == 'foo'
```

## XOR

A common "trick" is to use XOR bit operations.
This only works for languages that support bit operations.
Such as C.

```python
x = 0b1111
y = 0b1010

x = x ^ y
y = x ^ y
x = x ^ y
```

This only works for binary data.

## Python Tuple Swapping

In python, we have nicer sugars to solve this.
Enter implicit tuple packing and unpacking.

```python
x = 'foo'
y = 'bar'

x, y = y, x
assert x == 'bar'
assert y == 'foo'
```

The expression `y, x` is an implicit tuple, created by the presence of the comma.

And we use tuple unpacking to splat a list of values to a several variables.

```python
x, y = y, x

# Syntactic sugar for implicit tuple
x, y = (y, x)

# Syntactic sugar for unpacking
x = (y, x)[0]
y = (y, x)[1]

x, y, *z = y, x
x = (y, x)[0]
y = (y, x)[1]
z = (y, x)[2:]
```

Understanding what is going on behind the sugar can go quite a ways in freeing yourself from memorizing the rules.
We now know what the sugar is doing and can take advantage of its expressiveness.
