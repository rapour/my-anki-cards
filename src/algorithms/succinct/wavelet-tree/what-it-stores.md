What is a **wavelet tree**, and what does it store for the sequence 5, 2, 7, 2, 4, 1, 2, 6, whose values are from 0 to 7?

---

A wavelet tree stores a sequence of `n` symbols, taken from an alphabet of `σ` (sigma) possible values, as a binary tree of bit arrays. Each node covers a range of values and stores **one bit per element that reaches it**: 0 for the lower half of its range, 1 for the upper half.

It answers three basic questions, each in `O(log σ)` steps:

- **access(i)**: the element at position `i`;
- **rank(c, i)**: how many times `c` appears in the first `i` elements;
- **select(c, k)**: the position of the `k`-th `c`.

How it is built:

1. The **root** covers the whole alphabet, here 0 to 7. It splits it into a lower half, 0 to 3, and an upper half, 4 to 7.
2. The root stores one bit per element, in order: `0` if the element is in the lower half, `1` if it is in the upper half. For 5, 2, 7, 2, 4, 1, 2, 6 that is `10101001`.
3. The elements with a `0` go, **in their original order**, to the left child (0 to 3): 2, 2, 1, 2. Those with a `1` go to the right child (4 to 7): 5, 7, 4, 6.
4. Each child splits its own range in half the same way, until a range holds a single value. That node is a **leaf** and needs no bits.

