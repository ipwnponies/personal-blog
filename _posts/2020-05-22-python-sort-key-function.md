---
title: Python Key Functions
categories:
- programming
tags:
- python
---

Several `python` functions, such as `sorted` and `max`, accept a `key` parameter that acts as the comparator.

The comparator provides the ordering for a given element.
For integers, this is based on value.
For strings, this is lexical ordering (length and letter order).

## History

Before python 2.4, these functions took a `cmp` param for the comparator function, much like Java and C#.
But since then, it's changed to a `key` function, that behaves slightly differently.

[`functools.cmp_to_key`][1] is available to convert old-style comparators to key functions.

[1]:https://docs.python.org/3.8/library/functools.html#functools.cmp_to_key

## Old-style cmp

An old-style `cmp` function was easy enough to write:

```python
def custom_cmp(obj1, obj2):
  if obj1.property == obj2.property:
    return 0
  elif obj1.property == 'Something' and obj2.property == 'different':
    return 1
  else:
    return -1

sorted(list_of_custom, cmp=custom_cmp)
```

The interface was a two parameter function which returned an integral value.
0 meant equally ranking, positive meant the first param was larger, and negative meant it was less than.

The `sort` and `max` functions would compare two elements using this function, using the result to rank them.

## Key Function

Key functions are easy to write too:

```python
def custom_key(obj):
  return obj.property

sorted(list_of_custom, key=custom_key)
```

The interface was a single parameter function which returns a key object.

A common use case is sorting strings by length, the `key` is `len`.
For every string in the list, the length is generated and that is used for ranking.

## cmp vs. key function

It took me some time to wrap my head around the difference.

`cmp`-style gave a function for the `sort` to compare between two elements.
The output of the `cmp` was directly stating the relative ordering of the two elements.

`key`-style gave a function for `sort` to generate a separate *key* element.
The *key* would like scores, used for ranking.

## How Does It Work Under The Hood

### cmp_to_key

We can take a look at [`functools.cmp_to_key`][2] to give us a high-level intuition.

[2]: https://wiki.python.org/moin/HowTo/Sorting#The_Old_Way_Using_the_cmp_Parameter

```python
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
```

It takes the `cmp` and wraps it with a custom class.
The `key` function is simply the constructor.

When it comes time to rank and sort, these objects have all their operators re-implemented to use the `cmp`.

### Using Key Function

Let's look at how `CPython` actually uses the `key` function.
Here's is the [implementation for 3.9][cpython source].

[cpython source]: https://github.com/python/cpython/blob/b5cc2089cc354469f12eabc7ba54280e85fdd6dc/Objects/listobject.c#L2234-L2243

```python
if (keyfunc == NULL) {
    keys = NULL;
    lo.keys = saved_ob_item;
    lo.values = NULL;
}
else {
    ...
    ...
    for (i = 0; i < saved_ob_size ; i++) {
        keys[i] = PyObject_CallOneArg(keyfunc, saved_ob_item[i]);
      ...
      ...
    }

    lo.keys = keys;
    lo.values = saved_ob_item;
}
```

For every element in the list, `cpython` is running it through the key function.
The elements are stored in `lo.values` and the keys in `lo.keys`.

If not key function is provided, than `lo.keys` is the list.

This pattern is referred to as a [Schwartzian transform][3].
The motivation is to transform every element to its ranking value only once.
For expensive computation, this can be beneficial as sorting requires average of `nlog(n)` comparisons whereas
generation happens `n` times.

[3]: https://en.wikipedia.org/wiki/Schwartzian_transform

Lists in python can contain non-homogenous types.
Comparison between different types is possible, as they are all inherit from `Object` and
can make use of `__gt__`, `__lt__`, `__eq__`, etc.
But these methods require lookups in the dispatch tables, such is object oriented programming.
`key` functions allow for transforming these objects to primitives, such as integer.
The interpreter can do smarts with primitives and optimize it greatly.
