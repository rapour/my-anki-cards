On a TLB hit, what exactly does the TLB give back: the whole physical address, or something the CPU still has to combine? How is the physical address formed from a virtual address, and what is different on a TLB miss?

---

The TLB gives back the **frame number** of the page, with the page's permission bits. It does not compute anything. The physical address is that frame number **followed by the page offset**, and the offset never goes through the TLB at all.

With 4 KiB pages, a virtual address has two parts:

- the low 12 bits are the **offset** inside the page (2¹² = 4096). Translation never changes them;
- the bits above are the **virtual page number**.

A *page frame* is a 4 KiB block of RAM that can hold one page; frames are numbered from 0. A TLB entry is a saved answer from the page table: virtual page number → frame number, plus permission bits (present, writable, user or kernel only).

<div class="diagram">
<svg viewBox="0 0 640 262" width="100%" style="max-width:640px" role="img" aria-label="A virtual address splits into a virtual page number and a 12-bit offset. The TLB maps the page number to a frame number. The offset is copied unchanged. The physical address is the frame number followed by the offset.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="20" y="22" text-anchor="start">virtual address 0x7f3a12345678</text>
<rect x="40" y="32" width="380" height="40" rx="6" class="k"/>
<text x="230.0" y="48.5" text-anchor="middle">virtual page number 0x7f3a12345</text>
<text x="230.0" y="64.5" text-anchor="middle" class="m">bits 47 to 12</text>
<rect x="420" y="32" width="180" height="40" rx="6" class="g"/>
<text x="510.0" y="48.5" text-anchor="middle">offset 0x678</text>
<text x="510.0" y="64.5" text-anchor="middle" class="m">bits 11 to 0</text>
<line x1="230" y1="74" x2="230" y2="104" class="pg" marker-end="url(#cgm)"/>
<rect x="90" y="106" width="280" height="46" rx="6" class="k"/>
<text x="230.0" y="125.5" text-anchor="middle">TLB entry</text>
<text x="230.0" y="141.5" text-anchor="middle" class="m">page 0x7f3a12345 → frame 0x1a2b3, rw, user</text>
<line x1="230" y1="154" x2="230" y2="184" class="pg" marker-end="url(#cgm)"/>
<line x1="510" y1="74" x2="510" y2="184" class="pg" marker-end="url(#cgm)"/>
<text x="520" y="132" text-anchor="start" class="tg">copied unchanged:</text>
<text x="520" y="148" text-anchor="start" class="tg">never goes through</text>
<text x="520" y="164" text-anchor="start" class="tg">the TLB</text>
<rect x="40" y="186" width="380" height="40" rx="6" class="k"/>
<text x="230.0" y="202.5" text-anchor="middle">frame number 0x1a2b3</text>
<text x="230.0" y="218.5" text-anchor="middle" class="m">from the TLB</text>
<rect x="420" y="186" width="180" height="40" rx="6" class="g"/>
<text x="510.0" y="202.5" text-anchor="middle">offset 0x678</text>
<text x="510.0" y="218.5" text-anchor="middle" class="m">the same 12 bits</text>
<text x="20" y="250" text-anchor="start">physical address 0x1a2b3678: the two parts side by side, nothing added</text>
</svg>
</div>

**On a hit:**

1. the virtual page number is looked up in the TLB, which returns the frame number;
2. the CPU checks the permission bits. Writing to a read-only page, for example, raises a page fault;
3. physical address = frame number followed by the 12 offset bits, `(frame << 12) | offset`. The bits are only placed side by side: nothing is added.

**On a miss**, the page walker reads the page table. On x86-64 that is four levels, and each level is indexed by 9 bits of the virtual page number. The last entry holds the frame number and the permissions. The walker saves them in the TLB, and the access goes on as a hit. So the "calculation from page table entries" happens only on a miss, and its result is kept.

**With a 2 MiB huge page** the offset is the low 21 bits, and one TLB entry gives the number of a 2 MiB frame.

**Where the frame number goes next.** The L1 data cache usually chooses its set from the offset bits while the TLB is still working, then compares the frame number with the tags in that set. The L2 and L3 caches receive the whole physical address.

**In Rust**, with a real frame number. `/proc/self/pagemap` is the kernel's record of each of this process's pages: 8 bytes per page, with bit 63 meaning "in RAM" and bits 0 to 54 holding the frame number. It shows the frame number only to a program running as root:

```rust
use std::fs::File;
use std::os::unix::fs::FileExt;

const PAGE_BITS: u32 = 12; // 4 KiB pages: 12 offset bits

/// Split a virtual address into (virtual page number, page offset).
fn split(vaddr: u64) -> (u64, u64) {
    (vaddr >> PAGE_BITS, vaddr & ((1 << PAGE_BITS) - 1))
}

/// Join a frame number and an offset into a physical address.
/// Nothing is added or computed: the bits are placed side by side.
fn join(frame: u64, offset: u64) -> u64 {
    (frame << PAGE_BITS) | offset
}

/// The kernel's record of a virtual page: 8 bytes per page in
/// /proc/self/pagemap. Bit 63 = present in RAM; bits 0-54 = frame
/// number (shown as 0 unless the program runs as root).
fn pagemap_entry(vpn: u64) -> u64 {
    let mut buf = [0u8; 8];
    let f = File::open("/proc/self/pagemap").unwrap();
    f.read_exact_at(&mut buf, vpn * 8).unwrap();
    u64::from_le_bytes(buf)
}

fn main() {
    // worked example: the TLB maps page 0x7f3a12345 to frame 0x1a2b3
    let (vpn, offset) = split(0x7f3a_1234_5678);
    assert_eq!((vpn, offset), (0x7f3a12345, 0x678));
    assert_eq!(join(0x1a2b3, offset), 0x1a2b3678);

    // a real one: a value on the heap, its page and its frame
    let x = Box::new(42u64);
    let vaddr = &*x as *const u64 as u64;
    let (vpn, offset) = split(vaddr);
    let entry = pagemap_entry(vpn);
    assert!(entry >> 63 == 1, "the page is in RAM");
    let frame = entry & ((1 << 55) - 1);
    let paddr = join(frame, offset);
    // the offset passes through translation unchanged
    assert_eq!(paddr & 0xfff, vaddr & 0xfff);
    println!("virtual  {vaddr:#x}: page {vpn:#x}, offset {offset:#x}");
    println!(
        "physical {paddr:#x}: frame {frame:#x}, offset {offset:#x}"
    );
}
```

```text
virtual  0x56117c59fd60: page 0x56117c59f, offset 0xd60
physical 0x15b94dd60: frame 0x15b94d, offset 0xd60
```

The last three hex digits, `d60`, are the offset, the same in both addresses.
