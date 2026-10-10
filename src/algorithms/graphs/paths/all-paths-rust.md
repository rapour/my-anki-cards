Write a Rust function that returns every simple route between two currencies, using DFS backtracking with an on-path set.

---

Each call pushes the current node on entry and pops it on exit, so `path` and `on_path` always describe the route being built. When we reach the target we store a **clone** of the path (a copy), because `path` keeps changing afterwards.

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

fn collect_routes<'a>(
    graph: &Graph<'a>,
    current: &'a str,
    target: &str,
    path: &mut Vec<&'a str>,
    on_path: &mut HashSet<&'a str>,
    routes: &mut Vec<Vec<&'a str>>,
) {
    path.push(current);
    on_path.insert(current);

    if current == target {
        routes.push(path.clone()); // save a copy of this finished route
    } else {
        for &(next, _rate) in graph.get(current).into_iter().flatten() {
            if !on_path.contains(next) {
                collect_routes(graph, next, target, path, on_path, routes);
            }
        }
    }

    path.pop(); // undo: backtrack
    on_path.remove(current);
}

fn all_routes<'a>(graph: &Graph<'a>, from: &'a str, to: &str) -> Vec<Vec<&'a str>> {
    let mut routes = Vec::new();
    collect_routes(graph, from, to, &mut Vec::new(), &mut HashSet::new(), &mut routes);
    routes
}

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.2,GBP:USD:1.25");
    let routes = all_routes(&graph, "GBP", "CAD");
    assert_eq!(
        routes,
        vec![vec!["GBP", "EUR", "USD", "CAD"], vec!["GBP", "USD", "CAD"]]
    );
    println!("{routes:?}");
}
```
