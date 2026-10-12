Codeforces 126B *Password*: find the longest string that is a prefix of `s`, a suffix of `s`, **and** also appears strictly inside `s`. How does hashing solve it?

---

1. **Prefix equals suffix.** For each length `l`, compare `hash(0, l)` with `hash(n − l, n)`. The lengths that match are the candidates, in increasing order.
2. **Appears inside.** For a candidate length `l`, check every start `i` from `1` while `i + l < n`, comparing `hash(i, i + l)` with the prefix hash. That is `O(n)` per length.
3. **Binary search.** If the prefix of length `l` appears inside, so does every shorter prefix (same start, fewer letters). So the answers along the candidate list are "yes, yes, ..., no, no". `partition_point` finds the last "yes".

The cost is `O(n log n)` instead of `O(n²)`.

```rust
const P: u64 = 31;
const M: u64 = 1_000_000_007;

struct RollingHash {
    prefix: Vec<u64>,
    power: Vec<u64>,
}

impl RollingHash {
    fn new(s: &str) -> Self {
        let mut prefix = vec![0];
        let mut power = vec![1];
        for byte in s.bytes() {
            prefix.push(
                (prefix.last().unwrap() * P + (byte - b'a' + 1) as u64)
                    % M,
            );
            power.push(power.last().unwrap() * P % M);
        }
        Self { prefix, power }
    }

    fn get(&self, l: usize, r: usize) -> u64 {
        (self.prefix[r] + M - self.prefix[l] * self.power[r - l] % M)
            % M
    }
}

/// The longest string that is a prefix of `s`, a suffix of `s`,
/// and also
/// appears strictly inside.
fn password(s: &str) -> Option<&str> {
    let n = s.len();
    let hashed = RollingHash::new(s);

    // lengths where the prefix equals the suffix, in increasing
    // order
    let borders: Vec<usize> = (1..n)
        .filter(|&l| hashed.get(0, l) == hashed.get(n - l, n))
        .collect();

    // does the prefix of length l also start somewhere strictly
    // inside,
    // at i with 1 <= i and i + l < n?
    let occurs_inside = |l: usize| {
        (1..n - l).any(|i| hashed.get(i, i + l) == hashed.get(0, l))
    };

    // if length l occurs inside, every shorter prefix does too,
    // so the
    // answers go "yes ... yes, no ... no"
    let yes = borders.partition_point(|&l| occurs_inside(l));
    if yes == 0 {
        None
    } else {
        Some(&s[..borders[yes - 1]])
    }
}

fn password_slowly(s: &str) -> Option<&str> {
    (1..s.len())
        .rev()
        .map(|l| &s[..l])
        .find(|t| s.ends_with(t) && s[1..s.len() - 1].contains(t))
}

fn main() {
    assert_eq!(password("fixprefixsuffix"), Some("fix"));
    // "abc" is a prefix and a suffix but not inside
    assert_eq!(password("abcdabc"), None);

    // compare with the slow method on pseudo-random strings
    let mut x: u64 = 11;
    let mut next = || {
        x = x
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        (x >> 33) as usize
    };
    for _ in 0..1000 {
        let s: String = (0..1 + next() % 20)
            .map(|_| (b'a' + (next() % 2) as u8) as char)
            .collect();
        assert_eq!(password(&s), password_slowly(&s), "{s}");
    }
}
```

Samples: `fixprefixsuffix` gives `fix`. For `abcdabc` there is no answer, because `abc` is a prefix and a suffix but not inside. The program also compares with a slow search on 1,000 random strings.
