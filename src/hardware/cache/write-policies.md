What does a CPU cache do on a **write**? Explain **write-through** and **write-back** (with the **dirty bit**), **write-allocate** and **no-write-allocate**, and say which combination ordinary memory uses on x86.

---

Two separate decisions, as the CMU course 15-213 lists them:

**1. On a write hit** (the line is in the cache):

- **write-through**: write to the cache **and** immediately to memory. Memory is always up to date, but every write costs memory traffic. Drepper: "A program which, for instance, modifies a local variable over and over again would create a lot of traffic on the FSB even though the data is likely not used anywhere else". (The FSB was the bus between the CPU and memory.)
- **write-back**: write only to the cache and set the line's **dirty bit**: "the line differs from memory". The line is written to memory once, when it is evicted. Drepper: "Write-back caches have the chance to be significantly better performing, which is why most memory in a system with a decent processor is cached this way."

<div class="diagram">
<svg viewBox="0 0 640 244" width="100%" style="max-width:640px" role="img" aria-label="Write-through sends every write to memory: 1000 writes for a counter incremented 1000 times. Write-back marks the line dirty and writes it to memory once, when it is evicted.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="160" y="22" text-anchor="middle" class="to">write-through</text>
<rect x="20" y="34" width="280" height="34" rx="6" class="k"/>
<text x="160.0" y="55.5" text-anchor="middle">CPU: counter += 1, 1000 times</text>
<rect x="20" y="96" width="280" height="40" rx="6" class="r"/>
<text x="160.0" y="112.5" text-anchor="middle">cache line</text>
<text x="160.0" y="128.5" text-anchor="middle" class="m">updated on every write</text>
<rect x="20" y="172" width="280" height="34" rx="6" class="k"/>
<text x="160.0" y="193.5" text-anchor="middle">memory</text>
<line x1="160" y1="70" x2="160" y2="94" class="pg" marker-end="url(#cgm)"/>
<text x="480" y="22" text-anchor="middle" class="tg">write-back</text>
<rect x="340" y="34" width="280" height="34" rx="6" class="k"/>
<text x="480.0" y="55.5" text-anchor="middle">CPU: counter += 1, 1000 times</text>
<rect x="340" y="96" width="280" height="40" rx="6" class="g"/>
<text x="480.0" y="112.5" text-anchor="middle">cache line, dirty bit set</text>
<text x="480.0" y="128.5" text-anchor="middle" class="m">updated on every write</text>
<rect x="340" y="172" width="280" height="34" rx="6" class="k"/>
<text x="480.0" y="193.5" text-anchor="middle">memory</text>
<line x1="480" y1="70" x2="480" y2="94" class="pg" marker-end="url(#cgm)"/>
<line x1="160" y1="138" x2="160" y2="170" class="po" marker-end="url(#co)"/>
<text x="170" y="158" text-anchor="start" class="to">1000 writes</text>
<path d="M480 138 V170" class="pg" marker-end="url(#cgm)"/>
<text x="490" y="158" text-anchor="start" class="tg">1 write, at eviction</text>
<text x="320" y="232" text-anchor="middle" class="m">write-allocate: a write miss first loads the line; no-write-allocate: the write goes straight to memory</text>
</svg>
</div>

**2. On a write miss** (the line is not in the cache):

- **write-allocate**: first load the line into the cache, then write into it. Good if more writes to the same line follow;
- **no-write-allocate**: send the write straight to memory and don't cache the line.

The usual pairs are write-back with write-allocate, and write-through with no-write-allocate. On x86, ordinary memory is **write-back with write-allocate**. Special memory types (write-through, write-combining, uncached), chosen by the OS for regions such as device memory, behave differently.

**A simulation in Rust** that counts the traffic between a 48 KiB cache and memory:

