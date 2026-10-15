How do you answer **select1(k)**, the position of the 1 number `k` (counting from 0) in a large bit array, without scanning from the start?

---

Store the position of every 256th 1, jump there, then skip whole 64-bit words using `count_ones`.

1. When building, store `samples[j]` = the position of the 1 number `j · 256`.
2. To answer `select1(k)`, start at `samples[k / 256]`. There are still `k % 256` 1s to pass.
3. Skip whole words: while a word holds no more 1s than are left to pass, subtract its `count_ones` and move to the next word.
4. The answer is inside the current word. Find it there with a *select in a word*: clear the lowest 1 the right number of times, then take `trailing_zeros`.

Example: a bit array in which every 4th bit is 1, so the 1 number `k` is at `4k` and each word holds 16 1s. For `select1(600)`:

- `600 / 256 = 2`, so start at `samples[2] = 2048`, the position of the 1 number 512. There are `600 % 256 = 88` 1s left to pass.
- 2048 is the first bit of word 32. Words 32 to 36 hold 16 1s each, so skip all five: `88 - 5 · 16 = 8` left.
- Word 37 covers bits 2368 to 2431, and its 1 number 8 is at bit 32 of the word.
- `select1(600) = 37 · 64 + 32 = 2400`. Check: `4 · 600 = 2400`.

`count_ones` (`popcnt` on x86) and `trailing_zeros` (`tzcnt`) are single CPU instructions, so each skipped word costs very little.

The scan stays short when the 1s are spread fairly evenly. A long run of 0s between two samples makes it slower. To keep the worst case short, some libraries store every position in such sparse stretches.

The Rust search engine library rise-rs uses this scheme, a stored position every 256 1s, on the bit arrays of its compressed lists.

```rust
// store the position of every 256th 1
const SAMPLE: usize = 256;

struct SelectBits {
    words: Vec<u64>,
    // samples[j] = position of the 1 number j * SAMPLE
    samples: Vec<usize>,
}

/// Position of the 1 number k (from 0) inside one word.
fn select_in_word(mut word: u64, k: u32) -> u32 {
    for _ in 0..k {
        // clear the lowest 1
        word &= word - 1;
    }
    word.trailing_zeros()
}

impl SelectBits {
    fn new(bits: &[bool]) -> Self {
        let mut words = vec![0u64; bits.len().div_ceil(64)];
        let mut samples = Vec::new();
        let mut ones = 0;
        for (i, &b) in bits.iter().enumerate() {
            if b {
                words[i / 64] |= 1 << (i % 64);
                if ones % SAMPLE == 0 {
                    samples.push(i);
                }
                ones += 1;
            }
        }
        SelectBits { words, samples }
    }

    /// Position of the 1 number k (counting from 0).
    fn select1(&self, k: usize) -> usize {
        // 1. jump to the nearest stored 1 at or before k
        let start = self.samples[k / SAMPLE];
        // 1s still to pass after that one
        let mut left = (k % SAMPLE) as u32;
        // 2. skip whole words, ignoring the bits before the sample
        let mut w = start / 64;
        let mut word = self.words[w] & (!0u64 << (start % 64));
        loop {
            let ones = word.count_ones();
            if left < ones {
                // 3. the answer is inside this word
                return w * 64 + select_in_word(word, left) as usize;
            }
            left -= ones;
            w += 1;
            word = self.words[w];
        }
    }
}

fn main() {
    // every 4th bit is 1: start at samples[2] = 2048, skip
    // words 32 to 36, and find the 1 number 8 at bit 32 of word 37
    let every4: Vec<bool> = (0..4096).map(|i| i % 4 == 0).collect();
    let s = SelectBits::new(&every4);
    assert_eq!(s.samples[2], 2048);
    assert_eq!(s.select1(600), 37 * 64 + 32);

    // pseudo-random bits, about 1 in 8 is 1
    let mut x: u64 = 7;
    let bits: Vec<bool> = (0..20_000)
        .map(|_| {
            x = x
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1_442_695_040_888_963_407);
            (x >> 61) == 0
        })
        .collect();

    // compare with the list of every 1's position
    let s = SelectBits::new(&bits);
    let positions: Vec<usize> =
        (0..bits.len()).filter(|&i| bits[i]).collect();
    for (k, &p) in positions.iter().enumerate() {
        assert_eq!(s.select1(k), p, "k = {k}");
    }
}
```
