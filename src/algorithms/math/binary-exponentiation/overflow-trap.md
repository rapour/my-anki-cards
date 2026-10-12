Why can a binary exponentiation function panic in a debug build for `3⁴⁰`, even though the answer fits in a `u64`?

---

The loop squares `base` once more after the last bit, even though that square is never used. For `3⁴⁰` the last square would be `3⁶⁴`, which does not fit in a `u64`, so a debug build stops with *attempt to multiply with overflow*. A release build wraps around quietly, so the bug can hide until you test in debug mode.

```rust
fn power(mut base: u64, mut exp: u64) -> u64 {
    let mut result = 1;
    while exp > 0 {
        if exp & 1 == 1 {
            result *= base;
        }
        // also runs after the last bit, where the square is never used
        base *= base;
        exp >>= 1;
    }
    result
}
// power(3, 40) panics in a debug build
```

**Fix:** shift first, and only square when there are bits left:

```rust
fn power(mut base: u64, mut exp: u64) -> u64 {
    let mut result = 1;
    while exp > 0 {
        if exp & 1 == 1 {
            result *= base;
        }
        exp >>= 1;
        if exp > 0 {
            base *= base; // only square when more bits are left
        }
    }
    result
}
```

The recursive version does not have this problem.
