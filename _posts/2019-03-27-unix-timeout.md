---
title: timeout cmd
categories:
- programming
tags:
- unix
---

I was investigating performance regression, to do with caching (or missing places that needed caching).
I would run `pytest` and wait for it to complete and see if the execution time was longer than baseline.
This ended up being real tedious because it's hard to tell the difference between 20-25 seconds and 35-40 seconds.
Then I discovered `timeout`.

```sh
timeout 30s pytest tests/
```

The `timeout` command accepts a time duration, after which it will send a signal to the spawned process.
The timeout can be specified in different units (e.g. 1h) and the signal can be changed from the default of `SIGTERM`.
There's also an option to send `SIGKILL` after sending the first signal, to forcefully kill the process if needed.
