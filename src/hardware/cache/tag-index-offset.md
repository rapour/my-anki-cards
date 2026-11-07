How does a set-associative cache find a line? Split a physical address into **tag**, **set index** and **offset** for a cache of *S* sets, *E* ways and *B*-byte lines, and work it through for a real L1 data cache.

---

**The shape of a cache** (in the notation of Bryant and O'Hallaron's *Computer Systems: A Programmer's Perspective*):

- *B* bytes per line;
- *S* **sets**: groups of slots;
- *E* **ways**: slots per set. Each holds one line, its tag and a valid bit;
- size *C* = *S* × *E* × *B*.

A memory line may only go in **one** set, chosen by its address, but in any way of that set.

**Splitting the address**, lowest bits first:

| Part | Bits | What it does |
|---|---|---|
| offset | log₂ *B* | which byte inside the line |
| set index | log₂ *S* | which set to look in |
| tag | the rest | which line, among all the lines that share this set |

**A lookup:**

1. the set index picks one set;
2. the tag is compared with the tags of all *E* lines in that set at once, among the lines with the valid bit set;
3. hit: the offset picks the bytes. Miss: the line is fetched from the next level, and one line of the set is evicted to make room.

<div class="diagram">
<svg viewBox="0 0 640 262" width="100%" style="max-width:640px" role="img" aria-label="A physical address splits into a tag, a set index and an offset. The set index picks one of 64 sets; the tag is compared with the 12 tags in that set; the offset picks the byte in the line.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="20" y="20" text-anchor="start">physical address 0x1a2b3678 in this machine&#x27;s L1d (64 sets × 12 ways × 64 B)</text>
<rect x="40" y="30" width="300" height="40" rx="6" class="k"/>
<text x="190.0" y="46.5" text-anchor="middle">tag 0x1a2b3</text>
<text x="190.0" y="62.5" text-anchor="middle" class="m">bits 47 to 12</text>
<rect x="340" y="30" width="140" height="40" rx="6" class="g"/>
<text x="410.0" y="46.5" text-anchor="middle">set index 25</text>
<text x="410.0" y="62.5" text-anchor="middle" class="m">bits 11 to 6</text>
<rect x="480" y="30" width="120" height="40" rx="6" class="k"/>
<text x="540.0" y="46.5" text-anchor="middle">offset 56</text>
<text x="540.0" y="62.5" text-anchor="middle" class="m">bits 5 to 0</text>
<text x="142" y="113" text-anchor="end" class="m">set 0</text>
<rect x="151" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="187" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="223" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="259" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="295" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="331" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="367" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="403" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="439" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="475" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="511" y="100" width="33" height="15" rx="2" class="c"/>
<rect x="547" y="100" width="33" height="15" rx="2" class="c"/>
<text x="142" y="133" text-anchor="end" class="m">set 1</text>
<rect x="151" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="187" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="223" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="259" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="295" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="331" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="367" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="403" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="439" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="475" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="511" y="120" width="33" height="15" rx="2" class="c"/>
<rect x="547" y="120" width="33" height="15" rx="2" class="c"/>
<text x="142" y="153" text-anchor="end" class="m">…</text>
<text x="142" y="173" text-anchor="end" class="m">set 25</text>
<rect x="151" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="187" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="223" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="259" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="295" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="331" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="367" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="403" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="439" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="475" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="511" y="160" width="33" height="15" rx="2" class="cg"/>
<rect x="547" y="160" width="33" height="15" rx="2" class="cg"/>
<text x="142" y="193" text-anchor="end" class="m">…</text>
<text x="142" y="213" text-anchor="end" class="m">set 63</text>
<rect x="151" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="187" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="223" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="259" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="295" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="331" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="367" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="403" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="439" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="475" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="511" y="200" width="33" height="15" rx="2" class="c"/>
<rect x="547" y="200" width="33" height="15" rx="2" class="c"/>
<text x="366" y="96" text-anchor="middle" class="m">12 ways: each holds one line and its tag</text>
<path d="M410 72 V80 H612 V167 H588" class="pg" marker-end="url(#cgm)"/>
<text x="366" y="234" text-anchor="middle" class="m">1. the set index picks one row   2. the tag is compared with all 12 tags at once</text>
<text x="366" y="250" text-anchor="middle" class="m">3. on a match, the offset picks the byte inside the 64-byte line</text>
</svg>
</div>

**This machine's caches:**

```sh
$ lscpu --caches=NAME,ONE-SIZE,WAYS,SETS,COHERENCY-SIZE,TYPE
NAME ONE-SIZE WAYS   SETS COHERENCY-SIZE TYPE
L1d       48K   12     64             64 Data
L1i       32K    8     64             64 Instruction
L2         2M   16   2048             64 Unified
L3       260M   20 212992             64 Unified
```

`COHERENCY-SIZE` is the line size. For the L1d: 64 × 12 × 64 = 49,152 bytes = 48 KiB. 6 bits of offset (64 = 2⁶) and 6 bits of set index (64 = 2⁶).

**Worked example**, physical address `0x1a2b3678`:

- L1d: offset = low 6 bits = `0x38` (56); set = next 6 bits = `0x19` (25); tag = everything from bit 12 up = `0x1a2b3`.
- L2, 2,048 sets: 11 bits of set index, so set `0x4d9` and tag `0xd15`.
- L3: 212,992 sets is not a power of two, so its set can't be plain bits of the address. Large L3 caches are split into *slices*, and a hash of the address picks the slice.

**In Rust:**

```rust
/// A cache's geometry: sets, ways (lines per set), line size.
struct Geometry {
    sets: u64,
    ways: u64,
    line: u64,
}

impl Geometry {
    fn size(&self) -> u64 {
        self.sets * self.ways * self.line
    }

    /// Split an address into (tag, set index, offset in line).
    fn split(&self, addr: u64) -> (u64, u64, u64) {
        let offset_bits = self.line.trailing_zeros();
        let index_bits = self.sets.trailing_zeros();
        let offset = addr & (self.line - 1);
        let index = (addr >> offset_bits) & (self.sets - 1);
        let tag = addr >> (offset_bits + index_bits);
        (tag, index, offset)
    }
}

fn main() {
    // this machine's caches, from /sys/devices/system/cpu/cpu0/cache
    let l1d = Geometry { sets: 64, ways: 12, line: 64 };
    let l2 = Geometry { sets: 2048, ways: 16, line: 64 };
    assert_eq!(l1d.size(), 48 * 1024);
    assert_eq!(l2.size(), 2 * 1024 * 1024);

    let addr = 0x1a2b3678;
    // L1d: 6 offset bits, 6 index bits, the tag is the rest
    assert_eq!(l1d.split(addr), (0x1a2b3, 0x19, 0x38));
    // L2: 6 offset bits, 11 index bits
    assert_eq!(l2.split(addr), (0xd15, 0x4d9, 0x38));

    // addresses 4096 bytes apart differ only above bit 11,
    // so in the L1d they always share a set
    for k in 1..100 {
        assert_eq!(l1d.split(addr + k * 4096).1, 0x19);
    }
}
```

The last check shows a consequence: addresses 4096 bytes apart always fall in the same L1d set, since they differ only above bit 11.
