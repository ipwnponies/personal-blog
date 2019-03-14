---
title: TravisCI and Tox
categories:
- programming
tags:
- travisci
- github
- tox
- python
---

I recently had the displeasure of configuring `TravisCI` to work with `tox`.
`TravisCI` has a "build matrix" system, where you can configure different environment conditions to test your code.

Oh hey, that sounds just like `tox` you said. Yup.

However, `tox` runs anywhere.
I don't get to develop on `TravisCI` machines.
So we have to support both systems in a crude manner, at least until `TravisCI` has better native support.

# Tox environments

I use tox environments to test pytest-antilru under different conditions:

* Python 2.7/3.5/3.6/3.7
* `backports.functools_lru_cache`
* `functools32.lru_cache`

This is done using environment factors, as demonstrated in [pytest-antilru tox.ini]:

[pytest-antilru tox.ini]: https://github.com/ipwnponies/pytest-antilru/blob/a78af3da55c6b71e1c2172c3368c70f6f7d93713/tox.ini#L2

```ini
[tox]
envlist = py{27}-{backports,functools32}-pytest{2,3,4},py{35,36,37}-pytest{2,3,4},project_tests
```

These work like bash brace expansion, which results in a cartesian product.
Tox documentation has [more details].

[more details]: https://tox.readthedocs.io/en/latest/config.html#generating-environments-conditional-settings

What results is an expanded list of many combinations:

```sh
$ tox -l
py27-backports-pytest2
py27-backports-pytest3
py27-backports-pytest4
py27-functools32-pytest2
py27-functools32-pytest3
py27-functools32-pytest4
py35-pytest2
py35-pytest3
py35-pytest4
py36-pytest2
py36-pytest3
py36-pytest4
py37-pytest2
py37-pytest3
py37-pytest4
project_tests
```

# TravisCI Build Matrix

`TravisCI` supports a very similar idea, called [build matrix].
Many of the config parameters accept lists, which expands in cartesian product manner.

[build matrix]: https://docs.travis-ci.com/user/customizing-the-build/#build-matrix

When different python version is set, `TravisCI` is using `pyenv` internally to switch.
We could use this knowledge to our benefit but it's real janky.
Instead, we should play nice and instead have `TravisCI` invoke only the applicable tests for the python version.

Unfortunately, `tox` doesn't support globbing on environments.
We can't simply tell `TravisCI` to run all `py27` factors, we need to explicitly pass every single env to `tox`.
Ugh.

Enter this [mess] that I stole from [flake8].
I think mine is a little bit more readable (I try to avoid too much bash magic).

[flake8]: https://github.com/jamescooke/flake8-aaa/blob/2e9059472775e54413acd68fc7ced5b5e6bd86c3/.travis.yml
[mess]: https://github.com/ipwnponies/pytest-antilru/blob/v0.2.0/.travis.yml#L13-L16

```yaml
script:
  # Travis only supports one python version per environment (pyenv).Tox doesn't support running all permutations of a
  # factor. They found each other, though the magic of grep and sed.
  - export PY_VERSION=$(echo "${TRAVIS_PYTHON_VERSION}" | sed 's/\.//')
  - export TOXENV=$(tox --listenvs | grep "py${PY_VERSION}-" | tr '\n' ',')
- tox
```

1. We first get the python version from environment.
   This corresponds to '3.5' or '3.7-dev' strings.
1. Some string manipulation to format it to `tox` python version format (two-letter value).
1. Grep through the possible tox environments for the ones that apply.
1. More gross string manipulation because tox only accepts comma-delimited string.
1. Set `TOXENV`. `tox` reads from several places to get the [environment list].

[environment list]: https://tox.readthedocs.io/en/latest/config.html#conf-envlist

With all this set in place, `TravisCI` generates one test runner for each python version in parallel.
It's nice because failures will be isolated and easily identified from `TravisCI` build email.
And separate logs is nice.

But I really wish these two would play better with each other, more native support.
