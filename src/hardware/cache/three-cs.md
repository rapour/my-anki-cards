Cache misses are classified as **compulsory**, **capacity** and **conflict** misses: the "three Cs". What does each mean, how can you tell which kind a miss is, and what cures each kind?

---

Definitions, from the CMU course *Introduction to Computer Systems* (15-213):

- **Compulsory** (cold) miss: "Cold misses occur because the cache is empty." It is the first access to the line, so no cache could have had it.
- **Capacity** miss: "Occurs when the set of active cache blocks (working set) is larger than the cache."
- **Conflict** miss: "Conflict misses occur when the level k cache is large enough, but multiple data objects all map to the same level k block." The data would fit, but too much of it falls in the same set.

**How to tell them apart** (Mark Hill's method): replay the same accesses through an imaginary *fully associative* cache of the same size, where any line can go anywhere, so there are no conflicts.

<div class="diagram">
<svg viewBox="0 0 640 246" width="100%" style="max-width:640px" role="img" aria-label="Classifying a miss: if the line was never accessed before, it is a compulsory miss. Otherwise, if a fully associative cache of the same size would also miss, it is a capacity miss; if not, it is a conflict miss.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<rect x="20" y="70" width="110" height="40" rx="6" class="r"/>
<text x="75.0" y="94.5" text-anchor="middle">a miss</text>
<line x1="132" y1="90" x2="168" y2="90" class="pg" marker-end="url(#cgm)"/>
<rect x="170" y="66" width="200" height="48" rx="6" class="k"/>
<text x="270.0" y="86.5" text-anchor="middle">first access to this</text>
<text x="270.0" y="102.5" text-anchor="middle" class="m">line since the start?</text>
<line x1="372" y1="90" x2="448" y2="50" class="pg" marker-end="url(#cgm)"/>
<text x="400" y="58" text-anchor="middle" class="m">yes</text>
<rect x="450" y="26" width="170" height="44" rx="6" class="g"/>
<text x="535.0" y="44.5" text-anchor="middle">compulsory (cold)</text>
<text x="535.0" y="60.5" text-anchor="middle" class="m">no cache could have it</text>
<line x1="270" y1="116" x2="270" y2="150" class="pg" marker-end="url(#cgm)"/>
<text x="282" y="136" text-anchor="start" class="m">no</text>
<rect x="150" y="152" width="240" height="48" rx="6" class="k"/>
<text x="270.0" y="172.5" text-anchor="middle">would a fully associative cache</text>
<text x="270.0" y="188.5" text-anchor="middle" class="m">of the same size miss too?</text>
<line x1="392" y1="168" x2="448" y2="130" class="pg" marker-end="url(#cgm)"/>
<text x="418" y="140" text-anchor="middle" class="m">yes</text>
<rect x="450" y="108" width="170" height="44" rx="6" class="g"/>
<text x="535.0" y="126.5" text-anchor="middle">capacity</text>
<text x="535.0" y="142.5" text-anchor="middle" class="m">the working set is too big</text>
<line x1="392" y1="186" x2="448" y2="210" class="pg" marker-end="url(#cgm)"/>
<text x="418" y="212" text-anchor="middle" class="m">no</text>
<rect x="450" y="190" width="170" height="44" rx="6" class="g"/>
<text x="535.0" y="208.5" text-anchor="middle">conflict</text>
<text x="535.0" y="224.5" text-anchor="middle" class="m">too many lines in one set</text>
</svg>
</div>

**A simulation in Rust** of a 48 KiB, 12-way cache with 64 sets and LRU replacement, the shape of this machine's L1d, next to a fully associative cache of the same size:

```rust
use std::collections::{HashSet, VecDeque};

const LINE: u64 = 64;

/// A cache with `sets` sets of `ways` lines, evicting the least
/// recently used line of the set.
struct Cache {
    sets: Vec<VecDeque<u64>>, // per set: lines, least recent first
    ways: usize,
}

impl Cache {
    fn new(sets: usize, ways: usize) -> Cache {
        Cache { sets: vec![VecDeque::new(); sets], ways }
    }

    /// Look up an address; true on a hit.
    fn access(&mut self, addr: u64) -> bool {
        let line = addr / LINE;
        let n = self.sets.len() as u64;
        let set = &mut self.sets[(line % n) as usize];
        let hit = match set.iter().position(|&l| l == line) {
            Some(i) => {
                set.remove(i);
                true
            }
            None => {
                if set.len() == self.ways {
                    set.pop_front(); // evict the least recently used
                }
                false
            }
        };
        set.push_back(line); // now the most recently used
        hit
    }
}

/// Count (compulsory, capacity, conflict) misses of a 48 KiB,
/// 12-way cache, like this machine's L1d.
fn three_cs(trace: &[u64]) -> (usize, usize, usize) {
    let mut real = Cache::new(64, 12);
    // the same size, but any line may go anywhere
    let mut full = Cache::new(1, 64 * 12);
    let mut seen = HashSet::new();
    let (mut compulsory, mut capacity, mut conflict) = (0, 0, 0);
    for &addr in trace {
        let first_time = seen.insert(addr / LINE);
        let full_hit = full.access(addr);
        if real.access(addr) {
            continue;
        }
        if first_time {
            compulsory += 1; // no cache could have had it
        } else if !full_hit {
            capacity += 1; // even a fully associative cache missed
        } else {
            conflict += 1; // only the restriction to one set missed
        }
    }
    (compulsory, capacity, conflict)
}

/// Read `bytes` from address 0, one access per line, `times` times.
fn sweep(bytes: u64, times: usize) -> Vec<u64> {
    let once: Vec<u64> = (0..bytes).step_by(LINE as usize).collect();
    once.repeat(times)
}

/// Visit `n` lines 4096 bytes apart, `times` times.
fn same_set(n: u64, times: usize) -> Vec<u64> {
    let once: Vec<u64> = (0..n).map(|i| i * 4096).collect();
    once.repeat(times)
}

fn main() {
    // 48 KiB twice: fits exactly, so only the first pass misses
    assert_eq!(three_cs(&sweep(48 << 10, 2)), (768, 0, 0));
    // 64 KiB twice: too big, the second pass misses throughout
    assert_eq!(three_cs(&sweep(64 << 10, 2)), (1024, 1024, 0));
    // 13 lines (832 bytes) that all fall in one 12-way set
    assert_eq!(three_cs(&same_set(13, 100)), (13, 0, 1287));
    // 12 of them fit in the set's 12 ways
    assert_eq!(three_cs(&same_set(12, 100)), (12, 0, 0));
}
```

| Accesses | Compulsory | Capacity | Conflict |
|---|---|---|---|
| read 48 KiB twice | 768 | 0 | 0 |
| read 64 KiB twice | 1,024 | 1,024 | 0 |
| 13 lines 4096 bytes apart, 100 times | 13 | 0 | 1,287 |
| 12 lines 4096 bytes apart, 100 times | 12 | 0 | 0 |

- 48 KiB is exactly the cache size, so only the first touch of each of its 768 lines misses.
- 64 KiB is too big: with LRU, a repeated scan evicts each line just before it is needed again, so the whole second pass misses.
- 13 lines are only 832 bytes, but addresses 4096 apart share one set of 12 ways. The 13th line always pushes one out.

**Cures:**

| Kind | Cure |
|---|---|
| compulsory | can't be avoided, only hidden: prefetching, and using every byte of each line fetched |
| capacity | a smaller working set: process data in blocks that fit (*tiling*), use more compact data types |
| conflict | change the addresses: avoid power-of-two strides, pad arrays; or a more associative cache |

On a multicore CPU there is a fourth C: **coherence** misses, when another core's write has invalidated this core's copy of the line.
