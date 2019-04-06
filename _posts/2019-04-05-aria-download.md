---
title: Downloading Files Faster With Aria2
categories:
- programming
tags:
- tools
---

I found this nifty `wget`-like tool named [`aria2`].
`wget` can only download a file with a single connection.
`aria2` is capable of chunking the target file and downloading each chunk with a separate connection.

[`aria2`]: https://aria2.github.io/

Depending on the server and speed limits per connection, this can increase the throughput greatly.

# Why Are Multiple Connections Faster

The internet is a network of devices.
With a single connection, data is traveling through a single pathway (not completely true) and can be bottle-necked
along this journey.
Multiple simultaneous connections open up for more pathways.

More accurately, there are usually middle-men (web hosting providers) that limit bandwidth per connection and this is a
means to circumvent that.
In a true and ideal internet, a single connection would be sending small packets through many different paths of the
network (by design of the internet), allowing for maximizing throughput.

Note that there will not be a speed up if bandwidth is limited on either the downloader or source server.

# How-To

```sh
aria2c --max-connection-per-server 16 --split 16 https://example.com/big-ass-file
```

This splits the file into 16 connections.

# Resuming Partial Download

With `wget --continue`, you can continue a partially downloaded file.
This is implicit behaviour with `aria2` (sane defaults!).

While downloading with `aria2`, you'll notice there are two files:

* the target file. This is really just a placeholder to reserve space.
  It gets swapped with final file when  download is complete.
* a temporary that contains the partial data and metadata for resuming.
  This file is cleaned up automatically when download is complete.
