You have `n` points `(x, y)` and many queries of the form: how many points lie inside the rectangle `x1 ≤ x ≤ x2`, `y1 ≤ y ≤ y2`? How does a wavelet tree answer each query in `O(log n)` steps?

---

**Turn the rectangle into a range count.** Sort the points by `x` and write their `y` values down in that order. Then:

1. **The `x` condition** picks a run of neighbouring positions `[l, r)`, meaning positions `l` to `r - 1`. Two binary searches on the sorted `x` values find it.
2. **The `y` condition** asks how many of the values at those positions lie between `y1` and `y2`.
3. A wavelet tree built over the `y` values answers that with one **range count**.

*Recap.* A wavelet tree over a sequence answers "how many elements at positions `[l, r)` have values between `a` and `b`?" by walking down from the root. A node whose values all lie inside `a..b` adds its whole position range, `r - l`. A node with none adds 0. A node that is partly inside passes the range to its children with rank. At most two nodes per level are partly inside, so it visits `O(log σ)` nodes for `σ` possible values.

**Example.** Eight shops on a map: (1, 5), (2, 2), (3, 7), (4, 2), (5, 4), (6, 1), (7, 2), (8, 6). How many lie in the rectangle `x` from 2 to 7, `y` from 2 to 5?

<div class="diagram">
<svg viewBox="0 0 640 262" width="100%" style="max-width:640px" role="img" aria-label="Eight points; the rectangle x 2 to 7, y 2 to 5 holds four of them. Sorted by x, their y values are 5, 2, 7, 2, 4, 1, 2, 6. The x range is positions 1 to 6, and four of the values there lie between 2 and 5.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .nt{fill:#007A66;font-size:11px}svg .cl{fill:rgba(250,100,25,.22);stroke:#FA6419;stroke-width:1}svg .pth{fill:none;stroke:#007A66;stroke-width:2;stroke-dasharray:5 3}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}svg .dim{opacity:.35}.nightMode svg .tg,.night_mode svg .tg,.nightMode svg .nt,.night_mode svg .nt{fill:#14C1A0}.nightMode svg .pth,.night_mode svg .pth{stroke:#14C1A0}</style>
<line x1="40" y1="236" x2="274" y2="236" class="ln"/>
<line x1="40" y1="236" x2="40" y2="28" class="ln"/>
<text x="66" y="251" text-anchor="middle" class="m">1</text>
<text x="31" y="214" text-anchor="middle" class="m">1</text>
<text x="92" y="251" text-anchor="middle" class="m">2</text>
<text x="31" y="188" text-anchor="middle" class="m">2</text>
<text x="118" y="251" text-anchor="middle" class="m">3</text>
<text x="31" y="162" text-anchor="middle" class="m">3</text>
<text x="144" y="251" text-anchor="middle" class="m">4</text>
<text x="31" y="136" text-anchor="middle" class="m">4</text>
<text x="170" y="251" text-anchor="middle" class="m">5</text>
<text x="31" y="110" text-anchor="middle" class="m">5</text>
<text x="196" y="251" text-anchor="middle" class="m">6</text>
<text x="31" y="84" text-anchor="middle" class="m">6</text>
<text x="222" y="251" text-anchor="middle" class="m">7</text>
<text x="31" y="58" text-anchor="middle" class="m">7</text>
<text x="248" y="251" text-anchor="middle" class="m">8</text>
<text x="31" y="32" text-anchor="middle" class="m">8</text>
<text x="278" y="240" text-anchor="start" class="m">x</text>
<text x="40" y="20" text-anchor="middle" class="m">y</text>
<rect x="86" y="100" width="142" height="90" rx="4" fill="rgba(250,100,25,.08)" stroke="#FA6419" stroke-width="1.5" stroke-dasharray="5 3"/>
<text x="232" y="110" text-anchor="start" class="to">x 2..7, y 2..5</text>
<circle cx="66" cy="106" r="6" class="c"/>
<circle cx="92" cy="184" r="6" class="cg"/>
<circle cx="118" cy="54" r="6" class="c"/>
<circle cx="144" cy="184" r="6" class="cg"/>
<circle cx="170" cy="132" r="6" class="cg"/>
<circle cx="196" cy="210" r="6" class="c"/>
<circle cx="222" cy="184" r="6" class="cg"/>
<circle cx="248" cy="80" r="6" class="c"/>
<text x="324" y="66" text-anchor="end" class="m">x</text>
<text x="324" y="113" text-anchor="end">y</text>
<text x="324" y="50" text-anchor="end" class="m">position</text>
<text x="347.0" y="50" text-anchor="middle" class="m">0</text>
<text x="347.0" y="66" text-anchor="middle" class="m">1</text>
<rect x="332" y="96" width="30" height="24" rx="2" class="c"/>
<text x="347.0" y="113" text-anchor="middle">5</text>
<text x="381.0" y="50" text-anchor="middle" class="m">1</text>
<text x="381.0" y="66" text-anchor="middle" class="m">2</text>
<rect x="366" y="96" width="30" height="24" rx="2" class="cg"/>
<text x="381.0" y="113" text-anchor="middle">2</text>
<text x="415.0" y="50" text-anchor="middle" class="m">2</text>
<text x="415.0" y="66" text-anchor="middle" class="m">3</text>
<rect x="400" y="96" width="30" height="24" rx="2" class="cl"/>
<text x="415.0" y="113" text-anchor="middle">7</text>
<text x="449.0" y="50" text-anchor="middle" class="m">3</text>
<text x="449.0" y="66" text-anchor="middle" class="m">4</text>
<rect x="434" y="96" width="30" height="24" rx="2" class="cg"/>
<text x="449.0" y="113" text-anchor="middle">2</text>
<text x="483.0" y="50" text-anchor="middle" class="m">4</text>
<text x="483.0" y="66" text-anchor="middle" class="m">5</text>
<rect x="468" y="96" width="30" height="24" rx="2" class="cg"/>
<text x="483.0" y="113" text-anchor="middle">4</text>
<text x="517.0" y="50" text-anchor="middle" class="m">5</text>
<text x="517.0" y="66" text-anchor="middle" class="m">6</text>
<rect x="502" y="96" width="30" height="24" rx="2" class="cl"/>
<text x="517.0" y="113" text-anchor="middle">1</text>
<text x="551.0" y="50" text-anchor="middle" class="m">6</text>
<text x="551.0" y="66" text-anchor="middle" class="m">7</text>
<rect x="536" y="96" width="30" height="24" rx="2" class="cg"/>
<text x="551.0" y="113" text-anchor="middle">2</text>
<text x="585.0" y="50" text-anchor="middle" class="m">7</text>
<text x="585.0" y="66" text-anchor="middle" class="m">8</text>
<rect x="570" y="96" width="30" height="24" rx="2" class="c"/>
<text x="585.0" y="113" text-anchor="middle">6</text>
<line x1="366" y1="130" x2="566" y2="130" class="ln"/>
<line x1="366" y1="125" x2="366" y2="135" class="ln"/>
<line x1="566" y1="125" x2="566" y2="135" class="ln"/>
<text x="466.0" y="150" text-anchor="middle" class="m">x from 2 to 7: positions [1, 7)</text>
<text x="466" y="188" text-anchor="middle" class="nt">values 2..5 among them: 2, 2, 4, 2</text>
<text x="466" y="208" text-anchor="middle" class="tg">count(1, 7, 2, 5) = 4</text>
</svg>
</div>

