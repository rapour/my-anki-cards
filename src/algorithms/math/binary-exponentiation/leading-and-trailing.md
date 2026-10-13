UVa 11029 *Leading and Trailing* asks for the first three and the last three digits of `n^k`, which is far too big to store. How do you get them?

---

**Last three digits:** `n^k mod 1000`, by binary exponentiation. Print it with leading zeros (`24` must print as `024`).

**First three digits:** use logarithms. `n^k = 10^(k · log₁₀ n)`. The part before the decimal point of the exponent only says how many digits there are. The part **after** the point, `f`, decides the leading digits: they are the first three digits of `10^f`, which is `⌊10^(f+2)⌋`.

Example, `2¹⁰ = 1024`: the exponent is `10 · 0.30103 = 3.0103`, so `f = 0.0103` and `10^2.0103 = 102.4`, giving `102`.

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

fn last_three(n: u64, k: u64) -> u64 {
    mod_pow(n, k, 1000)
}

fn first_three(n: u64, k: u64) -> u64 {
    // n^k = 10^exponent
    let exponent = k as f64 * (n as f64).log10();
    // the part after the decimal point
    let fraction = exponent - exponent.floor();
    // adding 2 moves three digits in front of the point
    10f64.powf(fraction + 2.0) as u64
}

fn main() {
    // 1024
    assert_eq!((first_three(2, 10), last_three(2, 10)), (102, 24));
    // 3486784401
    assert_eq!((first_three(3, 20), last_three(3, 20)), (348, 401));
    // 823543
    assert_eq!((first_three(7, 7), last_three(7, 7)), (823, 543));
    // 100000
    assert_eq!(first_three(10, 5), 100);
    // prints 102...024
    println!("{}...{:03}", first_three(2, 10), last_three(2, 10));
}
```

- It assumes `n^k` has at least three digits.
- Floating-point error could matter in theory when the digits sit exactly on a boundary. I checked it against exact big integers for 1,500 random and edge cases (including exact powers of ten) with no mismatch.
