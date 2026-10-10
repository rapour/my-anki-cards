How do you return **the cycle itself** (for example "which CSV columns form the circular dependency?") instead of only saying that one exists? Give a complete Rust implementation.

---

Keep a `stack`: the list of nodes on the route DFS is following right now, in order. When you meet a node that is *in progress*, you have found a loop, and that node is somewhere in the stack. The loop is everything in the stack **from that node onwards**, plus the node again to close the circle.

For example, if the stack is `[0, 1, 2, 3]` and node 3 points back to node 1, the cycle is `[1, 2, 3, 1]`. Node 0 led into the loop but is not part of it, so it is left out.

Important: pop the node off the stack when you finish it, so the stack always matches the current route.

```rust
#[derive(Clone, Copy, PartialEq)]
enum State {
    Unvisited,
    InProgress,
    Done,
}

fn find_cycle(graph: &[Vec<usize>]) -> Option<Vec<usize>> {
    fn visit(
        node: usize,
        graph: &[Vec<usize>],
        state: &mut [State],
        stack: &mut Vec<usize>,
    ) -> Option<Vec<usize>> {
        state[node] = State::InProgress;
        stack.push(node);
        for &next in &graph[node] {
            match state[next] {
                State::InProgress => {
                    // `next` is on the current route: slice the stack from there
                    let start = stack.iter().position(|&n| n == next).unwrap();
                    let mut cycle = stack[start..].to_vec();
                    cycle.push(next); // close the circle
                    return Some(cycle);
                }
                State::Unvisited => {
                    if let Some(cycle) = visit(next, graph, state, stack) {
                        return Some(cycle);
                    }
                }
                State::Done => {}
            }
        }
        stack.pop();
        state[node] = State::Done;
        None
    }

    let mut state = vec![State::Unvisited; graph.len()];
    let mut stack = Vec::new();
    for start in 0..graph.len() {
        if state[start] == State::Unvisited {
            if let Some(cycle) = visit(start, graph, &mut state, &mut stack) {
                return Some(cycle);
            }
        }
    }
    None
}

fn main() {
    // 0 -> 1 -> 2 -> 3 -> 1: node 0 leads into the loop but is not in it
    let graph = vec![vec![1], vec![2], vec![3], vec![1]];
    assert_eq!(find_cycle(&graph), Some(vec![1, 2, 3, 1]));

    let no_loop = vec![vec![1], vec![2], vec![]];
    assert_eq!(find_cycle(&no_loop), None);
    println!("{:?}", find_cycle(&graph));
}
```
