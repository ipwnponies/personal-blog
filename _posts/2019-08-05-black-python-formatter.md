---
title: Black Python Formatter
categories:
  - programming
tags:
  - python
  - code style
  - tools
---

[*Black*][1] is a python code formatter.
It has minimal reconfigurability and is opinionated so that you don't have to be.
What that means is that you hand over control of personal preferences and accept the common set of conventions.
If other projects also use this tool, then contributors to either projects will benefit from a common code style
interface when reading and writing code.

[1]: https://black.readthedocs.io/en/stable/the_black_code_style.html

I'll go over a summary of some of the philosophy it takes when deciding the convention to use.

# Spacing

## Line Length

The default line length is 88 characters.
This is based on PEP 8's 80 character line width, with 10% allowance.
It's like a highway speed limit: you're only supposed to go 80 but nobody is going to a stickler if you're at 83.

## Line Wrapping

For horizontal line lengths, *Black* will apply PEP 8 rules.
I haven't found an issue with this, it's aligned with how I write code.

For vertical height, it does its best to reduce the unnecessary space and try to maximize use of horizontal space.
If a line can be reduced to a single line, it will do so.
This is probably the most noticeable change to my code style.
I often choose to multi-line trivial dictionaries, for what I perceive to be more readable.
And it'll join it, into one single line.
This is jarring but I think I can accept this over time.
It's no less readable but is more condense and can fit 2 or 3 extra lines of code onto the screen.

Pytest parametrize unit tests are an example of where I'll need to figure something out:

```python
@pytest.mark.parametrize('input,output', [
    (1, True),  # This is for blah
    (2, False), # But not this
])
```

Black will collapse this to reduce the vertical height:

```python
@pytest.mark.parametrize(
    'input,output', [(1, True), (2, False),]
)  # This is for blah But not this
```

It's less readable but not any more dense.
Test code tends to have lots of boilerplate so maybe this will end up being more useful, to fit more boilerplate onto
the screen at one time.
In practice, if your unit test set is short enough to fit onto a single line, it's trivial enough to read.
The annoyance on my part is primarily aesthetics and a change to my workflow.

## Spaces Between Stuff

Spaces around binary operators help with readability.
Pylint and Flake8 complain about this and it's always annoying to handle manually.
So to have Black take care of this is just dandy.

It will remove extraneous spaces after parenthesis or brackets.
Just dandy.

# String and Numeric Literals

## Prefixes

Black will standardize string and numeric literal prefixes, using lowercase lettering.

## Quotes

Black prefers using double quotes instead of single quotes.
The reason is to handle apostrophes, which inevitably require user to switch to double quotes or to use backslash
escaping.

For US keyboards, this requires the use of shift key, which is why I prefer single quotes.
At first, I was a little peeved by this and used the `--skip-string-normalization` option to disable this.
But then I read this quote from the docs and maybe it doesn't really matter to me:

> My recommendation here is to keep using whatever is faster to type and let Black handle the transformation.

Just use whatever you want and let Black handle it.
Seriously, just use whatever, write shittily formatted code, and Black will take care of things.
Just like ESLint!
