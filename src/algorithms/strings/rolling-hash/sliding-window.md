How do you slide a hash window one letter to the right in `O(1)`?

---

For a window of `k` letters:

1. **Remove the oldest letter.** It sits at the highest power, so subtract `letter · p^(k−1)`.
2. **Shift.** Multiply by `p`, moving every remaining letter up one power.
3. **Add the new letter** at `p⁰`.

Example with `p = 31`, window `"ab"` becoming `"bc"` in `"abcd"`: the hash of `"ab"` is `1·31 + 2 = 33`. Remove `a`: `33 − 1·31 = 2`. Shift and add `c`: `2·31 + 3 = 65`, which is the hash of `"bc"`.

```rust
const P: u64 = 31;
const M: u64 = 1_000_000_007;

fn value(byte: u8) -> u64 {
    (byte - b'a' + 1) as u64
}

fn hash(s: &str) -> u64 {
    s.bytes().fold(0, |h, byte| (h * P + value(byte)) % M)
}

fn main() {
    // slide the window "ab" to "bc" in the text "abcd"
    // the window "ab" has hash 1 * 31 + 2 = 33
    let mut window = hash("ab");
    // P^(k-1) with k = 2 letters: the weight of the oldest letter
    let top = P;
    // 1. remove the oldest letter: 33 - 31 = 2
    window = (window + M - value(b'a') * top % M) % M;
    // 2. shift up one place and add the new letter: 2 * 31 + 3 =
    // 65
    window = (window * P + value(b'c')) % M;
    assert_eq!(window, 65);
    assert_eq!(window, hash("bc"));

    // slide a window of 3 over a longer text and compare each
    // step with a
    // fresh hash
    let text = "thequickbrownfox";
    let k = 3;
    let top = (1..k).fold(1, |acc, _| acc * P % M); // P^(k-1)
    let bytes = text.as_bytes();
    let mut window = hash(&text[..k]);
    for start in 0..text.len() - k {
        window = (window + M - value(bytes[start]) * top % M) % M;
        window = (window * P + value(bytes[start + k])) % M;
        assert_eq!(window, hash(&text[start + 1..start + 1 + k]));
    }
}
```
