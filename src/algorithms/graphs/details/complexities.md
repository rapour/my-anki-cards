What are the running times (time complexities) of BFS, DFS, Dijkstra, Bellman-Ford and "list all routes", and what do `V`, `E` and `k` stand for in plain words?

---

**The letters.** `V` is the number of nodes (vertices) and `E` is the number of edges. For currencies, `V` is the number of currencies and `E` is the number of quotes (twice that if you add the reverse of each quote). `k` is the limit on the number of edges (legs, hops) a route may use in the "at most k" variants.

| Algorithm | Time | Why, in plain words |
|---|---|---|
| **BFS** | `O(V + E)` | Every node is queued once and every edge is looked at once |
| **DFS** | `O(V + E)` | Every node is entered once and every edge is looked at once |
| **Dijkstra** (cheapest route, no negative costs) | `O(E log V)` with a binary heap | Like BFS, but each push and pop on the priority queue (a collection that always hands back its smallest item first) costs about `log V` |
| **Bellman-Ford** (a shortest-path algorithm that allows negative costs; used for arbitrage) | `O(V × E)` | Up to `V - 1` rounds, and each round looks at all `E` edges |
| **Bellman-Ford limited to `k` legs** | `O(k × E)` | Only `k` rounds are run |
| **Kahn's algorithm** (an order in which every edge points forwards) | `O(V + E)` | Each node is queued once and each edge reduces one counter |
| **Union-find** | close to constant per operation | Path compression and union by size keep the trees almost flat |
| **List all routes** | exponential | The number of routes can double each time you add a node (a fully connected graph has about `(V - 2)!` routes between two nodes) |
| **Optimal account balancing** (settling a group's debts with the fewest payments) | exponential | It tries many ways to pair up people, so it only suits small inputs |

**Space:** BFS, DFS and the cycle and topological methods need `O(V)` extra memory for the visited markers and the queue or stack. Rebuilding a route needs one more map that stores, for each node, the node it was first reached from (a *parent map*), also `O(V)`.

**Remember:** `O(V + E)` means "no worse than a single pass over the graph". You cannot do better than that for reachability, because you must at least read the input.
