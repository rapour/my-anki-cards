rise-rs, a Rust library for search engine indexes, stores each sorted list of numbers with Elias-Fano. Every number `x` is split into a low part (its lowest `l` bits, kept in an array) and a high part `x >> l`. The high parts go into a bit array, the **high bits**: first one `0` that belongs to no number, then for each possible high part in order, one `1` per number with that high part and a `0` to close it. How does rise-rs find the first number that is at least `y`, without scanning from the start?

---

It stores the **position of every 512th 0** of the high bits, because the 0s mark where each high part begins.

Counting the leading `0` as 0 number 0, the 0 number `h` comes just before the numbers whose high part is at least `h`. The `1` of a number with high part `h` has exactly `h + 1` 0s before it: the leading one, and one closing each smaller high part.

1. `h = y >> l` and `k = h / 512`. Start at the stored position of the 0 number `k · 512`. For `k = 0`, start at position 0.
2. Walk forward over `h - k · 512` more 0s (fewer than 512) to reach the 0 number `h`, at position `p`.
3. Before `p` there are `h` 0s, so the other `p - h` bits are 1s, one per number. The first number whose high part is at least `h` is at index `i = p - h`.
4. Scan forward from `i`, comparing whole numbers, until one is at least `y`.

Example: the list 0, 3, 6, ..., 29997 (number `i` is `3i`), with `l = 1`. To find the first number that is at least 1801:

- `h = 1801 >> 1 = 900` and `k = 900 / 512 = 1`. Start at the stored position of the 0 number 512, which is 854.
- Walk `900 - 512 = 388` more 0s to reach the 0 number 900, at position 1500.
- `i = 1500 - 900 = 600`. Number 600 is 1800, which is too small. Number 601 is 1803, the answer.

<div class="diagram">
<svg viewBox="0 0 640 248" width="100%" style="max-width:640px" role="img" aria-label="A stored position for every 512th 0 lets the search jump close to the target, then walk fewer than 512 0s.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}</style>
<rect x="20" y="70" width="600" height="26" rx="2" class="c"/>
<text x="20" y="26" text-anchor="start">high bits of 0, 3, 6, ..., 29997 (l = 1)</text>
<line x1="120" y1="64" x2="120" y2="102" stroke="#FA6419" stroke-width="3"/>
<text x="120" y="58" text-anchor="middle" class="m">0 number 512</text>
<line x1="260" y1="64" x2="260" y2="102" stroke="#FA6419" stroke-width="3"/>
<text x="260" y="58" text-anchor="middle" class="m">1024</text>
<line x1="400" y1="64" x2="400" y2="102" stroke="#FA6419" stroke-width="3"/>
<text x="400" y="58" text-anchor="middle" class="m">1536</text>
<line x1="540" y1="64" x2="540" y2="102" stroke="#FA6419" stroke-width="3"/>
<text x="540" y="58" text-anchor="middle" class="m">2048</text>
<line x1="226" y1="64" x2="226" y2="102" class="ln" stroke-width="3"/>
<text x="226" y="44" text-anchor="middle" class="tg">0 number 900, at 1500</text>
<line x1="120" y1="114" x2="226" y2="114" class="ln"/>
<line x1="120" y1="109" x2="120" y2="119" class="ln"/>
<line x1="226" y1="109" x2="226" y2="119" class="ln"/>
<text x="238" y="118" text-anchor="start" class="m">walk 900 - 512 = 388 more 0s</text>
<rect x="10" y="186" width="220" height="30" rx="6" class="r"/>
<text x="120.0" y="205.5" text-anchor="middle">zero_samples[0] = 854</text>
<line x1="120" y1="186" x2="120" y2="122" class="ln" marker-end="url(#ah)"/>
<text x="320" y="238" text-anchor="middle" class="m">i = 1500 - 900 = 600: number 600 is 1800 (too small), number 601 is 1803</text>
</svg>
</div>

