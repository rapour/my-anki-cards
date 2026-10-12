How can you shrink the exponent first when it is itself enormous, for example `a^(b^c) mod p`?

---

**Fermat's little theorem:** if `p` is prime and does not divide `a`, then `a^(p−1) ≡ 1 (mod p)`. So the exponent only matters modulo `p − 1`:

`a^e ≡ a^(e mod (p−1)) (mod p)`

For `a^(b^c)`: first compute `e = b^c mod (p−1)` with binary exponentiation, then compute `a^e mod p`.

```rust
fn mod_pow(mut base: u64, mut exp: u64, m: u64) -> u64 {
    let mut result = 1 % m;
    base %= m;
    while exp > 0 {
        if exp & 1 == 1 {
            result = result * base % m;
        }
        base = base * base % m;
        exp >>= 1;
    }
    result
}

/// a^(b^c) mod p, for a prime p that does not divide a.
fn tower(a: u64, b: u64, c: u64, p: u64) -> u64 {
    // Fermat: a^(p-1) = 1, so the exponent only matters mod p - 1
    let exponent = mod_pow(b, c, p - 1);
    mod_pow(a, exponent, p)
}

fn main() {
    // small enough to check without the trick: 2^(3^5) = 2^243
    assert_eq!(tower(2, 3, 5, 13), mod_pow(2, 243, 13));
    assert_eq!(
        tower(5, 7, 9, 1_000_000_007),
        mod_pow(5, 7u64.pow(9), 1_000_000_007)
    );
    assert_eq!(tower(5, 7, 9, 1_000_000_007), 140_242_535);

    // a huge exponent can be shrunk first
    let p = 1_000_000_007;
    let big = 1_000_000_000_000_000_000;
    assert_eq!(mod_pow(3, big, p), mod_pow(3, big % (p - 1), p));
}
```

- For a composite modulus `m` with `gcd(a, m) = 1`, replace `p − 1` by **Euler's totient** `φ(m)`.
- The condition on `a` matters. If `p` divides `a`, the result is `0`, not `a^0 = 1`.
