How does a wavelet tree count how many times a value `c` appears among the first `i` elements, **rank(c, i)**?

---

Walk down along `c`'s path. At each node, keep only the elements before position `i` that go the same way as `c`: `i = rank_b(i)`, where `b` is `c`'s side. At the leaf every element is a `c`, so the final `i` is the answer.

*Recap.* A wavelet tree stores a sequence whose values come from a range, such as 0 to 7, as a binary tree. Each node covers a range of values and stores one bit per element that reaches it: `0` for the lower half of its range, `1` for the upper half. The elements then go on, in their original order, to the left child (`0`) or the right child (`1`). `rank_b(i)` is the number of `b` bits before position `i` in a node.

At each node:

1. `b` = `0` if `c` is in the lower half of the node's range, `1` if it is in the upper half.
2. Among the first `i` elements of this node, the ones on `c`'s side are counted by `rank_b(i)`. In the child they are exactly the first `rank_b(i)` elements, because the order is kept.
3. Set `i = rank_b(i)` and move to child `b`.

Example: rank(2, 7) on 5, 2, 7, 2, 4, 1, 2, 6. The first 7 elements hold the value 2 three times, at positions 1, 3 and 6.

| Node (values) | Side of 2 | First `i` bits | New `i` |
|---|---|---|---|
| 0..7 | 0..3: `0` | `1010100` | rank0(7) = 4 |
| 0..3 | 2..3: `1` | `1101` | rank1(4) = 3 |
| 2..3 | 2: `0` | `000` | rank0(3) = 3 |
| leaf 2 | | | answer **3** |

<div class="diagram">
<svg viewBox="0 0 640 314" width="100%" style="max-width:640px" role="img" aria-label="rank(2, 7) follows the path of 2 and counts the matching bits before i at each node: 4, then 3, then 3.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .nt{fill:#007A66;font-size:11px}svg .cl{fill:rgba(250,100,25,.22);stroke:#FA6419;stroke-width:1}svg .pth{fill:none;stroke:#007A66;stroke-width:2;stroke-dasharray:5 3}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}svg .dim{opacity:.35}.nightMode svg .tg,.night_mode svg .tg,.nightMode svg .nt,.night_mode svg .nt{fill:#14C1A0}.nightMode svg .pth,.night_mode svg .pth{stroke:#14C1A0}</style>
<rect x="219.0" y="15" width="202" height="46" rx="6" class="pth"/>
<text x="215.0" y="49" text-anchor="end" class="m">0..7</text>
<text x="236.0" y="29" text-anchor="middle" class="m">5</text>
<rect x="225.0" y="34" width="22" height="22" rx="2" class="cl"/>
<text x="236.0" y="49" text-anchor="middle">1</text>
<text x="260.0" y="29" text-anchor="middle" class="m">2</text>
<rect x="249.0" y="34" width="22" height="22" rx="2" class="cl"/>
<text x="260.0" y="49" text-anchor="middle">0</text>
<text x="284.0" y="29" text-anchor="middle" class="m">7</text>
<rect x="273.0" y="34" width="22" height="22" rx="2" class="cl"/>
<text x="284.0" y="49" text-anchor="middle">1</text>
<text x="308.0" y="29" text-anchor="middle" class="m">2</text>
<rect x="297.0" y="34" width="22" height="22" rx="2" class="cl"/>
<text x="308.0" y="49" text-anchor="middle">0</text>
<text x="332.0" y="29" text-anchor="middle" class="m">4</text>
<rect x="321.0" y="34" width="22" height="22" rx="2" class="cl"/>
<text x="332.0" y="49" text-anchor="middle">1</text>
<text x="356.0" y="29" text-anchor="middle" class="m">1</text>
<rect x="345.0" y="34" width="22" height="22" rx="2" class="cl"/>
<text x="356.0" y="49" text-anchor="middle">0</text>
<text x="380.0" y="29" text-anchor="middle" class="m">2</text>
<rect x="369.0" y="34" width="22" height="22" rx="2" class="cl"/>
<text x="380.0" y="49" text-anchor="middle">0</text>
<text x="404.0" y="29" text-anchor="middle" class="m">6</text>
<rect x="393.0" y="34" width="22" height="22" rx="2" class="c"/>
<text x="404.0" y="49" text-anchor="middle">1</text>
<text x="425.0" y="49" text-anchor="start" class="nt">0s before 7: i = 4</text>
<line x1="310" y1="58" x2="160" y2="98" class="ln"/>
<text x="226.0" y="81.0" text-anchor="middle" class="m">0</text>
<line x1="330" y1="58" x2="480" y2="98" class="ln"/>
<text x="414.0" y="81.0" text-anchor="middle" class="m">1</text>
<rect x="107.0" y="97" width="106" height="46" rx="6" class="pth"/>
<text x="103.0" y="131" text-anchor="end" class="m">0..3</text>
<text x="124.0" y="111" text-anchor="middle" class="m">2</text>
<rect x="113.0" y="116" width="22" height="22" rx="2" class="cl"/>
<text x="124.0" y="131" text-anchor="middle">1</text>
<text x="148.0" y="111" text-anchor="middle" class="m">2</text>
<rect x="137.0" y="116" width="22" height="22" rx="2" class="cl"/>
<text x="148.0" y="131" text-anchor="middle">1</text>
<text x="172.0" y="111" text-anchor="middle" class="m">1</text>
<rect x="161.0" y="116" width="22" height="22" rx="2" class="cl"/>
<text x="172.0" y="131" text-anchor="middle">0</text>
<text x="196.0" y="111" text-anchor="middle" class="m">2</text>
<rect x="185.0" y="116" width="22" height="22" rx="2" class="cl"/>
<text x="196.0" y="131" text-anchor="middle">1</text>
<text x="217.0" y="131" text-anchor="start" class="nt">1s before 4: i = 3</text>
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
<rect x="205.0" y="198" width="22" height="22" rx="2" class="cl"/>
<text x="216.0" y="213" text-anchor="middle">0</text>
<text x="240.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="229.0" y="198" width="22" height="22" rx="2" class="cl"/>
<text x="240.0" y="213" text-anchor="middle">0</text>
<text x="264.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="253.0" y="198" width="22" height="22" rx="2" class="cl"/>
<text x="264.0" y="213" text-anchor="middle">0</text>
<text x="285.0" y="213" text-anchor="start" class="nt">i = 3</text>
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

Cost: one bit rank per level, so `O(log σ)` for `σ` possible values. Without the tree you would scan all `i` elements, or keep a count array for every value, which takes `σ · n` numbers.

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
        if c < self.lo || c > self.hi {
            return 0;
        }
        let mut node = self;
        while let Some(kids) = &node.kids {
            // c's side: 1 for the upper half
            let b = c > (node.lo + node.hi) / 2;
            i = node.rank_bit(b, i);
            node = &kids[b as usize];
        }
        i
    }
}

fn main() {
    let seq = [5, 2, 7, 2, 4, 1, 2, 6];
    let tree = WaveletTree::new(&seq, 0, 7);

    // i goes 7 -> 4 -> 3 -> 3
    assert_eq!(tree.rank(2, 7), 3);

    // every value and every prefix, against a plain count
    for c in 0..8 {
        for i in 0..=seq.len() {
            let want = seq[..i].iter().filter(|&&v| v == c).count();
            assert_eq!(tree.rank(c, i), want, "c = {c}, i = {i}");
        }
    }
}
```
