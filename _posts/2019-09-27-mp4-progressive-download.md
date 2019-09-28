---
title: Video Streaming and Progressive Playback
categories:
- technology
tags:
- formats
---

Have you wondered how web browsers stream videos?
Am I dating myself if I said I remember when "video buffering" was a problem?

Video streaming technology has gotten quite advanced in the last decade.
We all take for granted that it should be possible to play a video and interact with it as though it were a local file.
This is thanks to the advancement in progressive playback technologies.

I read over [this blog][1] to get a high-level understanding.

[1]: https://fabiensanglard.net/mobile_progressive_playback/index.php

# MP4

`MP4` container technology is based on Apple's `Quicktime` format.

It's ubiquitous as a video format for streaming.

# File Format Layout

The rough file layout is:

- metadata header
- `moov` atom, which is index to keyframes
- data payload, the actual video content

But you can also find it as:

- metadata header
- data payload, the actual video content
- `moov` atom, which is index to keyframes

Why?
The `moov` index can only be written after the video data has been produced.
It's size will be variable as it depends on how much video data is produced.
Many video editors write this one at the very end of the video encoding process.

To write the `moov` atom before payload would require making space in the file by shifting everything.
Or pre-allocating space, which can lead to wasted space if not used.

# Progressive Playback

Progressive playback is the concept of streaming videos out of order.
You can "progressively" download and play any part of the video.
There's no need to download the video in sequential order.

Why is this impressive?
Reading file is random access, it's sequential access:
read the first byte, then the second byte, and so on.
It's nonsensical to randomly read byte 250 and expect to be able to correctly interpret the data there.

An analogy is tape drive technology.
To seek forward, you still need to wind through the tape, it's not instantaneous.

# HTTP Request Range Header

When a browser begins to stream a video, it will send a request to web server with the [`Range` header][2].
This requests partial content ([206][3]), the video header data.

[2]: https://en.wikipedia.org/wiki/List_of_HTTP_header_fields#range-request-header
[3]: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#206

If the `moov` atom is found in this initial request, its information is used to find the keyframe for initial request.
Then a subsequent request is made to web server, requesting data with offset.
The web server will return video data from the middle of the stream.

If the `moov` atom is not found, then the browser knows it's been written to the end of the file.
It will need to make another partial request to get the index information, before the video can start streaming.
This is an extra round-trip that is similar to the cost of a cache miss.

Writing the `moov` atom at the beginning front-loads the cost to encode-time.
Typically videos are read a lot more than written so it's generally a good idea to write the `moov` atom to the front.
