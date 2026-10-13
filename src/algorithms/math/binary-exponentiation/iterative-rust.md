Write the iterative version of binary exponentiation in Rust, and trace `3¹³` through it.

---

Each step looks at the lowest bit of the exponent. If it is `1`, multiply the result by the current power of the base. Then shift to the next bit and square the base, so it becomes the next power (`a`, `a²`, `a⁴`, `a⁸`, ...).

```rust
fn power(mut base: u64, mut exp: u64) -> u64 {
    let mut result = 1;
    while exp > 0 {
        if exp & 1 == 1 {
            // this bit is set: use this power of the base
            result *= base;
        }
        exp >>= 1; // move on to the next bit
        if exp > 0 {
            // base becomes a^2, a^4, a^8, ... for the next bits
            base *= base;
        }
    }
    result
}

fn main() {
    assert_eq!(power(3, 13), 1_594_323);
    assert_eq!(power(2, 10), 1024);
    assert_eq!(power(7, 0), 1);
    // fits in a u64
    assert_eq!(power(3, 40), 12_157_665_459_056_928_801);
}
```

Trace for `3¹³` (13 is `1101` in binary):

| exponent left | lowest bit | base now | result after |
|---|---|---|---|
| `1101` | 1 | 3 | 3 |
| `110` | 0 | 9 | 3 |
| `11` | 1 | 81 | 243 |
| `1` | 1 | 6561 | 1,594,323 |

- `result` starts at `1`, the "do nothing" value for multiplication.
- This loop is usually faster than the recursive one: no function calls.
- The base is only squared while bits remain. Squaring it after the last bit is wasted work and can overflow a `u64` even though the answer fits (for `3⁴⁰` the unused last square would be `3⁶⁴`).
