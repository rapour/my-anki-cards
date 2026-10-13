How do you answer "can I get from A to B using **at most k** edges?" and "what is the **cheapest** route using at most k edges?" (An edge is one hop, for example one currency conversion or one flight leg.)

---

The twist is a limit on the number of edges (called *hops* or *legs*) a route may use.

**Reachability within k hops: BFS level by level.** BFS naturally works in *levels*: level 0 is the start, level 1 is everything one edge away, level 2 everything two edges away. Process one whole level at a time and stop after level `k`. If the target appeared in any level from 0 to `k`, the answer is yes. A node found in level `i` has a fewest-edges distance of exactly `i`, so a visited set is still correct.

**Cheapest within k legs: Bellman-Ford rounds.** Dijkstra's algorithm (the usual cheapest-route search) cannot simply be told "at most k legs", because the cheapest way to reach a node might use more legs than allowed, while a dearer way with fewer legs is the only usable one. Dijkstra throws that dearer option away. Bellman-Ford, a shortest-path algorithm that works in rounds, handles it naturally:

- Keep `dist[node]` = the cheapest known cost using the legs allowed so far.
- Each round allows exactly **one more leg**: for every edge, check whether `previous_dist[from] + cost` beats `dist[to]`.
- Crucially, read from a **copy of the previous round's distances** (`previous_dist`). If you read from the table you are updating, one round could chain several legs together and break the limit.
- After `k` rounds, `dist[target]` is the cheapest cost using at most `k` legs.

This is LeetCode 787 (*Cheapest Flights Within K Stops*). Complexity is `O(k × E)`, where `E` is the number of edges.

Be careful with the off-by-one: "k conversions" is `k` edges, but LeetCode's "k stops" means `k + 1` edges.
