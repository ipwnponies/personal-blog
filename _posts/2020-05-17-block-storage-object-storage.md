---
title: "Object Storage vs. Block Storage"
categories:
- programming
tags:
- cloud
- system design
---

In the world of system design and cloud computing, there is the choice between *object storage* or *block storage*.
For AWS, this is S3 (Simple Storage Service) and EBS (Elastic Block Storage).

## Object Storage

Object storage is very easy to understand.
It's a network file share.
You access files with a URL and the entire file is served to you.

The atom in object storage is a whole, self-contained file.
It is OS agnostic.

It can scale infinitely, with sharding and horizontal scaling.
Your file lives on a specific partition and it's quick and easy to go to the shard that contains it.

## Block Storage

Block storage behaves like a block device.
A block device is one where you write and manipulate the blocks of data manually, such as a hard drive.

This couples the block storage to the OS.
It's up to the OS to format and partition the block storage, maintaining the metadata for all files.

Because the OS has full control of all the blocks, it can use addressing math to move around quickly.
This results in very low latency operations and high write throughput.
If you had block storage for SQL data, updating a column for all records is very fast as the SQL engine immediately knows
which block needs to be updated.
This can also result in fragmentation (dependent on the file system), just like a regular hard drive.

To scale performance, you can scale vertically for higher IO.
Or you can use RAID, to stripe or replicate for performance.
But you cannot horizontally scale, as you cannot shard the data.

## When to Use Either

You probably want object storage.
It has all the benefits and simplicity.
The ease of use of S3 as a giant file store is testament.
And that S3 has 6 or 7 nine's shows how easy it is to maintain high availability and durability.
If write is few (and not overly time-sensitive) and read is many.

You'll need to attach and use block storage when you need performance, in terms of latency and IO.
The obvious examples are data stores.
They need to be able to read and write quickly.
They cannot afford to hit a network share to get a file or do a lookup.
