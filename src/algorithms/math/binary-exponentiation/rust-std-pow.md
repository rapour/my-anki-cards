Does Rust's standard library already do exponentiation by squaring, and how does it handle overflow?

---

Yes. The integer types have `pow`, which uses exponentiation by squaring, and three variants that say what to do on overflow:

```rust
fn main() {
    assert_eq!(3u64.pow(13), 1_594_323);
    assert_eq!(10u64.checked_pow(19), Some(10_000_000_000_000_000_000));
    // 10^20 does not fit: None, not a panic
    assert_eq!(10u64.checked_pow(20), None);
    // wraps around modulo 2^32
    assert_eq!(2u32.wrapping_pow(33), 0);
    // the wrapped value and an overflow flag
    assert_eq!(2u8.overflowing_pow(8), (0, true));
}
```

- `pow` panics on overflow in a debug build.
- `checked_pow` returns `None`.
- `wrapping_pow` wraps around modulo `2^bits`.
- `overflowing_pow` returns the wrapped value and a flag.
- There is **no** modular `pow` in the standard library. For `a^b mod m` you write your own: binary exponentiation with a remainder after every multiplication.
