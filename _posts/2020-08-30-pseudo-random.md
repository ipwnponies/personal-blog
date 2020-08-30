---
title: Pseudo-randomness
categories:
- programming
tags:
- computer science
---

Randomness is often used in computing.
The world is unpredictable and probabilistic and we want to model many things like this.
Whether it's rolling a dice or random sampling a data set.

Using randomness is pretty straight-forward and easy, given the libraries.
Today, we're going to discuss the implementation of the random functions themselves.

## What is Pseudo-Random

The terms *true random* and *pseudo-random* are often mentioned.
True random is what we all intuitively understand.
Pseudo-random is an approximation of true random.

True Random
: Truly random. It's what we all commonly define as random

Pseudo Random
: Not completely random, there is deterministic behaviour involved

Why do we want to approximate random?
Turns out it's much easier for computers (and humans) to think in deterministic terms.
Given a set of inputs, produce a set of outputs.
We can come up with algorithms and math models that are deterministic.
And we can make this very fast.

How do we reconcile this?
Easy, inject the random parts into the deterministic part!
That reduces the scope of random aspects to a single value, referred to as the *seed*.

seed
: The initial value to a a deterministic function.
As long as this value is randomly chosen, the output of generator will also be random (ish)

These functions are referred to as pseudo-random generators.
Part of the function is random (input) and the part of the function is not (output).

## Why Not Use True Random

As alluded to earlier, pseudo-random functions are easy to write and understand.
They are very fast and require little resources.

True random, on the other hand, is heavy-handed.
Random values are often obtained from nature, such as noise in signals or changes in temperatures.
But sensors and the interpretation of their values are designed by humans for consumption, meaning discrete quantized values.
If you sample a low quality sensor too frequently, there may be patterns or the subsequent values won't have enough variance.
The continuous nature of analog signals doesn't allow for discontinuous, uncoupled values.

This is why `/dev/random` is slow.
It blocks until it's collected enough entropy to confidently produce a value that can be considered random.
You cannot sampled more frequently if the entropy sources has large inertia and changes in gradual and continuous manner

entropy
: bits of randomness, often collected by hardware sensors such as variance in fan noise or HDD)

### When to use true random

Reserve the use of true random values for applications that require it, such as generating cryptographic keys.
If you only need a random value for sampling data source, pseudo-random is sufficient.
Basically, what is vulnerability can be introduced if you can predict the next random value?

For generating a key, this can catastrophic.
An attacker can predict all the subsequent keys that will be generated, effectively breaking many, many keys.

For sampling data, it's a different story.
While an attacker will know which messages will be sampled, it's difficult for them to ensure they get chosen,
as there are other actors in the system.
And the harm they can do is different.
It's not clear that we need true random for this use case, given the costs.

Seeding a random number generator with a true random value might be valuable technique.
This gives you a randomly instantiated generator, which will produce deterministic values after that point.
The initial cost of instantiation will pay off with the many uses.
You can do this periodically, so that there's a TTL on how long a "session" is.

## Example Pseudo-Random Generator

I'm going to use a greatly simplified example.

Imagine you are generating numbers between 0-9.
This means our `modulo` is 10.
We'll use this function as the generator:

```default
x_1 = x_0 + 7 % 10
```

Given a seed of 0, the random sequence is `7, 4, 1, 8, 5, 2, 9, 6, 3, 0`.
This function is using 7, which is coprime with the modulo 10.

As you can see, if the seed changes, the sequence starts at a different point.
With a seed of 5, the sequence is `2, 9, 6, 3, 0, 7, 4, 1, 8, 5`.

As long as I seed this randomly enough, it's hard to predict the next value, which gives the illusion of randomness.

This is function is called a *linear congruence generator*, where the output becomes the input for the next output.
This function is typically a mathematical formula and is trivial for a computer to process.