1. Sorted by `x`, the `y` values are 5, 2, 7, 2, 4, 1, 2, 6. Position `i` holds the shop with `x = i + 1`.
2. `x` from 2 to 7: the first position with `x ≥ 2` is `l = 1`, and the first with `x > 7` is `r = 7`. So the rectangle's `x` range is positions `[1, 7)`, holding the `y` values 2, 7, 2, 4, 1, 2.
3. `y` from 2 to 5: among those, 2, 2, 4 and 2 qualify, so the answer is **4**. The tree finds it without visiting the points one by one. The node for values 2..3 adds its 3 elements (the three 2s), and the node for 4..5 adds 1 (the 4).
4. Check on the map: the shops inside are (2, 2), (4, 2), (5, 4) and (7, 2). (3, 7) is too high and (6, 1) too low. (1, 5) and (8, 6) fail the `x` condition, which is why positions 0 and 7 were never looked at.

**Real coordinates.** Coordinates are rarely small whole numbers. Replace each `y` by its **rank**: its index among the distinct `y` values in sorted order. This is called *coordinate compression*. The tree then holds values 0 to at most `n - 1`, so it has about `log2 n` levels. Turn a query's `y1` and `y2` into a rank range with two more binary searches. `x` needs no change, because it is only binary-searched.

