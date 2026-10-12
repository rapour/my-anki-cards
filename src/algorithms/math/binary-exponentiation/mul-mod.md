How do you compute `a · b mod m` using only `u64`, when `m` is close to 2⁶³ and the product does not fit?

---

Use the same trick as binary exponentiation, but with **addition** instead of multiplication. Write `b` in binary, and add the doubles of `a` (`a`, `2a`, `4a`, ...) that match its set bits, taking the remainder each time:

```rust
/// a * b mod m without a wider type. Needs m < 2^63 so that a + a
/// cannot
/// overflow.
fn mul_mod(mut a: u64, mut b: u64, m: u64) -> u64 {
    let mut result = 0;
    a %= m;
    while b > 0 {
        if b & 1 == 1 {
            // add this multiple of a
            result = (result + a) % m;
        }
        a = (a + a) % m; // a, 2a, 4a, 8a, ...
        b >>= 1;
    }
    result
}

fn main() {
    assert_eq!(mul_mod(7, 8, 5), 1);

    let m = 4_611_686_018_427_387_847; // close to 2^62
    let mut x: u64 = 123_456_789;
    for _ in 0..1000 {
        // pseudo-random values below m
        x = x
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        let (a, b) = (x % m, x.rotate_left(17) % m);
        let expected = (a as u128 * b as u128 % m as u128) as u64;
        assert_eq!(mul_mod(a, b, m), expected);
    }
}
```

- It needs `m < 2⁶³`, so that `a + a` cannot overflow a `u64`.
- It costs `O(log b)` additions.
- In Rust there is a shortcut: `(a as u128 * b as u128 % m as u128) as u64`. The doubling method matters in languages without a wider type.
