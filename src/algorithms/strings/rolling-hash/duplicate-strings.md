How can you group identical strings from a list using their hashes?

---

Hash every string, collect the indices that share a hash, and each group is a set of identical strings (up to collisions). It costs one pass over all the letters, instead of comparing pairs of strings.

```rust
use std::collections::HashMap;

const P: u64 = 31;
const M: u64 = 1_000_000_007;

fn hash(s: &str) -> u64 {
    s.bytes().fold(0, |h, byte| (h * P + (byte - b'a' + 1) as u64) % M)
}

/// Groups of positions that hold identical strings.
fn group_identical(strings: &[&str]) -> Vec<Vec<usize>> {
    let mut groups: HashMap<u64, Vec<usize>> = HashMap::new();
    for (i, s) in strings.iter().enumerate() {
        groups.entry(hash(s)).or_default().push(i);
    }
    let mut result: Vec<Vec<usize>> = groups.into_values().collect();
    result.sort();
    result
}

fn main() {
    let strings = ["abc", "abd", "abc", "x", "abd"];
    assert_eq!(
        group_identical(&strings),
        vec![vec![0, 2], vec![1, 4], vec![3]]
    );
}
```

**In Rust you rarely need to do this by hand:** `HashMap<&str, Vec<usize>>` already hashes the whole string. The polynomial hash pays off when you need the hash of **substrings** or windows, for example when comparing substrings or sliding a window over a text.
