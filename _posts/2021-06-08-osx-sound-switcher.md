---
title: OSX Sound Output Switcher
categories: programming
tags:
  - automation
  - osx
---

I wrote a simple AppleScript to change the audio source in OSX.
This was useful because I have several sources available for sound at any given time:

- headphone (3.5 mm jack)
- laptop speaker (internal)
- airpods (bluetooth)
- monitor speakers (hdmi)

Generally I know which one I want to use, based on whether it's plugged in or not:

- if the airpods are connected, then we probably want to use those
- if external headphones are plugged in, we want to use those
- if the laptop is docked and attached to the external monitor, we will use those speakers

But sometimes I want to use the internal speakers.
This can be because I don't feel like unplugging the headphones.
I've written a script that will toggle between the internal speakers and the either of the other available sources.

<!-- markdownlint-disable MD033-->
<script src="https://gist.github.com/ipwnponies/2eabf2816d62139718133fd8502a231c.js"></script>
<!-- markdownlint-enable MD033-->
