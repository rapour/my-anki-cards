How do you answer **rank1(p)**, the number of 1s before position `p` in a large bit array, in constant time with little extra space?

---

Store one count every 512 bits, and count the rest with `count_ones`.

1. Split the bits into **blocks** of 512 bits, which is 8 words of 64 bits.
2. For every block, store how many 1s come before it. Call these stored counts `s[0], s[1], ...`.
3. To answer `rank1(p)`, add three things:
    - the stored count `s[p / 512]` for `p`'s block;
    - `count_ones` of each whole word in the block before `p`'s word (at most 7 words);
    - `count_ones` of `p`'s own word, masked to keep only the bits below `p`.

`count_ones` counts the 1s in a word with one CPU instruction (`popcnt` on x86), so every query does a fixed amount of work.

<div class="diagram">
<svg viewBox="0 0 640 236" width="100%" style="max-width:640px" role="img" aria-label="The bit array is split into blocks of 512 bits. Each block stores how many 1s come before it. Inside the block, whole words before p are counted with count_ones, then the part of p&#x27;s word below p.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}</style>
<rect x="20" y="46" width="138" height="40" rx="6" class="k"/>
<text x="89.0" y="62.5" text-anchor="middle">block 0</text>
<text x="89.0" y="78.5" text-anchor="middle" class="m">bits 0 to 511</text>
<text x="89.0" y="36" text-anchor="middle" class="m">stored: 1s before = s[0]</text>
<rect x="170" y="46" width="138" height="40" rx="6" class="k"/>
<text x="239.0" y="62.5" text-anchor="middle">block 1</text>
<text x="239.0" y="78.5" text-anchor="middle" class="m">bits 512 to 1023</text>
<text x="239.0" y="36" text-anchor="middle" class="m">stored: 1s before = s[1]</text>
<rect x="320" y="46" width="138" height="40" rx="6" class="r"/>
<text x="389.0" y="62.5" text-anchor="middle">block 2</text>
<text x="389.0" y="78.5" text-anchor="middle" class="m">bits 1024 to 1535</text>
<text x="389.0" y="36" text-anchor="middle" class="m">stored: 1s before = s[2]</text>
<rect x="470" y="46" width="138" height="40" rx="6" class="k"/>
<text x="539.0" y="62.5" text-anchor="middle">block 3</text>
<text x="539.0" y="78.5" text-anchor="middle" class="m">bits 1536 to 2047</text>
<text x="539.0" y="36" text-anchor="middle" class="m">stored: 1s before = s[3]</text>
<line x1="320" y1="86" x2="40" y2="150" class="ln"/>
<line x1="458" y1="86" x2="600" y2="150" class="ln"/>
<rect x="41" y="150" width="68" height="30" rx="2" class="cg"/>
<text x="75.0" y="196" text-anchor="middle" class="m">word 0</text>
<rect x="111" y="150" width="68" height="30" rx="2" class="cg"/>
<text x="145.0" y="196" text-anchor="middle" class="m">word 1</text>
<rect x="181" y="150" width="68" height="30" rx="2" class="cg"/>
<text x="215.0" y="196" text-anchor="middle" class="m">word 2</text>
<rect x="251" y="150" width="68" height="30" rx="2" class="cg"/>
<text x="285.0" y="196" text-anchor="middle" class="m">word 3</text>
<rect x="321" y="150" width="68" height="30" rx="2" class="cg"/>
<text x="355.0" y="196" text-anchor="middle" class="m">word 4</text>
<rect x="391" y="150" width="28" height="30" rx="2" class="cr"/>
<rect x="419" y="150" width="40" height="30" rx="2" class="c"/>
<text x="425.0" y="196" text-anchor="middle" class="m">word 5</text>
<rect x="461" y="150" width="68" height="30" rx="2" class="c"/>
<text x="495.0" y="196" text-anchor="middle" class="m">word 6</text>
<rect x="531" y="150" width="68" height="30" rx="2" class="c"/>
<text x="565.0" y="196" text-anchor="middle" class="m">word 7</text>
<line x1="419" y1="132" x2="419" y2="148" class="ln" marker-end="url(#ah)"/>
<text x="419" y="128" text-anchor="middle">p</text>
<text x="215.0" y="142" text-anchor="middle" class="m">count_ones of whole words</text>
<text x="320" y="224" text-anchor="middle" class="m">rank1(p) = s[2] + count_ones(words 0 to 4) + count_ones(word 5, bits below p)</text>
</svg>
</div>

The extra space is one count per 512 bits. With 32-bit counts that is 32 / 512, or 6.25% more space. The Rust search engine library rise-rs uses this layout (512-bit blocks) in its bitmap encoding of dense lists. It stores each count in `ceil(log2(n + 1))` bits, where `n` is the number of 1s.

```rust
// bits per block; one stored count per block
const BLOCK: usize = 512;

struct RankBits {
    // the bits, 64 per word
    words: Vec<u64>,
    // samples[b] = number of 1s before bit b * BLOCK
    samples: Vec<u64>,
}

impl RankBits {
    fn new(bits: &[bool]) -> Self {
        let mut words = vec![0u64; bits.len().div_ceil(64)];
        for (i, &b) in bits.iter().enumerate() {
            if b {
                words[i / 64] |= 1 << (i % 64);
            }
        }
        let mut samples = vec![0];
        let mut ones = 0;
        for (w, word) in words.iter().enumerate() {
            ones += word.count_ones() as u64;
            // the count at the start of the next block
            if (w + 1) % (BLOCK / 64) == 0 {
                samples.push(ones);
            }
        }
        RankBits { words, samples }
    }

    /// Number of 1s in positions 0 .. p.
    fn rank1(&self, p: usize) -> u64 {
        let block = p / BLOCK;
        // the 1s before the block are stored
        let mut ones = self.samples[block];
        // whole words from the start of the block up to p's word
        for w in block * (BLOCK / 64)..p / 64 {
            ones += self.words[w].count_ones() as u64;
        }
        // the bits of p's word that are below p
        if p % 64 != 0 {
            let mask = (1u64 << (p % 64)) - 1;
            ones += (self.words[p / 64] & mask).count_ones() as u64;
        }
        ones
    }
}

fn main() {
    // pseudo-random bits, about 3 in 8 are 1
    let mut x: u64 = 1;
    let bits: Vec<bool> = (0..5000)
        .map(|_| {
            x = x
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1_442_695_040_888_963_407);
            (x >> 61) < 3
        })
        .collect();

    // compare with a running count at every position
    let r = RankBits::new(&bits);
    let mut slow = 0;
    for p in 0..=bits.len() {
        assert_eq!(r.rank1(p), slow, "p = {p}");
        if p < bits.len() && bits[p] {
            slow += 1;
        }
    }
    // one count per 512 bits
    assert_eq!(r.samples.len(), 5000 / 512 + 1);
}
```
