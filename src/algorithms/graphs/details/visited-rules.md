Graph searches use a "visited" marker in three slightly different ways. What are the three rules, and what goes wrong if you use the wrong one?

---

| Search | When to mark a node | When to unmark it | Why |
|---|---|---|---|
| **BFS** (any purpose) | The moment you **add it to the queue** | Never | Stops the same node being queued twice by different neighbours |
| **DFS for reachability, cycles in undirected graphs, components** | The moment you **arrive** at it | Never | Each node needs exploring only once, so the cost stays `O(V + E)` |
| **DFS for all routes, or backtracking** | When you **step into** it | When you **step back out** (undo) | A node must stay available to *other* routes, so the marker only describes the route being built right now |

**What goes wrong:**

- *BFS, marking when you take the node out of the queue instead.* The node can be added several times before it is processed. Results are still correct for plain reachability, but the work is wasted, and counts such as "number of routes" or "distance" can be wrong.
- *All-routes DFS with a permanent marker.* The first route that passes through a node uses it up. Every other route through that node is silently dropped, so you list too few routes (and a "best" answer can be wrong).
- *Reachability DFS that unmarks on the way back.* The search is now correct but can take exponential time, because every route is explored again and again rather than each node once.

Directed cycle detection is the one extra case: it needs the three states (unvisited, in progress, done), where "in progress" is the temporary marker that is removed (becomes *done*) when you step back.

The next two cards show the DFS and BFS mistakes in running code.
