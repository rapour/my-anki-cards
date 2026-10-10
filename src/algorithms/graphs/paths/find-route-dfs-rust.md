Write a Rust function that returns the actual route between two currencies using DFS and a path stack.

---

`path` is the route from the start to the node we are standing on. We push on entry and pop when a node leads nowhere. When we reach the target we return `true` and leave `path` untouched, so it holds the finished route.

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

fn search<'a>(
    graph: &Graph<'a>,
    current: &'a str,
    target: &str,
    visited: &mut HashSet<&'a str>,
    path: &mut Vec<&'a str>,
) -> bool {
    path.push(current); // step into the node
    if current == target {
        return true; // keep the path as it is
    }
    visited.insert(current);
    for &(next, _rate) in graph.get(current).into_iter().flatten() {
        if !visited.contains(next) && search(graph, next, target, visited, path) {
            return true;
        }
    }
    path.pop(); // dead end: step back out
    false
}

fn find_route<'a>(graph: &Graph<'a>, from: &'a str, to: &str) -> Option<Vec<&'a str>> {
    let mut path = Vec::new();
    search(graph, from, to, &mut HashSet::new(), &mut path).then_some(path)
}

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.2,GBP:USD:1.25");
    let route = find_route(&graph, "GBP", "CAD").unwrap();
    // DFS follows the first neighbour each time: GBP -> EUR -> USD -> CAD
    assert_eq!(route, vec!["GBP", "EUR", "USD", "CAD"]);
    assert_eq!(find_route(&graph, "CAD", "CAD"), Some(vec!["CAD"]));
    assert_eq!(find_route(&graph, "CAD", "NOPE"), None);
    println!("{route:?}");
}
```

Notice that the route found has three conversions even though a two-step route (GBP, USD, CAD) exists. DFS gives *a* route, not the shortest. For the shortest, use the BFS version.
