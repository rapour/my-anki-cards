On a bit array, what do **rank** and **select** return? Work them out on `01101001`.

---

- **rank1(p)**: how many 1s are in positions `0` to `p - 1`, that is, before `p`. **rank0(p)** counts the 0s, so `rank0(p) = p - rank1(p)`.
- **select1(k)**: the position of the 1 number `k`, counting from 0. **select0(k)** does the same for 0s.

They undo each other: `rank1(select1(k)) = k`. In the example below, `select1(2) = 4` and `rank1(4) = 2`.

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| bit | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 1 |

- `rank1(4) = 2`: positions 0 to 3 hold `0110`.
- `select1(0) = 1` and `select1(3) = 7`. The 1s are at 1, 2, 4 and 7.
- `select0(2) = 5`. The 0s are at 0, 3, 5 and 6.

Why they matter: compressed structures store their data as bit arrays and use rank and select to find their way around instead of pointers. Elias-Fano, a compressed sorted list, uses select1 to read the number at an index and select0 to find the first number at least some value. With a small extra index, both can be answered in constant time.

Libraries differ on whether rank counts position `p` itself, so check before using one.

```rust
/// Number of 1s in positions 0 .. p (p itself not included).
fn rank1(bits: &[bool], p: usize) -> usize {
    bits[..p].iter().filter(|&&b| b).count()
}

/// Number of 0s in positions 0 .. p.
fn rank0(bits: &[bool], p: usize) -> usize {
    p - rank1(bits, p)
}

/// Position of the 1 number k, counting from 0.
fn select1(bits: &[bool], k: usize) -> Option<usize> {
    let ones = bits.iter().enumerate().filter(|(_, b)| **b);
    ones.map(|(p, _)| p).nth(k)
}

/// Position of the 0 number k, counting from 0.
fn select0(bits: &[bool], k: usize) -> Option<usize> {
    let zeros = bits.iter().enumerate().filter(|(_, b)| !**b);
    zeros.map(|(p, _)| p).nth(k)
}

fn main() {
    let bits: Vec<bool> =
        "01101001".chars().map(|c| c == '1').collect();

    // positions 0 to 3 hold 0110
    assert_eq!(rank1(&bits, 4), 2);
    assert_eq!(rank0(&bits, 4), 2);
    // the 1s are at 1, 2, 4 and 7
    assert_eq!(select1(&bits, 0), Some(1));
    assert_eq!(select1(&bits, 3), Some(7));
    // there are only four 1s
    assert_eq!(select1(&bits, 4), None);
    // the 0s are at 0, 3, 5 and 6
    assert_eq!(select0(&bits, 2), Some(5));

    // rank and select undo each other
    for k in 0..4 {
        let p = select1(&bits, k).unwrap();
        assert_eq!(rank1(&bits, p), k);
    }
}
```
