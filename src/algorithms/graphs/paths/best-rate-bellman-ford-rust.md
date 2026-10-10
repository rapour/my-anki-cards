Write a Rust function that finds the best exchange rate from one currency to all others using logarithms and Bellman-Ford, and returns `None` if an arbitrage loop makes the answer unbounded.

---

Idea: turn each rate into the weight `-ln(rate)`. The smallest total weight is the largest product. Bellman-Ford repeats "try to improve every edge" up to `V - 1` times, which is enough for the best routes to settle if no negative loop exists. One extra pass then checks: if any edge can *still* be improved, a negative loop (arbitrage) exists.

The `1e-12` margin stops tiny floating-point rounding errors from looking like improvements.

Here the quotes are one-way (no reverse edges), and currencies are numbered: 0 = USD, 1 = EUR, 2 = GBP, 3 = CAD.

```rust
/// Best achievable product of rates from `source` to every node.
/// 0.0 means "unreachable". Returns None if arbitrage makes it unbounded.
fn best_rates(n: usize, edges: &[(usize, usize, f64)], source: usize) -> Option<Vec<f64>> {
    let mut dist = vec![f64::INFINITY; n];
    dist[source] = 0.0;

    for _ in 0..n - 1 {
        let mut changed = false;
        for &(from, to, rate) in edges {
            let weight = -rate.ln();
            if dist[from] + weight < dist[to] - 1e-12 {
                dist[to] = dist[from] + weight;
                changed = true;
            }
        }
        if !changed {
            break; // nothing improved, so nothing ever will
        }
    }

    // one more pass: any further improvement means a negative loop
    for &(from, to, rate) in edges {
        if dist[from].is_finite() && dist[from] - rate.ln() < dist[to] - 1e-12 {
            return None;
        }
    }
    Some(dist.into_iter().map(|d| (-d).exp()).collect())
}

fn main() {
    // GBP->EUR 1.2, EUR->USD 1.1, GBP->USD 1.25, USD->CAD 1.3
    let edges = [(2, 1, 1.2), (1, 0, 1.1), (2, 0, 1.25), (0, 3, 1.3)];
    let rates = best_rates(4, &edges, 2).unwrap();
    assert!((rates[3] - 1.716).abs() < 1e-9); // GBP -> CAD, best route
    assert_eq!(best_rates(4, &edges, 3).unwrap()[2], 0.0); // CAD cannot reach GBP

    // add USD->GBP at 0.9: GBP->USD->GBP now multiplies to 1.125, a money-making loop
    let looped = [(2, 1, 1.2), (1, 0, 1.1), (2, 0, 1.25), (0, 3, 1.3), (0, 2, 0.9)];
    assert!(best_rates(4, &looped, 2).is_none());
    println!("best GBP to CAD: {:.3}", rates[3]);
}
```

`dist` holds the *total of the negative logs*, so the final line converts each one back with `exp(-d)`. For an unreachable node the distance stays infinite and `exp(-inf)` is `0.0`.
