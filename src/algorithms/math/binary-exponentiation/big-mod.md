UVa 374 *Big Mod* asks for `B^P mod M` with a huge `P`. How do you compute it in Rust?

---

Use binary exponentiation and take the remainder after **every** multiplication, so no number ever gets bigger than `M`.

```rust
fn mod_pow(base: u64, mut exp: u64, modulus: u64) -> u64 {
    // u128: the product of two values below m cannot overflow
    let m = modulus as u128;
    // 1 % m, so that modulus 1 gives 0
    let mut result = 1 % m;
    let mut base = base as u128 % m;
    while exp > 0 {
        if exp & 1 == 1 {
            result = result * base % m;
        }
        base = base * base % m;
        exp >>= 1;
    }
    result as u64
}

fn main() {
    assert_eq!(mod_pow(3, 18132, 17), 13);
    assert_eq!(mod_pow(2, 10, 1000), 24);
    // everything is 0 modulo 1
    assert_eq!(mod_pow(5, 0, 1), 0);
    assert_eq!(
        mod_pow(3, 1_000_000_000_000_000_000, 1_000_000_007),
        246_336_683
    );

    // compare with slow repeated multiplication
    for base in 0..20u64 {
        for exp in 0..20u64 {
            let slow = (0..exp).fold(1u64, |acc, _| acc * base % 97);
            assert_eq!(mod_pow(base, exp, 97), slow);
        }
    }
}
```

- The values are widened to `u128`, because the product of two numbers just below `M` can be as large as `M²`.
- `1 % m` makes the answer `0` when `m = 1`.
- UVa 1230 *MODEX* asks the same thing (`x^y mod n`, for many test cases), so the same function solves it.
- The cost is `O(log P)` multiplications, however large `P` is.
