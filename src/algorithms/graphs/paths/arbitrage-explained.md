What is **currency arbitrage**, how can you detect it in a graph, and what does a **negative cycle** have to do with it?

---

**Arbitrage** means making money from nothing by converting around a loop of currencies and ending up with more than you started with. Example: start with 1 USD.

- USD to EUR at 0.9 gives 0.9 EUR.
- EUR to GBP at 0.8 gives 0.72 GBP.
- GBP to USD at 1.5 gives 1.08 USD.

You started with 1 and finished with 1.08, so the loop's rates multiply to 1.08, which is more than 1. You could repeat it forever.

**Turning it into a graph question.** Replace every rate with `-ln(rate)` (the negative natural logarithm). Multiplying rates becomes *adding* these weights. A loop whose rates multiply to more than 1 becomes a loop whose weights add to **less than zero**, which is called a **negative cycle**. So "is there arbitrage?" means "is there a negative cycle?".

**Detecting it with Bellman-Ford.**

1. Start every node at distance 0. This makes sure that every loop in the graph is reachable, wherever it is.
2. Repeat "try to improve every edge" up to `V` times.
3. Without a negative cycle, improvements must stop after at most `V - 1` rounds, because a best route never needs more than `V - 1` edges.
4. If an edge can *still* be improved in round number `V`, a negative cycle exists, so the answer is yes.

Complexity is `O(V × E)`.

Practical tip: floating-point rounding can make a loop of exactly 1.0 look slightly different, so only count an improvement if it beats the old value by a small margin such as `1e-12`.
