Why does BFS give you the route with the **fewest steps** (an unweighted shortest path), and when does that matter in currency conversion?

---

An *unweighted* shortest path means every edge counts the same, so "shortest" simply means "fewest edges". In currency conversion, the number of edges is the number of conversions, and a question such as "what is the smallest number of conversions from GBP to CAD?" is exactly this problem.

BFS explores in rings. First every node one step from the start, then every node two steps away, then three. So the **first time BFS meets the target, it has arrived by the fewest possible steps**. No later arrival can be shorter, because everything closer was already handled. That is why you can stop as soon as the target appears.

To report the number of steps, keep a `distance` for each node: the start has distance 0, and a newly found neighbour has distance `current + 1`.

Two details that catch people out:

- **Mark nodes as visited when you add them to the queue, not when you take them out.** Otherwise the same node can be queued several times by different neighbours, which wastes work and can make counts wrong.
- **BFS only counts steps.** If "best" means the cheapest price or the best exchange rate, BFS is the wrong tool (see the next cards).
