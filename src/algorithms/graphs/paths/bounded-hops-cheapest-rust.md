Write a Rust function that finds the cheapest shipping cost from one place to another using **at most** `max_legs` legs, using Bellman-Ford rounds (the LeetCode 787 pattern).

---

Each of the `max_legs` rounds allows one extra leg. The line `let previous = dist.clone();` is the heart of the method: every update in a round reads from `previous` (the table as it was at the *start* of the round) and writes into `dist`. That guarantees that a single round extends routes by exactly one leg.

`u32::MAX` means "not reachable yet", so we check for it before adding a cost to avoid overflow.

Places are numbered: 0 = NYC, 1 = LON, 2 = PAR, 3 = MAD.

```rust
fn cheapest_within(
    places: usize,
    legs: &[(usize, usize, u32)], // (from, to, cost)
    start: usize,
    target: usize,
    max_legs: usize,
) -> Option<u32> {
    let mut dist = vec![u32::MAX; places];
    dist[start] = 0;

    for _round in 0..max_legs {
        let previous = dist.clone(); // freeze the last round's answers
        for &(from, to, cost) in legs {
            if previous[from] != u32::MAX && previous[from] + cost < dist[to] {
                dist[to] = previous[from] + cost;
            }
        }
    }
    (dist[target] != u32::MAX).then_some(dist[target])
}

fn main() {
    let legs = [
        (0, 1, 500), // NYC -> LON
        (0, 2, 300), // NYC -> PAR
        (2, 1, 100), // PAR -> LON
        (0, 3, 100), // NYC -> MAD
        (3, 1, 350), // MAD -> LON
    ];
    assert_eq!(cheapest_within(4, &legs, 0, 1, 1), Some(500)); // only the direct leg fits
    assert_eq!(cheapest_within(4, &legs, 0, 1, 2), Some(400)); // via PAR becomes possible
    assert_eq!(cheapest_within(4, &legs, 1, 0, 3), None); // legs are one-way
    println!("bounded cheapest works");
}
```
