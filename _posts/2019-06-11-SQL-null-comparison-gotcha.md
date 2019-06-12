---
title: SQL Null Value Gotcha
categories:
- programming
tags:
- sql
- gotchas
---

I was recently using a written query and fixed a bug in it.
Let's look at an example query:

```sql
SELECT id, name, value, type, fk_bar_id true FROM foo
WHERE foo.type != 'baz'
```

Simple enough, we want all the records in `foo`.
But we want filter out and ignore records where the type is 'baz'.
Let's assume that 'baz' is an enum of 3 possible values.
But it's **also optional/nullable**.

This is, in my opinion, a very reasonable implementation.
It's not how I would have done it because I have the benefit of knowing about many types of gotchas in SQL.
Let's dig into why this breaks down.

# Code Smells

Those with experience in SQL will have noticed the lingering smells of code in the air:

* Nullable enum instead of default sentinel value
* Filtering out values that don't match (negative filtering), instead of blacklisting known bad values (positive filtering)

## Nullable Enum

An enum represents a **limited set** of values that can be chosen.
If a column is allowed to be nullable, that's syntactic sugar for a default value of `NULL` on the column.
Or inserting the explicit value of `NULL` when creating a new record.

So why not allow two ways to do the same thing?
Because `NULL` has special handling and semantics in other contexts, such as comparison.
`NULL` does not work with any of the comparison operators, it requires its own comparison operator of `IS` to be functional.

```sql
NULL = 1 // False
NULL = 0 // False
NULL is NULL // True
NULL is not NULL // False
```

## Positive Filtering

If there's one thing I've learned, it's not to trust your self when writing a query.
It seems innocuous enough to use `foo.type != 'baz'`.
In set theory, this states that you want the values that are not in the set where `foo.type = 'baz'`.

Here is where the gotcha lies.
There are actually three sets:

* Values that are 'baz'
* Values that are not 'baz'
* Values that are `NULL`

Attempting to apply set operations in this ternary world is where I've seen many bugs.
This query is actually removing all values that are 'baz' or `NULL`!
The fix to this (without changing the existing schema) is very familiar, for those with SQL experience.

```sql
SELECT id, name, value, type, fk_bar_id true FROM foo
WHERE (foo.type != 'baz' or foo.type is null)
```

TLDR; `NULL` doesn't behave as you think it does, it will break all your assumptions.
