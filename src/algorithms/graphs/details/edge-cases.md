What standard **edge cases** should you handle in graph problems like currency conversion, and how do you write them in Rust? Include the floating-point warning.

---

Decide each of these before you write the main loop. Interviewers often look for them.

| Situation | Typical answer |
|---|---|
| Source equals target (EUR to EUR) | Return the amount unchanged (rate 1.0), a route of length zero |
| A currency that does not appear in the data | Return "not possible" (`None` in Rust, `-1` in many interview statements) |
| Both currencies exist but are on separate islands (no route) | Return "not possible" |
| Empty input | Every query is "not possible" |

**Floating-point numbers are inexact.** `1.1 * 1.3` is not stored as exactly 1.43, and going USD to CAD and back may give 0.9999999999999999 instead of 1. So:

- never compare floats with `==`; compare with a tolerance, such as `(a - b).abs() < 1e-9`;
- round only when you **print or return** the final answer, never in the middle of the calculation.

Order of checks matters: confirm both currencies exist *before* you say "same currency, rate 1.0", so that a request such as `XYZ` to `XYZ` is still rejected if `XYZ` is unknown.

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

fn rate_between<'a>(
    graph: &Graph<'a>,
    current: &'a str,
    target: &str,
    product: f64,
    visited: &mut HashSet<&'a str>,
) -> Option<f64> {
    if current == target {
        return Some(product);
    }
    visited.insert(current);
    for &(next, rate) in graph.get(current).into_iter().flatten() {
        if !visited.contains(next) {
            if let Some(found) = rate_between(graph, next, target, product * rate, visited) {
                return Some(found);
            }
        }
    }
    None
}

fn convert(graph: &Graph, from: &str, to: &str, amount: f64) -> Option<f64> {
    if !graph.contains_key(from) || !graph.contains_key(to) {
        return None; // unknown currency
    }
    if from == to {
        return Some(amount); // nothing to convert
    }
    let (from, _) = graph.get_key_value(from).unwrap(); // borrow the name from the graph
    rate_between(graph, from, to, 1.0, &mut HashSet::new()).map(|rate| amount * rate)
}

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1,JPY:KRW:9.0");

    assert_eq!(convert(&graph, "EUR", "EUR", 50.0), Some(50.0)); // same currency
    assert_eq!(convert(&graph, "XYZ", "XYZ", 50.0), None); // unknown currency
    assert_eq!(convert(&graph, "EUR", "JPY", 50.0), None); // separate islands

    let cad = convert(&graph, "EUR", "CAD", 100.0).unwrap();
    assert!((cad - 143.0).abs() < 1e-9); // compare with a tolerance, never ==
    println!("100 EUR = {cad:.2} CAD"); // round only when printing
}
```
