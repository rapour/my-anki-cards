The **FM-index**, the best-known use of wavelet trees: how do you count how often a pattern `P` occurs in a text, using only the text's Burrows-Wheeler transform, a small count table, and a wavelet tree?

---

Keep the block of sorted rotations that start with a suffix of `P`, and extend it **one character to the left at a time** (backward search). Each step needs two rank queries on the BWT, and the wavelet tree answers them. The final block's size is the count.

*Recap.*

- The **Burrows-Wheeler transform** of a text ending in `$` (smaller than every letter) is the last column `L` of its sorted rotations.
- `C[c]` is the number of characters in the text smaller than `c`.
- `rank(c, i)` is the number of `c`'s in `L` above row `i`.
- The rotations that start with any string `S` form one block of rows `[sp, ep)`, meaning rows `sp` to `ep - 1`, because the rows are sorted.

**The step.** Suppose `[sp, ep)` holds the rows that start with `S`. To put `c` in front:

`sp' = C[c] + rank(c, sp)` and `ep' = C[c] + rank(c, ep)`

The rows of the block whose `L` is `c` are exactly the places where `c` comes right before `S` in the text. The text's `k`-th `c` in `L` is also its `k`-th `c` in the first column (the LF property), so these rows map, in order, to the rows that start with `cS`. Those rows begin after the `C[c]` rows that start with a smaller character, and after the `rank(c, sp)` rows that start with `c` but sort before `cS`.

Example: count `abra` in `abracadabra$`, where `L = ard$rcaaaabb` and `C = {$: 0, a: 1, b: 6, c: 8, d: 9, r: 10}`.

| Rows start with | `c` | `C[c]` | `rank(c, sp)`, `rank(c, ep)` | New `[sp, ep)` |
|---|---|---|---|---|
| (anything) | | | | [0, 12) |
| `a` | a | 1 | 0, 5 | [1, 6) |
| `ra` | r | 10 | 0, 2 | [10, 12) |
| `bra` | b | 6 | 0, 2 | [6, 8) |
| `abra` | a | 1 | 1, 3 | [2, 4) |

For example, the last step: `sp = 1 + rank(a, 6) = 1 + 1 = 2` and `ep = 1 + rank(a, 8) = 1 + 3 = 4`.

The answer is `4 - 2 = 2`. Rows 2 and 3 are the rotations starting at text positions 7 and 0.

