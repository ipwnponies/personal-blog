---
title: Raid - Redundant Array Of Independent Disks
categories: technology
tags:
  - hardware
  - performance
  - disks
---

_Redundant Array of Independent Disks_ ([RAID][1]) is a technology for connecting together many physical hard drives
into a single operating unit.
The motivation to do so can be for:

- performance
- reliability
- availability
- capacity
- redundancy

[1]: https://en.wikipedia.org/wiki/RAID

## Reasons to Use RAID

### Performance

Performance is improved by employing more hard drives to service a single request.
This is your typical multiprocessing motivations, where hard drives are analog to processors.
Even with modern SSDs, the scale of data we operate is often higher than the transfer rate of a single drive.
For video editing, 4K 60 FPS video requires 1.5 GB/s [^1].
For scientific computing, we might be processing GBs of raw data.
HDD are operating around 150 MB/s and SDD are 500 MB/s.

[^1]: https://en.wikipedia.org/wiki/Uncompressed_video#Data_rates

### Reliability

Reliability is improved with RAID as your data (or part of it) is written to more than a single location.
RAID also allows you to use less reliable HDD and have assurance that complete data loss will be mitigated.
A CPU analogy is that we all can't afford to use the fastest single-core Intel processor but we can use slower
multi-core processors to get the job done.

### Availability

Certain RAID setups allow for multiple drive failures.
This allows the array to remain online, while the failed drive is replaced and rebuilt.

### Capacity

Capacity of a logical volume can be larger.
RAID is an abstraction layer to connect physical hardware to logical software.
If you want to write a big ass file to disk, connecting many small disks via RAID will allow this to seamless occur.
Otherwise you would be required to manually split up the data and manage the data.

### Redundancy

Redundancy is probably the main reason to use RAID.
By employing parity bits, you can recover from disk failures without data loss.
How does this work?
A parity bit is written for each set of data.
The data on the failed disk can be recovered using this parity bit information.
When a physical fails, it can be complete data loss.
Using RAID makes this a more gradual process, as it takes multiple disk failures to take out the array.

## Complexities Introduced By RAID

Simply using RAID doesn't solve all problems, it introduces its own.
You need to be cognizant, otherwise poor practices can undo the advantages of RAID.

### Correlated Failures

When building a RAID array, you're likely to use similar drives.
Why?
The size of a partition is capped by the smallest drive in array.
The speed may be limited by the slowest drive, throttling the faster drives.
The local maxima is generally by having an array of identical drives.

Similar drives will share the same characteristics.
This include lifetime characteristics.
If there is a disk failure, what are the chances of a second drive suffering the same fate?
And what it happens while you're rebuilding, effectively dooming you from the time of first disk failure.
This is called correlated failure and it's what you really wanted to avoid by having redundancy in the first place!

### Rebuild Times

While drives have grown in capacity, the error rate and transfer speeds have not kept pace with the scaling.
In real world terms, this means larger drives take longer to read and they will experience larger absolute number of errors.
These are two things are not things you not want to hear at all, if you need to rebuild a drive.

A scheme like RAID 6 increases fault tolerance but it doesn't solve it, just throws more money to try to alleviate the problem.

### Atomicity

Atomicity is something we take for granted.
RAID can amplify this problem as you're involving more hardware (RAID controller) and it's required to write more
things (parity).
More moving parts gives more opportunity for data corruption or writes to be dropped.

## RAID Configuration

There are several [standard RAID levels][2].

[2]: https://en.wikipedia.org/wiki/Standard_RAID_levels

### RAID 0

In RAID 0, data is evenly partitioned across all disks.
Blocks of data are round-robined across the disks.
The usable size of a partition will be limited to the size of the smallest disk in array.

This setup has no redundancy and failure of a single drive will take out the whole array.
The chance of failure is even higher than for independent disks because there are more moving parts to get right.
Contrast this with simply keeping the drives independent: if one drive fail, the other drive is unaffected.

The motivation for using this is high read and write performance.

