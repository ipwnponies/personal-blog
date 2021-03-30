---
title: ISP Speed Tests
categories:
- programming
tags:
- automation
---

I recently switched internet service providers.
While the installer guy was here, he gave some tips to ensure I would be making full use of the increased bandwidth:

- elevate the WiFi router off the floor (apartment concrete floor)
- switch to 5 GHz frequency

My initial thought was: "how could this make any difference?"
And thus begins the scientific process.

## Changes for higher bandwidth

### Elevate the WiFi router off the floor

I put the router on the floor out of convenience.
The modem's jack outlet is in an area of the room without suitable furniture nearby.
So I just left it there and didn't think much of it.

Having it on the floor was supposedly not good for signal propagation because the floor of this apartment is made of concrete.
Concrete and brick materials significantly attenuate wireless signals because they absorb or scatter it.
I couldn't find much recommendations or material on the web; most search results focus on discussing signal coverage
through concrete walls of a room or between floors of a house.

When it's on the floor, half of the omni-directional signal is sent into the floor and absorbed by the concrete.
But when elevated, maybe the signal is able to reflect off other surfaces?

### Use 5 Ghz instead of 2.4 Ghz

[802.11ac] is a modern wireless networking standard.
It extends wireless N (802.11n), whose prominent feature was the use of the 5 GHz spectrum.
Many routers and receivers are considered "dual-band" if they can operate at both 2.4 or 5 Ghz frequencies.

[802.11ac]: https://en.wikipedia.org/wiki/IEEE_802.11ac

The 5 GHz spectrum is another spectrum allocated to consumer wireless uses.
It's newer, in the sense that the FCC opened up access to it in recent memory.
As there are much less existing devices, it's not as congested as the 2.4 GHz band.
2.4 GHz is [shared with microwaves, cordless phones, garage door openers][ism], etc.

[ism]: https://en.wikipedia.org/wiki/ISM_band#Common_non-ISM_uses

Higher frequency signals allows for higher bandwidth.
This is identical to radio, where FM radio has higher fidelity than AM radio.
However, higher frequency signals are more attenuated when passing through matter.
AM radio has higher coverage area than FM radio and is commonly provides higher coverage over rural areas.
This is one reason why the 5 G cellular network (fifth generation, not at all indicative of its frequency) has had a
hard time gaining traction:
even though it has higher bandwidth, the lower coverage requires many more cell towers.

## Terminology

Let's define some common networking terminology before we start.

### Bandwidth

Bandwidth is the rate of data being moved.
It's the primary metric that is touted by ISP and network providers, especially in their advertising.

When you're streaming a movie or downloading a video game, the goal is to move a pile of data from the source to your computer.
You only care about the total time it takes to move 100% of the content, not how long each fragment takes individually.

If we use a moving houses as an analogy, the "speed" (latency) of the moving truck is not as important as the capacity (bandwidth).
If you can load up the truck and make one large trip, the bandwidth will be high.
Whereas a sedan would have its throughput bottle-necked by the smaller trunk space.

### Upload vs. Download

Consumer usage tends to skew download-heavy.
As such, many ISP will provide high bandwidth for download but much less upload bandwidth.
This asymmetric setup is quite common.

However, with the modern world doing remote work and video-conferencing, this skew needs to shift back.
Without sufficient upload bandwidth, you'll hit saturation and your friends will see degradation in quality of your streams.
Meanwhile, you have capacity for download and can receive their high-quality video streams just fine.

This leads to the dreaded situation I've continually encountered over the years, far too many times:

> It's not my internet, I see you just fine.
>
> My 15 year-old router, that is 802.11 g and supports a dozen devices, is totally not the problem.
> Also my ISP is trash because shitty Canadian ISPs.

Yes, many Canadians are unaware that their internet is notoriously shitty and probably in the bottom 20% of the world.
And that it's not anywhere near the top 20%, like most of Canada's other quality of life metrics.

### Latency

Latency is the response time.
It's the "speed" of your connection and measure of how fast individual bytes of data move within your network.
Latency is the speed of a sports car vs. a moving truck, capable of moving 200+ km/h.

Latency is very important when it comes to real-time applications, such as video conferencing or online gaming.
Video data is not useful when it's delayed as it disrupts the conversations.
Similarly, delayed data in online gaming is highly detrimental, as other players in the game will continue playing
without you.
You'll be either a dead-weight teammate or an easy opponent.

Non-real-time applications, such as Netflix, do not require low latency and only need high bandwidth.
To mitigate high latency, it can pull data into a buffer earlier than it's needs.
It'd be like planning to go to an event 1 hour early, because the rush-hour traffic is variable.