<div class="diagram">
<svg viewBox="0 0 640 302" width="100%" style="max-width:640px" role="img" aria-label="The sorted rotations of abracadabra$, with the row ranges that start with a, ra, bra and abra: rows 1 to 5, 10 to 11, 6 to 7, and 2 to 3.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .nt{fill:#007A66;font-size:11px}svg .cl{fill:rgba(250,100,25,.22);stroke:#FA6419;stroke-width:1}svg .pth{fill:none;stroke:#007A66;stroke-width:2;stroke-dasharray:5 3}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}svg .dim{opacity:.35}.nightMode svg .tg,.night_mode svg .tg,.nightMode svg .nt,.night_mode svg .nt{fill:#14C1A0}.nightMode svg .pth,.night_mode svg .pth{stroke:#14C1A0}</style>
<text x="20" y="26" text-anchor="middle" class="m">row</text>
<text x="113.0" y="26" text-anchor="middle" class="tg">F</text>
<text x="311.0" y="26" text-anchor="middle" class="to">L</text>
<text x="20" y="53" text-anchor="middle" class="m">0</text>
<rect x="105" y="41" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="54" text-anchor="middle" class="mono">$</text>
<text x="131.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="54" text-anchor="middle" class="mono">b</text>
<text x="167.0" y="54" text-anchor="middle" class="mono">r</text>
<text x="185.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="54" text-anchor="middle" class="mono">c</text>
<text x="221.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="54" text-anchor="middle" class="mono">d</text>
<text x="257.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="54" text-anchor="middle" class="mono">b</text>
<text x="293.0" y="54" text-anchor="middle" class="mono">r</text>
<rect x="303" y="41" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="20" y="72" text-anchor="middle" class="m">1</text>
<rect x="105" y="60" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="73" text-anchor="middle" class="mono">$</text>
<text x="149.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="73" text-anchor="middle" class="mono">b</text>
<text x="185.0" y="73" text-anchor="middle" class="mono">r</text>
<text x="203.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="73" text-anchor="middle" class="mono">c</text>
<text x="239.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="73" text-anchor="middle" class="mono">d</text>
<text x="275.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="73" text-anchor="middle" class="mono">b</text>
<rect x="303" y="60" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="73" text-anchor="middle" class="mono">r</text>
<text x="20" y="91" text-anchor="middle" class="m">2</text>
<rect x="105" y="79" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="92" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="92" text-anchor="middle" class="mono">b</text>
<text x="149.0" y="92" text-anchor="middle" class="mono">r</text>
<text x="167.0" y="92" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="92" text-anchor="middle" class="mono">$</text>
<text x="203.0" y="92" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="92" text-anchor="middle" class="mono">b</text>
<text x="239.0" y="92" text-anchor="middle" class="mono">r</text>
<text x="257.0" y="92" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="92" text-anchor="middle" class="mono">c</text>
<text x="293.0" y="92" text-anchor="middle" class="mono">a</text>
<rect x="303" y="79" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="92" text-anchor="middle" class="mono">d</text>
<text x="20" y="110" text-anchor="middle" class="m">3</text>
<rect x="105" y="98" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="111" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="111" text-anchor="middle" class="mono">b</text>
<text x="149.0" y="111" text-anchor="middle" class="mono">r</text>
<text x="167.0" y="111" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="111" text-anchor="middle" class="mono">c</text>
<text x="203.0" y="111" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="111" text-anchor="middle" class="mono">d</text>
<text x="239.0" y="111" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="111" text-anchor="middle" class="mono">b</text>
<text x="275.0" y="111" text-anchor="middle" class="mono">r</text>
<text x="293.0" y="111" text-anchor="middle" class="mono">a</text>
<rect x="303" y="98" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="111" text-anchor="middle" class="mono">$</text>
<text x="20" y="129" text-anchor="middle" class="m">4</text>
<rect x="105" y="117" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="130" text-anchor="middle" class="mono">c</text>
<text x="149.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="130" text-anchor="middle" class="mono">d</text>
<text x="185.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="130" text-anchor="middle" class="mono">b</text>
<text x="221.0" y="130" text-anchor="middle" class="mono">r</text>
<text x="239.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="130" text-anchor="middle" class="mono">$</text>
<text x="275.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="130" text-anchor="middle" class="mono">b</text>
<rect x="303" y="117" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="130" text-anchor="middle" class="mono">r</text>
<text x="20" y="148" text-anchor="middle" class="m">5</text>
<rect x="105" y="136" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="149" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="149" text-anchor="middle" class="mono">d</text>
<text x="149.0" y="149" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="149" text-anchor="middle" class="mono">b</text>
<text x="185.0" y="149" text-anchor="middle" class="mono">r</text>
<text x="203.0" y="149" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="149" text-anchor="middle" class="mono">$</text>
<text x="239.0" y="149" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="149" text-anchor="middle" class="mono">b</text>
<text x="275.0" y="149" text-anchor="middle" class="mono">r</text>
<text x="293.0" y="149" text-anchor="middle" class="mono">a</text>
<rect x="303" y="136" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="149" text-anchor="middle" class="mono">c</text>
<text x="20" y="167" text-anchor="middle" class="m">6</text>
<rect x="105" y="155" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="168" text-anchor="middle" class="mono">b</text>
<text x="131.0" y="168" text-anchor="middle" class="mono">r</text>
<text x="149.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="168" text-anchor="middle" class="mono">$</text>
<text x="185.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="168" text-anchor="middle" class="mono">b</text>
<text x="221.0" y="168" text-anchor="middle" class="mono">r</text>
<text x="239.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="168" text-anchor="middle" class="mono">c</text>
<text x="275.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="168" text-anchor="middle" class="mono">d</text>
<rect x="303" y="155" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="20" y="186" text-anchor="middle" class="m">7</text>
<rect x="105" y="174" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="187" text-anchor="middle" class="mono">b</text>
<text x="131.0" y="187" text-anchor="middle" class="mono">r</text>
<text x="149.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="187" text-anchor="middle" class="mono">c</text>
<text x="185.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="187" text-anchor="middle" class="mono">d</text>
<text x="221.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="187" text-anchor="middle" class="mono">b</text>
<text x="257.0" y="187" text-anchor="middle" class="mono">r</text>
<text x="275.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="187" text-anchor="middle" class="mono">$</text>
<rect x="303" y="174" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="20" y="205" text-anchor="middle" class="m">8</text>
<rect x="105" y="193" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="206" text-anchor="middle" class="mono">c</text>
<text x="131.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="206" text-anchor="middle" class="mono">d</text>
<text x="167.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="206" text-anchor="middle" class="mono">b</text>
<text x="203.0" y="206" text-anchor="middle" class="mono">r</text>
<text x="221.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="206" text-anchor="middle" class="mono">$</text>
<text x="257.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="206" text-anchor="middle" class="mono">b</text>
<text x="293.0" y="206" text-anchor="middle" class="mono">r</text>
<rect x="303" y="193" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="20" y="224" text-anchor="middle" class="m">9</text>
<rect x="105" y="212" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="225" text-anchor="middle" class="mono">d</text>
<text x="131.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="225" text-anchor="middle" class="mono">b</text>
<text x="167.0" y="225" text-anchor="middle" class="mono">r</text>
<text x="185.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="225" text-anchor="middle" class="mono">$</text>
<text x="221.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="225" text-anchor="middle" class="mono">b</text>
<text x="257.0" y="225" text-anchor="middle" class="mono">r</text>
<text x="275.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="225" text-anchor="middle" class="mono">c</text>
<rect x="303" y="212" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="20" y="243" text-anchor="middle" class="m">10</text>
<rect x="105" y="231" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="244" text-anchor="middle" class="mono">r</text>
<text x="131.0" y="244" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="244" text-anchor="middle" class="mono">$</text>
<text x="167.0" y="244" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="244" text-anchor="middle" class="mono">b</text>
<text x="203.0" y="244" text-anchor="middle" class="mono">r</text>
<text x="221.0" y="244" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="244" text-anchor="middle" class="mono">c</text>
<text x="257.0" y="244" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="244" text-anchor="middle" class="mono">d</text>
<text x="293.0" y="244" text-anchor="middle" class="mono">a</text>
<rect x="303" y="231" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="244" text-anchor="middle" class="mono">b</text>
<text x="20" y="262" text-anchor="middle" class="m">11</text>
<rect x="105" y="250" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="263" text-anchor="middle" class="mono">r</text>
<text x="131.0" y="263" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="263" text-anchor="middle" class="mono">c</text>
<text x="167.0" y="263" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="263" text-anchor="middle" class="mono">d</text>
<text x="203.0" y="263" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="263" text-anchor="middle" class="mono">b</text>
<text x="239.0" y="263" text-anchor="middle" class="mono">r</text>
<text x="257.0" y="263" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="263" text-anchor="middle" class="mono">$</text>
<text x="293.0" y="263" text-anchor="middle" class="mono">a</text>
<rect x="303" y="250" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="263" text-anchor="middle" class="mono">b</text>
<line x1="338" y1="62" x2="338" y2="151" class="ln"/>
<line x1="338" y1="62" x2="333" y2="62" class="ln"/>
<line x1="338" y1="151" x2="333" y2="151" class="ln"/>
<text x="343" y="110.5" text-anchor="start" class="m">1. a</text>
<text x="343" y="123.5" text-anchor="start" class="m">[1, 6)</text>
<line x1="400" y1="233" x2="400" y2="265" class="ln"/>
<line x1="400" y1="233" x2="395" y2="233" class="ln"/>
<line x1="400" y1="265" x2="395" y2="265" class="ln"/>
<text x="405" y="253.0" text-anchor="start" class="m">2. ra</text>
<text x="405" y="266.0" text-anchor="start" class="m">[10, 12)</text>
<line x1="462" y1="157" x2="462" y2="189" class="ln"/>
<line x1="462" y1="157" x2="457" y2="157" class="ln"/>
<line x1="462" y1="189" x2="457" y2="189" class="ln"/>
<text x="467" y="177.0" text-anchor="start" class="m">3. bra</text>
<text x="467" y="190.0" text-anchor="start" class="m">[6, 8)</text>
<line x1="524" y1="81" x2="524" y2="113" class="ln"/>
<line x1="524" y1="81" x2="519" y2="81" class="ln"/>
<line x1="524" y1="113" x2="519" y2="113" class="ln"/>
<text x="529" y="101.0" text-anchor="start" class="tg">4. abra</text>
<text x="529" y="114.0" text-anchor="start" class="m">[2, 4)</text>
</svg>
</div>

