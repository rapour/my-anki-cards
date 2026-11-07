What is **false sharing**, why does it slow down threads that never touch the same variable, and how do you fix it in Rust? Show it with a measurement.

---

**False sharing** happens when threads on different cores write **different** variables that sit in the **same cache line**. The cache keeps whole 64-byte lines consistent, not single variables. A core may only write a line once every other core's copy is invalidated (in the MESI protocol, a *read for ownership*). So the line travels from core to core on nearly every write, as if the threads were really sharing data.

<div class="diagram">
<svg viewBox="0 0 640 218" width="100%" style="max-width:640px" role="img" aria-label="False sharing: four counters in one cache line make every write move the line between cores, 1650 ms for 4 threads. Each counter on its own line: 354 ms.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="160" y="22" text-anchor="middle" class="to">one line, four counters</text>
<text x="480" y="22" text-anchor="middle" class="tg">one line per counter</text>
<rect x="20" y="36" width="64" height="34" rx="6" class="k"/>
<text x="52.0" y="57.5" text-anchor="middle">core 0</text>
<rect x="92" y="36" width="64" height="34" rx="6" class="k"/>
<text x="124.0" y="57.5" text-anchor="middle">core 1</text>
<rect x="164" y="36" width="64" height="34" rx="6" class="k"/>
<text x="196.0" y="57.5" text-anchor="middle">core 2</text>
<rect x="236" y="36" width="64" height="34" rx="6" class="k"/>
<text x="268.0" y="57.5" text-anchor="middle">core 3</text>
<rect x="40" y="120" width="58" height="30" rx="2" class="cr"/>
<text x="69" y="140" text-anchor="middle">a</text>
<rect x="100" y="120" width="58" height="30" rx="2" class="cr"/>
<text x="129" y="140" text-anchor="middle">b</text>
<rect x="160" y="120" width="58" height="30" rx="2" class="cr"/>
<text x="189" y="140" text-anchor="middle">c</text>
<rect x="220" y="120" width="58" height="30" rx="2" class="cr"/>
<text x="249" y="140" text-anchor="middle">d</text>
<text x="160" y="168" text-anchor="middle" class="m">one 64-byte line</text>
<line x1="52" y1="72" x2="69" y2="118" class="po" marker-end="url(#co)"/>
<line x1="124" y1="72" x2="129" y2="118" class="po" marker-end="url(#co)"/>
<line x1="196" y1="72" x2="189" y2="118" class="po" marker-end="url(#co)"/>
<line x1="268" y1="72" x2="249" y2="118" class="po" marker-end="url(#co)"/>
<text x="160" y="190" text-anchor="middle" class="to">each write steals the line from the other cores</text>
<text x="160" y="206" text-anchor="middle" class="to">4 threads: 1650 ms</text>
<rect x="340" y="36" width="64" height="34" rx="6" class="k"/>
<text x="372.0" y="57.5" text-anchor="middle">core 0</text>
<rect x="340" y="120" width="64" height="30" rx="2" class="cg"/>
<text x="372" y="140" text-anchor="middle">a</text>
<line x1="372" y1="72" x2="372" y2="118" class="pg" marker-end="url(#cgm)"/>
<rect x="412" y="36" width="64" height="34" rx="6" class="k"/>
<text x="444.0" y="57.5" text-anchor="middle">core 1</text>
<rect x="412" y="120" width="64" height="30" rx="2" class="cg"/>
<text x="444" y="140" text-anchor="middle">b</text>
<line x1="444" y1="72" x2="444" y2="118" class="pg" marker-end="url(#cgm)"/>
<rect x="484" y="36" width="64" height="34" rx="6" class="k"/>
<text x="516.0" y="57.5" text-anchor="middle">core 2</text>
<rect x="484" y="120" width="64" height="30" rx="2" class="cg"/>
<text x="516" y="140" text-anchor="middle">c</text>
<line x1="516" y1="72" x2="516" y2="118" class="pg" marker-end="url(#cgm)"/>
<rect x="556" y="36" width="64" height="34" rx="6" class="k"/>
<text x="588.0" y="57.5" text-anchor="middle">core 3</text>
<rect x="556" y="120" width="64" height="30" rx="2" class="cg"/>
<text x="588" y="140" text-anchor="middle">d</text>
<line x1="588" y1="72" x2="588" y2="118" class="pg" marker-end="url(#cgm)"/>
<text x="480" y="168" text-anchor="middle" class="m">four 64-byte lines</text>
<text x="480" y="190" text-anchor="middle" class="tg">each core keeps its own line</text>
<text x="480" y="206" text-anchor="middle" class="tg">4 threads: 354 ms</text>
</svg>
</div>

**A measurement in Rust**, like the experiment in Drepper's *What Every Programmer Should Know About Memory*: each thread adds 1 to its **own** counter 20 million times. Then the same again, with each counter padded onto its own line:

```rust
use std::sync::atomic::{AtomicU64, Ordering::Relaxed};
use std::thread;
use std::time::{Duration, Instant};

const ADDS: u64 = 20_000_000;

/// Four counters packed into one 64-byte cache line.
#[repr(align(64))]
struct OneLine([AtomicU64; 4]);

/// A counter alone on its own 64-byte cache line.
#[repr(align(64))]
#[derive(Default)]
struct Padded(AtomicU64);

/// One thread per counter, each adding 1 to its own counter.
fn race(counters: &[&AtomicU64]) -> Duration {
    let start = Instant::now();
    thread::scope(|s| {
        for &c in counters {
            s.spawn(move || {
                for _ in 0..ADDS {
                    c.fetch_add(1, Relaxed);
                }
            });
        }
    });
    start.elapsed()
}

fn main() {
    let packed = OneLine(Default::default());
    let padded: [Padded; 4] = Default::default();
    // the packed counters really share one line
    let first = &packed.0[0] as *const _ as usize;
    assert_eq!(first % 64, 0);

    for n in [1, 2, 4] {
        let same: Vec<_> = packed.0[..n].iter().collect();
        let own: Vec<_> = padded[..n].iter().map(|p| &p.0).collect();
        let (a, b) = (race(&same).as_millis(), race(&own).as_millis());
        println!(
            "{n} threads: one line {a:>4} ms, own lines {b:>4} ms"
        );
    }
    // no update was lost in either layout: counter 0 ran 3 times,
    // counter 1 twice, counters 2 and 3 once
    for (k, runs) in [3, 2, 1, 1].into_iter().enumerate() {
        assert_eq!(packed.0[k].load(Relaxed), runs * ADDS);
        assert_eq!(padded[k].0.load(Relaxed), runs * ADDS);
    }
}
```

One run, on 4 cores:

```text
1 threads: one line  137 ms, own lines  137 ms
2 threads: one line  475 ms, own lines  172 ms
4 threads: one line 1650 ms, own lines  354 ms
```

- 1 thread: no difference. Nobody else wants the line.
- 4 threads: almost 5 times slower when the counters share a line, for exactly the same work and results.

**The fix:** give each thread's hot data its own line.

- `#[repr(align(64))]` on a wrapper type makes every value start on a new line and fill it.
- The crossbeam crate's `CachePadded<T>` does the same, with the right size for each CPU family.
- Better still, let each thread work on its own local variable and write the shared result once at the end.

**Watch for it** in arrays of per-thread counters, statistics structs, and work queues whose head and tail indexes are written by different threads.

Padding fixes only *false* sharing. If threads really do write the same variable, they still pass its line around; only a different design, such as one counter per thread added up at the end, removes that cost.
