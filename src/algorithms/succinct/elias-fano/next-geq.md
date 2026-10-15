Elias-Fano stores each number `x` of a sorted list as a low part (its lowest `l` bits, kept in an array) and a high part `x >> l`. The high parts are kept as a bit array: for each *bucket* (each possible high part) in order, one `1` per number in it, then a `0` that closes the bucket. How do you find the first number that is at least `y`?

---

Jump to the start of `y`'s bucket with **select0**, then scan forward.

**select0(k)** returns the position of the 0 number `k`, counting from 0.

1. `h = y >> l` is the bucket `y` falls into.
2. All numbers in buckets `0` to `h - 1` come before the `0` that closes bucket `h - 1`, which is the 0 number `h - 1`. Let `p = select0(h - 1)`. When `h = 0`, start at index 0 instead.
3. Before position `p` there are `h - 1` zeros, so the other `p - (h - 1)` bits are 1s, one per number. Start at index `i = p - (h - 1)`.
4. Read numbers from index `i` onwards until one is at least `y`.

There are at least `n` buckets, so a bucket holds at most one number on average and the scan is short.

Example: 3, 4, 7, 13, 14, 15, 21, 43 with `l = 2` and high bits `10110011100100000100`.

- For `y = 8`: `h = 2`. The 0 number 1 is at position 4, so `i = 4 - 1 = 3`.
- Index 3 holds 13, and 13 ≥ 8, so the answer is index 3.
- For `y = 14`: `h = 3`. The 0 number 2 is at position 5, so `i = 5 - 2 = 3`. Index 3 holds 13, which is too small, so the scan moves on: index 4 holds 14, the answer.

Search engines use this search to find the documents that contain two words. Each word has a sorted list of the ids of the documents that contain it. For each id of the first list, `next_geq` on the second list finds the first id that is at least as large; when it is equal, both words are in that document. Taking 4, 14, 22, 43 as the first list, `next_geq` on the list above finds 4, 14, 43 and 43, so the common ids are 4, 14 and 43.

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
    // the scan passes 13 to reach 14
    assert_eq!(next_geq(&ef, 14), Some(4));
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

    // ids in both lists: next_geq lands exactly on them
    let first = [4, 14, 22, 43];
    let mut common = Vec::new();
    for y in first {
        if let Some(i) = next_geq(&ef, y) {
            if values[i] == y {
                common.push(y);
            }
        }
    }
    assert_eq!(common, vec![4, 14, 43]);
}
```
