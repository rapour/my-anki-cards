Write a Rust function `can_reach` that says whether currency `from` can be converted into currency `to`, given quotes such as `"USD:CAD:1.3,EUR:USD:1.1"`. Use DFS with a visited set.

---

The function first turns the text into a graph (each quote becomes two edges: the quote itself and its reverse with rate `1/rate`). Then `can_reach` walks the graph depth first. Every node is added to `visited` the moment we arrive at it, so no node is explored twice and loops cannot trap us. `reachable` is the entry point: it checks that both currencies are in the graph before searching, so an unknown currency is rejected even when it is compared with itself.

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

fn reachable(graph: &Graph, from: &str, to: &str) -> bool {
    // look both names up first: an unknown currency is never reachable, even from itself
    match graph.get_key_value(from) {
        Some((from, _)) if graph.contains_key(to) => {
            can_reach(graph, from, to, &mut HashSet::new())
        }
        _ => false,
    }
}

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.2,JPY:KRW:9.0");

    // EUR -> USD -> CAD exists
    assert!(reachable(&graph, "EUR", "CAD"));
    // JPY and KRW live on a separate island
    assert!(!reachable(&graph, "EUR", "JPY"));
    // a currency that is not in the data at all
    assert!(!reachable(&graph, "XYZ", "USD"));
    // the same currency twice: fine if it exists, rejected if it does not
    assert!(reachable(&graph, "EUR", "EUR"));
    assert!(!reachable(&graph, "XYZ", "XYZ"));
    println!("reachability works");
}
```

Notes on the Rust details:

- `graph.get(current).into_iter().flatten()` means "the neighbours of `current`, or nothing at all if `current` is not in the graph".
- `reachable` creates a fresh `HashSet` for every search, because the visited set belongs to one search.
- The BFS version is identical in outcome. Replace the recursion with a `VecDeque` (see the BFS card).
