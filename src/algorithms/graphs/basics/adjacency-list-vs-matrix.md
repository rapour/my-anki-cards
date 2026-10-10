What are the two usual ways to store a graph in memory, and when do you choose each?

---

An **adjacency list** keeps, for every node, a list of its neighbours. An **adjacency matrix** is a `V × V` grid where cell `[a][b]` says whether there is an edge from `a` to `b` (or its weight).

| | Adjacency list | Adjacency matrix |
|---|---|---|
| Memory | `O(V + E)` | `O(V²)` |
| Is there an edge `a` to `b`? | scan `a`'s list, `O(degree)` (or `O(1)` with a hash set) | `O(1)` |
| List the neighbours of `a` | `O(degree)` | `O(V)`: scan the whole row |
| BFS or DFS over the whole graph | `O(V + E)` | `O(V²)` |
| Best for | **sparse** graphs, where most pairs are not connected | **dense** graphs, a small `V`, or algorithms that ask about pairs all the time |

Currencies, shipping routes and dependencies are all sparse, so **use an adjacency list by default**. In Rust that is a `Vec<Vec<usize>>` when nodes are numbered, or a `HashMap<&str, Vec<(&str, f64)>>` when nodes have names and edges carry weights.

```rust
// the same graph both ways: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
let list: Vec<Vec<usize>> =
    vec![vec![1, 2], vec![3], vec![3], vec![]];

let mut matrix = vec![vec![false; 4]; 4];
for (a, neighbours) in list.iter().enumerate() {
    for &b in neighbours {
        matrix[a][b] = true;
    }
}

assert!(matrix[0][1] && !matrix[1][0]); // edges are one-way
```
