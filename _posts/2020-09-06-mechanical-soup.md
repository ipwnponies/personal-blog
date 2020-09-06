---
title: Mechanical Soup
categories:
- programming
tags:
- python
- automation
- scripting
---

There's a `python` library call [`MechanicalSoup`][1].
It glues together `BeautifulSoup` and `Requests`, to allow for automating parsing and submitting of forms.

[1]: https://github.com/MechanicalSoup/MechanicalSoup

## What does it do

`Requests` deals with HTTP requests, which is stateless.
`BeautifulSoup` parses html pages.
If you need to emulate a user that is submitting form information and progressing through a web session,
you'll end up writing `MechanicalSoup`.

It adds state (missing from `requests`) and helpers for form handling (specialized use of `beautifulsoup`).

## Why not use Selenium

`Selenium` is a web driver, which means it controls a real web browser.
This makes all the browser implementation quirks are preserved.
`Selenium` is simply clicking on behalf of the user.
Spinning up and controlling a web browser process is very expensive.

`MechanicalSoup` is a lightweight Selenium stand-in.
It's stitches together web requests and only speaks HTTP.
So you clearly will not have Javascript or CSS or whatever quirks come with a full-browser instance.

## When to use

Only use this package if you are submitting forms.
It's a very special-purpose, abstraction on top of `beautiful soup`.
But submitting forms is a common operation for web pages.

If you need to do anything else, you'll end up fallback to the underlying `beautifulsoup` API.

If the site relies on Javascript or CSS or other quirks, then you must use `Selenium` and pay the cost of complete page rendering.