A related concept is *loaded* latency.
Loaded latency the measurement while the system is under stress and congestion when other things are being downloaded at
the same time.
It indicates how stable the network continues to perform under stress and congestion.
Imagine this is the latency during rush hour congestion:
a car will experience high latency, while a motorcycle can still maintain low latency by lane splitting:

- if the roads are too tight and restrictive, it's too dangerous to lane split and the latency of the motorcycle is same
as the car
- if the roads are wide, a motorcycle can easily lane-split and bypass traffic, with little cost to latency

## Experiment Setup

So I decided to run tests.
The different variables that I've manipulated are:

- router elevation
- frequency

And for each, I measured results across two speed test sites (fast.com and speedtest.net) and between ISP.
The metrics measured are:

- download bandwidth
- upload bandwidth
- latency (unloaded)
- latency (loaded)

### speedtest.net vs. fast.com

Ookla (speedtest.net) is the OG internet speed site.
It shows results for download, upload, and latency.

Netflix launched fast.com in 2016 to make it easier for users to test internet speeds.
It focuses on a simple and clean UI.
Ookla results are clearly designed for a tech-savvy, power user and can be intimidating the general population.
There are many terms and numbers that are only useful to power users and those are tucked away in teh UI.

Both seem to be serviceable.
I wanted to throw both in to mitigate against ISPs cheating.
I've heard of how some ISPs can detect when speed tests are being performed via a whitelist of known speed test servers.
And they temporarily disable throttling, which skews the real-world-ness of our results.

### Multiple Runs

Besides performing multiple rounds for more data points, I was curious to see if the tests would improve or degrade over
several consecutive runs:

- if it sped up, maybe this indicates some sort of caching behaviour going on
- if it slowed down, this could indicate service throttling

Either way, we ideally want very little variance between each run.
This indicates a stable and consistent connection as it becomes loaded over time.
In the real-world, this means you have a dependable connection, which becomes more important as we use the internet for
real-time services.

## Running the Experiment

### Approach

I started out naive and was going to manually click some buttons for the webpages for a couple runs.
Then I did some math:

```none
2 elevations * 2 frequencies * 2 ISP * 2 speed tests sites = 16 combinations
```

But a true scientist needs repeatable results!
So **3 runs** each is **48 combinations**.

I could manually perform all 48 runs and transcribe the results by hand.
But that sounds like hard labour...

### Scraping speed test results

So time to automate some of this work.

What have my shitty web skills taught me?
There's a [mutation observer] web API that lets you add listen to changes on a DOM element.
If we can target a "test completed" event, we can query and parse the elements that contain results.

[mutation observer]: https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver

Fortunately, both sites have a container element that changes CSS classes when testings are in progress and completed.
By setting a callback on this container, we can read out the results automatically when the test completes.
This makes the test run "fire and forget", which is a big win for automation.

You could even script it to perform consecutive test runs sequentially!
Imagine just running a function and coming back in 15 minutes with all results ready to transcribe.
Unfortunately, I only came up with this brilliant idea just now.

I did this all in the browser console.
This was easier than setting up a headless browser.
One of the limitations is that [copy][firefox-console-helpers] cannot be used non-interactively, such as during event
handling of the callback.
So instead, I printed out the comma-separate values to the console output to allow for copy-pasting into a spreadsheet.
Now thinking about it, I could have assigned the output to a global variable (`output`), allowing me to call
`copy(output)` to automatically fill the clipboard.
Oh well, live and learn to automate better.

[firefox-console-helpers]: https://developer.mozilla.org/en-US/docs/Tools/Web_Console/Helpers

### Analyzing data in a spreadsheet

Once we've copied the results over to a spreadsheet, we can use the [SPLIT][spreadsheet-split] spreadsheet function to
denormalize a single CSV value to multiple cells.

[spreadsheet-split]: https://support.google.com/docs/answer/3094136?hl=en

From there, it's quite trivial to produce a fully denormalized table.
And then it's a just excel-ing and spreadsheeting.

All this done without without having to manually enter 144 results (48 runs \* download + upload + latency results).

### fast.com script

<!-- markdownlint-disable MD033-->
<script src="https://gist.github.com/ipwnponies/88bcfd19a029a84dc1b0fdc4ae713e11.js?file=fast-scraper.js"></script>
<!-- markdownlint-enable MD033-->

### speedtest.net script

<!-- markdownlint-disable MD033-->
<script src="https://gist.github.com/ipwnponies/88bcfd19a029a84dc1b0fdc4ae713e11.js?file=speedtest-scraper.js"></script>
<!-- markdownlint-enable MD033-->
