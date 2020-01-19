---
title: Python Coverage, TravisCI, and Coveralls
categories:
- programming
tags:
- python
- coverage
- travisci
---

I  setup coverage for [pytest-antilru] and wanted to report this to [coveralls].
This was much harder than it had to be because TravisCI and Coveralls documentation sucks.
I share the same sentiments as this [blog post].

[pytest-antilru]: https://github.com/ipwnponies/pytest-antilru
[coveralls]: https://coveralls.io/
[blog post]: http://blog.pythonity.com/coveralls-with-travis-ci-tox-pytest.html

## Coveralls

Coveralls is a site that accepts and parses different coverage data formats.
It's provides a nice way to view real-time coverage information, without having to go to `master` branch in TravisCI and
parsing the test output manually.
You can also add a badge with the stats to your project's documentation, which is pretty.

## Integration with TravsCI

Here's where the docs started to quickly break down.
You need to set the coveralls API token to submit coverage data.
But if you're using TravisCI, this magically exists, somehow.
It's poorly documented in the sense that it seems to be written by the same user for both TravisCI and Coveralls, where
they never explicitly state that TravisCI has integrations but at the same time acknowledge it magically just works™.

The takeaway here is:

* If you're using TravisCI, you only need to call `coveralls` client and it will be able to communicate.
* If you're **not** using TravisCI, you need to include the API token as an environment variable.

## python-coveralls vs. coveralls-python

> `python-coveralls` by Andrea De Marco `coveralls-python` by Ilya Baryshev
> Instructions in README’s.

Yeah..., these instructions are worthless.
In the end, I chose `coveralls-python` because that blog post determined it had a tiny bit more features.
And it was the `coveralls` package on PyPI.

I install this in the `.travis.yml`:

```yaml
install:
- pip install tox coveralls
...
after_success:
- coveralls
```

My python tests were already being run with `coverage`, which produces a `.coverage` data file.
`coveralls` reads and uploads this file to `coveralls.io`.
