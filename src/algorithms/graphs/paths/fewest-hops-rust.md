Write a Rust function that returns the smallest number of conversions between two currencies using BFS and a distance map.

---

`distance` does two jobs at once: it records how many steps it took to reach a node, and, because a node is only inserted the first time we see it, it also acts as the visited set. A node never gets a second, longer distance.

```rust
use std::collections::{HashMap, VecDeque};

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

fn fewest_conversions(graph: &Graph, start: &str, target: &str) -> Option<usize> {
    let mut distance: HashMap<&str, usize> = HashMap::from([(start, 0)]);
    let mut queue = VecDeque::from([start]);

    while let Some(current) = queue.pop_front() {
        if current == target {
            return Some(distance[current]); // first arrival is the shortest
        }
        for &(next, _rate) in graph.get(current).into_iter().flatten() {
            if !distance.contains_key(next) {
                distance.insert(next, distance[current] + 1);
                queue.push_back(next);
            }
        }
    }
    None
}

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.2,GBP:USD:1.25");
    assert_eq!(fewest_conversions(&graph, "GBP", "CAD"), Some(2));
    assert_eq!(fewest_conversions(&graph, "EUR", "EUR"), Some(0));
    assert_eq!(fewest_conversions(&graph, "EUR", "NOPE"), None);
    println!("fewest conversions GBP to CAD: 2");
}
```
