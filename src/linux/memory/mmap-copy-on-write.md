A process maps four pages, each holding `'x'` or zeros: a **private** and a **shared** mapping of a file, and a **private** and a **shared** anonymous mapping (memory with no file behind it). It calls `fork`, and the child writes `'C'` into all four. What does the parent see in each afterwards, and what reaches the files? Explain the mechanism, *copy on write*.

---

| Mapping | The parent sees | The file holds |
|---|---|---|
| private, file-backed | `'x'`, the old value | `'x'`: unchanged |
| shared, file-backed | `'C'` | `'C'` |
| private, anonymous | `0`, the old value | no file |
| shared, anonymous | `'C'` | no file |

**Copy on write.** `fork` gives the child a copy of the parent's whole address space, but the kernel doesn't copy any memory. It copies only the *page tables*, the maps from virtual addresses to physical pages. Both processes now point at the same physical pages. In **private** mappings the kernel marks these pages read-only. When either process writes one:

1. the CPU stops the write with a *page fault*, because the page is read-only;
2. the kernel copies the page and points the writer's page table at the copy, now writable;
3. the write is retried and goes to the copy.

The other process still has the original. **Shared** mappings are not marked this way: both processes keep using the one page, so each sees the other's writes, and for a file the write goes to the file's page in the page cache, and from there to disk.

<div class="diagram">
<svg viewBox="0 0 640 226" width="100%" style="max-width:640px" role="img" aria-label="After fork, a write to a private mapping copies the page for the writer only, so the parent still sees the old value. A shared mapping has one page, so the parent sees the child&#x27;s write.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="mo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="mg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="165" y="22" text-anchor="middle" class="to">MAP_PRIVATE: the child writes &#x27;C&#x27;</text>
<text x="475" y="22" text-anchor="middle" class="tg">MAP_SHARED: the child writes &#x27;C&#x27;</text>
<rect x="20" y="38" width="130" height="40" rx="6" class="k"/>
<text x="85.0" y="62.5" text-anchor="middle">parent</text>
<rect x="180" y="38" width="130" height="40" rx="6" class="k"/>
<text x="245.0" y="62.5" text-anchor="middle">child</text>
<rect x="20" y="130" width="130" height="46" rx="6" class="k"/>
<text x="85.0" y="149.5" text-anchor="middle">page &#x27;x&#x27;</text>
<text x="85.0" y="165.5" text-anchor="middle" class="m">the original</text>
<rect x="180" y="130" width="130" height="46" rx="6" class="r"/>
<text x="245.0" y="149.5" text-anchor="middle">copy, now &#x27;C&#x27;</text>
<text x="245.0" y="165.5" text-anchor="middle" class="m">made by the write</text>
<line x1="85" y1="80" x2="85" y2="127" class="pg" marker-end="url(#mg)"/>
<line x1="245" y1="80" x2="245" y2="127" class="po" marker-end="url(#mo)"/>
<line x1="215" y1="80" x2="140" y2="127" class="dsh"/>
<text x="174" y="96" text-anchor="end" class="m">before</text>
<text x="165" y="200" text-anchor="middle" class="m">the write gives the child its own copy;</text>
<text x="165" y="214" text-anchor="middle" class="m">the parent still sees &#x27;x&#x27;</text>
<rect x="330" y="38" width="130" height="40" rx="6" class="k"/>
<text x="395.0" y="62.5" text-anchor="middle">parent</text>
<rect x="490" y="38" width="130" height="40" rx="6" class="k"/>
<text x="555.0" y="62.5" text-anchor="middle">child</text>
<rect x="410" y="130" width="130" height="46" rx="6" class="g"/>
<text x="475.0" y="149.5" text-anchor="middle">page &#x27;C&#x27;</text>
<text x="475.0" y="165.5" text-anchor="middle" class="m">the only copy</text>
<line x1="395" y1="80" x2="450" y2="127" class="pg" marker-end="url(#mg)"/>
<line x1="555" y1="80" x2="500" y2="127" class="pg" marker-end="url(#mg)"/>
<text x="475" y="200" text-anchor="middle" class="m">no copy is made: there is one page,</text>
<text x="475" y="214" text-anchor="middle" class="m">so the parent sees &#x27;C&#x27; too</text>
</svg>
</div>

