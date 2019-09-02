---
title: "Mixins, Composition, and Inheritance"
categories:
- programming
tags:
- design patterns
---

I recently read about *mixins*, which is a general design concept, and not some framework specific terminology.
In python, at least.
It seems that similar concepts show up in other languages and frameworks under different names (interfaces in `C#`,
plugins, modular systems, etc.)

Nope, turns out it's a design pattern related to inheritance and composition.

# What are Mixins

*Mixins* are one of those design patterns that you might be able to find but never really found a need to put a name to it.
Here's an illustrative example that we can work off:

```python
def Bun:
    is_gluten = True
    ...

def Patty:
    is_beef = True
    ...

def VeggiePatty:
    is_beef = True
    ...

def Cheese:
    is_dairy = True
    ...

def Burger(Bun, Patty, Cheese):
    ...

def VeganBurger(Bun, VeggiePatty):
    ...

burger = Burger()
burger.is_gluten
burger.is_beef
burger.is_dairy

veggie_burger = VeganBurger()
```

What is a mixin?
It's simply multiple inheritance but for the purposes of bolting on additional behaviour.
It's very similar to a modular, plugin architecture.

# Mixin vs. Inheritance

In the example, we used multiple inheritance in python to achieve this.
In other languages or frameworks, there may be better supported way to do this, inheritance isn't strictly necessary.

In python, you can achieve this using `decorators`.

Inheritance is a "is-a" relationship.
Mixins are a "has-a" relationship.
If anything, mixins are multiple interfaces, such as in `C#`.

# Mixin vs. Composition

Composition allows for "has-a" relationships because it, literally, will have the components.
However, composition requires you to hook up these components, whereas mixins allow for easy plugin behaviour.

This comes at the cost of code maintainability though, as well as having to deal with multiple inheritance issues.
i.e. when using mixins, it's possible to have name collision and accidentally shadowing functionality.
Whereas with composition, there is a lot of necessary boilerplate to hook everything up, but this boilerplate makes it
obvious and explicit how all the piping comes together.

# Examples of Use

These aren't real examples of mixins in action but rather what I think are good candidates for them.

I started reading into mixins as I was trying to solve the design of a 6502 CPU emulator.
The main `Cpu` class was becoming bloated with every single instruction and I wanted to think of a way to separate out
related instructions.
If I used mixins, I could make the `Cpu` class smaller and focused only on fetching and decoding instructions, while the
mixins will import all the necessary functions to handle the CPU instructions.

I could also use composition instead, where the `Cpu` is only responsible for mapping OP codes to their respective
components and forwarding the work as necessary.
