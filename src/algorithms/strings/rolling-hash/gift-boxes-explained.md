HackerRank *Gift Boxes*: items arrive one by one on a belt, and as soon as the newest items spell the box pattern they are packed and removed. How can the hash with the degree-0 term last solve it quickly?

---

**The problem.** Each item is a letter. Whenever the items at the end of the belt are exactly the pattern, they are removed together and one box is packed. Count the boxes. Example with pattern `ab`:

| item arrives | belt after arriving | newest 2 items | what happens | boxes |
|---|---|---|---|---|
| a | `a` | too few | nothing | 0 |
| a | `aa` | `aa` | no match | 0 |
| b | `aab` | `ab` | match: both leave, belt is `a` | 1 |
| b | `ab` | `ab` | match: both leave, belt is empty | 2 |

Belt `aabb` gives 2 boxes. (After the first box leaves, the belt is `a`, and the next `b` forms a new `ab`.)

**The idea.** Treat the belt as a stack and keep the hash of the **whole belt** after each item, in a list `hashes`:

- *Add an item:* `new = old · p + letter`, a push at the right end.
- *Hash of the newest `k` items:* `hashes[len] − hashes[len−k] · p^k`. Compare it with the pattern hash.
- *Pack a box:* cut the list back by `k` entries. The hashes that remain are still correct for the shorter belt, so nothing needs recomputing.

Each item is handled once, so the cost is `O(n)`. The degree-0-last form is the natural fit: pushing at the right end is one multiply and add, and removing items just drops entries.