**Where the wavelet tree comes in.** The index keeps `L` as a wavelet tree, so each `rank(c, i)` takes `O(log σ)` for an alphabet of `σ` characters. That gives:

- **Count `P`** in `O(|P| log σ)` steps, whatever the length of the text.
- **Space** about the size of the text, or less with a compressed wavelet tree, instead of a suffix array's `n log2 n` bits.

This is the FM-index of Ferragina and Manzini (2000). Grossi, Gupta and Vitter introduced the wavelet tree (2003) for compressed text indexes like it. To also find *where* the matches are, store the text position of every few rows and follow LF from a match until reaching a stored row.

**Where it is used:**

- **DNA read aligners** such as BWA and Bowtie are built on the FM-index. For DNA's 4 letters, plain tables of counts also work.
- Wavelet trees matter when the alphabet is large: protein sequences, text in any language, or word ids.
- The C++ library SDSL builds its compressed suffix arrays on wavelet trees.

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

/// The BWT: the last column of the sorted rotations.
fn bwt(text: &[u8]) -> Vec<u8> {
    let n = text.len();
    let rotation = |s: usize| [&text[s..], &text[..s]].concat();
    let mut starts: Vec<usize> = (0..n).collect();
    starts.sort_by_key(|&s| rotation(s));
    starts.iter().map(|&s| text[(s + n - 1) % n]).collect()
}