```rust
const LINE: u64 = 64;
const LINES: usize = 768; // 48 KiB, direct-mapped to keep it short

/// A cache that counts its traffic with memory.
struct Cache {
    slots: Vec<Option<(u64, bool)>>, // (line, dirty)
    write_back: bool,                // else write-through
    write_allocate: bool,            // else no-write-allocate
    line_reads: u32,                 // whole lines read from memory
    mem_writes: u32,                 // writes sent to memory
}

impl Cache {
    fn new(write_back: bool, write_allocate: bool) -> Cache {
        Cache {
            slots: vec![None; LINES],
            write_back,
            write_allocate,
            line_reads: 0,
            mem_writes: 0,
        }
    }

    fn slot(line: u64) -> usize {
        (line % LINES as u64) as usize
    }

    fn present(&self, line: u64) -> bool {
        let slot = self.slots[Self::slot(line)];
        matches!(slot, Some((l, _)) if l == line)
    }

    /// Bring a line in, writing back the dirty line it replaces.
    fn fill(&mut self, line: u64) {
        if let Some((_, true)) = self.slots[Self::slot(line)] {
            self.mem_writes += 1;
        }
        self.line_reads += 1;
        self.slots[Self::slot(line)] = Some((line, false));
    }

    fn read(&mut self, addr: u64) {
        if !self.present(addr / LINE) {
            self.fill(addr / LINE);
        }
    }

    fn write(&mut self, addr: u64) {
        let line = addr / LINE;
        if !self.present(line) {
            if !self.write_allocate {
                self.mem_writes += 1; // straight to memory
                return;
            }
            self.fill(line);
        }
        if self.write_back {
            self.slots[Self::slot(line)] = Some((line, true));
        } else {
            self.mem_writes += 1;
        }
    }

    /// Write back every dirty line, as an eviction eventually would.
    fn flush(&mut self) {
        for s in self.slots.iter_mut() {
            if let Some((l, true)) = *s {
                self.mem_writes += 1;
                *s = Some((l, false));
            }
        }
    }
}

/// A counter at one address, read and incremented 1000 times.
fn counter(c: &mut Cache) -> (u32, u32) {
    for _ in 0..1000 {
        c.read(0);
        c.write(0);
    }
    c.flush();
    (c.line_reads, c.mem_writes)
}

/// Fill 1 MiB with zeros, 8 bytes at a time, never reading it.
fn zero_fill(c: &mut Cache) -> (u32, u32) {
    for addr in (0..1 << 20).step_by(8) {
        c.write(addr);
    }
    c.flush();
    (c.line_reads, c.mem_writes)
}

fn main() {
    // write-back + write-allocate: what x86 does for normal memory
    assert_eq!(counter(&mut Cache::new(true, true)), (1, 1));
    // write-through + no-write-allocate: every write goes out
    assert_eq!(counter(&mut Cache::new(false, false)), (1, 1000));

    // zeroing 1 MiB: write-allocate first reads every line it is
    // about to overwrite completely: 16,384 reads for nothing
    assert_eq!(zero_fill(&mut Cache::new(true, true)), (16384, 16384));
    // no-write-allocate reads nothing, but sends 131,072 small writes
    assert_eq!(zero_fill(&mut Cache::new(false, false)), (0, 131072));
}
```

| Job | Policy | Lines read | Writes to memory |
|---|---|---|---|
| a counter incremented 1000 times | write-back + allocate | 1 | 1 |
|  | write-through, no allocate | 1 | 1000 |
| zero 1 MiB, 8 bytes at a time | write-back + allocate | 16,384 | 16,384 |
|  | write-through, no allocate | 0 | 131,072 |

The weak spot of write-allocate: when zeroing a buffer, it first **reads** every line it is about to overwrite completely. x86 has **non-temporal** ("streaming") store instructions for this case: they collect whole lines in write-combining buffers and send them to memory without reading them first or keeping them in the cache. In Rust they are available as, for example, `core::arch::x86_64::_mm_stream_si128`.
