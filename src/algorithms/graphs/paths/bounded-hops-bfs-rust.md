Write a Rust function that says whether currency `to` can be reached from `from` using **at most** `max_hops` conversions, processing BFS one level at a time.

---

`level` holds every node that is exactly `i` steps from the start. Each loop iteration first checks the level for the target, and then builds the next level from unvisited neighbours. The loop runs `max_hops + 1` times, covering level 0 (the start itself) up to level `max_hops`.

```rust
use std::collections::{HashMap, HashSet};

type Graph<'a> = HashMap<&'a str, Vec<(&'a str, f64)>>;

fn build_graph(input: &str) -> Graph<'_> {
    let mut graph: Graph = HashMap::new();
    for quote in input.split(',') {
        let parts: Vec<&str> = quote.trim().split(':').collect();
        let (from, to) = (parts[0], parts[1]);
        let rate: f64 = parts[2].parse().unwrap();
        graph.entry(from).or_default().push((to, rate));
        graph.entry(to).or_default().push((from, 1.0 / rate));
    }
    graph
}

fn reachable_within<'a>(graph: &Graph<'a>, start: &'a str, target: &str, max_hops: usize) -> bool {
    let mut visited = HashSet::from([start]);
    let mut level = vec![start]; // nodes exactly `hops` steps away

    for _hops in 0..=max_hops {
        if level.iter().any(|&node| node == target) {
            return true;
        }
        let mut next_level = Vec::new();
        for &node in &level {
            for &(next, _rate) in graph.get(node).into_iter().flatten() {
                if visited.insert(next) {
                    next_level.push(next);
                }
            }
        }
        level = next_level;
    }
    false
}

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.2,GBP:USD:1.25");
    assert!(!reachable_within(&graph, "GBP", "CAD", 1)); // needs 2 conversions
    assert!(reachable_within(&graph, "GBP", "CAD", 2));
    assert!(reachable_within(&graph, "GBP", "GBP", 0)); // already there
    println!("bounded BFS works");
}
```
