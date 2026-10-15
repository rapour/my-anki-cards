rise-rs, a Rust library for search engine indexes, stores sorted lists with Elias-Fano: each number is split into a low part (its lowest `l` bits) and a high part, and the high parts go into a bit array, the **high bits**. To jump around quickly, rise-rs also stores the position in the high bits of every 256th 1 and every 512th 0. How much space do these stored positions cost?

---

Very little: **at most about `w / 128` bits per number**, where `w` is the width of one stored position. With `w = 21`, as in the example below, that is about 0.16 bits per number.

Each stored position takes `w = ceil(log2(length of the high bits))` bits.

- **Positions of 1s**: one per 256 numbers, so `w / 256` bits per number.
- **Positions of 0s**: the high bits hold at most about `2n` 0s for `n` numbers, so at most `2n / 512` positions. That is also about `w / 256` bits per number.

rise-rs keeps the whole list in one bit array laid out as `[ 0 positions | 1 positions | low parts | high bits ]`.

Example: one million numbers below 2^32.

| Part | Bits |
|---|---|
| low parts (`l = 12`) | 12,000,000 |
| high bits | 2,048,578 |
| 2048 positions of 0s, 21 bits each | 43,008 |
| 3906 positions of 1s, 21 bits each | 82,026 |
| **total** | **14,173,612** |

That is about 14.17 bits per number, instead of 32, and the stored positions are 0.88% of it.

```rust
/// floor(log2(v)), and 0 for v = 0, like rise-rs's msb()
fn msb(v: u64) -> u64 {
    v.checked_ilog2().unwrap_or(0) as u64
}

/// ceil(log2(v)) for v >= 1, like rise-rs's ceil_log2()
fn ceil_log2(v: u64) -> u64 {
    if v == 1 {
        0
    } else {
        msb(v - 1) + 1
    }
}

/// Bits of each part of rise-rs's Elias-Fano for n numbers below u:
/// (low parts, high bits, positions of 0s, positions of 1s).
fn ef_bits(u: u64, n: u64) -> (u64, u64, u64, u64) {
    let l = if u > n { msb(u / n) } else { 0 };
    // the high bits, with a 0 at each end
    let high_len = n + (u >> l) + 2;
    // width of one stored position
    let w = ceil_log2(high_len);
    let low = n * l;
    // every 512th 0 and every 256th 1
    let zero_positions = ((high_len - n) >> 9) * w;
    let one_positions = (n >> 8) * w;
    (low, high_len, zero_positions, one_positions)
}

fn main() {
    let (low, high, zeros, ones) = ef_bits(1 << 32, 1_000_000);
    // l = floor(log2(4294.97)) = 12
    assert_eq!(low, 12_000_000);
    assert_eq!(high, 2_048_578);
    // ceil(log2(2_048_578)) = 21 bits per position
    assert_eq!(zeros, 2048 * 21);
    assert_eq!(ones, 3906 * 21);

    let total = low + high + zeros + ones;
    assert_eq!(total, 14_173_612);
    let share = (zeros + ones) as f64 / total as f64;
    assert!((share - 0.0088).abs() < 0.0001);
}
```
