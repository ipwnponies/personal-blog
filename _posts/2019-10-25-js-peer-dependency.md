---
title: JavaScript Packaging With Peer Dependencies
category:
- programming
tags:
- javascript
- packaging
---

# Peer dependencies

In js package world, packages are installed with their own, isolated hierarchy of components.
This is nice because it means that there can not be version incompatibilities.
The downside is that there can be a lot of duplication and there's tooling that exists to have shared, compatible
packages symlink.

A peer dependency is when a package declares that it has a dependency that needs to be coupled with the installed version.
That is, don't install and use a siloed dependency, we want to use a shared one.

There are strong use cases for this: different versions of `React` cannot be used at the same time, it's not like each
component is going to roll their own `React`.

Here's a very [concise explanation][1].

[1]: https://stackoverflow.com/a/56289419

## Comparison to Python `Virtualenv`

There is only one version of a package installed in a `virtualenv`.
By definition, this means that all dependencies are "peer dependencies".

This comes with all the downsides of peer dependencies, such as version incompatibilities.

## Lack of Tooling

There's a distinct [lack of tooling][2] in this space.
It's up to the dev to check and verify that they are installing compatible versions.

[2]: https://github.com/yarnpkg/yarn/issues/1503

`yarn` will throw warnings when it notices that peer dependencies are not correctly satisfied but it doesn't cause failures.
Developers must be vigilant to resolve all warnings when installing peer dependencies.
