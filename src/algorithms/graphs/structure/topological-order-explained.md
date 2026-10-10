What is a **topological order**, when do you need one (for example validating CSV rows only after the rows they reference), and how does **Kahn's algorithm** produce it?

---

A **topological order** is a way of lining up the nodes of a directed graph so that every edge points forwards: if there is an edge from A to B, then A appears before B in the list. Think of getting dressed: socks must come before shoes, and trousers before the belt. The edges say "this must happen before that", and the topological order is one valid schedule.

In the CSV problem: a row that refers to another row can only be checked once the row it points to has been loaded, so you process rows in a topological order of the "refers to" relationships.

It only exists if the graph has **no cycle**. If A needs B and B needs A, no valid order exists.

**Kahn's algorithm** (a BFS-style method):

1. Count each node's **in-degree**: the number of edges pointing *into* it, meaning how many things must come before it.
2. Put every node with in-degree 0 in a queue. These have nothing waiting on them, so they can go first.
3. Take a node from the queue and add it to the output order. It is now "done", so for each node it points to, reduce that node's in-degree by 1. If a neighbour's in-degree reaches 0, add it to the queue.
4. Repeat until the queue is empty.

**Free cycle detection:** if the output contains fewer than `V` nodes, some nodes never reached in-degree 0, because they are stuck waiting on each other, so there is a cycle.

Cost: `O(V + E)`.

The alternative is DFS: record each node when it *finishes* (post-order), then reverse that list.
