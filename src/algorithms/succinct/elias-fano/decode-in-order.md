Elias-Fano stores each number `x` of a sorted list as a low part (its lowest `l` bits, kept in an array) and a high part. The high parts are kept as a bit array in which number `i` (counting from 0) sets the bit at position `(x >> l) + i`. How do you decode the whole list in order quickly, 64 bits at a time?

---

Walk the 1s of the high bits one 64-bit word at a time with two bit tricks. When the `1` of number `i` is at position `p`, the high part is `p - i`.

- `word.trailing_zeros()` gives the position of the lowest `1` in the word. It is one CPU instruction, for example `tzcnt` on x86.
- `word &= word - 1` clears that lowest `1`, so the next call finds the following one. Subtracting 1 turns the lowest `1` into `0` and the `0`s below it into `1`s, so the AND keeps only the bits above it: `1011_0100 - 1 = 1011_0011`, and `1011_0100 & 1011_0011 = 1011_0000`.
- When the word becomes 0, load the next word.

Example: 3, 4, 7, 13, 14, 15, 21, 43 with `l = 2`. Their high bits fit in one word, `0x209CD`, with 1s at positions 0, 2, 3, 6, 7, 8, 11 and 17.

| i | `1` at | high = position - i | low | number |
|---|---|---|---|---|
| 0 | 0 | 0 | 3 | 3 |
| 1 | 2 | 1 | 0 | 4 |
| 2 | 3 | 1 | 3 | 7 |
| 3 | 6 | 3 | 1 | 13 |
| 4 | 7 | 3 | 2 | 14 |
| 5 | 8 | 3 | 3 | 15 |
| 6 | 11 | 5 | 1 | 21 |
| 7 | 17 | 10 | 3 | 43 |

After number 0, `word &= word - 1` turns the low bits `1100_1101` into `1100_1100`, so the next `trailing_zeros` returns 2.

Each number costs a few instructions and needs no select (no search for the k-th 1). The Rust search engine library rise-rs reads its lists this way, in `UnaryEnumerator::next_one`.

```rust
/// Walks the 1s of a bit array from left to right.
struct OnesWalker<'a> {
    words: &'a [u64],
    word_index: usize,
    // the current word, with the 1s already visited cleared
    buf: u64,
}

impl<'a> OnesWalker<'a> {
    fn new(words: &'a [u64]) -> Self {
        OnesWalker { words, word_index: 0, buf: words[0] }
    }

    /// Position of the next 1.
    fn next_one(&mut self) -> usize {
        // no 1s left in this word: load the next one
        while self.buf == 0 {
            self.word_index += 1;
            self.buf = self.words[self.word_index];
        }
        // the lowest 1
        let pos_in_word = self.buf.trailing_zeros() as usize;
        // clear it so the next call finds the following 1
        self.buf &= self.buf - 1;
        self.word_index * 64 + pos_in_word
    }
}

/// Decode a whole Elias-Fano list in order.
fn decode(high_words: &[u64], low: &[u64], l: u32) -> Vec<u64> {
    let mut walker = OnesWalker::new(high_words);
    (0..low.len())
        .map(|i| {
            // the i earlier 1s pushed this one right by i
            let high = (walker.next_one() - i) as u64;
            (high << l) | low[i]
        })
        .collect()
}

/// Build the high bits (as 64-bit words) and the low parts.
fn encode(values: &[u64], l: u32) -> (Vec<u64>, Vec<u64>) {
    let n = values.len() as u64;
    let u = values[values.len() - 1] + 1;
    let high_len = n + (u >> l) + 1;
    let mut high_words = vec![0u64; (high_len as usize).div_ceil(64)];
    let mut low = Vec::new();
    for (i, &x) in values.iter().enumerate() {
        low.push(x & ((1 << l) - 1));
        let pos = (x >> l) as usize + i;
        high_words[pos / 64] |= 1 << (pos % 64);
    }
    (high_words, low)
}

fn main() {
    let values = [3u64, 4, 7, 13, 14, 15, 21, 43];
    let (high_words, low) = encode(&values, 2);
    // 1s at 0, 2, 3, 6, 7, 8, 11 and 17
    assert_eq!(high_words, vec![0x209CD]);
    assert_eq!(decode(&high_words, &low, 2), values);

    // a longer list that spans many words
    let long: Vec<u64> = (0..5000u64).map(|i| i * 7 + i % 3).collect();
    let l = ((long[long.len() - 1] + 1) / 5000).ilog2();
    let (high_words, low) = encode(&long, l);
    assert_eq!(decode(&high_words, &low, l), long);
}
```
