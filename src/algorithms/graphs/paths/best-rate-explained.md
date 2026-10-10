In currency conversion, how do you find the route that gives the **highest final amount** (the best rate)? Why is Dijkstra unsafe here, and what are the two approaches?

---

When you convert through several currencies, the rates are **multiplied**, not added. GBP to EUR at 1.2, then EUR to USD at 1.1, then USD to CAD at 1.3 gives 1.2 × 1.1 × 1.3 = 1.716. A route is better when its product is bigger.

**Why Dijkstra is unsafe.** Dijkstra assumes that extending a route can never make it cheaper. With exchange rates the opposite can happen: a rate above 1 makes your amount grow when you add a step. In "shortest path" language, such a step behaves like a *negative* cost, and Dijkstra can give wrong answers when negative costs exist.

**Approach 1: try every simple route (small graphs).** Use DFS to walk every route that never visits the same node twice, multiply the rates along each one, and remember the largest product. It is simple and always correct, but the number of routes can grow exponentially, so it only suits the small graphs in interviews.

**Approach 2: logarithms and Bellman-Ford.** The logarithm turns multiplication into addition: `ln(a × b) = ln(a) + ln(b)`. So maximising the product of rates is the same as minimising the sum of `-ln(rate)`. Every rate above 1 becomes a negative number, which is fine for **Bellman-Ford**, the shortest-path algorithm that tolerates negative costs. Afterwards, convert back with `exp(-total)`.

**The important catch.** If a loop of conversions can make money (a cycle whose rates multiply to more than 1, called *arbitrage*), you could go round it forever and "the best rate" has no upper limit. Bellman-Ford reports that situation rather than an answer.

This matters if you add the reverse quote `1/rate` for every given rate. As soon as two different routes between the same pair of currencies have different products, going one way and returning the other way is an arbitrage loop. So with reverse quotes added, approach 1 (simple routes only) is the safe choice. Approach 2 suits one-way quotes with no arbitrage.
