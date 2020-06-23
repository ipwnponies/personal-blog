---
title: Python List Append vs. Extend
categories:
- programming
tags:
- python
---

Python list objects have both `append` and `extend` methods.
They are both used to mutate the list instance and add more elements.

## Append

`append` takes a single object and adds it to the end of the array.
If you give it an iterable (list, set, dict), then it will add the entire iterable object as an element to the list.
Probably not what you'd expect!

Why the end?
Because this is `O(1)` operation because the memory has already been allocated.
This is how many dynamic arrays are resized, which amortizes the cost to resize (O(N)) over time.

## Extend

`extend` takes an iterable and adds all its content onto the end of the list.
If you give it a `str`, it will iterate over the string and add each character individually!
Probably not what you'd want.
If you give it a `int`, it will fail because `int` is not an iterable.

Isn't this just like `append`, why are we reinventing the wheel here?

```python
result = []
add_me = [1,2,3]

if True:
  result.extend(add_me)
else:
  for i in add_me:
    result.append(i)
```

Because [performance][1], that's why.
`extend` is implemented in `C` and can perform the loop iteration more efficiently.
This use case is fast enough that the overhead of making function calls in python (for iterator) has non-negligible impact.
This is an example of iterop-ing to other libraries (C) for performance and not being fixated on doing everything in Python.

[1]: https://stackoverflow.com/a/28119966
