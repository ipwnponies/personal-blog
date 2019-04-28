---
title: Filesystem Mocking with pyfakefs
categories:
- programming
tags:
- python
- testing
---

[`pyfakefs`] is a python testing library for mocking out filesystem IO.

It's common to mock out `open()` so you don't accidentally create files during unit tests.
But what about `pathlib.Path.open()`?
What about other libraries that wrap it?

This is to filesystem testing as [`responses`] is to [`requests`].

[`pyfakefs`]: https://jmcgeheeiv.github.io/pyfakefs/release/intro.html
[`responses`]: https://github.com/getsentry/responses
[`requests`]: https://2.python-requests.org/en/master/#

# Preventing FS Leaks

I like to set up a `pytest` autouse fixture for `responses`, so that the default mode of operation is to block all
network requests.
This works like a whitelist, where each test must explicitly setup the expected network calls.
This prevents accidentally making real requests during tests.

We can do the same here.
`pyfakefs` comes with a `pytest` fixture named `fs`.
It works well to patch out most uses of common filesystem libraries (`os.path`, `pathlib`, `io`, `builtin`).

```python
# conftest.py
@pytest.fixture(autouse=True)
def mock_fs(fs):
    yield
```

# Gotchas

## Reloading Modules

There are pitfalls due to the way `pytest` and python imports work.
`pytest` first collects all tests (imports them), then run tests with fixtures.
After importing a module, it's too late to monkey patch.

```python
# moduleA.py
path = open('path')

def foo():
  return path.read()

# moduelA_test.py
def test_foo():
  asset foo() == 'This is actual file contents on disk!'
```

`pyfakefs`'s solution is to dynamically reload the modules.
You mark the modules that have import-level side-effects related to file IO and tell `pyfakefs` that it'll need to
reload them to properly mock out.

[solution]: https://jmcgeheeiv.github.io/pyfakefs/release/usage.html#modules-to-reload

```python
@pytest.fixture(autouse=True)
def mock_fs():
    """ Fake filesystem. """
    with Patcher(modules_to_reload=[xdg]) as patcher:
    ¦   yield patcher.fs
```

In this example, I've marked `xdg` to be reloaded.
`xdg` generates the [`XDG_CONFIG_HOME`] at module-level.
`pathlib` needs to be mocked out by `pyfakefs` before you even import `xdg`.

[`XDG_CONFIG_HOME`]: https://github.com/srstevenson/xdg/blob/ec570eee85d2750ac83e60eeb7e1ac592c8166a8/src/xdg.py#L106

## Patching Third-Party Libraries

Some libraries will have custom file IO functionality that doesn't use any of the common libraries.
In this case, you can use [`modules_to_patch`] to mock out functions.

[`modules_to_patch`]: https://jmcgeheeiv.github.io/pyfakefs/release/usage.html#modules-to-patch

I haven't personally used this but it seems like a special case of `mock.Mock` but integrated into the fake filesystem.

## Debugging with pudb

`pudb` is a ncurses TUI for debugging.
It saves preferences as files on disk and also uses `stdin` and `stdout` as files.
`pyfakefs` did not like this at all.

While you could mark all related modules with [`additional_skip_names`], this is messy if you end up using those same
modules for reals.

[`additional_skip_names`]: https://jmcgeheeiv.github.io/pyfakefs/release/usage.html#additional-skip-names

What you actually want to do is to temporarily pause and allow `pudb` to access the real filesystem.
This is done by pausing the fake filesystem before invoking the debugger but resuming it afterwards.

```python
def test_foo(fs):
  fs.pause(); pu.db; fs.resume();

  actual = foo()
  assert actual == 1
```
