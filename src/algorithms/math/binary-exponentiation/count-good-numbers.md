LeetCode 1922 *Count Good Numbers*: a digit string is **good** if the digits at even positions are even and the digits at odd positions are prime. How many good strings of length `n` are there (`n` up to 10¹⁵), modulo 10⁹ + 7?

---

Positions are counted from 0, and every position is chosen independently:

- Even positions (0, 2, 4, ...) need an even digit: `0 2 4 6 8`, so **5** choices.
- Odd positions (1, 3, 5, ...) need a prime digit: `2 3 5 7`, so **4** choices.

For length `n` there are `⌈n/2⌉` even positions and `⌊n/2⌋` odd ones, so the answer is

`5^⌈n/2⌉ · 4^⌊n/2⌋ mod (10⁹ + 7)`

Example: `2582` is good (2 and 8 are even, 5 and 2 are prime). With `n = 4` there are `5 · 4 · 5 · 4 = 400` good strings.

```rust
const MOD: u64 = 1_000_000_007;

fn mod_pow(mut base: u64, mut exp: u64, m: u64) -> u64 {
    let mut result = 1;
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

fn count_good_numbers(n: u64) -> u64 {
    // positions 0, 2, 4, ...: 5 choices each
    let even_slots = n.div_ceil(2);
    // positions 1, 3, 5, ...: 4 choices each
    let odd_slots = n / 2;
    mod_pow(5, even_slots, MOD) * mod_pow(4, odd_slots, MOD) % MOD
}

fn main() {
    assert_eq!(count_good_numbers(1), 5);
    assert_eq!(count_good_numbers(4), 400);
    assert_eq!(count_good_numbers(50), 564_908_303);
    assert_eq!(count_good_numbers(1_000_000_000_000_000), 711_414_395);

    // brute force over every digit string of length 1 to 5
    for n in 1..=5u32 {
        let mut good = 0;
        for x in 0..10u64.pow(n) {
            let ok = (0..n).all(|i| {
                let digit = x / 10u64.pow(n - 1 - i) % 10;
                if i % 2 == 0 {
                    digit % 2 == 0
                } else {
                    [2, 3, 5, 7].contains(&digit)
                }
            });
            good += ok as u64;
        }
        assert_eq!(count_good_numbers(n as u64), good);
    }
}
```

`n` is far too big for a loop, but two modular powers take about 100 multiplications.
