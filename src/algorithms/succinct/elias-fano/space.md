Elias-Fano stores a sorted list of `n` numbers below `u` by splitting each number into a low part and a high part. How many bits does it use, and why?

---

At most about **2 + log2(u / n) bits per number**.

How the encoding spends its bits:

- With `l = floor(log2(u / n))`, the **low part** of each number is its lowest `l` bits, stored as they are.
- The **high part** `x >> l` is written into a bit array, the **high bits**: one `1` per number, and one `0` closing each *bucket* (each possible high part). There are about `u / 2^l` buckets.

Per number that is `l + 1 + u / (n · 2^l)` bits. Write `u / n = 2^(l + f)`, where `f` is between 0 and 1. The total becomes `log2(u / n) - f + 1 + 2^f`. Since `2^f - f` is at most 1 in that range, the total is at most `log2(u / n) + 2`.

**How close to the best possible?** There are "u choose n" different sets of `n` numbers below `u`, so any encoding needs at least `log2(u choose n)` bits to tell them apart. When `n` is much smaller than `u`, that is about `log2(u / n) + 1.44` bits per number, so Elias-Fano then uses at most about half a bit per number more than the minimum.

Example: one million sorted numbers below 2^32, such as the ids of the documents that contain one word in a search engine.

- `u / n ≈ 4295 ≈ 2^12.07`, so `l = 12` and `f ≈ 0.07`.
- Low parts: 12 bits per number.
- High bits: 1 bit for each number's `1`, plus `2^32 / 2^12 = 1,048,576` 0s shared by a million numbers, about 1.05 bits each.
- Total: about 14.05 bits per number, under the bound `12.07 + 2 = 14.07`, instead of 32 for a plain `u32`.
- The minimum, `log2(u choose n)`, is about 13.51 bits per number, so Elias-Fano uses 0.54 bits per number more.

```rust
/// Bits used by Elias-Fano for n sorted numbers below u.
fn ef_bits(u: u64, n: u64) -> u64 {
    let l = if u > n { (u / n).ilog2() as u64 } else { 0 };
    // l bits per number
    let low = n * l;
    // one 1 per number, plus about u >> l 0s
    let high = n + (u >> l) + 1;
    low + high
}

/// log2 of "u choose n": the fewest bits that can tell apart
/// every possible set of n distinct numbers below u.
fn lower_bound(u: u64, n: u64) -> f64 {
    (0..n).map(|i| ((u - i) as f64 / (n - i) as f64).log2()).sum()
}

fn main() {
    // the bound holds for every size we try
    for n in 1..300u64 {
        for u in n..3000u64 {
            let per = 2.0 + (u as f64 / n as f64).log2();
            let bound = n as f64 * per;
            assert!(ef_bits(u, n) as f64 <= bound + 1.0, "u={u} n={n}");
        }
    }

    // one million numbers below 2^32
    let (u, n) = (1u64 << 32, 1_000_000u64);
    let per_number = ef_bits(u, n) as f64 / n as f64;
    let best = lower_bound(u, n) / n as f64;
    // instead of 32 bits
    assert!((per_number - 14.05).abs() < 0.01);
    // no encoding can go below this
    assert!((best - 13.51).abs() < 0.01);
}
```
