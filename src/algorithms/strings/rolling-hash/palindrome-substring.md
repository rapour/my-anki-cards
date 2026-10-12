How do you test whether `s[l..r)` is a palindrome in `O(1)` with hashing? (Used in Codeforces 835D *Palindromic Characteristics*.)

---

A palindrome reads the same backwards, so compare the hash of the substring with the hash of the same part read **backwards**. Build prefix hashes for the string and for its reverse.

Letter `i` of `s` is letter `n − 1 − i` of the reversed string, so `s[l..r)` read backwards is the part `[n − r, n − l)` of the reversed string. The substring is a palindrome when the two hashes are equal.

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

struct Palindromes {
    n: usize,
    forward: RollingHash,
    backward: RollingHash, // hashes of the reversed string
}

impl Palindromes {
    fn new(s: &str) -> Self {
        let reversed: String = s.chars().rev().collect();
        Self {
            n: s.len(),
            forward: RollingHash::new(s),
            backward: RollingHash::new(&reversed),
        }
    }

    /// Is s[l..r) a palindrome? Position i of s is position n - 1
    /// - i of
    /// the reversed string,
    /// so s[l..r) read backwards is the reversed string's part [n
    /// - r, n
    /// - l).
    fn is_palindrome(&self, l: usize, r: usize) -> bool {
        self.forward.get(l, r)
            == self.backward.get(self.n - r, self.n - l)
    }
}

fn main() {
    let s = "abacabaxyx";
    let pal = Palindromes::new(s);
    assert!(pal.is_palindrome(0, 7)); // "abacaba"
    assert!(pal.is_palindrome(7, 10)); // "xyx"
    assert!(!pal.is_palindrome(0, 4)); // "abac"
    // one letter is always a palindrome
    assert!(pal.is_palindrome(3, 4));
    // so is the empty string
    assert!(pal.is_palindrome(5, 5));

    for l in 0..=s.len() {
        for r in l..=s.len() {
            let part: Vec<char> = s[l..r].chars().collect();
            let slow = part.iter().eq(part.iter().rev());
            assert_eq!(pal.is_palindrome(l, r), slow);
        }
    }
}
```

Codeforces 835D asks, for every `k`, how many substrings are *k-palindromes*. A string is a 1-palindrome if it reads the same both ways, and a k-palindrome if its left and right halves are equal and both are (k−1)-palindromes. Constant-time palindrome and equality tests make each substring cheap to classify.
