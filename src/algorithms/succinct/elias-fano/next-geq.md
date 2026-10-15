Elias-Fano stores each number `x` of a sorted list as a low part (its lowest `l` bits, kept in an array) and a high part `x >> l`. The high parts are kept as a bit array: for each *bucket* (each possible high part) in order, one `1` per number in it, then a `0` that closes the bucket. How do you find the first number that is at least `y`?

---

Jump to the start of `y`'s bucket with **select0**, then scan forward.

**select0(k)** returns the position of the 0 number `k`, counting from 0.

1. `h = y >> l` is the bucket `y` falls into.
2. All numbers in buckets `0` to `h - 1` come before the `0` that closes bucket `h - 1`, which is the 0 number `h - 1`. Let `p = select0(h - 1)`. When `h = 0`, start at index 0 instead.
3. Before position `p` there are `h - 1` zeros, so the other `p - (h - 1)` bits are 1s, one per number. Start at index `i = p - (h - 1)`.
4. Read numbers from index `i` onwards until one is at least `y`.

There are at least `n` buckets, so a bucket holds at most one number on average and the scan is short. Search engines use this search to intersect two sorted lists of document ids: each list jumps forward to the first id that is at least the other list's current id.

Example: 3, 4, 7, 13, 14, 15, 21, 43 with `l = 2` and high bits `10110011100100000100`.

- For `y = 8`: `h = 2`. The 0 number 1 is at position 4, so `i = 4 - 1 = 3`.
- Index 3 holds 13, and 13 ≥ 8, so the answer is index 3.

```rust
struct EliasFano {
    l: u32,
    low: Vec<u64>,
    high: Vec<bool>,
}

fn encode(values: &[u64], u: u64) -> EliasFano {
    let n = values.len() as u64;
    let l = if u > n { (u / n).ilog2() } else { 0 };
    let mut high = vec![false; (n + (u >> l) + 1) as usize];
    let mut low = Vec::new();
    for (i, &x) in values.iter().enumerate() {
        low.push(x & ((1 << l) - 1));
        high[(x >> l) as usize + i] = true;
    }
    EliasFano { l, low, high }
}

/// Position of the 0 number `k` (counting from 0) in the bits.
fn select0(bits: &[bool], k: usize) -> Option<usize> {
    bits.iter().enumerate().filter(|(_, b)| !**b).nth(k).map(|(p, _)| p)
}

/// Index of the first number >= y, or None if all are smaller.
fn next_geq(ef: &EliasFano, y: u64) -> Option<usize> {
    // the bucket y falls into
    let h = (y >> ef.l) as usize;
    // skip the numbers of buckets 0 to h - 1: start at the 0 that
    // closes bucket h - 1, or at the very start when h = 0
    let (start, mut i) = if h == 0 {
        (0, 0)
    } else {
        // y is past every bucket when that 0 does not exist
        let p = select0(&ef.high, h - 1)?;
        (p, p - (h - 1))
    };
    // scan forward, rebuilding each number from its 1 and low part
    for q in start..ef.high.len() {
        if ef.high[q] {
            let x = (((q - i) as u64) << ef.l) | ef.low[i];
            if x >= y {
                return Some(i);
            }
            i += 1;
        }
    }
    None
}

fn main() {
    let values = [3, 4, 7, 13, 14, 15, 21, 43];
    let ef = encode(&values, 44);

    // 13 is the first number >= 8
    assert_eq!(next_geq(&ef, 8), Some(3));
    // an exact match
    assert_eq!(next_geq(&ef, 21), Some(6));
    assert_eq!(next_geq(&ef, 0), Some(0));
    // nothing is that big
    assert_eq!(next_geq(&ef, 44), None);

    // compare with a plain search for every y
    for y in 0..50 {
        let want = values.iter().position(|&v| v >= y);
        assert_eq!(next_geq(&ef, y), want, "y = {y}");
    }
}
```
