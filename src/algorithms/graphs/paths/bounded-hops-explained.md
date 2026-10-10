How do you answer "can I get from A to B using **at most k** conversions?" and "what is the **cheapest** route using at most k legs?" These are common follow-up questions in the currency and shipping problems.

---

The twist is a limit on the number of edges (called *hops*) you may use.

**Reachability within k hops: BFS level by level.** BFS naturally works in rings: ring 0 is the start, ring 1 is everything one step away, ring 2 everything two steps away. So process one whole ring at a time, and stop after ring k. If the target appeared in any ring from 0 to k, the answer is yes. Nodes found in ring `i` are exactly those whose fewest-steps distance is `i`, so using a visited set is still correct.

**Cheapest within k legs: Bellman-Ford rounds.** Dijkstra cannot simply be told "at most k legs", because the cheapest way to reach a node might use more legs than allowed, while a dearer way with fewer legs is the only usable one. Dijkstra throws that dearer option away. Bellman-Ford handles it naturally:

- Keep `dist[node]` = the cheapest known cost using the legs allowed so far.
- Each round allows exactly **one more leg**: for every edge, check whether `previous_dist[from] + cost` beats `dist[to]`.
- Crucially, read from a **copy of the previous round's distances**. If you read from the table you are updating, one round could chain several legs together and break the limit.
- After k rounds, `dist[target]` is the cheapest cost using at most k legs.

This is the pattern behind LeetCode 787 (Cheapest Flights Within K Stops). Complexity is `O(k × E)`.

Be careful with the off-by-one: "k conversions" is k edges, but LeetCode's "k stops" means k + 1 edges.
