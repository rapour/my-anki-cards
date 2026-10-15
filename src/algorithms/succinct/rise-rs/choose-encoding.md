rise-rs, a Rust library for search engine indexes, cuts each long sorted list of numbers into parts, and can store each part as Elias-Fano, as a bitmap, or as nothing at all. How does it choose for a part with `n` numbers that are all below `u`?

---

It works out the size in bits of each option from `u` and `n`, and takes the smallest.

1. **Nothing at all** when `n = u`: the part holds every number from 0 to `u - 1`. The reader already knows `u` and `n`, so 0 bits are needed.
2. **Bitmap** (rise-rs calls it `RankedBv`): one bit per possible number, plus a count of 1s every 512 bits (for rank) and the position of every 256th 1 (for select). Size: `u + (u / 512) · ceil(log2(n + 1)) + (n / 256) · ceil(log2(u))`. It is chosen when it is smaller than Elias-Fano.
3. **Elias-Fano** otherwise. Each number is split into a low part of `l = floor(log2(u / n))` bits and a high part, written into a bit array of about `n + u / 2^l` bits, plus stored positions for jumping.

Rule of thumb: the bitmap wins when a part is **dense**, holding more than about one number in four from its range. A bitmap costs `u / n` bits per number and Elias-Fano about `2 + log2(u / n)`, and the two meet at `u / n = 4`.

How the parts are made: rise-rs either cuts fixed blocks of 128 numbers, or searches for the cut points that make the total size close to the smallest. Each part stores its numbers as offsets from where it starts, so `u` is the width of that part's range, not of the whole list. Dense stretches of a list can then be bitmaps while sparse stretches stay Elias-Fano.

```rust
fn msb(v: u64) -> u64 {
    v.checked_ilog2().unwrap_or(0) as u64
}

fn ceil_log2(v: u64) -> u64 {
    if v == 1 {
        0
    } else {
        msb(v - 1) + 1
    }
}

/// Elias-Fano size in bits, as rise-rs estimates it:
/// low parts + high bits + stored positions.
fn ef_bits(u: u64, n: u64) -> u64 {
    let l = if u > n { msb(u / n) } else { 0 };
    let high_len = n + (u >> l) + 2;
    let w = ceil_log2(high_len);
    n * l + high_len + ((high_len - n) >> 9) * w + (n >> 8) * w
}

/// Bitmap size in bits: one bit per number below u, plus
/// a count of 1s per 512 bits and the position of every 256th 1.
fn bitmap_bits(u: u64, n: u64) -> u64 {
    u + (u >> 9) * ceil_log2(n + 1) + (n >> 8) * ceil_log2(u)
}

#[derive(Debug, PartialEq)]
enum Encoding {
    // every number below u is present: nothing to store
    AllOnes,
    // rise-rs calls this RankedBv
    Bitmap,
    EliasFano,
}

fn choose(u: u64, n: u64) -> Encoding {
    if u == n {
        Encoding::AllOnes
    } else if bitmap_bits(u, n) < ef_bits(u, n) {
        Encoding::Bitmap
    } else {
        Encoding::EliasFano
    }
}

fn main() {
    // 0, 1, ..., 999
    assert_eq!(choose(1000, 1000), Encoding::AllOnes);
    // dense: 1040 bits against 1946
    assert_eq!(choose(1000, 900), Encoding::Bitmap);
    assert_eq!(bitmap_bits(1000, 900), 1040);
    assert_eq!(ef_bits(1000, 900), 1946);
    // sparse: about 12 bits per number
    assert_eq!(choose(1_000_000, 1000), Encoding::EliasFano);
    assert_eq!(ef_bits(1_000_000, 1000), 12_027);

    // the switch happens at about one number in four
    let u = 1_000_000;
    let first =
        (1..u).find(|&n| choose(u, n) == Encoding::Bitmap).unwrap();
    assert_eq!(first, 257_817);
    assert!((3.8..4.0).contains(&(u as f64 / first as f64)));
}
```
