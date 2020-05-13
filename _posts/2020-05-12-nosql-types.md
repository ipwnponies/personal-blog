---
title: NoSQL Database Types
categories:
- programming
tags:
- data
---

*NoSQL* is such a bad name.
It was chosen to contrast against the ubiquitous relational databases.
Simply because it was different.
This category has grown so much and only caused more confusion due to naming.

Today, I'm going to dish out some knowledge.
And bring some pragmatic sanity to this.

## Relational Database

Relational database have tables with structured data.
Each table has a schema, that dictates which columns exist.
Each entry (row) fills out the schema.

When querying, you can use relationships (joins) to denormalize data.

They typically are ACID compliant.
This makes working with the data great but slow.
And scaling is hard, due to locks and synchronizations that are needed for data consistency.

## NoSQL

NoSQL has different flavours but the common theme is they sacrifice consistency for performance.
They usually have less ACID features, which directly hamper performance.

Relational dbs will take locks and block, in the name of consistency.
This lowers their write throughput.

Most NoSQL are eventually consistent.
They'll eventually get there but there's a real non-zero amount of time where you might read stale data.

They are highly available, fault tolerant, and fast.
All this because they allow momentary inconsistency.
This is all done by adding more and more nodes, which usually would increase the latency before the system converges on consistency.

## NoSQL Types

NoSQL comes in [many flavours][1].
This [video introduces][2] the common, high-level types are:

* key-value
* document
* columnar
* graph

[1]: https://en.wikipedia.org/wiki/NoSQL#Types_and_examples
[2]:https://www.youtube.com/watch?v=4bfX96C5644

### Key-Value

Key-value stores are very simple.
They're effective hashmaps.

Given a key, you can store a blob of data.
Doesn't matter what data, it is opaque to the store.

They are very useful as distributed caches.

The lack of structured data makes it difficult to do any advanced querying, beyond retrieval.

### Document

Document stores are step up from key-value.
It's a key-value lookup, where the data is loosely structured.

This allows some advanced querying and aggregations.

Documents are analogous to a row in SQL.
It is keyed and returns all the "fields".

### Columnar

Columnar stores the complement to SQL.
Unlike SQL, where data is partitioned by row, here it is partitioned by column.
i.e. All the user's first name goes into teh same column, all their last names into different column.
In SQL, the entire records is stored in consecutive memory.

Columns act as partitions and are sharded and replicated.
To look up all the attributes for *userA*, you would need to access all the shards and tables.

What are the advantages of this?
Column data tends to be the same data type.
And share other traits, such as common size, length, values, etc.
For example, the *birthyear* column would contain values in the range of 1900-2020, not every integer.

This makes it amenable to compression, aggregation, lookups.
Compression can reduce the storage size on disk and when querying, which allows it to perform at larger scale.
Aggregations are cheap, since you are only looking at the column you're performing aggregation on.

You could emulate a quasi-columnar database in SQL, by creating indexes for every column.

In SQL, data is row stored, which is heterogenous mixture.
This makes it impossible to do optimization smarts on the data.
It is expensive to query large sets of data, since this equates to wasting time reading irrelevant columns.

If your queries make use of most columns of a table, while only needing to access a few rows (column wide, row narrow),
then SQL is your man.
If you only need a column or two and are going queries or aggregation that cover the entire set (column narrow, row wide),
columnar store is your man.

### Graph

Graph databases represent vertices and edges of graphs.
They allow for very powerful relationships and querying of graph-like data.

If you have a table in SQL of friends, you would need to pull all the data and process it into [adjacency list][3] in
application code.
This might be infeasible to do in memory.

[3]: https://en.wikipedia.org/wiki/Adjacency_list

Or you could mock this with table self-joins.
But this would have limited degrees of separation.

Graph databases directly solve this niche problem-space.
