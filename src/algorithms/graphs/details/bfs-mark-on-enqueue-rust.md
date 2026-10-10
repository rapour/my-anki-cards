Show in Rust why BFS should mark a node as visited when it is **added** to the queue, rather than when it is **taken out**.

---

The graph is a diamond with a tail: node 0 leads to 1 and 2, both lead to node 3, and node 3 leads to node 4. Node 3 is discovered twice, once from each of its neighbours.

- **Marking when taken out:** neither node 1 nor node 2 has marked node 3 when they look at it, so both add it to the queue. It sits in the queue twice. A check when it comes out stops it being *processed* twice, but the queue has still grown by one extra entry. On a big graph with many shared neighbours, these duplicates pile up.
- **Marking when added:** node 1 adds node 3 and marks it straight away. When node 2 looks at node 3, it sees the mark and does nothing. Node 3 is queued exactly once.

The function below counts how many entries were ever added to the queue, which makes the difference visible.

```rust
use std::collections::VecDeque;

/// Returns how many entries were ever added to the queue.
fn queue_pushes(graph: &[Vec<usize>], start: usize, mark_on_enqueue: bool) -> usize {
    let mut visited = vec![false; graph.len()];
    let mut queue = VecDeque::from([start]);
    let mut pushes = 1; // the start node
    if mark_on_enqueue {
        visited[start] = true;
    }

    while let Some(node) = queue.pop_front() {
        if !mark_on_enqueue {
            if visited[node] {
                continue; // a duplicate entry: skip it now that it came out
            }
            visited[node] = true;
        }
        for &next in &graph[node] {
            if !visited[next] {
                if mark_on_enqueue {
                    visited[next] = true; // claim it before anyone else can
                }
                queue.push_back(next);
                pushes += 1;
            }
        }
    }
    pushes
}

fn main() {
    // 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3, 3 -> 4
    let graph = vec![vec![1, 2], vec![3], vec![3], vec![4], vec![]];

    assert_eq!(queue_pushes(&graph, 0, true), 5); // one entry per node
    assert_eq!(queue_pushes(&graph, 0, false), 6); // node 3 was queued twice
    println!("early marking: 5 entries, late marking: 6 entries");
}
```
