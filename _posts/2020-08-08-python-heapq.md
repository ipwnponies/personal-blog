---
title: Python Heapq
categories:
- programming
tags:
- python
---

The Python standard library has a [heap data structure][1], called `heapq`.
It allows for implementing a priority queue.
It's a little strange to use, as it's composed entirely of static functions.

[1]: https://docs.python.org/3.7/library/heapq.html

Somethings to note:

- heapq maintains a min queue.
  This means you will need to invert the key to turn a min heap into a max heap
- heapq modifies lists in place.
  Technically sequences, if you want to use custom classes

## Quickstart

```python
from heapq import heappush, heappop

heap = []
heappush(heap, 5)
heappush(heap, 7)
heappush(heap, 3)

assert heappop(heap) == 3
assert heappop(heap) == 5
assert heappop(heap) == 7
assert not heap

# Max heap
heappush(heap, -5)
heappush(heap, -7)
heappush(heap, -3)
assert -heappop(heap) == 7

# Convert a list into a heap structure, O(log(n))
heap = [5, 7, 3]
heapify(heap)
```

## Advanced

Although `heappush` and `heappop` suffice, there exist two optimized functions: `heapreplace` and `heappushpop`.
These should be used if you want to swap elements in heap, maintaining the heap size.

`heapreplace` is equivalent to `heappop` + `heappush`.
`heappushpop` is equivalent to `heappush` + `heappop`.
The difference is the order of operation and only makes a difference if the elements in discussion are min value.

These [increase efficiency][2].

[2]: https://stackoverflow.com/questions/33701160/python-heapq-difference-between-heappushpop-and-heapreplace/46031391#46031391

### heapreplace

```python
def naive_heapreplace(heap, elem):
  result = heappop(elem)
  heappush(heap, elem)
  return result

def heapreplace(heap, elem):
  result = heap[0]
  heap[0] = elem
  heapify(heap)
  return result
```

We can see that `heapreplace` avoids calling both `heappop` and `heappush`.
By combining the operations, we only perform the heapify operation once, which is `O(log(n))`.

### heappushpop

```python
def naive_heappushpop(heap, elem):
  heappush(heap, elem)
  return heappop(heap)

def heappushpop(heap, elem):
  if elem < heap[0]:
    return elem
  else:
    return heapreplace(heap, elem)
```

In this case, it's just edge case handling.
If `elem` is going to be the smallest value, then `heappushpop` will simply return `elem` and the heap contents will
remain unchanged.
So we can short-circuit the logic here to avoid unnecessary heapify operations.