struct FmIndex {
    // the distinct characters, sorted; a character's code is its index
    alphabet: Vec<u8>,
    // smaller[code] = C[c]: characters in the text smaller than c
    smaller: Vec<usize>,
    // the BWT, as codes, in a wavelet tree
    tree: WaveletTree,
    n: usize,
}

impl FmIndex {
    fn new(text: &[u8]) -> Self {
        let mut alphabet = text.to_vec();
        alphabet.sort();
        alphabet.dedup();
        let code = |c: u8| alphabet.binary_search(&c).unwrap() as u32;
        let l: Vec<u32> = bwt(text).iter().map(|&c| code(c)).collect();
        let below = |c: &u8| text.iter().filter(|&&x| x < *c).count();
        let smaller = alphabet.iter().map(below).collect();
        let tree = WaveletTree::new(&l, 0, alphabet.len() as u32 - 1);
        FmIndex { alphabet, smaller, tree, n: text.len() }
    }

    /// How many times p occurs in the text.
    fn count(&self, p: &[u8]) -> usize {
        // every row starts with the empty pattern
        let (mut sp, mut ep) = (0, self.n);
        for &c in p.iter().rev() {
            let Ok(code) = self.alphabet.binary_search(&c) else {
                return 0;
            };
            sp = self.smaller[code] + self.tree.rank(code as u32, sp);
            ep = self.smaller[code] + self.tree.rank(code as u32, ep);
            if sp >= ep {
                return 0;
            }
        }
        ep - sp
    }
}

fn main() {
    let text = b"abracadabra$";
    let index = FmIndex::new(text);
    assert_eq!(bwt(text), b"ard$rcaaaabb");
    assert_eq!(index.smaller, vec![0, 1, 6, 8, 9, 10]);

    // rows [1, 6) -> [10, 12) -> [6, 8) -> [2, 4)
    assert_eq!(index.count(b"abra"), 2);
    assert_eq!(index.count(b"a"), 5);
    assert_eq!(index.count(b"cad"), 1);
    assert_eq!(index.count(b"abc"), 0);
    assert_eq!(index.count(b"z"), 0);

    // every substring of the text, against a plain count
    let body = &text[..text.len() - 1];
    for i in 0..body.len() {
        for j in i + 1..=body.len() {
            let p = &body[i..j];
            let want =
                body.windows(p.len()).filter(|w| *w == p).count();
            assert_eq!(index.count(p), want);
        }
    }
}
```
