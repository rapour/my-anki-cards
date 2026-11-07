Most L1 data caches are **virtually indexed, physically tagged** (VIPT). What does that mean, why does it let the L1 look up data while the TLB is still translating the address, and why does it limit the L1's size to *ways × page size*?

---

Two terms: a cache's **index** is the address bits that choose the set to look in; its **tag** is the address bits stored with each line and compared to confirm a hit.

The options:

- **PIPT**, physically indexed and tagged: wait for the TLB, then look up. Simple, but the TLB's delay comes before every L1 access.
- **VIVT**, virtually indexed and tagged: no TLB needed at all, but virtual addresses are ambiguous. The same virtual address means different memory in different processes, and two virtual addresses can name the same memory.
- **VIPT**: take the **index from the virtual address** and compare **physical tags**. Wikipedia: "the cache set can be looked up in parallel with the TLB translation, however the tag cannot be compared until the physical address is available."

<div class="diagram">
<svg viewBox="0 0 640 286" width="100%" style="max-width:640px" role="img" aria-label="In a virtually indexed, physically tagged L1, the set index comes from the page offset bits, which translation does not change. The L1 reads the set while the TLB translates the page number; then the frame number is compared with the set&#x27;s physical tags.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="20" y="20" text-anchor="start">a virtual address, as this machine&#x27;s L1d uses it</text>
<rect x="40" y="30" width="330" height="40" rx="6" class="k"/>
<text x="205.0" y="46.5" text-anchor="middle">virtual page number</text>
<text x="205.0" y="62.5" text-anchor="middle" class="m">bits 47 to 12</text>
<rect x="370" y="30" width="120" height="40" rx="6" class="g"/>
<text x="430.0" y="46.5" text-anchor="middle">set index</text>
<text x="430.0" y="62.5" text-anchor="middle" class="m">bits 11 to 6</text>
<rect x="490" y="30" width="110" height="40" rx="6" class="k"/>
<text x="545.0" y="46.5" text-anchor="middle">byte in line</text>
<text x="545.0" y="62.5" text-anchor="middle" class="m">bits 5 to 0</text>
<text x="442" y="90" text-anchor="start" class="tg">page offset: the same in</text>
<text x="442" y="104" text-anchor="start" class="tg">virtual and physical address</text>
<line x1="175" y1="72" x2="175" y2="120" class="pg" marker-end="url(#cgm)"/>
<rect x="80" y="122" width="190" height="44" rx="6" class="k"/>
<text x="175.0" y="140.5" text-anchor="middle">TLB</text>
<text x="175.0" y="156.5" text-anchor="middle" class="m">page → frame number</text>
<line x1="430" y1="72" x2="430" y2="120" class="pg" marker-end="url(#cgm)"/>
<rect x="370" y="122" width="180" height="44" rx="6" class="g"/>
<text x="460.0" y="140.5" text-anchor="middle">L1 reads set 25</text>
<text x="460.0" y="156.5" text-anchor="middle" class="m">its 12 lines and tags</text>
<text x="320" y="144" text-anchor="middle" class="m">at the</text>
<text x="320" y="157" text-anchor="middle" class="m">same time</text>
<line x1="175" y1="168" x2="290" y2="202" class="pg" marker-end="url(#cgm)"/>
<line x1="460" y1="168" x2="350" y2="202" class="pg" marker-end="url(#cgm)"/>
<rect x="200" y="204" width="240" height="44" rx="6" class="k"/>
<text x="320.0" y="222.5" text-anchor="middle">compare the frame number</text>
<text x="320.0" y="238.5" text-anchor="middle" class="m">with the 12 physical tags: hit or miss</text>
<text x="320" y="274" text-anchor="middle" class="m">index + byte bits = 12 = the page offset, so the L1 can be at most 12 ways × 4 KiB = 48 KiB</text>
</svg>
</div>

**The trick:** choose the index only from bits **inside the page offset** (the low 12 bits for 4 KiB pages). Translation never changes those bits, so the virtual index *is* the physical index. On this machine's L1d: 6 bits of byte offset + 6 bits of set index = 12 bits, exactly the page offset.

**The size limit follows.** If only 12 bits may choose the byte and the set, one way can hold at most 4 KiB, and the cache can hold at most *ways* × 4 KiB. Wikipedia: "this limits the size of VIPT caches to the page size times the associativity of the cache." This machine fits exactly:

- L1d: 48 KiB = 12 ways × 4 KiB;
- L1i: 32 KiB = 8 ways × 4 KiB.

So an L1 grows by adding ways, not sets. The L2 and L3 are physically indexed and tagged: they are larger and are looked up after translation anyway.

**Why breaking the limit would hurt.** Say one way were 8 KiB. Then bit 12 would help choose the set, and bit 12 can differ between two virtual addresses of the same physical page: shared memory mapped twice, for example. The same data could then sit in two sets at once, and a write to one copy would leave the other one stale.

**In Rust**: one page of shared memory mapped at two virtual addresses. Both land on the same frame (the same physical tag) and in the same L1 set, so they are one cache line, and a write through one address is seen through the other:

```rust
use std::fs::File;
use std::os::unix::fs::FileExt;

extern "C" {
    fn memfd_create(name: *const i8, flags: u32) -> i32;
    fn ftruncate(fd: i32, len: i64) -> i32;
    fn mmap(
        addr: *mut u8,
        len: usize,
        prot: i32,
        flags: i32,
        fd: i32,
        offset: i64,
    ) -> *mut u8;
}
const PROT_READ_WRITE: i32 = 0x1 | 0x2;
const MAP_SHARED: i32 = 0x01;

/// Set index in this machine's L1d: 64-byte lines (bits 0-5),
/// 64 sets (bits 6-11). All of it lies inside the 4 KiB page offset.
fn l1_set(addr: usize) -> usize {
    (addr >> 6) & 63
}

/// The physical frame of a virtual address, from /proc/self/pagemap
/// (reads as 0 unless run as root).
fn frame(addr: usize) -> u64 {
    let mut buf = [0u8; 8];
    let f = File::open("/proc/self/pagemap").unwrap();
    f.read_exact_at(&mut buf, (addr / 4096 * 8) as u64).unwrap();
    u64::from_le_bytes(buf) & ((1 << 55) - 1)
}

fn main() {
    // one page of shared memory, mapped at two virtual addresses
    let fd = unsafe { memfd_create(c"page".as_ptr(), 0) };
    assert!(fd >= 0 && unsafe { ftruncate(fd, 4096) } == 0);
    let map = || unsafe {
        let p = std::ptr::null_mut();
        mmap(p, 4096, PROT_READ_WRITE, MAP_SHARED, fd, 0)
    };
    let (a, b) = (map(), map());
    assert_ne!(a, b);

    // write through one address, read through the other
    let (x, y) = unsafe { (a.add(0x678), b.add(0x678)) };
    unsafe { x.write_volatile(42) };
    assert_eq!(unsafe { y.read_volatile() }, 42);

    // same frame, so the same physical tag...
    assert_eq!(frame(x as usize), frame(y as usize));
    // ...and the same page offset, so the same L1 set
    assert_eq!(l1_set(x as usize), l1_set(y as usize));
    println!(
        "{x:?} and {y:?}: frame {:#x}, L1 set {}",
        frame(x as usize),
        l1_set(x as usize)
    );
}
```

```text
0x7f0f6a9e7678 and 0x7f0f6a9e6678: frame 0x11bd0a, L1 set 25
```

The two addresses differ only above bit 11, in the page number. The frame number comes from `/proc/self/pagemap`, which shows it only to root.
