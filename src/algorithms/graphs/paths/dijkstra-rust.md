Write Dijkstra's algorithm in Rust to find the cheapest shipping route and its cost, given legs such as `"NYC:LON:air:500,NYC:PAR:air:300"`.

---

Each leg is directed and has a method (air, rail and so on) and a cost. The heap stores `(cost, node)` wrapped in `Reverse`, because Rust's `BinaryHeap` is a *max*-heap and wrapping in `Reverse` turns it into the min-heap we need.

The line `if cost > best[node] { continue; }` skips stale heap entries. We never remove old entries when we find a cheaper way to a node, so an outdated, more expensive entry may still be in the heap. When it eventually comes out we simply ignore it.

```rust
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};

struct Leg<'a> {
    to: &'a str,
    method: &'a str,
    cost: u32,
}

type Network<'a> = HashMap<&'a str, Vec<Leg<'a>>>;

fn parse_routes(input: &str) -> Network<'_> {
    let mut network: Network = HashMap::new();
    for entry in input.split(',') {
        let p: Vec<&str> = entry.trim().split(':').collect();
        network.entry(p[0]).or_default().push(Leg {
            to: p[1],
            method: p[2],
            cost: p[3].parse().unwrap(),
        });
    }
    network
}

fn cheapest_route<'a>(
    network: &Network<'a>,
    start: &'a str,
    target: &str,
) -> Option<(u32, Vec<&'a str>)> {
    let mut best: HashMap<&str, u32> = HashMap::from([(start, 0)]);
    let mut parent: HashMap<&str, &str> = HashMap::new();
    let mut heap = BinaryHeap::from([Reverse((0u32, start))]);

    while let Some(Reverse((cost, node))) = heap.pop() {
        if cost > best[node] {
            continue; // stale entry: we already found a cheaper way here
        }
        if node == target {
            let mut route = vec![node];
            let mut step = node;
            while let Some(&before) = parent.get(step) {
                route.push(before);
                step = before;
            }
            route.reverse();
            return Some((cost, route));
        }
        for leg in network.get(node).into_iter().flatten() {
            let new_cost = cost + leg.cost;
            let improves = best.get(leg.to).map_or(true, |&old| new_cost < old);
            if improves {
                best.insert(leg.to, new_cost);
                parent.insert(leg.to, node);
                heap.push(Reverse((new_cost, leg.to)));
            }
        }
    }
    None
}

fn main() {
    let network = parse_routes(
        "NYC:LON:air:500,NYC:PAR:air:300,PAR:LON:rail:100,NYC:MAD:air:100,MAD:LON:rail:350",
    );
    let (cost, route) = cheapest_route(&network, "NYC", "LON").unwrap();
    assert_eq!(cost, 400);
    assert_eq!(route, vec!["NYC", "PAR", "LON"]); // 2 legs, but cheaper than the 1-leg route
    assert_eq!(cheapest_route(&network, "LON", "NYC"), None); // legs are one-way
    println!("{cost} via {route:?}");
}
```

(`method` is parsed but not used here. It would matter if the problem asked you to print how each leg is travelled.)