rise-rs first checks how far `y` is from the number it is currently at:

- **High part at most 8 above the current one**: scan forward from 1 to 1 (`EF_LINEAR_SCAN_THRESHOLD = 8`).
- **High part less than 512 above**: walk 0s from the current position.
- **Otherwise**: jump with the stored position (`EF_LOG_SAMPLING0 = 9`, so every 2^9 = 512 0s).
- **`y` beyond every number**: return the end of the list.

```rust
// rise-rs: 1 << EF_LOG_SAMPLING0
const ZEROS_STEP: usize = 512;

struct EliasFano {
    l: u32,
    u: u64,
    low: Vec<u64>,
    // position 0 is a 0 that belongs to no number
    high: Vec<bool>,
    // zero_samples[k - 1] = position of the 0 number k * 512,
    // counting the leading 0 as number 0
    zero_samples: Vec<usize>,
}

fn encode(values: &[u64]) -> EliasFano {
    let n = values.len() as u64;
    let u = values[values.len() - 1] + 1;
    let l = if u > n { (u / n).ilog2() } else { 0 };
    let mut high = vec![false; (n + (u >> l) + 2) as usize];
    let mut low = Vec::new();
    for (i, &x) in values.iter().enumerate() {
        // + 1 for the leading 0
        high[(x >> l) as usize + i + 1] = true;
        low.push(x & ((1 << l) - 1));
    }
    let zeros = (0..high.len()).filter(|&p| !high[p]);
    let zero_samples = zeros.step_by(ZEROS_STEP).skip(1).collect();
    EliasFano { l, u, low, high, zero_samples }
}

/// Position of the 0 number `k` (from 0), counting from `from`.
fn skip_zeros(bits: &[bool], from: usize, k: usize) -> usize {
    (from..bits.len()).filter(|&p| !bits[p]).nth(k).unwrap()
}

/// Index of the first number >= y, or None if all are smaller.
fn next_geq(ef: &EliasFano, y: u64) -> Option<usize> {
    if y >= ef.u {
        return None;
    }
    let h = (y >> ef.l) as usize;
    // jump to a stored 0, then walk fewer than 512 0s
    let k = h / ZEROS_STEP;
    let start = if k == 0 { 0 } else { ef.zero_samples[k - 1] };
    let zero = skip_zeros(&ef.high, start, h - k * ZEROS_STEP);
    // h 0s come before it; the other bits are 1s, one per number
    let mut i = zero - h;
    // scan forward until a number is big enough
    for p in zero..ef.high.len() {
        if ef.high[p] {
            let x = (((p - i - 1) as u64) << ef.l) | ef.low[i];
            if x >= y {
                return Some(i);
            }
            i += 1;
        }
    }
    None
}

fn main() {
    // 0, 3, 6, ..., 29997 and y = 1801: h = 900, start at the
    // stored 854, walk 388 0s to 1500, then i = 600
    let threes: Vec<u64> = (0..10_000).map(|i| 3 * i).collect();
    let ef = encode(&threes);
    assert_eq!(ef.zero_samples[0], 854);
    assert_eq!(skip_zeros(&ef.high, 854, 388), 1500);
    // number 600 is 1800 < 1801, number 601 is 1803
    assert_eq!(next_geq(&ef, 1801), Some(601));

    // 10,000 sorted pseudo-random numbers, gaps of 0 to 127
    let mut x: u64 = 9;
    let mut v = 0;
    let values: Vec<u64> = (0..10_000)
        .map(|_| {
            x = x
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1_442_695_040_888_963_407);
            v += x >> 57;
            v
        })
        .collect();

    let ef = encode(&values);
    assert!(ef.zero_samples.len() > 10);
    let last = values[values.len() - 1];
    for y in (0..last + 50).step_by(7) {
        let want = values.iter().position(|&v| v >= y);
        assert_eq!(next_geq(&ef, y), want, "y = {y}");
    }
}
```
