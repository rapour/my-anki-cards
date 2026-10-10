Write a Rust function that returns the route with the fewest conversions between two currencies using BFS and a parent map.

---

The `parent` map answers "which node did we come from when we first found this one?". When the target comes off the queue, we follow parents backwards to the start and reverse the list.

A node is marked visited when it is added to the queue (not when it is taken out), so it can never be queued twice. The start node is the only one with no parent, which is how the backwards walk knows when to stop.

```rust
use std::collections::{HashMap, HashSet, VecDeque};

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

fn shortest_route<'a>(graph: &Graph<'a>, start: &'a str, target: &str) -> Option<Vec<&'a str>> {
    let mut parent: HashMap<&str, &str> = HashMap::new();
    let mut visited = HashSet::from([start]);
    let mut queue = VecDeque::from([start]);

    while let Some(current) = queue.pop_front() {
        if current == target {
            // walk backwards from the target to the start
            let mut route = vec![current];
            let mut node = current;
            while let Some(&before) = parent.get(node) {
                route.push(before);
                node = before;
            }
            route.reverse();
            return Some(route);
        }
        for &(next, _rate) in graph.get(current).into_iter().flatten() {
            if visited.insert(next) {
                // insert returns true only the first time we see `next`
                parent.insert(next, current);
                queue.push_back(next);
            }
        }
    }
    None // the queue ran dry without meeting the target
}

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1,GBP:EUR:1.2,GBP:USD:1.25");
    let route = shortest_route(&graph, "GBP", "CAD").unwrap();
    assert_eq!(route, vec!["GBP", "USD", "CAD"]); // two conversions, not three
    assert_eq!(shortest_route(&graph, "CAD", "NOPE"), None);
    println!("{route:?}");
}
```

Careful: "fewest conversions" is not the same as "best exchange rate". Here GBP, USD, CAD has rate 1.25 × 1.3 = 1.625, while the longer GBP, EUR, USD, CAD gives 1.2 × 1.1 × 1.3 = 1.716, which is better for the customer.
