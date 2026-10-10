Write a Rust function `can_reach` that says whether currency `from` can be converted into currency `to`, given quotes such as `"USD:CAD:1.3,EUR:USD:1.1"`. Use DFS with a visited set.

---

The function first turns the text into a graph (each quote becomes two edges: the quote itself and its reverse with rate `1/rate`). Then `can_reach` walks the graph depth first. Every node is added to `visited` the moment we arrive at it, so no node is explored twice and loops cannot trap us.

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
        graph.entry(to).or_default().push((from, 1.0 / rate)); // the way back
    }
    graph
}

fn can_reach<'a>(
    graph: &Graph<'a>,
    current: &'a str,
    target: &str,
    visited: &mut HashSet<&'a str>,
) -> bool {
    if current == target {
        return true; // arrived
    }
    visited.insert(current);
    for &(next, _rate) in graph.get(current).into_iter().flatten() {
        if !visited.contains(next) && can_reach(graph, next, target, visited) {
            return true; // one successful branch is enough
        }
    }
    false // every branch from here was a dead end
}

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.2,JPY:KRW:9.0");

    // EUR -> USD -> CAD exists
    assert!(can_reach(&graph, "EUR", "CAD", &mut HashSet::new()));
    // JPY and KRW live on a separate island
    assert!(!can_reach(&graph, "EUR", "JPY", &mut HashSet::new()));
    // a currency that is not in the data at all
    assert!(!can_reach(&graph, "XYZ", "USD", &mut HashSet::new()));
    println!("reachability works");
}
```

Notes on the Rust details:

- `graph.get(current).into_iter().flatten()` means "the neighbours of `current`, or nothing at all if `current` is not in the graph".
- Each top-level call needs a fresh `HashSet`, because the visited set belongs to one search.
- The BFS version is identical in outcome. Replace the recursion with a `VecDeque` (see the BFS card).
