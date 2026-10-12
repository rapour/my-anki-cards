What is the recursive rule for `aⁿ` that halves the exponent, and why must the half be computed only once?

---

- `n = 0`: the answer is `1`.
- `n` even: `aⁿ = (a^(n/2))²`.
- `n` odd: `aⁿ = (a^((n−1)/2))² · a`.

In Rust integer division does the `(n−1)/2` for you, because `n / 2` rounds down.

```rust
fn power(base: u64, exp: u64) -> u64 {
    if exp == 0 {
        return 1;
    }
    // call once, then square the answer
    let half = power(base, exp / 2);
    if exp % 2 == 1 {
        half * half * base // odd exponent: one extra factor
    } else {
        half * half
    }
}

fn main() {
    assert_eq!(power(3, 13), 1_594_323);
    assert_eq!(power(2, 0), 1);
    assert_eq!(power(5, 1), 5);
    assert_eq!(power(3, 40), 12_157_665_459_056_928_801);
}
```

For `3¹³` the calls go `13 → 6 → 3 → 1 → 0`, so only 5 calls, not 13.

**Call `power` only once per level.** Writing `power(base, exp / 2) * power(base, exp / 2)` makes two calls at every level, which brings the cost back to `O(n)`. Store the half in a variable, then square it.
