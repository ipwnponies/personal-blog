---
title: Reverse Polish Notation
categories:
- programming
tags:
- computer science
- math
---

If you're asked to add 2 numbers, you are probably mentally imagining `2+2`.
What about:

```ignore
2 + 2  # infix
+ 2 2  # prefix
2 2 +  # postfix
```

I'm here today to dig up mathematical concepts I learned about back in school.
And have promptly forgotten because I do not build compilers for a living and neither should you.

## Infix, Postfix, Prefix

Have you ever thought about why we've chosen this ordering?
Or what it's even called?

The commonly seen is *infix* order.
For a binary operation, this means surrounding the operator with the two parameters.

Prefix order is when the operator comes first, followed by the parameters.
This is also called *Polish Notation*.

And postfix is when the operator comes last.
This is also called *Reverse Polish Notation*.

These are different representations of the same expression and are all equivalent.

## Motivations for Using Each

This [site][1] does a good job breaking it down.

[1]: http://www.cs.man.ac.uk/~pjj/cs212/fix.html

### Infix

Infix is the usual way we write expressions.
Why, who knows?
That's more a topic of linguistics, language, historical conventions, etc.

Infix notation has operator precedence rules.
i.e. multiplication is done before addition, in the absence of other information.
Parentheses can be used to directly change the ordering.

This is a nightmare for a program to parse.
It's like using unstructured, unschematized data.
You're literally wasting precious time on earth dealing with a problem you imposed upon yourself.
Don't do this.

### Prefix

This one feels... familiar.
Operator... then parameter1... then parameter2...

```python
operator(parameter1, parameter2)
```

Prefix is what we use in many programming languages!

Because it's ordered, there's no ambiguity and no need for parentheses.
However, consider this:

```ignore
2 + 3 * 3 (infix)
+ 2 * 3 3 (prefix)
```

When you're iterating through the symbols, you can't move on form the first operation until you resolve the second parameter.
Just like function calls!

```python
operator(parameter1, do_something(parameter2))
```

The way to do this calculation is just like function calls:
you must put everything onto the stack temporarily and defer the calculations to later.
And just like recursive function calls and stack overflow, it could possibly require lots of stack space.

### Postfix

This one feels weird.
But computers love this.
To them, it feels like a optimized tail-recursion.

```ignore
2 + 3 * 3 (infix)
2 3 3 * + (postfix)
```

The operator comes after the parameters.
This is the key understanding:
the operator comes **after** the parameters.
This implies the parameters have **resolved** by the time you reach an operator.

Just like in tail-recursion optimization, where the operator (return) comes after the parameter (function call) has resolved.
In tail-recursion optimization, the compiler is able to ignore the stack unrolling because it knows this invariant
exists (no use for stack after finishing recursive call).

When calculating postfix, a stack is still used.
As we can iterate through the tokens, we push them onto the stack.
When we reach operators, we pop from stack, evaluate and reduce to single value, and push back to stack.
Every operation is clobbering the previous stack values.
This means there is much less stack space required with postfix notation vs. prefix.

## Converting

Unfortunately, we live in world where the human-input is probably infix.
Just like human-input for datetime is literally anything but ISO8601.
We want to convert this to post or prefix, something that is more structured and easier for machines to consume.

Enter the [Shunting-yard algorithm][2].

[2]: https://en.wikipedia.org/wiki/Shunting-yard_algorithm

The general algorithm, while iterating through tokens:

1. If number, append to to output.
    Only operators are being moved around.
1. If operator, put on stack.
  This operator is pending a lower precedence operator, to delimit it.
1. If higher precedence operator and stack has values, continue adding operator.
1. If lower or equal precedence operator and stack has values, this demarcates the prior pending operators.
  Pop them off to the output.

Intuitively, in english, this makes sense.
"Add numbers to the output. If operator, I need to hold on and check if there is a higher precedence operator".
This need to look ahead is something that humans like but computers do not.
