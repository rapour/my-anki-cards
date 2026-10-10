How do you detect a **cycle in a directed graph**, for example a circular dependency between CSV columns where A refers to B, B refers to C and C refers to A? Why does the simple "ignore the parent" trick from undirected graphs not work?

---

A **cycle** is a route that leads back to where it started. In the CSV problem a cycle means the columns depend on each other in a circle, so there is no valid order to process them.

**Why a plain visited set is not enough.** In a directed graph you can legitimately reach the same node by two different routes without any cycle. Imagine A leads to B and to C, and both B and C lead to D. A search reaches D twice, but there is no loop, because you can never get *back* to A. So "I have seen this node before" does not prove a cycle.

**The real test:** you have a cycle only if, while exploring, you reach a node that is **still on your current route** (you have started exploring it but have not finished it).

**The three-colour method.** Give each node one of three states:

| State | Meaning |
|---|---|
| Unvisited (white) | not seen yet |
| In progress (grey) | on the route I am following right now |
| Done (black) | fully explored, and no cycle was found below it |

Run DFS. When you step into a node, mark it *in progress*. For each neighbour:

- *unvisited*: go deeper;
- *in progress*: **cycle found**, because we have come round to a node on our own route;
- *done*: ignore it, as it is safely finished and cannot lead back here.

After all neighbours are processed, mark the node *done*.

**Why the undirected trick fails.** For undirected graphs people say "a cycle exists if you meet a visited node that is not your parent". In a directed graph the edge is one-way, so meeting an already-visited node (for instance D in the example above) is perfectly normal. Only the in-progress state means a loop.

Cost: `O(V + E)`. Start a search from every unvisited node, since a cycle might sit in a part of the graph that your first start node cannot reach.
