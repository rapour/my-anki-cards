Codeforces 271D *Good Substrings*: count the **distinct** substrings that have at most `k` bad letters. How does hashing help?

---

*Distinct* means different content, so two substrings with the same letters in different places count once. To recognise repeats quickly, store each substring's `(length, hash)` in a set. Putting the length in the key makes a false match even less likely.

For every start position, extend the end to the right while the number of bad letters is at most `k`. Once it goes above `k`, stop: going further right can only add more bad letters.

That is `O(n²)` hashes. It is fine when the string has up to a few thousand letters.

The input also gives which letters are good: a string of 26 characters, `1` for a good letter and `0` for a bad one.

```rust
use std::collections::HashSet;

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

/// Distinct substrings with at most `k` bad letters. `good[c]` is
/// b'1' if
/// letter c is good.
fn count_good_substrings(s: &str, good: &str, k: usize) -> usize {
    let bytes = s.as_bytes();
    let hashed = RollingHash::new(s);
    let mut seen = HashSet::new();

    for start in 0..bytes.len() {
        let mut bad = 0;
        for end in start..bytes.len() {
            if good.as_bytes()[(bytes[end] - b'a') as usize] == b'0' {
                bad += 1;
            }
            if bad > k {
                // going further right only adds more bad letters
                break;
            }
            // the length goes into the key too, which makes a
            // false match
            // even less likely
            seen.insert((end + 1 - start, hashed.get(start, end + 1)));
        }
    }
    seen.len()
}

fn count_good_substrings_slowly(
    s: &str,
    good: &str,
    k: usize,
) -> usize {
    let mut seen = HashSet::new();
    for start in 0..s.len() {
        for end in start + 1..=s.len() {
            let bad = s[start..end]
                .bytes()
                .filter(|&c| {
                    good.as_bytes()[(c - b'a') as usize] == b'0'
                })
                .count();
            if bad <= k {
                seen.insert(&s[start..end]);
            }
        }
    }
    seen.len()
}

fn main() {
    let only_b_is_good = "01000000000000000000000000";
    let nothing_is_good = "00000000000000000000000000";
    assert_eq!(count_good_substrings("ababab", only_b_is_good, 1), 5);
    assert_eq!(
        count_good_substrings("acbacbacaa", nothing_is_good, 2),
        8
    );

    // compare with the slow method on pseudo-random strings
    let mut x: u64 = 99;
    let mut next = || {
        x = x
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        (x >> 33) as usize
    };
    for _ in 0..200 {
        let s: String = (0..25)
            .map(|_| (b'a' + (next() % 3) as u8) as char)
            .collect();
        let good: String = (0..26)
            .map(|_| if next() % 2 == 0 { '1' } else { '0' })
            .collect();
        let k = next() % 4;
        assert_eq!(
            count_good_substrings(&s, &good, k),
            count_good_substrings_slowly(&s, &good, k)
        );
    }
}
```

With `k` at least the length of the string, this counts all distinct substrings of the string.
