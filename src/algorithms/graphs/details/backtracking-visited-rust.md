Show in Rust what goes wrong when you count all routes with a **permanent** visited set, compared with an **on-path** set that is undone when you step back.

---

The graph has a "diamond" followed by a tail: node 0 leads to nodes 1 and 2, both of those lead to node 3, and node 3 leads to node 4. There are exactly **two** routes from 0 to 4: 0, 1, 3, 4 and 0, 2, 3, 4. Both pass through node 3.

- `count_wrong` marks nodes as visited forever. The first route passes through node 3 and leaves it marked. When the second route arrives at node 3, it looks "already visited", so that route is thrown away. Result: 1 route.
- `count_right` removes a node's mark when it steps back out. Node 3 is free again for the second route. Result: 2 routes.

```rust
use std::collections::HashSet;

fn count_wrong(graph: &[Vec<usize>], node: usize, target: usize, visited: &mut HashSet<usize>) -> usize {
    if node == target {
        return 1;
    }
    visited.insert(node); // never removed: this is the bug
    let mut total = 0;
    for &next in &graph[node] {
        if !visited.contains(&next) {
            total += count_wrong(graph, next, target, visited);
        }
    }
    total
}

fn count_right(graph: &[Vec<usize>], node: usize, target: usize, on_path: &mut HashSet<usize>) -> usize {
    if node == target {
        return 1;
    }
    on_path.insert(node);
    let mut total = 0;
    for &next in &graph[node] {
        if !on_path.contains(&next) {
            total += count_right(graph, next, target, on_path);
        }
    }
    on_path.remove(&node); // undo when stepping back
    total
}

fn main() {
    // 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3, 3 -> 4
    let graph = vec![vec![1, 2], vec![3], vec![3], vec![4], vec![]];

    assert_eq!(count_right(&graph, 0, 4, &mut HashSet::new()), 2);
    assert_eq!(count_wrong(&graph, 0, 4, &mut HashSet::new()), 1); // lost a route
    println!("wrong finds 1 route, right finds 2");
}
```
