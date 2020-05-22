---
title: CAP Theorem
categories:
- programming
tags:
- computer science
- distributed systems
---

The [*CAP theorem*][1] states that it's impossible for a distributed data store to maintain all 3 guarantees:

[1]: https://en.wikipedia.org/wiki/CAP_theorem

- Consistency
- Availability
- Partition Tolerance

The consistency guarantee is that every read will have the latest, most up-to-date value.
In layman's working terms, this involves locking and blocking all reads until the writes have been propagated to all replicas.

Availability refers to ensuring every request is serviced.

Partition tolerance refers to the ability of the system to operate when some nodes are disconnected from each other.

## Two Out of Three

A commonly misunderstood interpretation is "pick 2 of 3".
This is incorrect and misleading.

Network partition failure is can never be avoided.
Hence, it's actually of pick either *consistency* or *availability*.

When there is not network failure, it's possible to have all 3 guarantees at once.
The trade-off only comes into play during degraded state of operation.

## I Choose You, Consistency

You might consistency if you cannot afford reading a stale value.
It's easy to think of use cases, such as banking or investment trading.

In the event of a network failure during write, remaining consistent is trivial: don't service any read requests until
the network recovers and you're able to** finish writing to all nodes**.
The client will experience timeouts or errors and will not be able to get the information they requested.
The system will remain at a standstill until the writes fully propagate.
There is no opportunity to get out of sync.

Obviously, not servicing read requests means lower availability.

## I Choose You, Availability

High availability is obvious, everyone likes things to always work, all the time.
This is essentially the default operating mode, unless you have a use-case that requires consistency, as described above.

In the event of a network failure during write, availability means servicing read requests with **potentially stale** data.
[*Eventual consistency*][2] is a term to characterize this behaviour, that nodes will eventually be updated but with latency.
As long as clients agree to this working model, all that's needed from us is enough redundant nodes to avoid
having a *Single Point of Failure* (SPOF).

[2]: https://en.wikipedia.org/wiki/Eventual_consistency

Resolving consistency issues is a different topic but you can already see that you have a new problem.
This is the trade-off of availability, conflict resolution.
It's possible to have undesirable unexpected system state.

## Summary

Many RDBMS choose consistency, as it shares common characteristics with ACID properties for database transactions.
This is why SQL databases have a reputation for not easily scaling horizontally nor being highly available.

Many NoSQL data stores choose availability.
*Eventual consistency* is also known as BASE, to contrast with ACID:

- Basically Available - basic reads/writes are highly available, albeit possibly inconsistent
- Soft State - state at any time is not guaranteed to be correct as it may not have yet converged or finished resolving conflicts
- Eventually consistent - given enough time, the database will converge towards the correct state

When choosing, evaluate the access patterns to see which trade-off is worth it.
With high read vs. writes, consistency concerns are much less frequent and high availability will benefit reads.
With many writes, sequence of events may be important to consistency.
