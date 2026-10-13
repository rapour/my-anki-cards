Flight or shipping legs are written `FROM:TO:METHOD:PRICE`, for example `NYC:LON:air:500`. BFS finds the route with the fewest legs. Why does it **fail** when the question is "what is the **cheapest** route?", and what do you use instead?

---

BFS counts legs and ignores prices. Suppose you can ship from New York to London in three ways:

| Route | Legs | Total cost |
|---|---|---|
| NYC to LON directly | 1 | 500 |
| NYC to PAR (300), then PAR to LON (100) | 2 | 400 |
| NYC to MAD (100), then MAD to LON (350) | 2 | 450 |

BFS meets London first through the direct leg, because it has only one leg, so it reports 500. But the cheapest route is the two-leg one through Paris at 400. Fewest legs and lowest cost are different questions.

**The fix is Dijkstra's algorithm**, which you can think of as BFS where the plain queue is replaced by a **priority queue**: a collection that always hands back the item with the smallest cost first (a *min-heap*). Instead of "whoever joined first", you always process "whichever known place is cheapest to reach so far".

How it works:

1. Give the start a cost of 0 and put it in the priority queue.
2. Take the place with the lowest cost out of the queue.
3. For each leg from that place, work out the cost of arriving at the next place this way (cost so far plus the leg's price). If that beats the best cost known for the next place, record it and push the next place into the queue.
4. The first time the target comes out of the queue, its cost is the cheapest possible, so stop.

**One strict condition:** costs must never be negative. Dijkstra relies on the idea that adding another leg can never make a route cheaper, and that stops being true with negative costs.

Complexity: `O(E log V)` with a binary heap, where `V` is the number of places, `E` is the number of legs, and the `log V` comes from the heap.
