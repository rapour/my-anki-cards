Write a Rust function that detects currency arbitrage (a loop of conversions that returns more than you started with) using Bellman-Ford on `-ln(rate)`.

---

All distances start at zero, so every loop in the graph can be found no matter where it is. If the graph still improves in the final round (round number `n`), there must be a negative cycle. A `changed` flag lets us stop early with `false` as soon as a round improves nothing.

Currencies are numbered: 0 = USD, 1 = EUR, 2 = GBP.

```rust
fn has_arbitrage(currencies: usize, quotes: &[(usize, usize, f64)]) -> bool {
    let mut dist = vec![0.0_f64; currencies]; // every node starts at 0

    for _round in 0..currencies {
        let mut changed = false;
        for &(from, to, rate) in quotes {
            let weight = -rate.ln();
            if dist[from] + weight < dist[to] - 1e-12 {
                dist[to] = dist[from] + weight;
                changed = true;
            }
        }
        if !changed {
            return false; // settled before the last round: no negative cycle
        }
    }
    true // still improving in round `currencies`: a negative cycle exists
}

fn main() {
    // USD->EUR 0.9, EUR->GBP 0.8, GBP->USD 1.5 multiplies to 1.08: money from nothing
    let profitable = [(0, 1, 0.9), (1, 2, 0.8), (2, 0, 1.5)];
    assert!(has_arbitrage(3, &profitable));

    // GBP->USD 1.3 makes the loop multiply to 0.936: you lose money going round
    let fair = [(0, 1, 0.9), (1, 2, 0.8), (2, 0, 1.3)];
    assert!(!has_arbitrage(3, &fair));
    println!("arbitrage detection works");
}
```

To also report *which* loop it is, record each node's predecessor whenever you update it. Then take a node that changed in the last round and follow predecessors back `V` times, which is guaranteed to land inside the loop. From there, keep following predecessors until you return to the same node.
