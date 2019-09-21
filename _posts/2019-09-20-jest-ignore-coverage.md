---
title: 'Jest/Istanbul Coverage Ignore'
categories:
- programming
tags:
- javascript
- coverage
- testing
---

# Limiting Jest Coverage Noise

I've been using *Test-Driven Development* when writing test code.
This is done using `jest --watch --changesSince '@{u}` to trigger test runs whenever a change is made.

This will run test and coverage report but **only** for the files touched since upstream tracking branch.
The git command equivalent is `git diff '@{u}...@' --name-only -- '*.js'`

# Istanbul Ignores

I've also been learning how to correctly `istanbul` ignore statements.
The [`istanbul` docs][1] cover the heuristic that's used.

[1]: https://github.com/gotwarlost/istanbul/blob/master/ignoring-code-for-coverage.md

What made it click for me is to think of what the "next" thing is.

```js
/* istanbul ignore next */
const foo = {
    /* istanbul ignore next */
    bar: () => {},
    baz: '',
};
```

In this example, the "next" thing for both ignores is the assignments.
It doesn't work to ignore this and shouldn't ignore anyways, since it's trivial to get coverage for assignments or declarations.

There is still lack of function coverage, if we don't call `foo.bar()`.
To ignore the function execution, we need to get move the ignore closer to the "next" thing:

```js
const foo = {
    bar: /* istanbul ignore next */ () => {},
    baz: '',
};
```

We've now declared that we want to ignore coverage for the entire anonymous function.
