What do **direct-mapped**, **set-associative** and **fully associative** mean for a cache, what does each trade off, and how can 1.5 KiB of data keep missing in a 48 KiB, 12-way L1 cache?

---

They say **how many places a given memory line may be stored in**:

| Organisation | A line may go in | Lookup compares |
|---|---|---|
| **direct-mapped** | exactly one slot | 1 tag |
| ***E*-way set-associative** | any of the *E* slots (*ways*) of one set | *E* tags at once |
| **fully associative** | any slot in the cache | every tag at once |

<div class="diagram">
<svg viewBox="0 0 640 244" width="100%" style="max-width:640px" role="img" aria-label="Three cache organisations of 8 slots. Direct-mapped: each memory line has exactly one slot. 2-way set associative: a line may go in either slot of one set. Fully associative: a line may go in any slot.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="110" y="22" text-anchor="middle">direct-mapped</text>
<rect x="80" y="36" width="38" height="20" rx="2" class="c"/>
<text x="72" y="50" text-anchor="end" class="m">set 0</text>
<rect x="80" y="58" width="38" height="20" rx="2" class="c"/>
<text x="72" y="72" text-anchor="end" class="m">set 1</text>
<rect x="80" y="80" width="38" height="20" rx="2" class="c"/>
<text x="72" y="94" text-anchor="end" class="m">set 2</text>
<rect x="80" y="102" width="38" height="20" rx="2" class="c"/>
<text x="72" y="116" text-anchor="end" class="m">set 3</text>
<rect x="80" y="124" width="38" height="20" rx="2" class="cg"/>
<text x="72" y="138" text-anchor="end" class="m">set 4</text>
<rect x="80" y="146" width="38" height="20" rx="2" class="c"/>
<text x="72" y="160" text-anchor="end" class="m">set 5</text>
<rect x="80" y="168" width="38" height="20" rx="2" class="c"/>
<text x="72" y="182" text-anchor="end" class="m">set 6</text>
<rect x="80" y="190" width="38" height="20" rx="2" class="c"/>
<text x="72" y="204" text-anchor="end" class="m">set 7</text>
<text x="110" y="230" text-anchor="middle" class="m">line 12 → slot 12 mod 8 = 4 only</text>
<text x="320" y="22" text-anchor="middle">2-way set associative</text>
<rect x="290" y="36" width="38" height="20" rx="2" class="cg"/>
<rect x="330" y="36" width="38" height="20" rx="2" class="cg"/>
<text x="282" y="50" text-anchor="end" class="m">set 0</text>
<rect x="290" y="58" width="38" height="20" rx="2" class="c"/>
<rect x="330" y="58" width="38" height="20" rx="2" class="c"/>
<text x="282" y="72" text-anchor="end" class="m">set 1</text>
<rect x="290" y="80" width="38" height="20" rx="2" class="c"/>
<rect x="330" y="80" width="38" height="20" rx="2" class="c"/>
<text x="282" y="94" text-anchor="end" class="m">set 2</text>
<rect x="290" y="102" width="38" height="20" rx="2" class="c"/>
<rect x="330" y="102" width="38" height="20" rx="2" class="c"/>
<text x="282" y="116" text-anchor="end" class="m">set 3</text>
<text x="320" y="230" text-anchor="middle" class="m">line 12 → set 12 mod 4 = 0: 2 slots</text>
<text x="530" y="22" text-anchor="middle">fully associative</text>
<rect x="450" y="96" width="18" height="20" rx="2" class="cg"/>
<rect x="470" y="96" width="18" height="20" rx="2" class="cg"/>
<rect x="490" y="96" width="18" height="20" rx="2" class="cg"/>
<rect x="510" y="96" width="18" height="20" rx="2" class="cg"/>
<rect x="530" y="96" width="18" height="20" rx="2" class="cg"/>
<rect x="550" y="96" width="18" height="20" rx="2" class="cg"/>
<rect x="570" y="96" width="18" height="20" rx="2" class="cg"/>
<rect x="590" y="96" width="18" height="20" rx="2" class="cg"/>
<text x="530" y="230" text-anchor="middle" class="m">line 12 → any of the 8 slots</text>
<text x="320" y="210" text-anchor="middle" class="tg">a cache of 8 slots, three ways to organise it</text>
</svg>
</div>

**The trade-off.** More places means fewer *conflict misses*: a line evicted because its few allowed slots are full while the rest of the cache has room. But each lookup compares more tags in parallel, which costs circuitry, power and time. Drepper: "Fully associative caches are practical for small caches (for instance, the TLB caches on some Intel processors are fully associative)". The caches on this machine are set-associative, with 8 to 20 ways.

A classic direct-mapped failure: two arrays exactly one cache size apart, read in step (`x[i]`, `y[i]`, `x[i+1]`, …). `x[i]` and `y[i]` need the same single slot, so every read evicts the other array's line, and every read misses.

**Replacement.** When the chosen set is full, one of its lines must go. Drepper: "Most caches evict the Least Recently Used (LRU) element first. … With larger associativity … maintaining the LRU list becomes more and more expensive". Hardware with many ways uses cheaper approximations of LRU.

**Measured on this machine.** The L1d has 64 sets of 12 ways with 64-byte lines. The set index is bits 6 to 11 of the address, so addresses exactly 4096 bytes apart all land in **one** set. The program follows a chain of loads through `n` such addresses, each load needing the previous one. The order is scrambled so the hardware prefetcher can't guess the next address.

```rust
use std::time::Instant;

/// Average time of a load that needs the previous one, visiting
/// `n` addresses `stride` bytes apart, over and over, in a
/// scrambled order (so the stride prefetcher can't help).
fn ns_per_load(n: usize, stride: usize) -> f64 {
    let step = stride / 8; // in u64s
    let mut buf = vec![0u64; n * step];
    // visit slot 0, 7, 14, ... (mod n): one cycle when n % 7 != 0
    let order: Vec<usize> = (0..n).map(|i| i * 7 % n).collect();
    for k in 0..n {
        buf[order[k] * step] = (order[(k + 1) % n] * step) as u64;
    }
    let rounds = 20_000_000;
    let mut at = 0;
    let start = Instant::now();
    for _ in 0..rounds {
        at = buf[at] as usize;
    }
    std::hint::black_box(at);
    start.elapsed().as_nanos() as f64 / rounds as f64
}

fn main() {
    // this machine's L1d: 64 sets of 12 ways, 64-byte lines, so
    // addresses 4096 bytes apart all land in the same set
    for n in [8, 24] {
        let same_set = ns_per_load(n, 4096);
        let spread = ns_per_load(n, 4096 + 64); // a set each
        println!(
            "{n:>2} lines ({} bytes): 4096 apart {same_set:.1} ns, \
             4160 apart {spread:.1} ns",
            n * 64
        );
    }
}
```

```text
 8 lines (512 bytes): 4096 apart 2.2 ns, 4160 apart 2.0 ns
24 lines (1536 bytes): 4096 apart 5.7 ns, 4160 apart 1.8 ns
```

- 8 lines fit in the set's 12 ways: every load hits L1, about 2 ns.
- 24 lines 4096 apart compete for 12 ways, so they keep evicting each other and each load goes to the L2: 5.7 ns. Only 1.5 KiB of data, in a 48 KiB cache.
- 4160 bytes apart, each line gets a different set and everything fits again.

**Lesson:** beware power-of-two strides over large data, such as walking down a column of a matrix whose rows are 4096 bytes long. Padding each row by one line spreads the column over all the sets.