The best use case is when you need high performance and can tolerate data loss.
This makes scientific computing a good candidate, as you are working with large amounts of data that does not fit into memory.
The work being done is processing so disk failure is only intermediary data loss and requires recomputing.

### RAID 1

In RAID 1, data is mirrored across disks.
Similar to RAID0, the max size of the array is limited to smallest disk.

Because data is mirrored, any disk can be used to read data, increasing read performance.
There is no change in write performance, same amount of data needs to be written per-disk.
There is high redundancy as data is cloned on every disk.

This is a naive way to achieve redundancy and is very inefficient.

### RAID 2/3/4

In these configurations, data is striped across the array and a drive is dedicated to the parity bit.
The difference is the level they operate at:

- RAID 2 is bit-level
- RAID 3 is byte-level
- RAID 4 is block-level.

Having the parity bit on a dedicated drive creates a bottlneck, as the parity bit is always written to.
This also increases the stress and shortens the life of that drive, relative to the rest of the array.

#### RAID 2

One unique characteristic of RAID 2 is that it uses [Hamming codes][hamming-code] as the error-correcting code (ECC).
Hamming codes requires `log(N)` bits for the ECC, this translates to additional `log(N)` drives to store
the hamming code bits.
i.e. If you are partitioning across 4 data drives, then there must be 2 error-correcting code (ECC) drives.
If partitioning across 16 data drives, this requires an additional 4 drives.

[hamming-code]: https://en.wikipedia.org/wiki/Hamming_code

With data striped at the bit level, RAID 2 cannot service concurrent requests.
All the drives in array will need to be in the same position, reading the bits to reconstitute the byte or block of data.
The controller will synchronize the disks, so they spin at same speed, to move the same location.
A drive will not have autonomy to leave this synchronized dance.
On the flip side, they service single requests really quickly, linearly scaling read performance.

The use case for this mode is long, sequential reads.
This will be the case when reading big-ass files such as video processing or raw data for scientific computing.

#### RAID 3

This is the similar to RAID 2 but data is striped at the byte-level and uses parity bit for error detection.
Like RAID 2, it cannot process concurrent requests, as the bytes for a block will be in the same location on each drive.

The use case is same as RAID 2, for long, sequential reads.

The differentiator is that this only requires 1 additional drive for the parity bit instead of `log(N)` as in RAID 2.

### RAID 4

Data is partitioned at the block-level, with an additional drive for parity bit.
Working at the block-level allows servicing concurrent requests, since different requests might be able to be serviced
by an idle partition.
This improves random read performance.
However, write performance continues to be bottlenecked on updating the parity bit for every write operation.

One advantage over RAID 3 is that the array can be expanded online.
Since this operates at a block-level, adding more blocks is trivial:
blocks are managed with an allocation table, which can begin mapping new writes to the new drive.
RAID 3 cannot be easily extended because it would require re-sharding the existing bytes to add a partition.
Since each block on the new disk will be initialized to 0, it doesn't affect the parity computation.

### RAID 5

RAID 5 is similar to RAID 4 but the parity bit is distributed among the drives.
The parity block moves each row, such that it will be evenly distributed, rather than randomly.
This results in more even wear, as writing the parity doesn't hammer a single drive.

Read performance and write performance is high.
Modern controllers are able to compute the parity bit with little cost, so it's not as much of a performance concern.

RAID 5 can survive a single drive failure and can remain online, while rebuilding.

This is the most common configuration of RAID, as it balances performance, overhead, and data integrity.

### RAID 6

This is literally RAID 5 but with an additional parity block.
The second parity block gives 1 additional level of redundancy, allowing for 2 disk failures.

With two parity blocks, you can use fancier algorithms than simple parity calculations.
This comes at the cost of write performance, since there are 2x parity calculations per write request.

This configuration is desirable as a subsequent disk failure is more likely than chance.
And the act of rebuilding the failed drive is additional spike of stress, which might induce the subsequent disk failure.
Given larger drive capacities, [rebuilding takes much longer](#rebuild-times) as well, further exposing yourself.
