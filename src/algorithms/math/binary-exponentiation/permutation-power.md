How do you apply the same shuffle (permutation) `k` times, for a huge `k`, in `O(n log k)`?

---

Doing a shuffle twice is itself a shuffle: you can **combine** two permutations into one. Combining is associative, and "move nothing" is the identity, so binary exponentiation applies. Square the permutation, combine it into the result when the bit is set, and apply the final permutation **once**.

`compose(a, b)[i] = a[b[i]]` combines two permutations in `O(n)`.

```rust
/// Doing `b` first and then `a`: the result moves item i to
/// a[b[i]].
fn compose(a: &[usize], b: &[usize]) -> Vec<usize> {
    (0..a.len()).map(|i| a[b[i]]).collect()
}

fn permutation_power(mut p: Vec<usize>, mut k: u64) -> Vec<usize> {
    // identity: nothing moves
    let mut result: Vec<usize> = (0..p.len()).collect();
    while k > 0 {
        if k & 1 == 1 {
            result = compose(&result, &p);
        }
        k >>= 1;
        if k > 0 {
            p = compose(&p, &p);
        }
    }
    result
}

/// One round of the shuffle: position i of the new row takes the
/// item
/// from position p[i].
fn apply(items: &[char], p: &[usize]) -> Vec<char> {
    p.iter().map(|&i| items[i]).collect()
}

fn main() {
    // positions 0, 1, 2 rotate; positions 3 and 4 stay
    let p = vec![1, 2, 0, 3, 4];
    let start: Vec<char> = "ABCDE".chars().collect();

    // shuffling 5 times one by one gives the same row as applying
    // p^5
    // once
    let mut slow = start.clone();
    for _ in 0..5 {
        slow = apply(&slow, &p);
    }
    assert_eq!(apply(&start, &permutation_power(p.clone(), 5)), slow);

    // the rotation repeats every 3 rounds, so 3 * 10^18 rounds
    // change
    // nothing
    let identity: Vec<usize> = (0..5).collect();
    assert_eq!(
        permutation_power(p.clone(), 3_000_000_000_000_000_000),
        identity
    );
    assert_eq!(
        permutation_power(p.clone(), 3_000_000_000_000_000_001),
        p
    );
}
```

- The answer is a permutation too, so `k` can be as large as 10¹⁸.
- There is also a linear-time method: split the permutation into cycles and move each item `k mod (cycle length)` places.
