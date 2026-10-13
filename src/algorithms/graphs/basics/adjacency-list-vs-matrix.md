What are the two usual ways to store a graph in memory, and when do you choose each?

---

A graph has **nodes** (the things) and **edges** (the connections). Below, `V` is the number of nodes, `E` is the number of edges, and the **degree** of a node is the number of edges that leave it.

An **adjacency list** keeps, for every node, a list of its neighbours (the nodes it has an edge to). An **adjacency matrix** is a `V × V` grid where cell `[a][b]` says whether there is an edge from `a` to `b`, or what its weight is.

| | Adjacency list | Adjacency matrix |
|---|---|---|
| Memory | `O(V + E)` | `O(V²)` |
| Is there an edge `a` to `b`? | scan `a`'s list, `O(degree)` (or `O(1)` with a hash set) | `O(1)` |
| List the neighbours of `a` | `O(degree)` | `O(V)`: scan the whole row |
| BFS or DFS over the whole graph | `O(V + E)` | `O(V²)` |
| Best for | **sparse** graphs, where each node connects to only a few others | **dense** graphs (almost every pair connected), a small `V`, or algorithms that ask about pairs all the time |

Real graphs, such as currencies with exchange quotes, flight routes, or tasks with prerequisites, are almost always sparse, so **use an adjacency list by default**. In Rust that is a `Vec<Vec<usize>>` when nodes are numbered, or a `HashMap<&str, Vec<(&str, f64)>>` when nodes have names and edges carry weights.

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
