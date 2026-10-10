Write a Rust function that tells you whether a directed graph contains a cycle, using DFS with three states.

---

The graph is a list of neighbour lists: `graph[a]` holds every node that `a` points to. The inner function `visit` returns `true` as soon as it finds a cycle. The outer loop starts a search from every node that is still unvisited, so cycles in separate parts of the graph are not missed.

```rust
#[derive(Clone, Copy, PartialEq)]
enum State {
    Unvisited,
    InProgress, // on the route we are currently following
    Done,       // fully explored
}

fn has_cycle(graph: &[Vec<usize>]) -> bool {
    fn visit(node: usize, graph: &[Vec<usize>], state: &mut [State]) -> bool {
        state[node] = State::InProgress;
        for &next in &graph[node] {
            match state[next] {
                State::InProgress => return true, // came back to our own route
                State::Unvisited => {
                    if visit(next, graph, state) {
                        return true;
                    }
                }
                State::Done => {} // safe: already known not to loop back
            }
        }
        state[node] = State::Done;
        false
    }

    let mut state = vec![State::Unvisited; graph.len()];
    (0..graph.len()).any(|start| state[start] == State::Unvisited && visit(start, graph, &mut state))
}

fn main() {
    // 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3: D is reached twice, but there is no loop
    let diamond = vec![vec![1, 2], vec![3], vec![3], vec![]];
    assert!(!has_cycle(&diamond));

    // 0 -> 1 -> 2 -> 0: a real loop
    let triangle = vec![vec![1], vec![2], vec![0]];
    assert!(has_cycle(&triangle));

    // a node that points to itself is the smallest possible cycle
    assert!(has_cycle(&[vec![0]]));
    println!("cycle detection works");
}
```
