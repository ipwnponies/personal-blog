---
title: Patching Snes Roms
categories:
- technology
tags:
- snes
- emulation
---

International Patching System (IPS) is a file format for applying patches to snes roms.

Patches are smaller to distribute.
Also, there are no concerns regarding copyright law when distributing a patch, as opposed to the distributing a
post-patched rom.

# File Format

The [file format][1] is very simplistic diff patch.
It's similar to git patches but binary.

[1]: https://zerosoft.zophar.net/ips.php

Section | Size | Description
-|-|-
Offset | 3 bytes | Position in rom to start patching
Size | 2 bytes | Amount of data to be patched
Data | Amount of bytes specified by size | Bit dump of data to overwrite

As you can see, this is very simple file format.
There's no checksum, compression, or rom validation.
It will literally overwrite those blocks of the rom.

The only way to validate the rom is complete playthrough (100% rom coverage).

# Tools

[Lunar IPS][2] is a simple tool to apply a patch to a ROM.
It's how you apply rom hacks.

[2]: https://fusoya.eludevisibility.org/lips/

# Rom Expansion

Some rom hacks add more data and the rom needs to be resized.
The rom data section is enlarged, while keeping headers and footers intact.

[Coilsnakes][3] is a tool for editing *Earthbound* and it features the ability to expand a rom.

[3]: https://github.com/mrtenda/CoilSnake
