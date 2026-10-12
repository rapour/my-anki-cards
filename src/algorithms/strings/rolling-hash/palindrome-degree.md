Codeforces 7D *Palindrome Degree*: how do you find the sum of the palindrome degrees of all prefixes of a string?

---

**Definition.** Every string, even the empty one, is a *0-palindrome*. A string is a *k-palindrome* if it is a palindrome and its prefix of length `⌊n/2⌋` is a *(k−1)-palindrome*. The **degree** is the largest `k` that works. `"abaaba"` has degree 3.

So for a prefix of length `len`: if it is not a palindrome its degree is `0`, otherwise it is `degree[len / 2] + 1`. Add up the degree of every prefix.

**Palindrome test for every prefix, in `O(1)` each:** keep two hashes while reading the string.

- `forward = forward · p + letter` (the new letter goes last, at `p⁰`).
- `backward = backward + letter · p^i` (the new letter goes **first**, at the highest power).

The prefix is a palindrome when they are equal. Here the letters can be digits and upper and lower case letters, so the code uses the byte value and a base above 127.

```rust
// P is bigger than any letter or digit code: the input can mix
// them
const P: u64 = 131;
const M: u64 = 1_000_000_007;

/// Sum of the palindrome degrees of all prefixes of `s`.
fn palindrome_degree_sum(s: &str) -> u64 {
    // hash of the prefix, the degree-0 term last
    let mut forward = 0;
    // hash of the same prefix read backwards
    let mut backward = 0;
    let mut power = 1; // P^i
    // degree[len] = degree of the prefix of that length
    let mut degree = vec![0u64; s.len() + 1];
    let mut total = 0;

    for (i, byte) in s.bytes().enumerate() {
        let value = byte as u64;
        // new letter goes last, at P^0
        forward = (forward * P + value) % M;
        // new letter goes first, at P^i
        backward = (backward + value * power) % M;
        power = power * P % M;

        let len = i + 1;
        if forward == backward {
            // a palindrome whose left half has one degree less
            degree[len] = degree[len / 2] + 1;
        }
        total += degree[len];
    }
    total
}

fn is_palindrome(s: &[u8]) -> bool {
    s.iter().eq(s.iter().rev())
}

fn palindrome_degree_sum_slowly(s: &str) -> u64 {
    let mut degree = vec![0u64; s.len() + 1];
    let mut total = 0;
    for len in 1..=s.len() {
        if is_palindrome(&s.as_bytes()[..len]) {
            degree[len] = degree[len / 2] + 1;
        }
        total += degree[len];
    }
    total
}

fn main() {
    assert_eq!(palindrome_degree_sum("a2A"), 1);
    assert_eq!(palindrome_degree_sum("abacaba"), 6);
    // "abaaba" has degree 3 itself; its prefixes a, ab, aba,
    // abaa, abaab
    // have 1, 0, 2, 0, 0
    assert_eq!(palindrome_degree_sum("abaaba"), 1 + 0 + 2 + 0 + 0 + 3);

    // compare with the slow method on pseudo-random strings
    let mut x: u64 = 5;
    let mut next = || {
        x = x
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        (x >> 33) as usize
    };
    for _ in 0..500 {
        let s: String = (0..30)
            .map(|_| (b'a' + (next() % 2) as u8) as char)
            .collect();
        assert_eq!(
            palindrome_degree_sum(&s),
            palindrome_degree_sum_slowly(&s)
        );
    }
}
```
