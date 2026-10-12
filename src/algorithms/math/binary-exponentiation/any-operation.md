What does an operation need so that binary exponentiation works with it, and what plays the role of "1"?

---

Two things:

1. It must be **associative**: `(x · y) · z = x · (y · z)`. That is what lets you regroup `a · a · a · a · a` into squares.
2. It needs an **identity element**, a value that changes nothing, to start the result with.

It does **not** need to be commutative (`x · y = y · x`). Powers of the same `x` always commute with each other.

| Operation | Identity |
|---|---|
| numbers with `×` | 1 |
| numbers with `+` | 0 |
| matrices with `×` | the identity matrix |
| joining text | the empty string |
| combining permutations | the permutation that moves nothing |

```rust
fn power<T: Clone>(
    mut base: T,
    mut exp: u64,
    identity: T,
    multiply: impl Fn(&T, &T) -> T,
) -> T {
    let mut result = identity;
    while exp > 0 {
        if exp & 1 == 1 {
            result = multiply(&result, &base);
        }
        exp >>= 1;
        if exp > 0 {
            base = multiply(&base, &base);
        }
    }
    result
}

fn main() {
    // numbers with *: the ordinary power
    assert_eq!(power(3u64, 13, 1, |a, b| a * b), 1_594_323);

    // numbers with +: "add 3 to itself 13 times" is 3 * 13, found
    // by
    // doubling
    assert_eq!(power(3u64, 13, 0, |a, b| a + b), 39);

    // text with joining: repeat a word
    let joined = power("ab".to_string(), 3, String::new(), |a, b| {
        format!("{a}{b}")
    });
    assert_eq!(joined, "ababab");
}
```

This is why the same few lines solve so many problems: Fibonacci, walks in graphs, repeated shuffles and so on.
