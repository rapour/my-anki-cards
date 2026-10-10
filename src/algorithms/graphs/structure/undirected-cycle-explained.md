How do you detect a **cycle in an undirected graph**, and why do you have to skip the node you just came from?

---

In an undirected graph every edge works in both directions. When DFS walks from A to B, node B sees A in its own neighbour list. That is not a cycle. It is just the edge you arrived along. If you treated "I have seen A before" as proof of a loop, every graph with an edge would look like it had one.

**The fix: remember the parent.** The parent of a node is the node you came from. While exploring a node, skip its parent. If any *other* neighbour has already been visited, there is a second route between the two nodes, so there is a cycle.

1. Run DFS from each unvisited node, passing along the parent (none at the start).
2. Mark the current node as visited.
3. For each neighbour: if it is the parent, skip it.
4. If it is already visited, **cycle found**.
5. Otherwise go deeper, with the current node as the new parent.

Example: the path 0 - 1 - 2 has no cycle, because node 2 only sees its parent 1. The triangle 0 - 1 - 2 - 0 has one, because node 2 also sees node 0, which is visited and is not its parent.

**Alternative with union-find.** Go through the edges one at a time. If both ends of an edge are already in the same group, this edge closes a loop. Otherwise merge the two groups. This is handy when edges arrive one at a time.

**Watch out for repeated edges.** If two edges can join the same pair of nodes, that pair is itself a cycle, but skipping "the parent" would hide it. In that case track the edge number, not only the parent node.

**Directed graphs are different.** There, meeting a visited node proves nothing, and you need the three states (see the directed cycle card).

Cost: `O(V + E)`.
