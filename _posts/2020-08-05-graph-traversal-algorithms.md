---
title: Graph Traversal Algorithms
categories:
- programming
tags:
- algorithm
- computer science
---

Today we're going to talk about graph traversal algorithms.
These are the more well-known ones that handle your main use cases, such as shortest path or dependency ordering.

## Terminology

Single-source shortest path
: the algorithm produces a valid, shortest path solution from an origin to all other nodes.

All-source
: algorithm produces valid shortest path solutions between all nodes

Relaxing
: visiting a node and updating the path costs using the edge costs to neighbours

Node
: a position in the graph. For a map, this is simply a point.

Edge
: a connection between nodes. For a map, this is the street or path available to connect two points.

Sparse Graph
: a sparse graph has few connections among nodes.
The most sparse graph is where most nodes only have 1 edge

Dense Graph
: a dense graph has many interconnections among nodes.
The most dense graph is fully connected, where every node is connected to every other node.

## Dijkstra's Algorithm

[Dijkstra's algorithm][1] is a *single-source shortest path* algorithm.
It is a **greedy algorithm**, working on the concept that the shortest path from `u->w` is
also the shortest path from `u->v` and `v->w`.
This is implemented with a priority queue, which iteratively relaxes the path costs.
The closest/lowest cost node is processed next, ensuring we are always processing the next closest node.
When we reach the target node, we can stop and know that this is the shortest path.

[1]: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

### Visualization - Dijkstra's Algorithm

A metaphor to help illustrate Dijsktra's is imagining the flow of lava.
Nodes are markers on the ground, while edges are different paths and surfaces the lava can flow in.
The lava will reach the point that is closest and on the smoothest flowing surface first.
Then it proceeds to the next closest point.

### Use Case - Dijkstra's Algorithm

Dijkstra's is optimized for single-source shortest path.
This makes it useful for path-finding applications, such as Google Maps routing.

The algorithm doesn't necessarily visit all nodes and edges.
So even the intermediary nodes there were visited may not be optimal.

### Disadvantage - Dijkstra's Algorithm

It is not capable of handling negative weights.
Due to priority queue, negative weights introduce cycles.

### Time and Space Complexity - Dijkstra's Algorithm

Every node is visited once and all the neighbouring edges are updated once.
This is `O(V+E)`.
This means it works very well on sparse graphs.

## Bellman-Ford Algorithm

Like Dijsktra's, the [Bellman-Ford algorithm][2] is another *single-source shortest path* algorithm.
It visits every node and relaxes the shortest path for every edge in graph.
These changes cascade to downstream edges.

[2]: https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm

### Visualization - Bellman-Ford Algorithm

Visualize this algorithm like a mesh network (WIFI repeater).
As you encounter repeaters (nodes), broadcast the signal back out.
This causes a cascading effect where a repeater can receive the same broadcast from two different repeaters.

### Use Case - Bellman-Ford Algorithm

Bellman-Ford can detect and handle negative weights.
Use it if Dijsktra's cannot be used due to negative cost edges.

For dense graph, use Floyd-Warshall instead, as it runs in same time complexity but is **all-source** shortest path.

Due to the negative cost edge, these tend to show up in more abstract modeling.
Such as price or ad bidding optimizations.
A negative weight in these problems can represent cheaper options or more efficient bundling.

### Disadvantage - Bellman-Ford Algorithm

The algorithm visits every edge for every node.
It will run in worst time-complexity than Dijsktra's.

### Time and Space Complexity - Bellman-Ford Algorithm

For every node, the cumulative shortest path cost for every edge is updated.
This is `O(V*E)`.

As you can see, Dijsktra's will with better time complexity, even if the graph is sparse.
In a sparse graph where every node at least connected to the graph, there are `E ~ V` edges.
This means the time complexity for a sparse graph is `O(V^2)`.

For a dense graph, where `E ~ V^2`, the time complexity is `O(V^3)`.
This time complexity is the same as Floyd-Warshall but is only single-source shortest path.

## Floyd-Warshall

Floyd-Warshall algorithm is an *all-sources shortest path* algorithm.
It expands the edge costs between vertexes to a 2-d matrix and calculates the shortest path of `u->w` as the
shortest path of `u->v` and `v->w`.

[3]: https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm

This makes it similar to Dijsktra's but using a different approach instead of priority queue.
This trades space to remove the need for priority queue.
Floyd-Warshall works well for dense graphs, as it encodes the edge costs into the matrix, while the
execution scales number of nodes.

### Use Case - Floyd-Warshall

Floyd-Warshall expands a list of edges into a matrix.
And it iterates over every cell in the matrix.
So it is a great choice for handling dense graphs.

When Bellman-Ford is used on a dense graph, it devolves into the same time-complexity as Floyd-Warshal
(dense graph is`E ~ V^2`, `O(V^3)`), albeit only for single-source.

### Time-Complexity - Floyd-Warshall

The algorithm for Floyd-Warshall is to iterating calculate the shortest path through an intermediary node.
This requires 3 levels of iteration over all nodes, `O(V^3)`.

Rough psuedo-code:

```python
for intermediate_node in nodes:
  for origin in nodes:
    for target in nodes:
      shortest_path[origin][target] = min(shortest_path[origin][target], shortest_path[origin][intermediate_node] + shortest_path[intermediate_node][target])
```

## Topological Sort

Topological sort is used for managing dependency ordering.
It ensures that all neighbours for incoming edges are visited first.

A good example is getting all the prerequisites before unlocking the next step in the skill tree.
Only when you fulfil all the disparate criteria can you progress to the next step.

In practice, this is typically implemented with a degree count.
While parsing the graph, tally how many incoming edges there are for a node.
When visiting neighbours, decrement the degree.
When the degree reaches 0, this means all dependencies have been fulfilled and the node can be enqueued.
