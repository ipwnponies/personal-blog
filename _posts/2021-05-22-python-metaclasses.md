---
title: Python Metaclasses
categories: programming
tags:
  - python
  - oop
---

I'm working on a Python 3 migration and have been refreshing myself on the changes.
One of the syntax changes is how a class' metaclass is set:
Python 2 looks for a `__metaclass__` class attribute while Python 3 introduced a `metaclass` parameter in class declaration.
`futurize` is capable of [automatically converting][python-future] existing code so this is super easy fix.

[python-future]: https://python-future.org/automatic_conversion.html

But then I made the unfortunate choice to learn more about this, to understand the design decisions.
What even is a _metaclass_?

## What is a Metaclass

> A _metaclass_ is Python class that is used to create other classes.

Woah, \<insert pimp my ride meme>.
Seriously, what does this even mean?

### Classes are Objects

Let's lay some foundation.
Everything in Python is an object, even classes.
We are all very familiar with instances of classes being objects.
But the class itself being an first-class object is unique to some languages, such as Python and JavaScript.

You can add attributes to a class, use it as variable or parameter, and copy it (clone the object).
You can even use `id()` to get the object identifier.
This statement is straightforward for _instances_ in all OOP languages.
If you're familiar with JavaScript and it's prototypical OOP design, this is similar.

In languages where classes are not objects, you cannot do this.
In Java and C#, you cannot manipulate a class at runtime, at least not without reflection and other metaprogramming techniques.
You make these changes in static code and they are consumed at compile time.
The resulting compiled code doesn't make the class available as a plain old object.

### Creating Classes Dynamically

So you've all created classes statically using the `class` keyword.
This is static because it requires you to specify behaviour before runtime.
How does Python create an object out of this class definition?

`type()` is used to create a class object.
It more commonly used to get the type (use `isinstance` though!) but is overloaded to create class objects.

```python
# Normal class declaration
class ClassName(BaseA, BaseB):
  constant = 'Value'
  @staticmethod
  def get_value():
    ...

instance = ClassName()

# Dynamically creating a class
def get_func():
  ...

ClassName type('ClassName', (BaseA, BaseB), {'constant': 'VALUE', 'get_value': get_func})

instance = ClassName()
```

`type` is handy for creating classes.
Which is similar to the purpose of a metaclass, to create classes.

### Metaclass Definition

How do you tell the class of an instance?
All objects have a [`__class__` attribute][__class__].

[__class__]: https://docs.python.org/3/library/stdtypes.html#instance.__class__

Typically, this will return your class or a stdtype.

```python
num = 444
num.__class__
<class 'int'>

def foo(): pass
foo.__class__
<class 'function'>

class Bar: pass
Bar().__class__
<class '__main__.Bar'>
```

Everything in Python is an object, there are no primitives.
Strings and integers are standard types but they are still objects.
They are created by `int()` and `str()` respectively.

But since we said everything in Python is an object and all objects have a `__class__` attribute...

```python
num.__class__.__class__
<class 'type'>
num.__class__ is int
int.__class__
<class 'type'>

foo.__class__.__class__
<class 'type'>
```

We can see that even "primitive" strings and integers have a class that created them.
But `str` and `int` are the "classes" that create the instances.
So we can see here that `type` is the metaclass that created both `str` and `int`.
A class that creates other classes.
You can substitute the name "class factory" for "metaclass", if it helps conceptually.

Setting the `metaclass` parameter when declaring a class.
This is `type` by default.

## But Why

We've discussed at length what a metaclass is and how it behaves in practice.
But we still don't have a motivation for using it.
And it seems needlessly complicated, seeing as I've never had a use for it in all the code I've read over the years.

> Metaclasses are deeper magic that 99% of users should never worry about it.
> If you wonder whether you need them, you don't
> (the people who actually need them to know with certainty that they need them and don't need an explanation about why).
>
> - Tim Peters

Tim Peters invented the _TimSort_ algorithm for Python.

The main use case of metaclasses is to dynamically generate classes.
This is common in generating APIs such as database ORM or OpenAPI clientlibs.
By providing a spec, in yaml or json, the metaclass will generate a class with custom behaviour.
Or in `libast`, where you implement `visit_<NODE>` functions and the library will pick it up, without statically
defining all permutations.

Note that even in these cases, you can use `__getattr__` to hook in to arbitrary attribute calls and implement dynamic behaviour.
Granted, this doesn't give you a concrete class implementation at runtime, unlike metaclass.
But it achieves the same end goal, given that metaclasses are already runtime-ish and we already suffer from code
comprehension vs. static class definition.

## Summary

**TLDR;** metaclasses are classes that build other classes at runtime.
They have niche use cases and you only need to know about them in case you are working in these niche areas.
Otherwise, you can ignore their existence and work just fine.

I've seen code bases that did not use metaclasses and just used `__getattr__` to handle dynamic behaviour.
They even generated the code and committed the artifact, since static classes are easier to reason with, albeit auto-generated.
And the use of type annotations can help supplement IDEs.

I'd write down metaclasses as an implementation detail of the language and interpreter and you should not feel obliged
to use it,
just like 99% of the other magic implementation details of the language.
Make no mistake, metaclasses are used everywhere and integral to the language.
Just not to 99% of the development use cases.
