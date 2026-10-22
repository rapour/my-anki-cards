To answer rank (how many times `c` appears among the first `i` elements) on a sequence of `n` symbols from an alphabet of `σ` symbols, why use a wavelet tree rather than a plain array, or one bit array per symbol?

---

The wavelet tree is the middle ground. It is **as small as the plain array** and answers rank in **`O(log σ)` steps** instead of a scan.

*Recap.* A wavelet tree is a binary tree over the alphabet. Each node stores one bit per element that reaches it (`0` = lower half of its range, `1` = upper half), and rank, access and select each walk one path from the root to a leaf.

| Layout | Bits | access(i) | rank(c, i) |
|---|---|---|---|
| plain array, `⌈log2 σ⌉` bits per symbol | `n ⌈log2 σ⌉` | `O(1)` | `O(n)`: scan |
| one bit array per symbol, each with a rank index | `σ n` | `O(σ)`: check every array | `O(1)` |
| wavelet tree, each node with a rank index | `n ⌈log2 σ⌉` plus a little | `O(log σ)` | `O(log σ)` |

Example: a text of `n = 10^9` bytes, so `σ = 256`.

- One bit array per symbol: `256 · 10^9` bits, which is **32 GB**.
- Wavelet tree: `8 · 10^9` bits, which is **1 GB**, the size of the text itself. Each rank costs 8 bit-array ranks, one per level.

Why the size is `n ⌈log2 σ⌉`: the tree has `⌈log2 σ⌉` levels, and each element leaves one bit on every level.

Two common refinements:

- **Huffman shape.** Frequent symbols get short paths, as in a Huffman code. The size drops to about `n (H0 + 1)` bits, where `H0 = Σ (n_c / n) log2(n / n_c)` is the entropy of the symbol counts `n_c`: the fewest bits per symbol any code that looks at one symbol at a time can use.
- **Wavelet matrix.** Libraries often use this variant for large alphabets. It keeps one bit array per level and no tree pointers, and answers the same queries.

```rust
/// A wavelet tree over the values lo..=hi.
struct WaveletTree {
    lo: u32,
    hi: u32,
    // one bit per element: 1 if it is in the upper half
    bits: Vec<bool>,
    // ones[i] = number of 1s in bits[..i], so rank is a lookup
    ones: Vec<usize>,
    // the lower and the upper child; None at a leaf
    kids: Option<Box<[WaveletTree; 2]>>,
}

impl WaveletTree {
    fn new(seq: &[u32], lo: u32, hi: u32) -> Self {
        let mid = (lo + hi) / 2;
        let mut bits = Vec::new();
        // split in order: each half keeps the original order
        let (mut low, mut high) = (Vec::new(), Vec::new());
        for &v in seq {
            let up = lo < hi && v > mid;
            bits.push(up);
            if up {
                high.push(v);
            } else {
                low.push(v);
            }
        }
        let mut ones = vec![0];
        for &b in &bits {
            ones.push(ones[ones.len() - 1] + b as usize);
        }
        let kids = (lo < hi).then(|| {
            let left = Self::new(&low, lo, mid);
            let right = Self::new(&high, mid + 1, hi);
            Box::new([left, right])
        });
        WaveletTree { lo, hi, bits, ones, kids }
    }

    /// Number of bits equal to b in bits[..i].
    fn rank_bit(&self, b: bool, i: usize) -> usize {
        if b {
            self.ones[i]
        } else {
            i - self.ones[i]
        }
    }
}

impl WaveletTree {
    /// How many times c appears in seq[..i].
    fn rank(&self, c: u32, mut i: usize) -> usize {
        let mut node = self;
        while let Some(kids) = &node.kids {
            let b = c > (node.lo + node.hi) / 2;
            i = node.rank_bit(b, i);
            node = &kids[b as usize];
        }
        i
    }
}

/// Bits stored on each level (leaves store none).
fn level_bits(node: &WaveletTree, d: usize, out: &mut Vec<usize>) {
    let Some(kids) = &node.kids else { return };
    if out.len() == d {
        out.push(0);
    }
    out[d] += node.bits.len();
    for kid in kids.iter() {
        level_bits(kid, d + 1, out);
    }
}

fn main() {
    // 1000 pseudo-random bytes: sigma = 256, so 8 levels
    let mut x: u64 = 11;
    let bytes: Vec<u32> = (0..1000)
        .map(|_| {
            x = x
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1_442_695_040_888_963_407);
            (x >> 56) as u32
        })
        .collect();
    let tree = WaveletTree::new(&bytes, 0, 255);

    // 8 levels of exactly n bits: n * ceil(log2 256) in total
    let mut sizes = Vec::new();
    level_bits(&tree, 0, &mut sizes);
    assert_eq!(sizes, vec![1000; 8]);

    // rank matches a scan for a few values and prefixes
    for c in [0, 7, 128, 255] {
        for i in [0, 1, 500, 1000] {
            let want = bytes[..i].iter().filter(|&&v| v == c).count();
            assert_eq!(tree.rank(c, i), want);
        }
    }

    // a 10^9-byte text; a gigabyte is 8 * 10^9 bits
    let n: u64 = 1_000_000_000;
    let gb = |bits: u64| bits / 8_000_000_000;
    // one bit array per symbol, then the wavelet tree
    assert_eq!(gb(256 * n), 32);
    assert_eq!(gb(8 * n), 1);
}
```
