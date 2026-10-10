Write Kahn's algorithm in Rust: return a valid processing order for a directed graph, or `None` if there is a cycle.

---

`graph[a]` lists the nodes that must come *after* `a`. We first count how many things point into each node (`in_degree`). Nodes with count zero go into the queue. Each time we finish a node, we "release" the nodes that were waiting on it.

```rust
use std::collections::VecDeque;

fn topological_order(graph: &[Vec<usize>]) -> Option<Vec<usize>> {
    let n = graph.len();

    let mut in_degree = vec![0; n];
    for neighbours in graph {
        for &to in neighbours {
            in_degree[to] += 1;
        }
    }

    // nodes that are not waiting on anything can go first
    let mut queue: VecDeque<usize> = (0..n).filter(|&node| in_degree[node] == 0).collect();
    let mut order = Vec::with_capacity(n);

    while let Some(node) = queue.pop_front() {
        order.push(node);
        for &next in &graph[node] {
            in_degree[next] -= 1; // one of its prerequisites is done
            if in_degree[next] == 0 {
                queue.push_back(next); // all prerequisites done
            }
        }
    }

    // fewer than n means some nodes were stuck waiting on each other
    (order.len() == n).then_some(order)
}

fn main() {
    // 0 before 1 and 2; both 1 and 2 before 3
    let graph = vec![vec![1, 2], vec![3], vec![3], vec![]];
    assert_eq!(topological_order(&graph), Some(vec![0, 1, 2, 3]));

    // 0 -> 1 -> 2 -> 1 contains a loop, so no order exists
    let cyclic = vec![vec![1], vec![2], vec![1]];
    assert_eq!(topological_order(&cyclic), None);
    println!("{:?}", topological_order(&graph));
}
```
