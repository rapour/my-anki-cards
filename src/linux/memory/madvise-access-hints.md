What can a program tell the Linux kernel with `madvise` about how it will access a memory mapping? Explain `MADV_NORMAL`, `MADV_SEQUENTIAL`, `MADV_RANDOM`, `MADV_WILLNEED` and `MADV_DONTNEED`, and show the effect of one of them.

---

Three terms first:

- A **page fault** happens when a program touches a page that its page table doesn't map yet. It is *minor* if the page is already in memory and only needs mapping, and *major* if the kernel must wait for a disk read.
- The **page cache** is the kernel's copy of file data in RAM.
- **Read-ahead**: when the kernel has to read a page of a file from disk, it also reads the pages after it in the same request, betting they will be needed next.

`madvise(addr, length, advice)` describes the expected access pattern of a mapped range, so the kernel can adjust its read-ahead and caching:

| Advice | The program says | The kernel |
|---|---|---|
| `MADV_NORMAL` | nothing special (the default) | reads ahead a moderate amount |
| `MADV_SEQUENTIAL` | "I'll read these pages in order" | reads ahead more, and may free pages soon after they are read |
| `MADV_RANDOM` | "I'll jump around" | stops reading ahead: each fault reads only the page asked for |
| `MADV_WILLNEED` | "I'll need these soon" | starts reading them in now |
| `MADV_DONTNEED` | "I'm done with these" | frees them now. When touched again, a file mapping re-reads the file, losing any private changes; private anonymous memory comes back as zeros |

Only `MADV_DONTNEED` can change what a program reads. The others change only how fast it gets it.

<div class="diagram">
<svg viewBox="0 0 640 204" width="100%" style="max-width:640px" role="img" aria-label="With the default hint or MADV_SEQUENTIAL, one page fault reads the following pages too. With MADV_RANDOM, every page is its own disk read: 16,384 major faults for a 64 MiB file instead of 1.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="mo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="mg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="161" y="64" text-anchor="end">MADV_NORMAL</text>
<text x="161" y="78" text-anchor="end" class="m">and SEQUENTIAL</text>
<rect x="176" y="46" width="24" height="26" rx="2" class="cr"/>
<rect x="203" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="230" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="257" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="284" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="311" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="338" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="365" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="392" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="419" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="446" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="473" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="500" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="527" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="554" y="46" width="24" height="26" rx="2" class="cg"/>
<rect x="581" y="46" width="24" height="26" rx="2" class="cg"/>
<text x="161" y="154" text-anchor="end">MADV_RANDOM</text>
<rect x="176" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="203" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="230" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="257" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="284" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="311" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="338" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="365" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="392" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="419" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="446" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="473" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="500" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="527" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="554" y="136" width="24" height="26" rx="2" class="cr"/>
<rect x="581" y="136" width="24" height="26" rx="2" class="cr"/>
<path d="M177 38 V32 H604 V38" class="pg"/>
<text x="391.0" y="26" text-anchor="middle" class="tg">one disk read brings in the pages ahead (read-ahead)</text>
<text x="391.0" y="92" text-anchor="middle" class="m">orange: a major fault, a disk read; teal: already in memory</text>
<text x="391.0" y="124" text-anchor="middle" class="to">no read-ahead: every page is its own disk read</text>
<text x="320" y="192" text-anchor="middle" class="m">measured, reading a 64 MiB file page by page: 1 major fault against 16,384</text>
</svg>
</div>

**A measurement in Rust.** Map a 64 MiB file, empty it from the page cache first, give a hint, then read one byte from each of its 16,384 pages in order and count the major faults:

