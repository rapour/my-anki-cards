What does a CPU's **hardware prefetcher** do, which access patterns can it help with and which can't it, and how big is the difference? Show it with a measurement.

---

A **hardware prefetcher** watches the addresses a core misses on, spots a pattern, and loads the lines it predicts will be needed **before** the program asks for them. When the prediction is right, the load finds its line already in the cache, or on its way.

**Patterns it can predict:**

- sequential access: line after line, forwards or backwards;
- constant strides: every *k*-th line, as in walking down a column of a matrix.

**Patterns it can't:**

- following pointers to scattered addresses: linked lists, trees, graphs;
- random lookups, as in a hash table.

Drepper also notes a limit: hardware prefetching "cannot cross page boundaries", because the next page might not be mapped.

<div class="diagram">
<svg viewBox="0 0 640 204" width="100%" style="max-width:640px" role="img" aria-label="Reading lines in address order, the hardware prefetcher fetches the next lines before they are asked for: 15 ns per line. In a shuffled order it cannot predict anything: 144 ns per line.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="128" y="70" text-anchor="end">in address order</text>
<rect x="140" y="54" width="40" height="26" rx="2" class="c"/>
<text x="160.0" y="72" text-anchor="middle" class="m">0</text>
<rect x="186" y="54" width="40" height="26" rx="2" class="c"/>
<text x="206.0" y="72" text-anchor="middle" class="m">1</text>
<rect x="232" y="54" width="40" height="26" rx="2" class="cg"/>
<text x="252.0" y="72" text-anchor="middle" class="m">2</text>
<rect x="278" y="54" width="40" height="26" rx="2" class="cg"/>
<text x="298.0" y="72" text-anchor="middle" class="m">3</text>
<rect x="324" y="54" width="40" height="26" rx="2" class="cg"/>
<text x="344.0" y="72" text-anchor="middle" class="m">4</text>
<rect x="370" y="54" width="40" height="26" rx="2" class="cg"/>
<text x="390.0" y="72" text-anchor="middle" class="m">5</text>
<rect x="416" y="54" width="40" height="26" rx="2" class="cg"/>
<text x="436.0" y="72" text-anchor="middle" class="m">6</text>
<rect x="462" y="54" width="40" height="26" rx="2" class="cg"/>
<text x="482.0" y="72" text-anchor="middle" class="m">7</text>
<rect x="508" y="54" width="40" height="26" rx="2" class="cg"/>
<text x="528.0" y="72" text-anchor="middle" class="m">8</text>
<rect x="554" y="54" width="40" height="26" rx="2" class="cg"/>
<text x="574.0" y="72" text-anchor="middle" class="m">9</text>
<text x="183" y="100" text-anchor="middle" class="m">read</text>
<path d="M232 48 C 324 26, 416 26, 508 46" class="pg" marker-end="url(#cgm)"/>
<text x="370" y="18" text-anchor="middle" class="tg">the prefetcher spots the pattern and fetches ahead</text>
<text x="416" y="100" text-anchor="middle" class="tg">lines already on their way: 15 ns per line</text>
<text x="128" y="156" text-anchor="end">shuffled</text>
<rect x="140" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="160.0" y="158" text-anchor="middle" class="m">0</text>
<rect x="186" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="206.0" y="158" text-anchor="middle" class="m">1</text>
<rect x="232" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="252.0" y="158" text-anchor="middle" class="m">2</text>
<rect x="278" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="298.0" y="158" text-anchor="middle" class="m">3</text>
<rect x="324" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="344.0" y="158" text-anchor="middle" class="m">4</text>
<rect x="370" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="390.0" y="158" text-anchor="middle" class="m">5</text>
<rect x="416" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="436.0" y="158" text-anchor="middle" class="m">6</text>
<rect x="462" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="482.0" y="158" text-anchor="middle" class="m">7</text>
<rect x="508" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="528.0" y="158" text-anchor="middle" class="m">8</text>
<rect x="554" y="140" width="40" height="26" rx="2" class="cr"/>
<text x="574.0" y="158" text-anchor="middle" class="m">9</text>
<path d="M160 138 Q 321.0 103 482 138" class="po" marker-end="url(#co)"/>
<path d="M482 138 Q 390.0 112 298 138" class="po" marker-end="url(#co)"/>
<path d="M298 138 Q 436.0 106 574 138" class="po" marker-end="url(#co)"/>
<path d="M574 138 Q 390.0 100 206 138" class="po" marker-end="url(#co)"/>
<text x="370" y="192" text-anchor="middle" class="to">nothing to predict: each line is a full trip to RAM, 144 ns</text>
</svg>
</div>

**A measurement in Rust.** 256 MiB of 64-byte lines, far bigger than the caches, linked into one chain. Each load needs the result of the previous one, so the CPU can't overlap the loads by itself. The two runs touch exactly the same lines, the same number of times; only the order differs:

```rust
use std::time::Instant;

/// One 64-byte cache line holding the index of the next line.
#[repr(align(64))]
#[derive(Clone, Copy)]
struct Line {
    next: usize,
}

/// Link `n` lines into one cycle: in address order, or shuffled.
fn cycle(n: usize, shuffled: bool) -> Vec<Line> {
    let mut order: Vec<usize> = (0..n).collect();
    let mut s = 0x9e37_79b9_7f4a_7c15u64; // xorshift random numbers
    for i in (1..n).rev().filter(|_| shuffled) {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        order.swap(i, (s % i as u64) as usize);
    }
    let mut v = vec![Line { next: 0 }; n];
    for k in 0..n {
        v[order[k]].next = order[(k + 1) % n];
    }
    v
}

/// Follow the chain once around; nanoseconds per line. Each load
/// needs the one before, so only prefetching can get ahead.
fn ns_per_line(v: &[Line]) -> f64 {
    let start = Instant::now();
    let mut i = 0;
    for _ in 0..v.len() {
        i = v[i].next;
    }
    assert_eq!(i, 0, "one full cycle ends where it started");
    start.elapsed().as_nanos() as f64 / v.len() as f64
}

fn main() {
    let n = (256 << 20) / 64; // 256 MiB: far bigger than the caches
    let in_order = ns_per_line(&cycle(n, false));
    let shuffled = ns_per_line(&cycle(n, true));
    println!("in address order: {in_order:6.1} ns per line");
    println!("shuffled:         {shuffled:6.1} ns per line");
}
```

One run:

```text
in address order:   15.4 ns per line
shuffled:          144.3 ns per line
```

In address order the prefetcher fetches ahead, so most loads find their line already arriving: about 9 times faster. Shuffled, every load is a full trip to RAM.

**When software must help.** If the program knows the next address but the hardware can't guess it, it can ask for the line early with a prefetch instruction, a hint that never faults. In Rust: `core::arch::x86_64::_mm_prefetch`. Lookups in a hash table, where the keys are known a few steps ahead, are a typical case.
