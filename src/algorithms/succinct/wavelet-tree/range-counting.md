How does a wavelet tree count the elements at positions `l` to `r - 1` whose values lie between `a` and `b`? And how does that count the **points inside a rectangle**?

---

Search down from the root, carrying the position range into each child with rank:

- if a node's values are all **outside** `a..b`, it adds 0;
- if they are all **inside** `a..b`, every element in its position range counts, so it adds `r - l` and stops;
- otherwise, split: go left with positions `[rank0(l), rank0(r))` and right with `[rank1(l), rank1(r))`.

*Recap.* A wavelet tree stores a sequence whose values come from a range, such as 0 to 7, as a binary tree. Each node covers a range of values and stores one bit per element that reaches it: `0` for the lower half of its range, `1` for the upper half. The elements then go on, in their original order, to the left child (`0`) or the right child (`1`). `rank_b(i)` is the number of `b` bits before position `i` in a node.

On each level at most two nodes are only partly inside `a..b` (the ones holding `a` and `b`), so the search visits `O(log σ)` nodes for `σ` possible values.

Example: positions 1 to 6 of 5, 2, 7, 2, 4, 1, 2, 6 hold 2, 7, 2, 4, 1, 2. The values from 2 to 5 among them are 2, 2, 4, 2, so the answer is **4**.

A position range `[l, r)` means positions `l` to `r - 1`, and node labels such as 0..7 include both ends.

| Node (values) | Positions | Compared with 2..5 | Adds |
|---|---|---|---|
| 0..7 | [1, 7) | partly inside: split into [0, 4) (left) and [1, 3) (right) | |
| 0..3 | [0, 4) | partly inside: split into [0, 1) and [0, 3) | |
| 0..1 | [0, 1) | outside | 0 |
| 2..3 | [0, 3) | inside | 3 |
| 4..7 | [1, 3) | partly inside: split into [1, 2) and [0, 1) | |
| 4..5 | [1, 2) | inside | 1 |
| 6..7 | [0, 1) | outside | 0 |

<div class="diagram">
<svg viewBox="0 0 640 314" width="100%" style="max-width:640px" role="img" aria-label="Counting values 2 to 5 in positions 1 to 6: nodes fully inside the value range add their whole position range.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .nt{fill:#007A66;font-size:11px}svg .cl{fill:rgba(250,100,25,.22);stroke:#FA6419;stroke-width:1}svg .pth{fill:none;stroke:#007A66;stroke-width:2;stroke-dasharray:5 3}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}svg .dim{opacity:.35}.nightMode svg .tg,.night_mode svg .tg,.nightMode svg .nt,.night_mode svg .nt{fill:#14C1A0}.nightMode svg .pth,.night_mode svg .pth{stroke:#14C1A0}</style>
<rect x="219.0" y="15" width="202" height="46" rx="6" class="pth"/>
<text x="215.0" y="49" text-anchor="end" class="m">0..7</text>
<text x="236.0" y="29" text-anchor="middle" class="m">5</text>
<rect x="225.0" y="34" width="22" height="22" rx="2" class="c"/>
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
<rect x="205.0" y="198" width="22" height="22" rx="2" class="cg"/>
<text x="216.0" y="213" text-anchor="middle">0</text>
<text x="240.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="229.0" y="198" width="22" height="22" rx="2" class="cg"/>
<text x="240.0" y="213" text-anchor="middle">0</text>
<text x="264.0" y="193" text-anchor="middle" class="m">2</text>
<rect x="253.0" y="198" width="22" height="22" rx="2" class="cg"/>
<text x="264.0" y="213" text-anchor="middle">0</text>
<text x="285.0" y="213" text-anchor="start" class="nt">+3</text>
<line x1="230" y1="222" x2="200" y2="266" class="ln"/>
<text x="206.0" y="247.0" text-anchor="middle" class="m">0</text>
<line x1="250" y1="222" x2="280" y2="266" class="ln"/>
<text x="274.0" y="247.0" text-anchor="middle" class="m">1</text>
<rect x="427.0" y="97" width="106" height="46" rx="6" class="pth"/>
<text x="423.0" y="131" text-anchor="end" class="m">4..7</text>
<text x="444.0" y="111" text-anchor="middle" class="m">5</text>
<rect x="433.0" y="116" width="22" height="22" rx="2" class="c"/>
<text x="444.0" y="131" text-anchor="middle">0</text>
<text x="468.0" y="111" text-anchor="middle" class="m">7</text>
<rect x="457.0" y="116" width="22" height="22" rx="2" class="cl"/>
<text x="468.0" y="131" text-anchor="middle">1</text>
<text x="492.0" y="111" text-anchor="middle" class="m">4</text>
<rect x="481.0" y="116" width="22" height="22" rx="2" class="cl"/>
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
<rect x="401.0" y="198" width="22" height="22" rx="2" class="cg"/>
<text x="412.0" y="213" text-anchor="middle">0</text>
<text x="433.0" y="213" text-anchor="start" class="nt">+1</text>
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

