Show two ways in Rust to run DFS on a chain of 200,000 nodes without overflowing the stack: an explicit stack, and a recursive version on a thread with a larger stack.

---

The test graph is a single long chain, 0 to 1 to 2 and so on. A recursive search needs one call record for every node in the chain at the same moment, which is the worst case for stack depth.

**Version 1: explicit stack (preferred).** A `Vec` named `stack` replaces the call stack. We mark a node as visited when we push it, so it is never pushed twice.

**Version 2: recursion on a big thread.** The recursive function is ordinary, but we run it inside a thread created with a 256 MiB stack, so there is room for the deep chain. The stack memory is only reserved, and is used up gradually as the recursion goes deeper.

```rust
fn count_reachable(graph: &[Vec<usize>], start: usize) -> usize {
    let mut visited = vec![false; graph.len()];
    let mut stack = vec![start]; // lives on the heap, so it can grow large
    visited[start] = true;
    let mut count = 0;

    while let Some(node) = stack.pop() {
        count += 1;
        for &next in &graph[node] {
            if !visited[next] {
                visited[next] = true; // mark when pushing
                stack.push(next);
            }
        }
    }
    count
}

fn count_recursive(graph: &[Vec<usize>], node: usize, visited: &mut Vec<bool>) -> usize {
    visited[node] = true;
    let mut count = 1;
    for &next in &graph[node] {
        if !visited[next] {
            count += count_recursive(graph, next, visited);
        }
    }
    count
}

fn main() {
    let n = 200_000;
    // 0 -> 1 -> 2 -> ... -> n-1
    let graph: Vec<Vec<usize>> = (0..n)
        .map(|i| if i + 1 < n { vec![i + 1] } else { vec![] })
        .collect();

    // version 1: no recursion, no stack problem
    assert_eq!(count_reachable(&graph, 0), n);

    // version 2: recursion, but on a thread with a 256 MiB stack
    let handle = std::thread::Builder::new()
        .stack_size(256 * 1024 * 1024)
        .spawn(move || {
            let mut visited = vec![false; graph.len()];
            count_recursive(&graph, 0, &mut visited)
        })
        .unwrap();
    assert_eq!(handle.join().unwrap(), n);

    println!("both versions visited all {n} nodes");
}
```
