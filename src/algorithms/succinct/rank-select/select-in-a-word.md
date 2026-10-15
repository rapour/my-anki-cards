How do you find the position of the 1 number `k` (counting from 0) inside one 64-bit word, without looping over its 64 bits?

---

Treat the word as 8 small numbers of one byte each and work on all 8 at once. This is the method the Rust search engine library rise-rs uses.

1. **Count the 1s in every byte** at once with three shift, mask and add steps (the standard bit-counting trick).
2. **Turn the counts into running totals**: multiplying by `0x0101_0101_0101_0101` adds each byte into all the bytes above it, so byte `j` becomes the number of 1s in bytes 0 to `j`. Totals are at most 64, so they fit in a byte and never spill into the next one.
3. **Find the byte that holds the answer**: put `k + 128` in every byte and subtract the totals. A byte keeps its top bit exactly when its total is at most `k`. Totals only grow from byte to byte, so the number of bytes that keep it is the index of the answer's byte. Nothing borrows across bytes, because `128 + k - total` stays above 0.
4. **Finish inside that one byte.** rise-rs looks the answer up in a table of 2048 entries (256 byte values × 8 possible `k`). The code below clears at most 7 lowest 1s instead.

Example: `word = 0x0F00_0103`, with 1s at positions 0, 1, 8, 24, 25, 26 and 27, and `k = 4`.

| byte | 0 | 1 | 2 | 3 | 4 to 7 |
|---|---|---|---|---|---|
| 1s in the byte | 2 | 1 | 0 | 4 | 0 |
| running total | 2 | 3 | 3 | 7 | 7 |
| total at most 4? | yes | yes | yes | no | no |

- Three bytes have a total of at most 4, so the answer is in byte 3, which starts at bit `3 · 8 = 24`.
- The bytes before it hold 3 1s, so inside byte 3 (`0000_1111`) the answer is its 1 number `4 - 3 = 1`, at bit 1.
- The answer is `24 + 1 = 25`. Check: the 1s in order are at 0, 1, 8, 24, 25, so the 1 number 4 is at 25.

On x86 CPUs with the BMI2 instructions there is a shorter way: `_pdep_u64(1 << k, word).trailing_zeros()`. `pdep` moves bit `k` of its first argument onto the position of the `k`-th 1 of `word`. It is slow on some older AMD CPUs, so portable code often uses the byte method.

```rust
/// Position of the 1 number k (from 0) in `word`.
/// Needs k < word.count_ones().
fn select_in_word(word: u64, k: u32) -> u32 {
    // 1 in every byte, and the top bit of every byte
    const ONES: u64 = 0x0101_0101_0101_0101;
    const HIGHS: u64 = 0x8080_8080_8080_8080;

    // 1. count the 1s in every byte at once
    let pairs = 0x3333_3333_3333_3333;
    let mut s = word - ((word >> 1) & 0x5555_5555_5555_5555);
    s = (s & pairs) + ((s >> 2) & pairs);
    s = (s + (s >> 4)) & 0x0F0F_0F0F_0F0F_0F0F;

    // 2. running totals: byte j of `sums` = 1s in bytes 0 to j
    let sums = s.wrapping_mul(ONES);

    // 3. count the bytes whose total is <= k: byte j of
    //    (k + 128) - sums keeps its top bit exactly then
    let at_most_k = (((k as u64) * ONES | HIGHS) - sums) & HIGHS;
    // first bit of the answer's byte
    let shift = at_most_k.count_ones() * 8;
    // 1s in the bytes before it
    let before = ((sums << 8) >> shift) & 0xFF;

    // 4. finish inside one byte
    let mut byte = (word >> shift) & 0xFF;
    for _ in 0..(k as u64 - before) {
        byte &= byte - 1;
    }
    shift + byte.trailing_zeros()
}

fn select_in_word_slowly(word: u64, k: u32) -> u32 {
    (0..64).filter(|&i| word >> i & 1 == 1).nth(k as usize).unwrap()
}

fn main() {
    // 0b1011_0000 has 1s at positions 4, 5 and 7
    assert_eq!(select_in_word(0b1011_0000, 0), 4);
    assert_eq!(select_in_word(0b1011_0000, 2), 7);
    assert_eq!(select_in_word(1 << 63, 0), 63);
    assert_eq!(select_in_word(u64::MAX, 40), 40);
    // bytes hold 2, 1, 0, 4 1s: totals 2, 3, 3, 7, so byte 3,
    // and its 1 number 4 - 3 = 1 is at bit 24 + 1
    assert_eq!(select_in_word(0x0F00_0103, 4), 25);

    // compare with a bit-by-bit search on pseudo-random words
    let mut x: u64 = 3;
    for _ in 0..20_000 {
        x = x
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        let word = x ^ (x >> 17);
        for k in 0..word.count_ones() {
            let want = select_in_word_slowly(word, k);
            assert_eq!(select_in_word(word, k), want);
        }
    }
}
```
