Exchange rates arrive as text such as `"USD:CAD:1.3,EUR:USD:1.1"`, where each quote `FROM:TO:RATE` means that 1 unit of `FROM` buys `RATE` units of `TO`. How do you turn that text into a graph in Rust, and why do you add a reverse edge for each quote?

---

In the graph, every currency is a node and every quote is an edge with the rate as its weight.

Split the text twice: first on `,` to get each quote, then on `:` to get its parts. For each quote, store the neighbour in a map from node name to a list of `(neighbour, weight)` pairs. In Rust, `entry(key).or_default().push(...)` creates the empty list the first time a node is seen. (Python's equivalent is a `defaultdict(list)`.)

**The reverse edge.** A quote "1 USD = 1.3 CAD" works both ways: 1 CAD buys `1 / 1.3` USD. Without the reverse edge, a search could only walk in the direction the quotes happen to be written, and you could not convert CAD to USD. So we store both `USD to CAD at 1.3` and `CAD to USD at 1/1.3`.

For problems with truly one-way legs (such as flights) you add only the forward edge.

```rust
use std::collections::HashMap;

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

fn main() {
    let graph = build_graph("USD:CAD:1.3,EUR:USD:1.1");

    assert_eq!(graph["USD"].len(), 2); // USD -> CAD and USD -> EUR (the reverse)
    assert_eq!(graph["CAD"], vec![("USD", 1.0 / 1.3)]);
    assert_eq!(graph["EUR"], vec![("USD", 1.1)]);
    println!("{graph:?}");
}
```

The graph borrows its node names from the input string (that is what `<'a>` and `Graph<'_>` express), so no text is copied, but the input string must stay alive as long as the graph is in use.
