Reachability only answers yes or no. How do you get the **actual route** (the list of nodes from A to B)? Explain the DFS way and the BFS way.

---

You need to remember how you got to each node, so that when you reach B you can say which nodes you walked through. There are two standard ways.

**DFS with a path list.** The *path list* is a list called `path` that holds the nodes on the route DFS is following right now.

- When you step into a node, push it onto `path`.
- If you reach the target, `path` already holds the whole route, so return it.
- If a node turns out to be a dead end, you step back out of it, so pop it off `path`.

At every moment `path` is exactly the route from the start to the node you are standing on. The route found is *a* route, not necessarily the shortest or cheapest.

**BFS with a parent map.** The *parent map* is a map called `parent` that records, for each node, the node it was first reached from ("I first reached X from Y").

- Whenever you add a neighbour to the queue, record `parent[neighbour] = current`.
- When you take the target out of the queue, rebuild the route by walking backwards: target, its parent, that node's parent, and so on until you reach the start.
- That list is backwards, so reverse it.

Because BFS finds nodes in order of distance, this route has the **fewest edges**.

|  | DFS path list | BFS parent map |
|---|---|---|
| Extra memory | one list | one map entry per node |
| Route found | any route | route with fewest edges |
| Rebuilding | already built | walk backwards, then reverse |
