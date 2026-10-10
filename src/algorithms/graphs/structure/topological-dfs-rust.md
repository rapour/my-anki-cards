How do you produce a topological order with **DFS** (reversed post-order)? Give a complete Rust implementation that also reports a cycle.

---

In DFS, a node *finishes* only after everything it points to has finished. So if you write each node down at the moment it finishes (its **post-order**), every node appears *after* all the nodes that depend on it. That is exactly backwards for a schedule, so you **reverse** the list at the end.

The three states from cycle detection are reused: meeting an *in-progress* node means a cycle, so no order exists.

```rust
#[derive(Clone, Copy, PartialEq)]
enum State {
    Unvisited,
    InProgress,
    Done,
}

fn topological_order_dfs(graph: &[Vec<usize>]) -> Option<Vec<usize>> {
    fn visit(node: usize, graph: &[Vec<usize>], state: &mut [State], finished: &mut Vec<usize>) -> bool {
        state[node] = State::InProgress;
        for &next in &graph[node] {
            match state[next] {
                State::InProgress => return false, // cycle: no valid order
                State::Unvisited => {
                    if !visit(next, graph, state, finished) {
                        return false;
                    }
                }
                State::Done => {}
            }
        }
        state[node] = State::Done;
        finished.push(node); // written down at the moment it finishes
        true
    }

    let mut state = vec![State::Unvisited; graph.len()];
    let mut finished = Vec::new();
    for start in 0..graph.len() {
        if state[start] == State::Unvisited && !visit(start, graph, &mut state, &mut finished) {
            return None;
        }
    }
    finished.reverse();
    Some(finished)
}

fn main() {
    let graph = vec![vec![1, 2], vec![3], vec![3], vec![]];
    let order = topological_order_dfs(&graph).unwrap();

    // several valid orders exist, so check the rule instead of one exact answer
    let position = |node: usize| order.iter().position(|&n| n == node).unwrap();
    for (from, targets) in graph.iter().enumerate() {
        for &to in targets {
            assert!(position(from) < position(to));
        }
    }

    assert_eq!(topological_order_dfs(&[vec![1], vec![0]]), None);
    println!("{order:?}");
}
```
