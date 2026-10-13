Why does BFS give the route with the **fewest edges** (an *unweighted shortest path*), and why does that matter when converting currencies?

---

An *unweighted* shortest path means every edge counts the same, so "shortest" simply means "fewest edges". In currency conversion each edge is one conversion, so "what is the smallest number of conversions from GBP to CAD?" is exactly this problem.

BFS explores in *levels*: first every node one edge from the start, then every node two edges away, then three. So the **first time BFS meets the target, it has arrived by the fewest possible edges**. No later arrival can be shorter, because everything closer was already handled. That is why you can stop as soon as the target appears.

To report the number of edges, keep a `distance` for each node: the start has distance 0, and a newly found neighbour has distance `current + 1`.

Two details that catch people out:

- **Mark nodes as visited when you add them to the queue, not when you take them out.** Otherwise the same node can be queued several times by different neighbours, which wastes work and can make counts wrong.
- **BFS only counts edges.** If "best" means the cheapest price or the best exchange rate, BFS is the wrong tool. Use Dijkstra's algorithm for costs that add up, or Bellman-Ford if costs can be negative.
