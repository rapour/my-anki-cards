In the User Record Linking problem, if record A matches B and B matches C, all three belong to the same real-world person or company. How do you group the records, and what are **connected components**?

---

Treat each record as a **node** and each "these two records match" decision as an **edge**. A **connected component** is a group of nodes that can all reach each other by following edges: an island in the graph. Records A, B and C form one component even though A and C were never compared directly, because A reaches C through B. That "transitive linking" is exactly what the problem asks for.

**Method 1: BFS or DFS from each unvisited node.**

1. Make a list `component` that stores a group number for each node, starting as "unassigned".
2. Go through the nodes one by one. When you find an unassigned node, start a new group number and run BFS or DFS from it, giving every node you reach that same number.
3. Continue until every node is assigned.

Nodes with the same number belong to the same entity. Cost: `O(V + E)`.

**Method 2: union-find (also called disjoint-set union).** Keep a structure that supports two operations: "merge the groups of A and B" and "which group is A in?". It is often cleaner when matches arrive **one at a time**, because you simply merge as each one appears, with no need to build the whole graph first.

**Where the real cost is.** In this problem, working out the matches is usually the slow part. Scoring every pair of records for similarity (name, email, company) takes `O(n²)` comparisons for `n` records. Grouping them afterwards is cheap by comparison.
