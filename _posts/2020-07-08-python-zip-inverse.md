---
title: Python Inverse Zip
categories:
- programming
tags:
- python
---

## Zip

`zip` is a [builtin][1] that groups iterables together.
Imagine you have a list of names of users and a list of user ids:

```python
username = ['alice', 'bob', 'carol']
user_id = [1111, 2222, 1337]

users = zip(username, userid)
for name, id in users:
  print(f'I am {name} and my id is {id}')

# Less elegant but equivalent
for i in range(min(len(username), len(user_id))):
  name, id = username[i], user_id[i]
  print(f'I am {name} and my id is {id}')
```

[1]: https://docs.python.org/3/library/functions.html#zip

The data is segregated and we want to make it sane to work with.
Maybe the data came from a [columnar-esque datastore][2].

[2]: https://en.wikipedia.org/wiki/Column-oriented_DBMS

## Inverse

But what's the opposite?
How do you unzip?

Apparently you use [`zip` and tuple unpacking][3].

```python
username, user_id = zip(*users)
```

[3]: https://stackoverflow.com/questions/13635032/what-is-the-inverse-function-of-zip-in-python

How does this even work?
What is this wizardry?

It's actually not magic or special-case handling at all.
It's combining tuple unpacking (`*args`) with zip, to reverse the operation.

```python
users = [('alice', 111), ('bob', 222), ('carol', 1337)]

# *users expands to zip(('alice', 111), ('bob', 222), ('carol', 1337))
# It passes in 3 arguments, each an iterable of 2 items.
# Zip grabs the first item of each and collects them together
username, user+id = zip(*users)
```

Well, would you look at that.

Put more succinctly:

> In other words `lambda x: zip(*x)` is self-inverse.
