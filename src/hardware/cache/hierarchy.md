What caches does a typical x86-64 CPU core have, which of them are private to a core and which are shared, how big and how fast is each level, and what do **inclusive** and **exclusive** mean for a cache hierarchy?

---

From the core outwards, each level bigger and slower than the one before:

| Level | Here | Private or shared | Holds |
|---|---|---|---|
| L1d | 48 KiB, 12-way | one per core | data |
| L1i | 32 KiB, 8-way | one per core | instructions |
| L2 | 2 MiB, 16-way | one per core | both (*unified*) |
| L3 | 260 MiB, 20-way | shared by all cores | both |
| RAM | about 16 GiB | shared | everything |

The L1 is split in two so that fetching instructions and loading data don't compete for the same cache in the same cycle. Every level here uses 64-byte lines.

<div class="diagram">
<svg viewBox="0 0 640 302" width="100%" style="max-width:640px" role="img" aria-label="Each core has its own L1 data and instruction caches and its own L2; all cores share the L3; then RAM. Measured load times: L1d 2.9 ns, L2 6.7 ns, L3 39.7 ns, RAM 142.4 ns.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<rect x="20" y="20" width="290" height="132" rx="8" class="dsh"/>
<text x="165" y="36" text-anchor="middle" class="m">core 0</text>
<rect x="32" y="44" width="125" height="40" rx="6" class="g"/>
<text x="94.5" y="60.5" text-anchor="middle">L1d 48 KiB</text>
<text x="94.5" y="76.5" text-anchor="middle" class="m">2.9 ns</text>
<rect x="173" y="44" width="125" height="40" rx="6" class="k"/>
<text x="235.5" y="60.5" text-anchor="middle">L1i 32 KiB</text>
<text x="235.5" y="76.5" text-anchor="middle" class="m">instructions</text>
<rect x="32" y="100" width="266" height="40" rx="6" class="k"/>
<text x="165.0" y="116.5" text-anchor="middle">L2 2 MiB</text>
<text x="165.0" y="132.5" text-anchor="middle" class="m">6.7 ns</text>
<rect x="330" y="20" width="290" height="132" rx="8" class="dsh"/>
<text x="475" y="36" text-anchor="middle" class="m">core 3</text>
<rect x="342" y="44" width="125" height="40" rx="6" class="g"/>
<text x="404.5" y="60.5" text-anchor="middle">L1d 48 KiB</text>
<text x="404.5" y="76.5" text-anchor="middle" class="m">2.9 ns</text>
<rect x="483" y="44" width="125" height="40" rx="6" class="k"/>
<text x="545.5" y="60.5" text-anchor="middle">L1i 32 KiB</text>
<text x="545.5" y="76.5" text-anchor="middle" class="m">instructions</text>
<rect x="342" y="100" width="266" height="40" rx="6" class="k"/>
<text x="475.0" y="116.5" text-anchor="middle">L2 2 MiB</text>
<text x="475.0" y="132.5" text-anchor="middle" class="m">6.7 ns</text>
<text x="320" y="90" text-anchor="middle">…</text>
<rect x="20" y="172" width="600" height="40" rx="6" class="k"/>
<text x="320.0" y="188.5" text-anchor="middle">L3 260 MiB, shared by all cores</text>
<text x="320.0" y="204.5" text-anchor="middle" class="m">39.7 ns</text>
<rect x="20" y="232" width="600" height="40" rx="6" class="r"/>
<text x="320.0" y="248.5" text-anchor="middle">RAM</text>
<text x="320.0" y="264.5" text-anchor="middle" class="m">142.4 ns</text>
<line x1="165" y1="154" x2="165" y2="170" class="pg" marker-end="url(#cgm)"/>
<line x1="475" y1="154" x2="475" y2="170" class="pg" marker-end="url(#cgm)"/>
<line x1="320" y1="214" x2="320" y2="230" class="pg" marker-end="url(#cgm)"/>
<text x="320" y="292" text-anchor="middle" class="m">measured: one load that depends on the previous one, working set sized for each level</text>
</svg>
</div>

```sh
$ cat /sys/devices/system/cpu/cpu0/cache/index3/shared_cpu_list
0-3
```

The L3 (`index3`) is shared by CPUs 0 to 3, all four cores of this machine. The same file for `index0` (the L1d) says `0`: that core only.

**How fast?** The program builds a chain of 64-byte lines in random order and follows it. Each load needs the address from the previous one, so loads can't overlap, and the random order defeats the prefetcher. The working set is sized to fit in one level:

```rust
use std::time::Instant;

/// One 64-byte cache line holding the index of the next line.
#[repr(align(64))]
#[derive(Clone, Copy)]
struct Line {
    next: usize,
}

/// `n` lines linked into one cycle in a random order (Sattolo's
/// algorithm), so the hardware prefetcher can't guess what's next.
fn random_cycle(n: usize) -> Vec<Line> {
    let mut order: Vec<usize> = (0..n).collect();
    let mut s = 0x9e37_79b9_7f4a_7c15u64; // xorshift random numbers
    for i in (1..n).rev() {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        order.swap(i, (s % i as u64) as usize); // j < i: one cycle
    }
    let mut v = vec![Line { next: 0 }; n];
    for k in 0..n {
        v[order[k]].next = order[(k + 1) % n];
    }
    v
}

/// Nanoseconds per load when each load needs the previous result.
fn ns_per_load(v: &[Line]) -> f64 {
    let steps = 10_000_000;
    let mut i = 0;
    for _ in 0..v.len() {
        i = v[i].next; // first pass: bring what fits into the caches
    }
    let start = Instant::now();
    for _ in 0..steps {
        i = v[i].next;
    }
    std::hint::black_box(i);
    start.elapsed().as_nanos() as f64 / steps as f64
}

fn main() {
    // the chain really is one cycle through every line
    let v = random_cycle(1000);
    let (mut i, mut steps) = (v[0].next, 1);
    while i != 0 {
        i = v[i].next;
        steps += 1;
    }
    assert_eq!(steps, 1000);

    // working sets that fit in L1d (48 KiB), L2 (2 MiB), L3, none
    for (kib, level) in
        [(32, "L1d"), (512, "L2"), (4096, "L3"), (262144, "RAM")]
    {
        let ns = ns_per_load(&random_cycle(kib * 1024 / 64));
        println!("{kib:>6} KiB  {level:<3}  {ns:5.1} ns per load");
    }
}
```

One run, on a 2.1 GHz cloud virtual machine:

```text
    32 KiB  L1d    2.9 ns per load
   512 KiB  L2     6.7 ns per load
  4096 KiB  L3    39.7 ns per load
262144 KiB  RAM  142.4 ns per load
```

At the nominal 2.1 GHz that is roughly 6, 14, 83 and 300 cycles. Each step out costs several times more, so the level a working set fits in matters more than almost anything else. (On a VM the L3 is shared with other tenants, and at 256 MiB the TLB misses too, which adds to the RAM figure.)

**Inclusive or exclusive:**

- **inclusive**: every line in a smaller level is also in the larger one. Drepper: "each cache line in L1d is also present in L2. Therefore evicting from L1d is much faster". The cost is space: the same line is stored twice.
- **exclusive**: a line is in only one level at a time. More total capacity; a line evicted from L1 moves down to L2. Drepper describes this model as the one "used by AMD and VIA processors".

Some designs are neither strictly inclusive nor exclusive.
