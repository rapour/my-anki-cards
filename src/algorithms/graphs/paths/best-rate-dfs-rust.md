Write a Rust function that finds the best (highest) exchange rate between two currencies by trying every simple route with DFS.

---

We carry the running product of rates as we walk. A node is added to `on_path` when we step into it and removed when we step back out, so each route is free to reuse nodes that belong to *other* routes. At the target we return the product, and each node keeps the best value reported by any of its branches.

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

fn best_rate<'a>(
    graph: &Graph<'a>,
    current: &'a str,
    target: &str,
    product: f64,
    on_path: &mut HashSet<&'a str>,
) -> Option<f64> {
    if current == target {
        return Some(product);
    }
    on_path.insert(current);
    let mut best: Option<f64> = None;
    for &(next, rate) in graph.get(current).into_iter().flatten() {
        if on_path.contains(next) {
            continue; // a simple route never repeats a node
        }
        if let Some(found) = best_rate(graph, next, target, product * rate, on_path) {
            best = Some(best.map_or(found, |b| b.max(found)));
        }
    }
    on_path.remove(current); // undo, so other routes may use this node
    best
}

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.2,GBP:USD:1.25");
    let rate = best_rate(&graph, "GBP", "CAD", 1.0, &mut HashSet::new()).unwrap();
    // via EUR and USD: 1.2 * 1.1 * 1.3 = 1.716 beats the direct GBP->USD route: 1.625
    assert!((rate - 1.716).abs() < 1e-9);
    assert_eq!(best_rate(&graph, "GBP", "NOPE", 1.0, &mut HashSet::new()), None);
    println!("best GBP to CAD: {rate:.3}");
}
```

The cost grows exponentially with the number of nodes in the worst case, because the function explores every simple route.
