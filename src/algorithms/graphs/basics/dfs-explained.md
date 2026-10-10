What is **depth-first search (DFS)**? Explain in plain words how it works step by step, which data structure it relies on, and what it is good for.

---

Imagine walking through a maze with a ball of string. At every junction you pick one corridor and keep going **as deep as you can**. When you hit a dead end, you follow the string back to the last junction that still has an unexplored corridor and try that one. DFS explores a graph in exactly that way.

The tool that makes this possible is a **stack**: the most recent junction is the first one you return to ("last in, first out"). Recursion gives you a stack for free, because every function call sits on top of the previous one in the program's call stack.

Steps:

1. Mark the current node as *visited*.
2. For each neighbour that has not been visited, run DFS on that neighbour (go deeper).
3. When all neighbours are done, return to whoever called you (backtrack).

DFS costs `O(V + E)`, the same as BFS. It does **not** find the route with the fewest steps, because it may wander down a long corridor before trying a short one.

It is the natural choice when you need to answer "does a route exist?", "list every route", "is there a cycle?", or when you must try an option and then undo it (backtracking).

```rust
fn dfs(graph: &[Vec<usize>], node: usize, visited: &mut Vec<bool>, order: &mut Vec<usize>) {
    visited[node] = true;
    order.push(node);
    for &next in &graph[node] {
        if !visited[next] {
            dfs(graph, next, visited, order); // go deeper
        }
    } // falling out of the loop is the "backtrack"
}

fn dfs_order(graph: &[Vec<usize>], start: usize) -> Vec<usize> {
    let mut visited = vec![false; graph.len()];
    let mut order = Vec::new();
    dfs(graph, start, &mut visited, &mut order);
    order
}

fn main() {
    // 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3, 3 -> 4
    let graph = vec![vec![1, 2], vec![3], vec![3], vec![4], vec![]];
    // goes 0, 1, 3, 4 as deep as possible, then backtracks to try 2
    assert_eq!(dfs_order(&graph, 0), vec![0, 1, 3, 4, 2]);
    println!("{:?}", dfs_order(&graph, 0));
}
```