```rust
use std::fs::{self, File};
use std::os::fd::AsRawFd;
use std::time::Instant;

extern "C" {
    fn mmap(
        addr: *mut u8,
        len: usize,
        prot: i32,
        flags: i32,
        fd: i32,
        offset: i64,
    ) -> *mut u8;
    fn munmap(addr: *mut u8, len: usize) -> i32;
    fn madvise(addr: *mut u8, len: usize, advice: i32) -> i32;
    fn posix_fadvise(
        fd: i32,
        offset: i64,
        len: i64,
        advice: i32,
    ) -> i32;
    fn getrusage(who: i32, usage: *mut [i64; 18]) -> i32;
}
// Linux values of the flags
const PROT_READ: i32 = 0x1;
const PROT_READ_WRITE: i32 = 0x1 | 0x2;
const MAP_SHARED: i32 = 0x01;
const MAP_PRIVATE_ANONYMOUS: i32 = 0x02 | 0x20;
const MADV_NORMAL: i32 = 0;
const MADV_RANDOM: i32 = 1;
const MADV_SEQUENTIAL: i32 = 2;
const MADV_WILLNEED: i32 = 3;
const MADV_DONTNEED: i32 = 4;
const POSIX_FADV_DONTNEED: i32 = 4;
const LEN: usize = 64 << 20; // 64 MiB
const PAGES: usize = LEN / 4096;

/// Major page faults so far: faults that had to wait for the disk.
fn major_faults() -> i64 {
    let mut usage = [0i64; 18]; // struct rusage, as 64-bit words
    unsafe { getrusage(0, &mut usage) };
    usage[9] // ru_majflt
}

/// Map the file, give the hint, then read one byte of every page,
/// in order. Returns the number of major faults.
fn read_with_hint(file: &File, name: &str, advice: i32) -> i64 {
    let fd = file.as_raw_fd();
    // drop the file from the page cache, so reads must go to disk
    let rc = unsafe { posix_fadvise(fd, 0, 0, POSIX_FADV_DONTNEED) };
    assert_eq!(rc, 0);
    let p = unsafe {
        mmap(std::ptr::null_mut(), LEN, PROT_READ, MAP_SHARED, fd, 0)
    };
    assert_ne!(p as isize, -1, "mmap failed");
    assert_eq!(unsafe { madvise(p, LEN, advice) }, 0);

    let (faults, start) = (major_faults(), Instant::now());
    for page in 0..PAGES {
        assert_eq!(unsafe { p.add(page * 4096).read_volatile() }, 7);
    }
    let faults = major_faults() - faults;
    let ms = start.elapsed().as_millis();
    println!("{name:<15} {faults:>5} major faults  {ms:>4} ms");
    unsafe { munmap(p, LEN) };
    faults
}

fn main() {
    let path = std::env::temp_dir().join("hints.dat");
    fs::write(&path, vec![7u8; LEN]).unwrap();
    let file = File::open(&path).unwrap();
    file.sync_all().unwrap(); // on disk, so the cache can be dropped

    let normal = read_with_hint(&file, "MADV_NORMAL", MADV_NORMAL);
    let random = read_with_hint(&file, "MADV_RANDOM", MADV_RANDOM);
    read_with_hint(&file, "MADV_SEQUENTIAL", MADV_SEQUENTIAL);
    read_with_hint(&file, "MADV_WILLNEED", MADV_WILLNEED);

    // no read-ahead: every one of the 16,384 pages is a disk read
    assert_eq!(random, PAGES as i64);
    // read-ahead: one fault brings in many pages
    assert!(normal * 100 < random);

    // MADV_DONTNEED frees the pages now. Private anonymous memory has
    // no file to reload them from, so they read back as zeros.
    let p = unsafe {
        let flags = MAP_PRIVATE_ANONYMOUS;
        mmap(std::ptr::null_mut(), 4096, PROT_READ_WRITE, flags, -1, 0)
    };
    unsafe { p.write_volatile(42) };
    assert_eq!(unsafe { madvise(p, 4096, MADV_DONTNEED) }, 0);
    assert_eq!(unsafe { p.read_volatile() }, 0);
}
```

One run, on a Linux virtual machine:

```text
MADV_NORMAL         1 major faults    21 ms
MADV_RANDOM     16384 major faults   486 ms
MADV_SEQUENTIAL     1 major faults    21 ms
MADV_WILLNEED       1 major faults    20 ms
```

- With read-ahead, the first fault waits for the disk and brings in the following pages too. Every later page is already in memory, so its fault is minor.
- `MADV_RANDOM` turns read-ahead off, so all 16,384 pages are separate disk reads. Here that made the scan more than 20 times slower.
- `MADV_SEQUENTIAL` matched the default here, because the default read-ahead already keeps up with a scan in order.

**When each helps.** `MADV_RANDOM` suits truly random access over a large file, such as lookups in a hash index, where read-ahead would spend disk reads and memory on pages nobody uses. `MADV_SEQUENTIAL` suits a single pass over a big file. `MADV_WILLNEED` lets a program ask for pages before it needs them.

**For `read()` instead of `mmap`**, `posix_fadvise` takes the same hints for a file descriptor: `POSIX_FADV_SEQUENTIAL`, `RANDOM`, `WILLNEED` and `DONTNEED`. The program uses `POSIX_FADV_DONTNEED` to empty the page cache of the file before each run.
