---
title: Running Python Tests Real Fast
categories:
  - programming
tags:
  - python
  - testing
---

Writing tests is great.
Writing many small and granular tests is great.
At some point, it begins to look silly when you're changing one function and rerunning thousands of unaffected tests.

This is a sign that your code is decoupled from other functions in your package.
This in-of-itself is not a problem, it is good that there is decoupling between functionality.
But we also don't want to live in a micro-packages world.

What is one to do?
Doesn't `coverage` crawl through all python code and mark which lines are touched?
Wouldn't that have enough information to power more intelligent `pytest` runs?

# `pytest-testmon`
[`pytest-testmon`](https://github.com/tarpas/pytest-testmon/) is a `pytest` plugin that intelligently reruns tests.
It behaves very much like `jest --watch`, internally maintaining a dependency tree that it leverages to decide which
tests are unaffected.

The project has [details][1] on the algorithm for determination.
It's very much the same coverage, where each line if marked with the test that touches it.
This requires state, to keep a running snapshot that it can use to diff between runs.
It saves this data as a `.testmondata` file in the current directory.
This file can be committed into git if you want to maintain the canonical snapshot for each release (although it's a
binary file)

[1]: https://github.com/tarpas/pytest-testmon/wiki/Determining-affected-tests

## Integration with `pytest-watch`
`pytest-watch` is pretty simple `pytest` plugin: it listens for filesystem events, interrupts existing `pytest` runs,
and triggers a new run.

The important thing to remember is that it's really just `inotify`, re-implemented in pytest framework.
Because `testmon` is stateful, it doesn't behave well when interrupted.
It will have incomplete results, which cause it to get out-of-sync with the real world.
Maybe `testmon` has some transactional feature, to only update the test state after completed `pytest` run.

To work around this potential race condition, what we can do is freeze `testmon` data when beginning feature work.
Then start `pytest-watch -- --testmon --testmon-readonly`, which doesn't update `testmon`.
It will "diff" from the frozen snapshot, which is "only run tests for changes since branching" instead of "only run
tests for changes since last file write".
