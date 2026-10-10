Write a Rust function that tells you whether an undirected graph contains a cycle, using DFS and the parent node.

---

`graph[a]` lists the neighbours of `a`. Because the graph is undirected, an edge between `a` and `b` appears in both lists. `visit` receives the `parent` of the node, which is `None` for the first node of a search. Any neighbour that is already visited and is not the parent proves there is a cycle. The outer loop starts a search from every unvisited node, so a cycle in a separate part of the graph is not missed.

```rust
fn has_cycle_undirected(graph: &[Vec<usize>]) -> bool {
    fn visit(node: usize, parent: Option<usize>, graph: &[Vec<usize>], visited: &mut [bool]) -> bool {
        visited[node] = true;
        for &next in &graph[node] {
            if Some(next) == parent {
                continue; // the edge we arrived along is not a cycle
            }
            if visited[next] || visit(next, Some(node), graph, visited) {
                return true; // a second way to reach `next`
            }
        }
        false
    }

    let mut visited = vec![false; graph.len()];
    (0..graph.len()).any(|start| !visited[start] && visit(start, None, graph, &mut visited))
}

fn main() {
    // 0 - 1 - 2: a path, no cycle
    let path = vec![vec![1], vec![0, 2], vec![1]];
    assert!(!has_cycle_undirected(&path));

    // 0 - 1 - 2 - 0: a triangle
    let triangle = vec![vec![1, 2], vec![0, 2], vec![0, 1]];
    assert!(has_cycle_undirected(&triangle));

    // a path (0 - 1) and a separate triangle (2, 3, 4): the cycle is in the second part
    let two_parts = vec![vec![1], vec![0], vec![3, 4], vec![2, 4], vec![2, 3]];
    assert!(has_cycle_undirected(&two_parts));

    // a node joined to itself is the smallest cycle
    assert!(has_cycle_undirected(&[vec![0]]));
    println!("undirected cycle detection works");
}
```

This version assumes at most one edge between any two nodes. See the concept card for what to change if edges can repeat.
