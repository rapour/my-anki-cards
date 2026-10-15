rise-rs, a Rust library for search engine indexes, stores each sorted list of numbers with Elias-Fano. Every number `x` is split into a low part (its lowest `l` bits, kept in an array) and a high part `x >> l`. The high parts go into a bit array, the **high bits**, which starts with one `0` that belongs to no number. After it, number `i` (counting from 0) sets the bit at position `(x >> l) + i + 1`. How does rise-rs find the number at index `i` without scanning the high bits from the start?

---

It stores the **position of every 256th 1** of the high bits, jumps to the nearest one, and walks from there.

1. `k = i / 256`. Start at the stored position of the `1` of number `k · 256`. For `k = 0`, start at position 0.
2. Walk forward over `i - k · 256` more 1s, which is fewer than 256. rise-rs skips 64 bits at a time with `count_ones`, then finds the right 1 inside the last word.
3. At the `1`'s position `p`, `high = p - i - 1`: the `i` earlier 1s and the leading `0` each pushed it right by one. The number is `(high << l) | low[i]`.

Example: the list 0, 3, 6, ..., 29997 (number `i` is `3i`), with `n = 10,000` and `u = 29,998`, so `l = 1`. To read index 600:

- `k = 600 / 256 = 2`. Start at the stored position of the `1` of number 512, which is 1281.
- Walk `600 - 512 = 88` more 1s to reach position 1501.
- `high = 1501 - 600 - 1 = 900` and `low[600] = 0`, so the number is `(900 << 1) | 0 = 1800`, which is `3 · 600`.

<div class="diagram">
<svg viewBox="0 0 640 248" width="100%" style="max-width:640px" role="img" aria-label="A stored position for every 256th 1 lets the search jump close to the target, then walk fewer than 256 1s.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}</style>
<rect x="20" y="70" width="600" height="26" rx="2" class="c"/>
<text x="20" y="26" text-anchor="start">high bits of 0, 3, 6, ..., 29997 (l = 1)</text>
<line x1="120" y1="64" x2="120" y2="102" stroke="#FA6419" stroke-width="3"/>
<text x="120" y="58" text-anchor="middle" class="m">1 of number 256</text>
<line x1="260" y1="64" x2="260" y2="102" stroke="#FA6419" stroke-width="3"/>
<text x="260" y="58" text-anchor="middle" class="m">512</text>
<line x1="400" y1="64" x2="400" y2="102" stroke="#FA6419" stroke-width="3"/>
<text x="400" y="58" text-anchor="middle" class="m">768</text>
<line x1="540" y1="64" x2="540" y2="102" stroke="#FA6419" stroke-width="3"/>
<text x="540" y="58" text-anchor="middle" class="m">1024</text>
<line x1="308" y1="64" x2="308" y2="102" class="ln" stroke-width="3"/>
<text x="308" y="44" text-anchor="middle" class="tg">1 of number 600, at 1501</text>
<line x1="260" y1="114" x2="308" y2="114" class="ln"/>
<line x1="260" y1="109" x2="260" y2="119" class="ln"/>
<line x1="308" y1="109" x2="308" y2="119" class="ln"/>
<text x="320" y="118" text-anchor="start" class="m">walk 600 - 512 = 88 more 1s</text>
<rect x="150" y="186" width="220" height="30" rx="6" class="r"/>
<text x="260.0" y="205.5" text-anchor="middle">one_samples[1] = 1281</text>
<line x1="260" y1="186" x2="260" y2="122" class="ln" marker-end="url(#ah)"/>
<text x="320" y="238" text-anchor="middle" class="m">high = 1501 - 600 - 1 = 900, number = (900 &lt;&lt; 1) | 0 = 1800</text>
</svg>
</div>

rise-rs keeps a current position and first checks how far the target is from it:

- **At most 8 ahead**: step from 1 to 1 (`EF_LINEAR_SCAN_THRESHOLD = 8`).
- **Fewer than 256 ahead**: walk from the current position.
- **Otherwise**: jump with the stored position (`EF_LOG_SAMPLING1 = 8`, so every 2^8 = 256 1s).

The code mirrors this jump, with a bit-by-bit walk to keep it short.

```rust
// rise-rs: 1 << EF_LOG_SAMPLING1
const ONES_STEP: usize = 256;

struct EliasFano {
    l: u32,
    low: Vec<u64>,
    // position 0 is a 0 that belongs to no number
    high: Vec<bool>,
    // one_samples[k - 1] = position of the 1 of number k * 256
    one_samples: Vec<usize>,
}

fn encode(values: &[u64]) -> EliasFano {
    let n = values.len() as u64;
    let u = values[values.len() - 1] + 1;
    let l = if u > n { (u / n).ilog2() } else { 0 };
    let mut high = vec![false; (n + (u >> l) + 2) as usize];
    let mut low = Vec::new();
    let mut one_samples = Vec::new();
    for (i, &x) in values.iter().enumerate() {
        // + 1 for the leading 0
        let pos = (x >> l) as usize + i + 1;
        high[pos] = true;
        low.push(x & ((1 << l) - 1));
        if i > 0 && i % ONES_STEP == 0 {
            one_samples.push(pos);
        }
    }
    EliasFano { l, low, high, one_samples }
}

/// Position of the 1 number `k` (from 0), counting from `from`.
fn skip_ones(bits: &[bool], from: usize, k: usize) -> usize {
    (from..bits.len()).filter(|&p| bits[p]).nth(k).unwrap()
}

/// The number at index i.
fn access(ef: &EliasFano, i: usize) -> u64 {
    let k = i / ONES_STEP;
    // jump: the 1 of number k * 256 is stored (k = 0: position 0)
    let start = if k == 0 { 0 } else { ef.one_samples[k - 1] };
    // walk: fewer than 256 more 1s to pass
    let pos = skip_ones(&ef.high, start, i - k * ONES_STEP);
    // the i earlier 1s and the leading 0 pushed it right
    let high = (pos - i - 1) as u64;
    (high << ef.l) | ef.low[i]
}

fn main() {
    // 0, 3, 6, ..., 29997: index 600 starts at the stored 1281,
    // walks 88 1s to 1501, and gives (900 << 1) | 0 = 1800
    let threes: Vec<u64> = (0..10_000).map(|i| 3 * i).collect();
    let ef = encode(&threes);
    assert_eq!(ef.l, 1);
    assert_eq!(ef.one_samples[1], 1281);
    assert_eq!(skip_ones(&ef.high, 1281, 88), 1501);
    assert_eq!(access(&ef, 600), 1800);

    // 10,000 sorted pseudo-random numbers, gaps of 0 to 127
    let mut x: u64 = 5;
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
    assert_eq!(ef.one_samples.len(), 10_000 / 256);
    for (i, &want) in values.iter().enumerate() {
        assert_eq!(access(&ef, i), want, "i = {i}");
    }
}
```
