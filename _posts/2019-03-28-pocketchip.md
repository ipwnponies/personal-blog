---
title: PocketCHIP
categories:
- programming
tags:
- hardware
---

For hackathon at work, I wanted to play around with PocketCHIP that I bought a few years ago.

The parent company is defunct so I expect to run into issues and have little support.

# Connecting

The first thing I did was connect this to my laptop.
If successfully connected, there's a `/dev/tty.usbmodem1234` device that we can connect to.

Unfortunately, my list came up empty.
The USB cable turned out to be the culprit, it was a power only-cable.
Switching to a proper cable I was able to connect:

```sh
$ screen /dev/tty.usbmodem1234 -s 115200

Debian GNU/Linux 8 chip ttyGS0

chip login:
```

D'oh, I forgot my password.
The docs were missing but I was able to find the right combination for the root user.
I promptly created my own user and password, locking down the root.

# Connecting to Wifi

`nmtui` is the network manager TUI.
But it looked like trash for some reason.

![nmtui](/assets/nmtui.png)

I was able to find a forum post but it was on the now-defunct site.
Thank-god for the [wayback machine]!
The issue is the term is "vt102" and now someone from the last 3 decades.
A quick workaround is to set `TERM=ansi` and it renders decent enough to navigate the unicode characters.
From here, it is straight-forward to connect the PocketCHIP to wifi.

[wayback machine]: https://web.archive.org/web/20180919054813/https://bbs.nextthing.co/t/garbled-output-when-running-nmtui-on-mac-via-screen-usb/2415/2

# Installing Packages

Now we can update apt packages.

```unix
$ sudo apt update
Ign http://http.debian.net jessie-backports InRelease
E: The method driver /usr/lib/apt/methods/https could not be found.
N: Is the package apt-transport-https installed?
```

The issue is switching from http to https, the whole TLS 1.0/1.1 end-of-life migration that happened between 2015-2018.
Installing [`apt-transport-https`](https://askubuntu.com/a/517693) as instructed fixes this.

The *next thing* apt repos no longer exist but someone has put up a [mirror](http://chip.jfpossibilities.com/chip/debian/).
All we need to do is update `sudoedit /etc/apt/sources.list`:

```text
deb http://ftp.us.debian.org/debian/ jessie main contrib non-free
deb-src http://ftp.us.debian.org/debian/ jessie main contrib non-free

deb http://security.debian.org/ jessie/updates main contrib non-free
deb-src http://security.debian.org/ jessie/updates main contrib non-free

deb http://http.debian.net/debian jessie-backports main contrib non-free
deb-src http://http.debian.net/debian jessie-backports main contrib non-free

deb http://chip.jfpossibilities.com/chip/debian/repo jessie main
```

We need to update the last entry and point it to the new mirror.

# Where Next

I want to set this up as a pi-hole server (DNS blocking) and also as a lightweight server instance for running small
python scripts on a cron.
I don't really know how well these options will be supported vs. using a raspberry pi.
But what do I have to lose, I already bought this for $9.

---

# Windows

While this was trivial to connect to on OSX, Windows requires more setting up.
Drivers need to be installed and they can be gotten from the docs ([internet archive]).

[internet archive]: https://web.archive.org/web/20180528102419/https://docs.getchip.com/chip.html#windows-specific

I've always been curious why Windows needs manually installed drivers, while unix just magically works.
Is this complacency on Windows, for not including common drivers by default?
A design decision to reduce the number of drivers installed by default, maybe to reduce surface vector for exploits?
Or is linux working hard to proactively get drivers installed by default.

Either way, linux is clearly the winner here:
the vendor designed the device and knows/wrote the driver that is required to operate;
the OS can detect when devices are plugged in and decide which driver to load;
the user doesn't give a shit about the details, they just want their shit to work.
Whereas in Windows, the user is required know what driver the device, because they're the subject matter expert!?

Anyways, after the drivers are installed, the rest of the steps are the same as before.

# Pi-Hole

Installing `pi-hole` was easy, using the install-script.
Unfortunately, the chip was no longer supported.
While it did finish installation, nothing was working.
In fact, DNS resolution stopped working altogether.

After debugging a bit, I gave up.
I'm not a systems admin expert and I don't have the time nor inclination to pursue this.
I'd rather get a Raspberry Pi Zero (supported) and call it a day.

## Uninstalling

```sh
pihole uninstall
```

This seemed to work.
But the cleanup was not at all clean.
There's an [open github issue with a fix][1] to clean up the entries modified by `pi-hole`.
Remove leftover settings in `/etc/dhcpcd.conf`.

[1]: https://github.com/pi-hole/pi-hole/issues/2148#issuecomment-435703330

# So no pi-hole, what next

I guess I'll use the chip for more basic things.
Like a lightweight cron server.
Or entryway to gpio programming.
Kinda like in Terminator 2, when Edward attaches a PDA to an ATM or keypad entry.
