How likely is a hash collision, and how do two hashes help?

---

For a given pair of different strings the chance of a collision is about `1/m`. That looks tiny, but with many strings the **pairs** add up.

With `n` strings there are about `n²/2` pairs, so you expect about `n² / (2m)` collisions:

- `n = 10⁶` strings and `m ≈ 10⁹`: about **500** colliding pairs.

**Double hashing:** use two independent hashes with different `p` and `m`, and treat strings as equal only when **both** match. It behaves like a single hash with `m ≈ 10¹⁸`:

- `n = 10⁶` again: about `5 · 10⁻⁷` expected collisions, so a collision is very unlikely.

```rust
struct RollingHash {
    p: u64,
    m: u64,
    prefix: Vec<u64>,
    power: Vec<u64>,
}

impl RollingHash {
    fn new(s: &str, p: u64, m: u64) -> Self {
        let mut prefix = vec![0];
        let mut power = vec![1];
        for byte in s.bytes() {
            prefix.push(
                (prefix.last().unwrap() * p + (byte - b'a' + 1) as u64)
                    % m,
            );
            power.push(power.last().unwrap() * p % m);
        }
        Self { p, m, prefix, power }
    }

    fn get(&self, l: usize, r: usize) -> u64 {
        (self.prefix[r] + self.m
            - self.prefix[l] * self.power[r - l] % self.m)
            % self.m
    }
}

/// Two independent hashes: a false match needs both to collide at
/// once.
struct DoubleHash {
    first: RollingHash,
    second: RollingHash,
}

impl DoubleHash {
    fn new(s: &str) -> Self {
        Self {
            first: RollingHash::new(s, 31, 1_000_000_007),
            second: RollingHash::new(s, 37, 998_244_353),
        }
    }

    fn get(&self, l: usize, r: usize) -> (u64, u64) {
        (self.first.get(l, r), self.second.get(l, r))
    }
}

fn main() {
    let s = "abracadabra";
    let hashed = DoubleHash::new(s);
    // "abra" and "abra"
    assert_eq!(hashed.get(0, 4), hashed.get(7, 11));
    // "abra" and "brac"
    assert_ne!(hashed.get(0, 4), hashed.get(1, 5));
    assert_eq!(hashed.first.p, 31);

    // expected false matches among n strings with one hash of
    // size m:
    // about n * (n - 1) / 2 / m
    let (n, m) = (1_000_000f64, 1e9);
    // about 500
    println!("one hash: about {}", n * (n - 1.0) / 2.0 / m);
    // about 5e-7
    println!("two hashes: about {:e}", n * (n - 1.0) / 2.0 / (m * m));
}
```

Pick the bases at random when the program starts to defeat test data aimed at a fixed base.
