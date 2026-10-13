How do you precompute prefix hashes and powers of `p` in Rust, and how do you use them to compare substrings?

---

Keep two arrays:

- `prefix[i]` = the hash of the first `i` letters, so `prefix[0] = 0` and `prefix[i+1] = prefix[i] · p + s[i]`.
- `power[i]` = `p^i mod m`.

Both take `O(n)` to build. The method `get(l, r)` then returns the hash of `s[l..r)` in `O(1)` (the formula is `get(l, r) = prefix[r] − prefix[l] · power[r − l]`, modulo `m`).

To test whether two substrings are equal, compare their hashes: `"abra"` at positions 0 and 7 of `"abracadabra"`.

```rust
const P: u64 = 31;
const M: u64 = 1_000_000_007;

struct RollingHash {
    // prefix[i] = hash of the first i letters
    prefix: Vec<u64>,
    power: Vec<u64>,  // power[i] = P^i mod M
}

impl RollingHash {
    fn new(s: &str) -> Self {
        let mut prefix = vec![0];
        let mut power = vec![1];
        for byte in s.bytes() {
            let value = (byte - b'a' + 1) as u64;
            prefix.push((prefix.last().unwrap() * P + value) % M);
            power.push(power.last().unwrap() * P % M);
        }
        Self { prefix, power }
    }

    /// Hash of s[l..r), found without any division.
    fn get(&self, l: usize, r: usize) -> u64 {
        (self.prefix[r] + M - self.prefix[l] * self.power[r - l] % M)
            % M
    }
}

fn hash(s: &str) -> u64 {
    s.bytes().fold(0, |h, byte| (h * P + (byte - b'a' + 1) as u64) % M)
}

fn main() {
    let s = "abracadabra";
    let hashed = RollingHash::new(s);

    // every substring: the O(1) answer equals hashing that
    // substring from
    // scratch
    for l in 0..=s.len() {
        for r in l..=s.len() {
            assert_eq!(hashed.get(l, r), hash(&s[l..r]));
        }
    }
    // "abra" appears at positions 0 and 7
    assert_eq!(hashed.get(0, 4), hashed.get(7, 11));
    assert_ne!(hashed.get(0, 4), hashed.get(1, 5));
}
```

The test compares `get(l, r)` with hashing the substring from scratch for every `l` and `r`.
