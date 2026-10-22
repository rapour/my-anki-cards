How does a wavelet tree give back the element at position `i`, **access(i)**, when it stores only bits?

---

Walk down from the root. At each node the bit at `i` says which child the element went to, and **rank** on the bits gives its position inside that child. The leaf you reach is the answer.

*Recap.* A wavelet tree stores a sequence whose values come from a range, such as 0 to 7, as a binary tree. Each node covers a range of values and stores one bit per element that reaches it: `0` for the lower half of its range, `1` for the upper half. The elements then go on, in their original order, to the left child (`0`) or the right child (`1`).

At each node:

1. `b = bits[i]` tells which half the element is in.
2. The element's position in child `b` is **the number of `b` bits before `i`**, written `rank_b(i)`. The elements keep their order, so the ones before it that went to the same child are exactly the `b` bits before position `i`.
3. Set `i = rank_b(i)` and move to child `b`.

Example: access(6) on 5, 2, 7, 2, 4, 1, 2, 6.

| Node (values) | Bits | Bit at `i` | New `i` |
|---|---|---|---|
| 0..7 | `10101001` | bit 6 is `0`: go left | rank0(6) = 3 (0s at 1, 3, 5) |
| 0..3 | `1101` | bit 3 is `1`: go right | rank1(3) = 2 (1s at 0, 1) |
| 2..3 | `000` | bit 2 is `0`: go left | leaf **2** |

<div class="diagram">
<svg viewBox="0 0 640 314" width="100%" style="max-width:640px" role="img" aria-label="access(6) walks down: root bit 0, then bit 1, then bit 0, reaching the leaf 2.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .nt{fill:#007A66;font-size:11px}svg .cl{fill:rgba(250,100,25,.22);stroke:#FA6419;stroke-width:1}svg .pth{fill:none;stroke:#007A66;stroke-width:2;stroke-dasharray:5 3}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}svg .dim{opacity:.35}.nightMode svg .tg,.night_mode svg .tg,.nightMode svg .nt,.night_mode svg .nt{fill:#14C1A0}.nightMode svg .pth,.night_mode svg .pth{stroke:#14C1A0}</style>
<rect x="219.0" y="15" width="202" height="46" rx="6" class="pth"/>
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
<rect x="369.0" y="34" width="22" height="22" rx="2" class="cr"/>
<text x="380.0" y="49" text-anchor="middle">0</text>
<text x="404.0" y="29" text-anchor="middle" class="m">6</text>
<rect x="393.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="404.0" y="49" text-anchor="middle">1</text>
<text x="425.0" y="49" text-anchor="start" class="nt">bit 0, so i = rank0(6) = 3</text>
<line x1="310" y1="58" x2="160" y2="98" class="ln"/>
<text x="226.0" y="81.0" text-anchor="middle" class="m">0</text>
<line x1="330" y1="58" x2="480" y2="98" class="ln"/>
<text x="414.0" y="81.0" text-anchor="middle" class="m">1</text>
<rect x="107.0" y="97" width="106" height="46" rx="6" class="pth"/>
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
<rect x="185.0" y="116" width="22" height="22" rx="2" class="cr"/>
<text x="196.0" y="131" text-anchor="middle">1</text>
<text x="217.0" y="131" text-anchor="start" class="nt">bit 1, so i = rank1(3) = 2</text>
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
<rect x="199.0" y="179" width="82" height="46" rx="6" class="pth"/>
<text x="195.0" y="213" text-anchor="end" class="m">2..3</text>
<text x="216.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="205.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="216.0" y="213" text-anchor="middle">0</text>
<text x="240.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="229.0" y="198" width="22" height="22" rx="2" class="c"/>
<text x="240.0" y="213" text-anchor="middle">0</text>
<text x="264.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="253.0" y="198" width="22" height="22" rx="2" class="cr"/>
<text x="264.0" y="213" text-anchor="middle">0</text>
<text x="285.0" y="213" text-anchor="start" class="nt">bit 0</text>
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
<g><rect x="182" y="268" width="36" height="24" rx="6" class="g"/>
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

Cost: one rank per level, so `O(log σ)` for an alphabet of `σ` values, when rank on a bit array takes constant time.

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
    /// The element at position i.
    fn access(&self, mut i: usize) -> u32 {
        let mut node = self;
        while let Some(kids) = &node.kids {
            let b = node.bits[i];
            // the element's position inside child b
            i = node.rank_bit(b, i);
            node = &kids[b as usize];
        }
        node.lo
    }
}

fn main() {
    let seq = [5, 2, 7, 2, 4, 1, 2, 6];
    let tree = WaveletTree::new(&seq, 0, 7);

    // bit 0 at the root, rank0(6) = 3; bit 1, rank1(3) = 2; leaf 2
    assert_eq!(tree.rank_bit(false, 6), 3);
    assert_eq!(tree.access(6), 2);

    // every position of a pseudo-random sequence over 0 to 99
    let mut x: u64 = 1;
    let long: Vec<u32> = (0..2000)
        .map(|_| {
            x = x
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1_442_695_040_888_963_407);
            ((x >> 33) % 100) as u32
        })
        .collect();
    let tree = WaveletTree::new(&long, 0, 99);
    for (i, &v) in long.iter().enumerate() {
        assert_eq!(tree.access(i), v);
    }
}
```