- The `y` values 120, 45, 300, 45 have distinct sorted values 45, 120, 300, so their ranks are 1, 0, 2, 0.
- The query `y` from 50 to 300 becomes the ranks from 1 (the first value ≥ 50 is 120) to 2 (the last value ≤ 300 is 300).

**Cost.** Building takes `O(n log n)` time and about `n log2 n` bits plus small rank indexes. Each query takes `O(log n)`: four binary searches and one range count. Checking every point would take `O(n)` per query.

**Uses:**

- counting the places inside the visible part of a map;
- database queries that filter two number columns at once, such as orders with a price between 10 and 20 placed between two dates.

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
        if l >= r || b < self.lo || self.hi < a {
            return 0;
        }
        if a <= self.lo && self.hi <= b {
            return r - l;
        }
        let kids = self.kids.as_ref().unwrap();
        let (l0, r0) = self.in_child(false, l, r);
        let (l1, r1) = self.in_child(true, l, r);
        kids[0].count(l0, r0, a, b) + kids[1].count(l1, r1, a, b)
    }
}

/// Counts the points inside rectangles.
struct PointCounter {
    // the x values, sorted
    xs: Vec<i64>,
    // the distinct y values, sorted: a y's rank is its index here
    ys: Vec<i64>,
    // the y ranks, in x order
    tree: WaveletTree,
}

impl PointCounter {
    fn new(points: &[(i64, i64)]) -> Self {
        let mut points = points.to_vec();
        points.sort();
        let xs: Vec<i64> = points.iter().map(|p| p.0).collect();
        let mut ys: Vec<i64> = points.iter().map(|p| p.1).collect();
        ys.sort();
        ys.dedup();
        // coordinate compression: each y becomes its rank
        let rank = |y: i64| ys.binary_search(&y).unwrap() as u32;
        let ranks: Vec<u32> =
            points.iter().map(|p| rank(p.1)).collect();
        let tree = WaveletTree::new(&ranks, 0, ys.len() as u32 - 1);
        PointCounter { xs, ys, tree }
    }

    /// Points with x1 <= x <= x2 and y1 <= y <= y2.
    fn count(&self, x1: i64, x2: i64, y1: i64, y2: i64) -> usize {
        // the x condition: positions [l, r)
        let l = self.xs.partition_point(|&x| x < x1);
        let r = self.xs.partition_point(|&x| x <= x2);
        // the y condition: ranks [a, b)
        let a = self.ys.partition_point(|&y| y < y1);
        let b = self.ys.partition_point(|&y| y <= y2);
        if a >= b {
            return 0;
        }
        self.tree.count(l, r, a as u32, b as u32 - 1)
    }
}

fn main() {
    // eight shops (1, 5), (2, 2), (3, 7), ..., (8, 6);
    // the rectangle x 2..=7, y 2..=5 holds four of them
    let ys = [5, 2, 7, 2, 4, 1, 2, 6];
    let shops: Vec<(i64, i64)> = (1..=8).zip(ys).collect();
    let counter = PointCounter::new(&shops);
    assert_eq!(counter.count(2, 7, 2, 5), 4);

    // compression: the y values 120, 45, 300, 45 become 1, 0, 2, 0
    let far = [(10, 120), (20, 45), (30, 300), (40, 45)];
    let counter = PointCounter::new(&far);
    assert_eq!(counter.ys, vec![45, 120, 300]);
    // y from 50 to 300 is ranks 1 to 2: the points at x = 10 and 30
    assert_eq!(counter.count(0, 100, 50, 300), 2);

    // pseudo-random points and rectangles, against checking each point
    let mut s: u64 = 42;
    let mut next = || {
        s = s
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        ((s >> 33) % 2001) as i64 - 1000
    };
    let points: Vec<(i64, i64)> =
        (0..300).map(|_| (next(), next())).collect();
    let counter = PointCounter::new(&points);
    for _ in 0..2000 {
        let (xa, xb, ya, yb) = (next(), next(), next(), next());
        let (x1, x2) = (xa.min(xb), xa.max(xb));
        let (y1, y2) = (ya.min(yb), ya.max(yb));
        let inside = |&&(x, y): &&(i64, i64)| {
            (x1..=x2).contains(&x) && (y1..=y2).contains(&y)
        };
        let want = points.iter().filter(inside).count();
        assert_eq!(counter.count(x1, x2, y1, y2), want);
    }
}
```