<div class="diagram">
<svg viewBox="0 0 640 314" width="100%" style="max-width:640px" role="img" aria-label="A wavelet tree for 5, 2, 7, 2, 4, 1, 2, 6. The root holds the bits 1 0 1 0 1 0 0 1: 1 for values 4 to 7. The lower values 2, 2, 1, 2 go left, the upper values 5, 7, 4, 6 go right, and each child splits its range again.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .nt{fill:#007A66;font-size:11px}svg .cl{fill:rgba(250,100,25,.22);stroke:#FA6419;stroke-width:1}svg .pth{fill:none;stroke:#007A66;stroke-width:2;stroke-dasharray:5 3}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}svg .dim{opacity:.35}.nightMode svg .tg,.night_mode svg .tg,.nightMode svg .nt,.night_mode svg .nt{fill:#14C1A0}.nightMode svg .pth,.night_mode svg .pth{stroke:#14C1A0}</style>
<text x="10" y="14" text-anchor="start" class="m">small numbers: the values (for reading only); boxes: the stored bits</text>
<text x="215.0" y="49" text-anchor="end" class="m">0..7</text>
<text x="236.0" y="29" text-anchor="middle" class="m">5</text>
<rect x="225.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="236.0" y="49" text-anchor="middle">1</text>
<text x="260.0" y="29" text-anchor="middle" class="m">2</text>
<rect x="249.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="260.0" y="49" text-anchor="middle">0</text>
<text x="284.0" y="29" text-anchor="middle" class="m">7</text>
<rect x="273.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="284.0" y="49" text-anchor="middle">1</text>
<text x="308.0" y="29" text-anchor="middle" class="m">2</text>
<rect x="297.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="308.0" y="49" text-anchor="middle">0</text>
<text x="332.0" y="29" text-anchor="middle" class="m">4</text>
<rect x="321.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="332.0" y="49" text-anchor="middle">1</text>
<text x="356.0" y="29" text-anchor="middle" class="m">1</text>
<rect x="345.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="356.0" y="49" text-anchor="middle">0</text>
<text x="380.0" y="29" text-anchor="middle" class="m">2</text>
<rect x="369.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="380.0" y="49" text-anchor="middle">0</text>
<text x="404.0" y="29" text-anchor="middle" class="m">6</text>
<rect x="393.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="404.0" y="49" text-anchor="middle">1</text>
<line x1="310" y1="58" x2="160" y2="98" class="ln"/>
<text x="226.0" y="81.0" text-anchor="middle" class="m">0</text>
<line x1="330" y1="58" x2="480" y2="98" class="ln"/>
<text x="414.0" y="81.0" text-anchor="middle" class="m">1</text>
<text x="103.0" y="131" text-anchor="end" class="m">0..3</text>
<text x="124.0" y="111" text-anchor="middle" class="m">2</text>
<rect x="113.0" y="116" width="22" height="22" rx="2" class="c"/>
<text x="124.0" y="131" text-anchor="middle">1</text>
<text x="148.0" y="111" text-anchor="middle" class="m">2</text>
<rect x="137.0" y="116" width="22" height="22" rx="2" class="c"/>
<text x="148.0" y="131" text-anchor="middle">1</text>
<text x="172.0" y="111" text-anchor="middle" class="m">1</text>
<rect x="161.0" y="116" width="22" height="22" rx="2" class="c"/>
<text x="172.0" y="131" text-anchor="middle">0</text>
<text x="196.0" y="111" text-anchor="middle" class="m">2</text>
<rect x="185.0" y="116" width="22" height="22" rx="2" class="c"/>
<text x="196.0" y="131" text-anchor="middle">1</text>
<line x1="150" y1="140" x2="80" y2="180" class="ln"/>
<text x="106.0" y="163.0" text-anchor="middle" class="m">0</text>
<line x1="170" y1="140" x2="240" y2="180" class="ln"/>
<text x="214.0" y="163.0" text-anchor="middle" class="m">1</text>
<text x="59.0" y="213" text-anchor="end" class="m">0..1</text>
<text x="80.0" y="193" text-anchor="middle" class="m">1</text>
<rect x="69.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="80.0" y="213" text-anchor="middle">1</text>
<line x1="70" y1="222" x2="40" y2="266" class="ln"/>
<text x="46.0" y="247.0" text-anchor="middle" class="m">0</text>
<line x1="90" y1="222" x2="120" y2="266" class="ln"/>
<text x="114.0" y="247.0" text-anchor="middle" class="m">1</text>
<text x="195.0" y="213" text-anchor="end" class="m">2..3</text>
<text x="216.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="205.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="216.0" y="213" text-anchor="middle">0</text>
<text x="240.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="229.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="240.0" y="213" text-anchor="middle">0</text>
<text x="264.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="253.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="264.0" y="213" text-anchor="middle">0</text>
<line x1="230" y1="222" x2="200" y2="266" class="ln"/>
<text x="206.0" y="247.0" text-anchor="middle" class="m">0</text>
<line x1="250" y1="222" x2="280" y2="266" class="ln"/>
<text x="274.0" y="247.0" text-anchor="middle" class="m">1</text>
<text x="423.0" y="131" text-anchor="end" class="m">4..7</text>
<text x="444.0" y="111" text-anchor="middle" class="m">5</text>
<rect x="433.0" y="116" width="22" height="22" rx="2" class="c"/>
<text x="444.0" y="131" text-anchor="middle">0</text>
<text x="468.0" y="111" text-anchor="middle" class="m">7</text>
<rect x="457.0" y="116" width="22" height="22" rx="2" class="c"/>
<text x="468.0" y="131" text-anchor="middle">1</text>
<text x="492.0" y="111" text-anchor="middle" class="m">4</text>
<rect x="481.0" y="116" width="22" height="22" rx="2" class="c"/>
<text x="492.0" y="131" text-anchor="middle">0</text>
<text x="516.0" y="111" text-anchor="middle" class="m">6</text>
<rect x="505.0" y="116" width="22" height="22" rx="2" class="c"/>
<text x="516.0" y="131" text-anchor="middle">1</text>
<line x1="470" y1="140" x2="400" y2="180" class="ln"/>
<text x="426.0" y="163.0" text-anchor="middle" class="m">0</text>
<line x1="490" y1="140" x2="560" y2="180" class="ln"/>
<text x="534.0" y="163.0" text-anchor="middle" class="m">1</text>
<text x="367.0" y="213" text-anchor="end" class="m">4..5</text>
<text x="388.0" y="193" text-anchor="middle" class="m">5</text>
<rect x="377.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="388.0" y="213" text-anchor="middle">1</text>
<text x="412.0" y="193" text-anchor="middle" class="m">4</text>
<rect x="401.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="412.0" y="213" text-anchor="middle">0</text>
<line x1="390" y1="222" x2="360" y2="266" class="ln"/>
<text x="366.0" y="247.0" text-anchor="middle" class="m">0</text>
<line x1="410" y1="222" x2="440" y2="266" class="ln"/>
<text x="434.0" y="247.0" text-anchor="middle" class="m">1</text>
<text x="527.0" y="213" text-anchor="end" class="m">6..7</text>
<text x="548.0" y="193" text-anchor="middle" class="m">7</text>
<rect x="537.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="548.0" y="213" text-anchor="middle">1</text>
<text x="572.0" y="193" text-anchor="middle" class="m">6</text>
<rect x="561.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="572.0" y="213" text-anchor="middle">0</text>
<line x1="550" y1="222" x2="520" y2="266" class="ln"/>
<text x="526.0" y="247.0" text-anchor="middle" class="m">0</text>
<line x1="570" y1="222" x2="600" y2="266" class="ln"/>
<text x="594.0" y="247.0" text-anchor="middle" class="m">1</text>
<g class="dim"><rect x="22" y="268" width="36" height="24" rx="6" class="k"/>
<text x="40.0" y="284.5" text-anchor="middle">0</text></g>
<text x="40" y="306" text-anchor="middle" class="m">×0</text>
<g><rect x="102" y="268" width="36" height="24" rx="6" class="k"/>
<text x="120.0" y="284.5" text-anchor="middle">1</text></g>
<text x="120" y="306" text-anchor="middle" class="m">×1</text>
<g><rect x="182" y="268" width="36" height="24" rx="6" class="k"/>
<text x="200.0" y="284.5" text-anchor="middle">2</text></g>
<text x="200" y="306" text-anchor="middle" class="m">×3</text>
<g class="dim"><rect x="262" y="268" width="36" height="24" rx="6" class="k"/>
<text x="280.0" y="284.5" text-anchor="middle">3</text></g>
<text x="280" y="306" text-anchor="middle" class="m">×0</text>
<g><rect x="342" y="268" width="36" height="24" rx="6" class="k"/>
<text x="360.0" y="284.5" text-anchor="middle">4</text></g>
<text x="360" y="306" text-anchor="middle" class="m">×1</text>
<g><rect x="422" y="268" width="36" height="24" rx="6" class="k"/>
<text x="440.0" y="284.5" text-anchor="middle">5</text></g>
<text x="440" y="306" text-anchor="middle" class="m">×1</text>
<g><rect x="502" y="268" width="36" height="24" rx="6" class="k"/>
<text x="520.0" y="284.5" text-anchor="middle">6</text></g>
<text x="520" y="306" text-anchor="middle" class="m">×1</text>
<g><rect x="582" y="268" width="36" height="24" rx="6" class="k"/>
<text x="600.0" y="284.5" text-anchor="middle">7</text></g>
<text x="600" y="306" text-anchor="middle" class="m">×1</text>
</svg>
</div>

