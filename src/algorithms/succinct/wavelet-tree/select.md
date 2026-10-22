How does a wavelet tree find the position of the `k`-th occurrence of a value `c` (counting from 0), **select(c, k)**?

---

Go down to `c`'s leaf, then **walk back up**. At the leaf the answer is position `k`. At each parent, a position `p` in child `b` becomes the position of the `b` bit number `p`, which is `select_b(p)`. At the root, `p` is the position in the sequence.

*Recap.* A wavelet tree stores a sequence whose values come from a range, such as 0 to 7, as a binary tree. Each node covers a range of values and stores one bit per element that reaches it: `0` for the lower half of its range, `1` for the upper half. The elements then go on, in their original order, to the left child (`0`) or the right child (`1`). `select_b(p)` is the position of the `b` bit number `p` (counting from 0) in a node.

Why it works: the elements in child `b` are the elements of the parent that have bit `b`, in the same order. So element number `p` of the child is the parent's element at the position of its `p`-th `b` bit.

Example: select(2, 2), the third 2 in 5, 2, 7, 2, 4, 1, 2, 6. The 2s are at positions 1, 3 and 6, so the answer is 6.

| Node (values) | Came from child | Bits | New `p` |
|---|---|---|---|
| leaf 2 | | | `p = 2` (the third element of the leaf) |
| 2..3 | 2 is the `0` side | `000` | 0 number 2 is at **2** |
| 0..3 | 2..3 is the `1` side | `1101` | 1 number 2 is at **3** (1s at 0, 1, 3) |
| 0..7 | 0..3 is the `0` side | `10101001` | 0 number 3 is at **6** (0s at 1, 3, 5, 6) |

<div class="diagram">
<svg viewBox="0 0 640 314" width="100%" style="max-width:640px" role="img" aria-label="select(2, 2) starts at the leaf 2 with p = 2 and walks up: p becomes 2, then 3, then 6.">
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
<text x="425.0" y="49" text-anchor="start" class="nt">0 number 3 is at 6</text>
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
<text x="217.0" y="131" text-anchor="start" class="nt">1 number 2 is at 3</text>
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
<text x="285.0" y="213" text-anchor="start" class="nt">p = 2</text>
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

Cost: one bit select per level, so `O(log σ)` for `σ` possible values, when select on a bit array takes constant time. The code below finds the `b` bit with a scan to stay short.

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

/// Position of the b bit number k (from 0), if there is one.
fn select_bit(bits: &[bool], b: bool, k: usize) -> Option<usize> {
    let same = bits.iter().enumerate().filter(|(_, &x)| x == b);
    same.map(|(p, _)| p).nth(k)
}

impl WaveletTree {
    /// Position of the c number k (from 0), if there is one.
    fn select(&self, c: u32, k: usize) -> Option<usize> {
        let Some(kids) = &self.kids else {
            // a leaf holds only c, so its k-th element is at k
            return (k < self.bits.len()).then_some(k);
        };
        let b = c > (self.lo + self.hi) / 2;
        // the element's position inside child b ...
        let p = kids[b as usize].select(c, k)?;
        // ... is the b bit number p of this node
        select_bit(&self.bits, b, p)
    }
}

fn main() {
    let seq = [5, 2, 7, 2, 4, 1, 2, 6];
    let tree = WaveletTree::new(&seq, 0, 7);

    // p goes 2 -> 2 -> 3 -> 6
    assert_eq!(tree.select(2, 2), Some(6));
    // there are only three 2s
    assert_eq!(tree.select(2, 3), None);

    // every occurrence of every value, against a plain search
    for c in 0..8 {
        let places: Vec<usize> =
            (0..seq.len()).filter(|&i| seq[i] == c).collect();
        for (k, &p) in places.iter().enumerate() {
            assert_eq!(tree.select(c, k), Some(p));
        }
    }
}
```
