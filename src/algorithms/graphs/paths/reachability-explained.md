In a graph problem, how do you check whether **any path exists** from node A to node B (reachability)? Which should you use, BFS or DFS? Use "can I convert currency X into currency Y at all?" as the example.

---

Here you only want a yes or no answer, not the route and not the price. That makes it the simplest graph question.

How it works:

1. Start at A and keep a *visited* set of nodes you have already seen.
2. Look at A's neighbours, then their neighbours, and so on, never going back to a visited node.
3. If you ever arrive at B, the answer is **yes**.
4. If you run out of new nodes to visit without arriving at B, the answer is **no**.

**BFS or DFS?** Either one is correct, and both cost `O(V + E)` (every node and edge is looked at at most once). DFS is usually quicker to write because recursion keeps the "where was I?" bookkeeping for you.

**Why the visited set is essential.** Currency graphs have loops: USD leads to EUR and EUR leads back to USD. Without a visited set the search would go round that loop forever.

**Edge cases to decide up front:**

- A equals B: usually the answer is yes (no conversion needed).
- A or B does not appear in the data at all: the answer is no.
- A and B sit in two separate islands of the graph (for example JPY and KRW are linked to each other but not to USD): the answer is no.

Where it appears: Currency Conversion part 2 ("indirect conversion through another currency") and checking that a CSV foreign key points to something that exists.
