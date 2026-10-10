Quick rule: given a graph question, when do you choose **BFS**, when **DFS**, and when must you use something else (Dijkstra or Bellman-Ford)?

---

First ask what the question wants, and whether the edges carry numbers.

| The question asks for | Use | Reason |
|---|---|---|
| Does any route exist? | DFS (BFS also works) | You only need yes or no. DFS is the shortest to write |
| Any one route, shown as a list | DFS with a path stack, or BFS with a parent map | Either records how you got there |
| Fewest steps or hops | **BFS** | It meets nodes in order of distance, so the first arrival is the shortest |
| Reachable within `k` steps | BFS, one level at a time | Stop after level `k` |
| Every route | DFS with undo (backtracking) | You must try each branch and rub out your marks |
| Is there a cycle? Topological order? | DFS with three states (or Kahn's BFS for the order) | You need to know which nodes are on the current route |
| Which records are in one group? | BFS or DFS from each unvisited node, or union-find | Flood-fill each island |
| Evaluate a formula tree | DFS (post-order) | Children must be answered before parents |
| Try an option, recurse, undo (debt settling) | DFS backtracking | A search over choices |

**When each edge has its own cost, neither BFS nor DFS is enough:**

| The edge numbers are | Use |
|---|---|
| Prices or distances that add up, never negative | **Dijkstra** (BFS with a priority queue) |
| Anything that may be negative, or multiplied rates turned into logarithms | **Bellman-Ford** |
| A limit on the number of legs as well | Bellman-Ford with `k` rounds |

**One-line version:** BFS for fewest steps and level-by-level work. DFS for existence, all routes, cycles, backtracking and trees. If edges have different costs, move to Dijkstra or Bellman-Ford.
