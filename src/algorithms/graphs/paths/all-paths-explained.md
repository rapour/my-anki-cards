How do you list **every possible route** between two nodes? Why must you *undo* the visited marker when you step back (backtracking)? Use "list every route from USD to JPY" as the example.

---

Use DFS, but with a different kind of "visited" bookkeeping. In ordinary reachability a node is marked visited forever. When you need *all* routes, that is wrong.

**The idea: an "on this route right now" set.** Keep a list `path` of the nodes on the route you are currently building, plus a set `on_path` with the same nodes.

1. Step into a node: add it to `path` and `on_path`.
2. If it is the target, save a *copy* of `path` as one finished route.
3. Otherwise, try every neighbour that is not in `on_path`.
4. Step back out of the node: remove it from `path` and `on_path`. This is the **undo** that makes it backtracking.

A good picture: you walk a maze marking your route with chalk, and when you retreat from a corridor you rub the chalk out again, so that a different route can legitimately pass through that corridor later.

**Why a permanent visited set is wrong here.** Suppose there are two routes, A to B to D and A to C to D. The first route marks D as visited. When the search later arrives at D through C, D is already "visited", so the second route is silently thrown away. Undoing the marker on the way back is what keeps D available.

**Why `on_path` still exists.** It stops the route going round in circles (A to B to A to B and so on), so every route found is a *simple* route that visits each node at most once.

**Cost:** exponential in the worst case. A graph in which every node connects to every other has a number of routes between two nodes on the order of `(V - 2)!`. This approach only suits small graphs.
