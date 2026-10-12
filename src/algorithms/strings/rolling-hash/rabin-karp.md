How does Rabin–Karp find every occurrence of a pattern in a text? (SPOJ NHAY, *A Needle in the Haystack*)

---

Hash the pattern once. Then slide a window of the same length over the text, updating its hash in `O(1)` per step. Every position where the window hash equals the pattern hash is a match.

The cost is `O(n + k)` for a text of `n` letters and a pattern of `k` letters, instead of `O(n · k)` for comparing at every position.

```rust
const P: u64 = 31;
const M: u64 = 1_000_000_007;

fn value(byte: u8) -> u64 {
    (byte - b'a' + 1) as u64
}

/// Every position where `pattern` occurs in `text`.
fn find_all(text: &str, pattern: &str) -> Vec<usize> {
    let (text, pattern) = (text.as_bytes(), pattern.as_bytes());
    let (n, k) = (text.len(), pattern.len());
    if k == 0 || k > n {
        return Vec::new();
    }
    let top = (1..k).fold(1, |acc, _| acc * P % M); // P^(k-1)

    let mut target = 0;
    let mut window = 0;
    for i in 0..k {
        target = (target * P + value(pattern[i])) % M;
        window = (window * P + value(text[i])) % M;
    }

    let mut found = Vec::new();
    for start in 0..=n - k {
        if window == target {
            found.push(start);
        }
        if start + k < n {
            // drop the oldest letter
            window = (window + M - value(text[start]) * top % M) % M;
            // take in the next one
            window = (window * P + value(text[start + k])) % M;
        }
    }
    found
}

fn find_all_slowly(text: &str, pattern: &str) -> Vec<usize> {
    (0..=text.len() - pattern.len())
        .filter(|&i| &text[i..i + pattern.len()] == pattern)
        .collect()
}

fn main() {
    assert_eq!(find_all("abracadabra", "abra"), vec![0, 7]);
    // matches may overlap
    assert_eq!(find_all("aaaaa", "aaa"), vec![0, 1, 2]);
    assert_eq!(find_all("abc", "d"), Vec::<usize>::new());
    // pattern longer than the text
    assert_eq!(find_all("ab", "abc"), Vec::<usize>::new());

    // compare with the slow method on pseudo-random texts over a
    // small
    // alphabet
    let mut x: u64 = 42;
    let mut next = || {
        x = x
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        (x >> 33) as usize
    };
    for _ in 0..300 {
        let text: String = (0..40)
            .map(|_| (b'a' + (next() % 2) as u8) as char)
            .collect();
        let pattern: String = (0..1 + next() % 5)
            .map(|_| (b'a' + (next() % 2) as u8) as char)
            .collect();
        assert_eq!(
            find_all(&text, &pattern),
            find_all_slowly(&text, &pattern)
        );
    }
}
```

- Matches may overlap: `"aaa"` occurs three times in `"aaaaa"`.
- A hash match could be a collision. If you must be certain, compare the letters when the hashes agree. That costs `O(k)` per match.
- The program is compared with the slow method on 300 random cases.
