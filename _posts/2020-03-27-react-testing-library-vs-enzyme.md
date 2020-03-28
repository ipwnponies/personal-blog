---
title: "react testing library vs. enzyme"
categories:
- programming
tags:
- javascript
- testing
---

Recently, I tried out `react-testing-library` by converting a set of tests from `enzyme`.
Here are some of my personal thoughts and insights from this experience.

TLDR; it's pretty early but I think `rtl` when test has user actions (mouse click) to avoid reimplementing a browser,
`enzyme` when testing that `React` component responds to changes correct.
`rtl` for testing imperative actions, `enzyme` for testing declarative state.

## Emulating Browser Actions

It works really well for 50% of tests, where we attempt to emulate user behaviour.
These are actions such as toggling a checkbox or clicking a submit button.

`react-testing-library` provides testing functions for invoking actions that correspond 1:1 with user intentions.
Actions such as mouse click or keypresses.
These will correctly mimic browser behaviour, such as event propagation to other event handlers.
Such can be the case if you have an action that will trigger multiple events.
i.e. text input can trigger `keydown` and `textChanged` events.

To do the same in `enzyme`, you would retrieve the *event handler* prop for a component and invoke it manually, just
like invoking a regular method.
Since the browser passes events to the handler, you need to replicate these in the tests.

## Expressive Jest Matchers

`react-testing-library` provides extension to `jest` matchers called [`testing-library/jest-dom`][jest-dom].
This extends `jest` with more expressive matchers, that accompany the paradigm that `react-testing-library` works on,
the DOM.

[jest-dom]: https://github.com/testing-library/jest-dom

The following are some matchers that are likely to be very useful and explicit in intent:

- toBeDisabled
- toBeEnabled
- toBeInTheDocument
- toBeVisible
- toHaveTextContent
- toHaveValue
- toBeChecked

These matchers are loaded with semantic meaning and intent.
Being disabled for a HTML element doesn't necessarily mean `disable="true"` attribute is set.
I meant, it could be, but I dunno.
HTML elements are very inconsistent.

[`toBeVisible`][jest-dom-visible] is a good representation of why these matchers are powerful.
It checks a bunch of attributes that result in a component being invisible, many of which are easy to miss:

- css `display` is not set to none
- css `opacity` is not 0
- all parent elements are visible

[jest-dom-visible]: https://github.com/testing-library/jest-dom#tobevisible

There's no way in enzyme to test that a component is actually visible, not without reinventing all this wheel.
And I don't think the wheel needs to be reinvented, it's perfectly round and serviceable.

## White Box vs. Black Box

`react-testing-library` is a different testing paradigm, black box testing.
`enzyme` is white box testing.
We like white box testing because it's easier to get a lot of coverage.
But we understand the value of black box testing because it's the actual interface that will be used by users.

Porting `enzyme` tests to `react-testing-library` is non-trivial.
One does not simply convert white box tests to black box.
All black box tests are white box, but not all white box tests are black box.

To simply use 100% `react-testing-library` feels like it's the same statement as "we should only do black box testing".
This brings with it all the costs of black box/acceptance/integration tests:

- the unit under test is much larger.
  Maybe this is a non-issue for `react` component testing, I dunno yet.
  Maybe it makes your tests unmaintainable because it takes 30 lines of code to set up the state of the world.
- the interface for navigating the DOM is teh same as for a browser (think `document.querySelector`).
  If you’re ever written `grease monkey` scripts or user styles, you know how painful this is can be for some sites and
  much easier for others.
  Why? Because of how they've structured their HTML (`id`, css classes, data attributes).
  You can mitigate this changing your code to allow it to be more testable ([`data-testid`][data-testid])
- Getting full test coverage will not be fun, since large test unit means many more states and branches to consider.
  White box testing lets you directly manipulate the intermediary component's props as-needed.

[data-testid]: https://testing-library.com/docs/dom-testing-library/api-queries#bytestid

## Conclusion

Well not really.
I haven't reached a conclusion.
It’s still early on and I'm still experimenting, figuring out what test patterns exist, what best practices would
facilitate this transition.
But my initial impression is that both `enzyme` and `react-testing-library` have a place.

`enzyme` tests would unit tests, testing the crap out of single components.
You would test at a `React` component level, ensuring your code is compliant with `React` conventions.
Things like using hooks correctly (don't need a real browser to test react hook does stuff) or state changes.
You'd be able to quickly get lots of test coverage and have high confidence that you didn't do anything silly.

`react-testing-library` would be more like acceptance or integration tests.
Test cases where you want to mimic user browser actions.
You can catch unexpected behaviour, such as event propagation or CSS from parent elements interfering.