**A private file mapping is only private once written.** Until this process writes a page, it reads the file's page in the page cache, so it sees changes that others make to the file. `man mmap` says only that "It is unspecified whether changes made to the file after the mmap() call are visible in the mapped region." On Linux they are visible until the first write, and the program below checks this too.

**The experiment in Rust**, with the C library's `mmap` and `fork`. A file mapping can't be both private and shared, so it uses two files:

```rust
use std::fs::{self, OpenOptions};
use std::os::fd::AsRawFd;
use std::os::unix::fs::FileExt;

extern "C" {
    fn mmap(
        addr: *mut u8,
        len: usize,
        prot: i32,
        flags: i32,
        fd: i32,
        offset: i64,
    ) -> *mut u8;
    fn fork() -> i32;
    fn waitpid(pid: i32, status: *mut i32, options: i32) -> i32;
    fn _exit(code: i32) -> !;
}
// Linux values of the mmap flags
const PROT_READ_WRITE: i32 = 0x1 | 0x2;
const MAP_SHARED: i32 = 0x01;
const MAP_PRIVATE: i32 = 0x02;
const MAP_ANONYMOUS: i32 = 0x20;
const LEN: usize = 4096;

fn map(flags: i32, fd: i32) -> *mut u8 {
    let p = unsafe {
        mmap(std::ptr::null_mut(), LEN, PROT_READ_WRITE, flags, fd, 0)
    };
    assert_ne!(p as isize, -1, "mmap failed");
    p
}

/// A file of LEN bytes 'x', opened for reading and writing.
fn file_of_x(name: &str) -> (std::path::PathBuf, std::fs::File) {
    let path = std::env::temp_dir().join(name);
    fs::write(&path, [b'x'; LEN]).unwrap();
    let file =
        OpenOptions::new().read(true).write(true).open(&path).unwrap();
    (path, file)
}

fn main() {
    let (priv_path, priv_file) = file_of_x("cow-private.dat");
    let (shared_path, shared_file) = file_of_x("cow-shared.dat");
    let maps = [
        map(MAP_PRIVATE, priv_file.as_raw_fd()),
        map(MAP_SHARED, shared_file.as_raw_fd()),
        map(MAP_PRIVATE | MAP_ANONYMOUS, -1),
        map(MAP_SHARED | MAP_ANONYMOUS, -1),
    ];

    // fork: the child gets a copy of the parent's address space
    let pid = unsafe { fork() };
    if pid == 0 {
        // child: write 'C' into the first byte of all four
        for p in maps {
            unsafe { p.write_volatile(b'C') };
        }
        unsafe { _exit(0) };
    }
    unsafe { waitpid(pid, std::ptr::null_mut(), 0) };

    // parent: what does it see after the child's writes?
    let seen: Vec<u8> = maps.iter().map(|p| unsafe { **p }).collect();
    assert_eq!(seen, [b'x', b'C', 0, b'C']);
    // and what reached the files?
    assert_eq!(fs::read(&priv_path).unwrap()[0], b'x');
    assert_eq!(fs::read(&shared_path).unwrap()[0], b'C');
    let names =
        ["private file", "shared file", "private anon", "shared anon"];
    for (name, b) in names.iter().zip(&seen) {
        println!("{name:<12}  parent sees {:?}", *b as char);
    }

    // The parent has not written its private file page, so it still
    // reads the file's page in the page cache: a write to the file
    // shows through.
    priv_file.write_all_at(b"F", 0).unwrap();
    assert_eq!(unsafe { *maps[0] }, b'F');
    // Once the parent writes it, the page is its own copy, and later
    // writes to the file no longer show.
    unsafe { maps[0].write_volatile(b'P') };
    priv_file.write_all_at(b"G", 0).unwrap();
    assert_eq!(unsafe { *maps[0] }, b'P');
    assert_eq!(fs::read(&priv_path).unwrap()[0], b'G');
}
```

```text
private file  parent sees 'x'
shared file   parent sees 'C'
private anon  parent sees '\0'
shared anon   parent sees 'C'
```

**Why it matters:**

- `fork` is cheap even for a process with gigabytes of memory: only the page tables are copied, and only pages that are later written get copied.
- A forked child gets a frozen snapshot of the parent's private memory. Redis uses this to save its data to disk: it forks, and the child writes out the snapshot while the parent goes on serving requests.
- Every page the parent changes during that time costs a copy, so memory use can grow while the child runs.
