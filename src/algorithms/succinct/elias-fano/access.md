Elias-Fano stores each number `x` of a sorted list as a low part (its lowest `l` bits, kept in an array) and a high part `x >> l`. The high parts are kept as a bit array in which number `i` (counting from 0) sets the bit at position `(x >> l) + i`. How do you read the number at index `i`?

---

Find the position of the `1` of number `i` in the high bits, subtract `i`, and put the low part back:

1. `pos = select1(i)`. **select1(k)** returns the position of the 1 number `k`, counting from 0.
2. `high = pos - i`. The `i` numbers before it each added a `1` in front of it and pushed it right by one.
3. `x = (high << l) | low[i]`.

Example: 3, 4, 7, 13, 14, 15, 21, 43 below `u = 44`, so `l = 2`, and the high bits are `10110011100100000100`.

- Index 6: the 1 number 6 is at position 11.
- `high = 11 - 6 = 5`, and `low[6] = 1`.
- `(5 << 2) | 1 = 21`.

The cost is one select. With a small extra index (stored positions of every few hundred 1s, plus a short scan), select is fast, close to constant time in practice. The code below scans instead, to keep it short.

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

/// Position of the 1 number `k` (counting from 0) in the bits.
fn select1(bits: &[bool], k: usize) -> usize {
    bits.iter().enumerate().filter(|(_, b)| **b).nth(k).unwrap().0
}

/// The number at index `i`.
fn access(ef: &EliasFano, i: usize) -> u64 {
    // remove the i 1s that come before it
    let high = (select1(&ef.high, i) - i) as u64;
    (high << ef.l) | ef.low[i]
}

fn main() {
    let values = [3, 4, 7, 13, 14, 15, 21, 43];
    let ef = encode(&values, 44);

    // index 6: its 1 is at position 11, high = 11 - 6 = 5,
    // and (5 << 2) | 1 = 21
    assert_eq!(select1(&ef.high, 6), 11);
    assert_eq!(access(&ef, 6), 21);

    for (i, &x) in values.iter().enumerate() {
        assert_eq!(access(&ef, i), x);
    }
}
```
