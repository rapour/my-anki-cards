What is **breadth-first search (BFS)**? Explain in plain words how it works step by step, which data structure it relies on, and what it is good for.

---

Imagine dropping a stone in a pond. The ripple reaches everything one step away first, then everything two steps away, then three, and so on. BFS explores a graph in exactly that way: **closest nodes first**.

The tool that makes this possible is a **queue**, which works like a queue in a shop: the first node to join is the first node to be served ("first in, first out").

Steps:

1. Put the start node in the queue and mark it as *visited*.
2. Take the node at the front of the queue.
3. Look at each of its neighbours. If a neighbour has not been visited, mark it visited and add it to the back of the queue.
4. Repeat from step 2 until the queue is empty.

The *visited* marker matters because graphs can contain loops. Without it you would keep walking round the same loop forever.

Because nodes are served in the order they joined, every node one step from the start is processed before any node two steps away. That is why BFS finds **the route with the fewest steps** (when every edge counts the same).

It visits each node once and looks at each edge once, so it costs `O(V + E)`.

```rust
use std::collections::VecDeque;

/// Returns the nodes in the order BFS discovers them.
fn bfs_order(graph: &[Vec<usize>], start: usize) -> Vec<usize> {
    let mut visited = vec![false; graph.len()];
    let mut queue = VecDeque::new();
    let mut order = Vec::new();

    visited[start] = true; // mark when the node joins the queue
    queue.push_back(start);

    while let Some(node) = queue.pop_front() {
        order.push(node);
        for &next in &graph[node] {
            if !visited[next] {
                visited[next] = true;
                queue.push_back(next);
            }
        }
    }
    order
}

fn main() {
    // 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3, 3 -> 4
    let graph = vec![vec![1, 2], vec![3], vec![3], vec![4], vec![]];
    assert_eq!(bfs_order(&graph, 0), vec![0, 1, 2, 3, 4]);
    println!("{:?}", bfs_order(&graph, 0));
}
```
