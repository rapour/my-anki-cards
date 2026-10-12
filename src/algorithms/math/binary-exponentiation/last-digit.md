SPOJ LASTDIG asks for the last digit of `a^b` when `b` is huge. How do you solve it?

---

The last digit of a number is the number modulo 10, so you need `a^b mod 10`. Only the last digit of `a` matters, because `a mod 10` is all that enters the calculation. Then it is binary exponentiation with `m = 10`.

```rust
fn last_digit(a: u64, mut b: u64) -> u64 {
    let mut base = a % 10; // only the last digit of a matters
    let mut result = 1;
    while b > 0 {
        if b & 1 == 1 {
            result = result * base % 10;
        }
        base = base * base % 10;
        b >>= 1;
    }
    result
}

fn main() {
    assert_eq!(last_digit(2, 10), 4); // 1024
    assert_eq!(last_digit(7, 4), 1); // 2401
    assert_eq!(last_digit(0, 5), 0);
    // anything to the power 0 is 1
    assert_eq!(last_digit(5, 0), 1);
    assert_eq!(last_digit(123_456_789, 2_147_483_000), 1);
}
```

- If `a` is given as text, its last character is enough.
- `a^0 = 1`, even for `a = 0` in this convention.
- The last digits of the powers of a number repeat in a cycle of length 1, 2 or 4, so you could also reduce `b`. Binary exponentiation needs no special cases, so it is the safer choice.
