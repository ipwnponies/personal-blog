---
title: Generating Raw SQL From SQLAlchemy
categories:
- programming
tags:
- sqlalchemy
- databases
- python
---

`SQLAlchemy` is the python library that is used as an abstraction layer to different ORM.
It implements pythonic patterns and whatnot.
Whereas many ORMs are just syntax wrappers to write SQL in programming languages, SQLAlchemy allows for being even more agnostic.
You can model objects as python classes and have attributes automatically result in query lookups.
It is very powerful because it allows you to write your code fluidly, replacing an ORM with a different datastore (such
as pickling).
Many ORM wrappers allows you to switch between flavours of SQL engines.

# Printing Query For Quick Analysis

When there are performance issues, I often want to get the raw query so I can execute it directly on the database.
This allows for eliminating the code issues with `sqla` modeling or setup.

The `__str__` for a query object can be used to [print a representative query][1].
I say representative because it's not a sql dialect specific query but can be used to get a sense of the joins and conditions.

Basically this gives you an un-sugared python view and more SQL.
You can then use your understanding of SQL to sanity-check your code.

[1]: https://docs.sqlalchemy.org/en/13/faq/sqlexpressions.html#how-do-i-render-sql-expressions-as-strings-possibly-with-bound-parameters-inlined

# Printing Query for Specific Databases

Because dialects can have certain features disabled, it can be important to [print dialect-specific output][2] for debugging.
For example, MySQL did not have `RANK` until 8.0 (2017).
There are more quirks, such how you alias tables: sometimes you're allowed to use `AS` even though it's unnecessary but
sometimes it fails.

```python
from sqlalchemy.dialects import mysql
print(query.statement.compile(dialect=mysql.dialect()))
```

[2]: https://docs.sqlalchemy.org/en/13/faq/sqlexpressions.html#stringifying-for-specific-databases

# Printing Complete Query That Can Be Executed

This is what you probably all came here for.
SQLAlchemy uses parameterized queries (DBAPI) and that's what was printed in the previous examples.
Sometimes you really just want to copy-paste the query and actually execute it in the database.
The reason this behaviour isn't default is because it can lead to SQL injection if you're not careful.

```python
from sqlalchemy.dialects import mysql
print(query.statement.compile(dialect=mysql.dialect(), compile_kwargs={'literal_binds': True}))
```

The secret ingredient is to include the [`compile_kwargs` with `literal_binds` enabled][3].

[3]: https://docs.sqlalchemy.org/en/13/faq/sqlexpressions.html#rendering-bound-parameters-inline