Only the bits are stored. The values printed above them are there for reading: the tree can always work them out, because every node knows its range.

**Size.** There are `⌈log2 σ⌉` levels, 3 here. Every element passes through exactly one node on each level, so each level holds exactly `n` bits, 8 here. In total that is `n · ⌈log2 σ⌉` bits, 24 here, the same as writing every element in 3 bits. A small index on each bit array then makes rank and select on bits fast.

With the values 0 to 7, the bit at each level is simply one bit of the value. The root stores the top bit (5 = `101` gives `1`), the next level the middle bit, and the last level the lowest bit.

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

/// The bits as text, for example "1011".
fn text(bits: &[bool]) -> String {
    bits.iter().map(|&b| if b { '1' } else { '0' }).collect()
}

/// The bits of all nodes at each depth, left to right.
fn levels(node: &WaveletTree, depth: usize, out: &mut Vec<String>) {
    // a leaf holds a single value and needs no bits
    let Some(kids) = &node.kids else { return };
    if out.len() == depth {
        out.push(String::new());
    }
    out[depth] += &text(&node.bits);
    for kid in kids.iter() {
        levels(kid, depth + 1, out);
    }
}

fn main() {
    let seq = [5, 2, 7, 2, 4, 1, 2, 6];
    let tree = WaveletTree::new(&seq, 0, 7);

    // root: 1 for the upper half, 4 to 7
    assert_eq!(text(&tree.bits), "10101001");
    let kids = tree.kids.as_ref().unwrap();
    // left child: 2, 2, 1, 2 in order; 1 for 2 to 3
    assert_eq!(text(&kids[0].bits), "1101");
    // right child: 5, 7, 4, 6 in order; 1 for 6 to 7
    assert_eq!(text(&kids[1].bits), "0101");

    // 3 levels, each with exactly one bit per element
    let mut out = Vec::new();
    levels(&tree, 0, &mut out);
    assert_eq!(out, ["10101001", "11010101", "10001010"]);

    // each level's bit is one bit of the value: level d holds
    // bit 2 - d, with the elements stably sorted by the bits above
    for (d, level) in out.iter().enumerate() {
        let mut order = seq.to_vec();
        order.sort_by_key(|&v| v >> (3 - d));
        let bit = |v: u32| (v >> (2 - d)) & 1 == 1;
        let want: Vec<bool> = order.iter().map(|&v| bit(v)).collect();
        assert_eq!(level, &text(&want));
    }
}
```