**Points in a rectangle.** Sort `n` points by `x` and store their `y` values in that order. A rectangle `x1..x2 × y1..y2` becomes a position range `[l, r)` (two binary searches on the sorted `x` values) and a value range `y1..y2`. One count answers it in `O(log n)` steps, with about `n log n` bits of space. The example sequence is the 8 points (1, 5), (2, 2), (3, 7), (4, 2), (5, 4), (6, 1), (7, 2), (8, 6). The rectangle `x` from 2 to 7, `y` from 2 to 5 holds 4 of them.

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
    /// Where the elements at positions [l, r) that went to child b
    /// sit inside that child.
    fn in_child(&self, b: bool, l: usize, r: usize) -> (usize, usize) {
        (self.rank_bit(b, l), self.rank_bit(b, r))
    }

    /// How many of seq[l..r] are between a and b (inclusive).
    fn count(&self, l: usize, r: usize, a: u32, b: u32) -> usize {
        // empty range, or every value of this node outside a..b
        if l >= r || b < self.lo || self.hi < a {
            return 0;
        }
        // every value of this node inside a..b
        if a <= self.lo && self.hi <= b {
            return r - l;
        }
        let kids = self.kids.as_ref().unwrap();
        let (l0, r0) = self.in_child(false, l, r);
        let (l1, r1) = self.in_child(true, l, r);
        kids[0].count(l0, r0, a, b) + kids[1].count(l1, r1, a, b)
    }
}

fn main() {
    let seq = [5, 2, 7, 2, 4, 1, 2, 6];
    let tree = WaveletTree::new(&seq, 0, 7);
    // 2, 7, 2, 4, 1, 2: the values 2 to 5 are 2, 2, 4, 2
    assert_eq!(tree.count(1, 7, 2, 5), 4);

    // the points (1, 5), (2, 2), (3, 7), ..., (8, 6), sorted by x;
    // the tree stores their y values
    let xs: Vec<u32> = (1..=8).collect();
    let ys: Vec<u32> = seq.to_vec();
    let tree = WaveletTree::new(&ys, 0, 7);
    let in_rect = |x1: u32, x2: u32, y1: u32, y2: u32| {
        // positions of the points with x1 <= x <= x2
        let l = xs.partition_point(|&x| x < x1);
        let r = xs.partition_point(|&x| x <= x2);
        tree.count(l, r, y1, y2)
    };
    assert_eq!(in_rect(2, 7, 2, 5), 4);

    // every rectangle, against checking each point
    for (x1, x2) in [(0, 9), (2, 7), (3, 3), (5, 8)] {
        for y1 in 0..8 {
            for y2 in y1..8 {
                let want = xs
                    .iter()
                    .zip(&ys)
                    .filter(|(x, _)| (x1..=x2).contains(*x))
                    .filter(|(_, y)| (y1..=y2).contains(*y))
                    .count();
                assert_eq!(in_rect(x1, x2, y1, y2), want);
            }
        }
    }
}
```
