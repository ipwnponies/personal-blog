---
title: How Python super() Works
categories:
- programming
tags:
- python
- oop
---

I was trying to understand what the use of `super` in python was for and why we needed to include it with every constructor.
I read this great [StackOverflow answer][1] on this very subject.

[1]: https://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods/27134600#27134600

## What is super used for

### Constructors

In Python, `super()` is commonly used when subclassing and you need to call the base class' methods.

```python
class Base:
    def __init__(self):
        print('Base')

class Child(Base):
    def __init__(self):
        super().__init__()
        print('Child')
```

There is no mechanism to call methods automatically (such as chaining constructors), you must invoke it explicitly.

Requiring manual invocation has the advantage of having complete control over method ordering.
In other languages, such as Java or C#, the base class constructor call is implicitly added and, therefore, always runs
before child classes.
This is usually not an issue, as in OOP it is understood that you _build the base_ before _adding extensions_.

The disadvantage is that it requires programmers to do this every time.
Forgetting to do so will cause bugs for other classes, as the expectation of inheritance will not work correctly.
This is a big concern, as it requires every class to be designed correctly before you can expect to use `super()` and
have it behave as expected.

### Calling overridden functions

```python
class Base:
    def say(self):
        print('Base')

class Child(Base):
    def say(self):
        super().__init__()
        print('Child')
```

In python, when you name an attribute with the same as a base class attribute, you _shadow_ it.
This means you clobber the reference to the original function.

`super()` allows you to refer to the original function.

## Why do we need super

Why do we need `super()`?
Can't we just call `Base.__init__()` or `Base.say()`?

The answer is, yes, if the inheritance is trivially _single inheritance_.
`super()` does little more than indirectly reference the base class.
In most code, this is usually the case and it's so common that there are not many working examples in code bases to
illustrate the need for real value of `super()`.

Things get interesting when you get into multiple inheritance.
`super()` becomes mandatory to have things function sensibly, when attempting to design multiple inheritance.

### Diamond Problem

There's a [diamond problem][2] with multiple inheritance, which is when it's ambiguous which base class' method should
be called next.

[2]: https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem

```python
class SuperBase:
    def say(self):
        print('Super Base')

class BaseA(SuperBase):
    def say(self):
        print('BaseA')

class BaseB(SuperBase):
    def say(self):
        print('Baseb')

class Child(BaseA, BaseB):
    def say(self):
        super().say()
        print('Child')
```

When we call `say`, should it call `BaseA.super()` or `BaseB.super()`?
And what does it call after that?

This problem is solved with method resolution order (MRO).
Every class has a MRO and it can be shown with `Child.__mro__`.

This list of classes shows the class that `super()` will reference.
Note that this is dynamic, not hard-coded to a specific class.
Another class can subclass and statically calling `BaseA` is making dangerous assumptions.

```python
class AnotherChild(SuperBase):
    ...
class SubChild(AnotherChild, Child):
    ...
```

In this example, you cannot hard code all base class references in `AnotherChild` to be `SuperBase`.
`SubChild` inherits both `Child` and `AnotherChild` so the entire inheritance tree needs to be taken into consideration.
Since `SuperBase` is the root for both `Child` and `AnotherChild`, you cannot always call it directly from `AnotherChild`,
because you might need to call `BaseA` first (`Child`'s base class).

This inverted control of the inheritance tree means we need to defer resolution to runtime, which is why `super()` is useful.

### MRO

Method resolution order is a heuristic for determining the inheritance order of precedence.
Given a class with complex inheritance hierarchy (may include loops or duplicate, redundant inheritance), how can we get
an ordering that is deterministic and monotonic.

Deterministic means that it will not change at runtime.
If the hierarchy has not changed, the output should always be the same.
If we add or remove classes from the hierarchy, the order of everything else, relative to each other, should not change.

Monotonic means that the ordering always goes from most specific to least specific.
In other words, from the most "child" to the most "base.

It must handle recursion and duplication.
If a base class is inherited multiple times, it should resolve to a single call.
And this should be ordered **after all** the subclasses.

Python uses [C3 linearization][3].
It's pretty simple heuristic to follow, I'll try to condense to the core concept:

1. Generate inheritance tree for all objects.
1. If there's only one parent, then the ordering is trivially resolved.
1. Otherwise, pick the parent that does not appear in the middle of another parent's inheritance tree.
1. Rinse, repeat until all is resolved

[3]: https://en.wikipedia.org/wiki/C3_linearization#Example_demonstrated_in_Python_3
