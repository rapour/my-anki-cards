A graph question asks for one specific thing. How do you decide between BFS, DFS, Dijkstra's algorithm and Bellman-Ford?

---

First ask **what the question wants**, then ask **whether the edges carry numbers** such as costs, prices or rates.

**All edges count the same (or carry no numbers):**

| The question asks for | Use | Why |
|---|---|---|
| Does any route exist? | DFS (BFS also works) | You only need yes or no. DFS is the shortest to write |
| One route, as a list of nodes | DFS with a *path list*, or BFS with a *parent map* | Either remembers how you got to each node |
| The route with the fewest edges | **BFS** | It reaches nodes closest first, so the first arrival at the target is the shortest |
| Can I reach it using at most `k` edges? | BFS, one *level* at a time | A level is all the nodes that are the same number of edges from the start. Stop after level `k` |
| Every route | DFS with undo (backtracking) | Try each branch, then unmark the node so other routes can use it |
| Is there a cycle? Is there a valid order for tasks that depend on each other? | DFS with three states, or Kahn's algorithm for the order | You must know which nodes are on the route being followed right now |
| Which nodes form one connected group? | BFS or DFS started from each unvisited node, or union-find | Each search finds one whole group |
| Evaluate a formula written as a tree | DFS, children first (*post-order*) | A node's answer needs its children's answers |
| Try a choice, recurse, undo it (for example settling debts) | DFS backtracking | A search over choices, not over a graph you were given |

**Edges have costs:**

| The costs are | Use |
|---|---|
| Prices or distances that add up and are never negative | **Dijkstra** (like BFS, but with a priority queue) |
| Possibly negative, or rates that multiply (turned into logarithms) | **Bellman-Ford** |
| A limit on the number of edges as well | Bellman-Ford, stopped after `k` rounds |

**Terms used above**

- *Path list*: the list of nodes on the route DFS is following right now.
- *Parent map*: a map that stores, for each node, the node we first reached it from. Walking it backwards from the target rebuilds the route.
- *Three states*: every node is *unvisited*, *in progress* (on the current route) or *done*.
- *Priority queue*: a collection that always hands back its smallest item first.
- *Union-find*: a structure that merges groups and tells you which group a node belongs to.

**One-line version:** BFS for fewest edges and level by level. DFS for existence, all routes, cycles and trees. If edges have different costs, Dijkstra or Bellman-Ford.
