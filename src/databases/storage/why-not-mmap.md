A database engine could skip writing its own page cache and simply `mmap` its files, letting the operating system move pages between disk and memory. Why do most database designers advise against this? Name the main problems.

---

**What `mmap` does.** It maps a file into a program's address space: reading that memory reads the file, and writing it changes the file. The kernel loads each page from disk the first time it is touched (a *page fault*), evicts pages when memory runs short, and writes changed (*dirty*) pages back to the file **whenever it chooses**.

It is tempting: no cache code to write, and no copying between the kernel's page cache and the program. Andrew Crotty, Viktor Leis and Andrew Pavlo's paper *Are You Sure You Want to Use MMAP in Your Database Management System?* (CIDR 2022) explains why it goes wrong.

**1. Transactional safety.** A database must write the log record of a change before the changed page reaches the disk, so that a crash can be undone or redone. With `mmap`, "the OS can flush a dirty page to secondary storage at any time, irrespective of whether the writing transaction has committed. The DBMS cannot prevent these flushes and receives no warning when they occur."

<div class="diagram">
<svg viewBox="0 0 640 166" width="100%" style="max-width:640px" role="img" aria-label="With its own buffer pool, the DBMS writes the log before any changed page. With mmap, the OS can write a changed page to disk at any time, before the log or the commit.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .bolt{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="do" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="dg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="20" y="22" text-anchor="start" class="tg">Buffer pool: the DBMS decides when a page may reach the disk</text>
<rect x="20" y="32" width="140" height="40" rx="6" class="k"/>
<text x="90.0" y="56.5" text-anchor="middle">change a page</text>
<rect x="195" y="32" width="170" height="40" rx="6" class="g"/>
<text x="280.0" y="56.5" text-anchor="middle">write the log (WAL) first</text>
<rect x="400" y="32" width="220" height="40" rx="6" class="k"/>
<text x="510.0" y="56.5" text-anchor="middle">then write the page, later</text>
<path d="M162 52 H193" class="pg" marker-end="url(#dg)"/>
<path d="M367 52 H398" class="pg" marker-end="url(#dg)"/>
<text x="20" y="104" text-anchor="start" class="to">mmap: the OS decides</text>
<rect x="20" y="114" width="140" height="40" rx="6" class="k"/>
<text x="90.0" y="138.5" text-anchor="middle">change a page</text>
<rect x="195" y="114" width="425" height="40" rx="6" class="r"/>
<text x="407.5" y="130.5" text-anchor="middle">the OS may write the dirty page to disk at any moment,</text>
<text x="407.5" y="146.5" text-anchor="middle" class="m">before the log, before commit: the DBMS gets no warning</text>
<path d="M162 134 H193" class="po" marker-end="url(#do)"/>
</svg>
</div>

The ways around it, such as keeping a separate copy of every changed page, are complicated. LMDB, a well-known database built on `mmap`, solves it by allowing only one writer at a time.

**2. I/O stalls.** Any memory access can turn into a disk read, and the thread waits for it. "The DBMS cannot know whether the page is in memory," so it can't hand the read to asynchronous I/O and do other work meanwhile, as it can with a buffer pool of its own.

**3. Error handling.** With `read()`, a failed read returns an error code. With `mmap`, any line of code that touches mapped memory can instead receive `SIGBUS`, a signal that kills the process unless it has set up a signal handler.

A demonstration in Rust: map a two-page file, then shrink the file while it is mapped, which is the easiest way to cause a `SIGBUS`. A disk error on a mapped page arrives in the same way. The reading is done in a child process, which the parent checks:

```rust
use std::fs::{self, OpenOptions};
use std::os::fd::AsRawFd;
use std::os::unix::process::ExitStatusExt;
use std::process::Command;

// mmap from the C library, which Rust programs on Linux link anyway
extern "C" {
    fn mmap(
        addr: *mut u8,
        len: usize,
        prot: i32,
        flags: i32,
        fd: i32,
        offset: i64,
    ) -> *const u8;
}
const PROT_READ: i32 = 1;
const MAP_SHARED: i32 = 1;
const SIGBUS: i32 = 7;

/// Map a two-page "database file", shrink the file, then read.
fn reader(path: &std::path::Path) {
    fs::write(path, vec![b'x'; 8192]).unwrap();
    let file =
        OpenOptions::new().read(true).write(true).open(path).unwrap();
    let fd = file.as_raw_fd();
    let p = unsafe {
        mmap(std::ptr::null_mut(), 8192, PROT_READ, MAP_SHARED, fd, 0)
    };
    assert_ne!(p as isize, -1, "mmap failed");
    // reading this memory reads the file
    assert_eq!(unsafe { p.read_volatile() }, b'x');
    // the file shrinks: another process truncates it, say
    file.set_len(0).unwrap();
    // an ordinary memory read: no error code, the process just dies
    let _ = unsafe { p.read_volatile() };
    unreachable!("the read above never returns");
}

fn main() {
    let path = std::env::temp_dir().join("mapped-db-file");
    if std::env::args().nth(1).as_deref() == Some("reader") {
        reader(&path);
    }
    // run the reader in a child process, so it can die on its own
    let me = std::env::current_exe().unwrap();
    let status = Command::new(me).arg("reader").status().unwrap();
    assert_eq!(status.signal(), Some(SIGBUS));
    println!("reader killed by signal {:?}", status.signal());
}
```

```text
reader killed by signal Some(7)
```

Signal 7 is `SIGBUS` on Linux x86-64. The first read returned `b'x'`; the second, an ordinary memory read, killed the process.

**4. Performance.** When the kernel evicts a mapped page, every CPU core that might have the page's address translation cached in its *TLB* (translation lookaside buffer, a small cache of virtual-to-physical page mappings) must be interrupted to drop it: a *TLB shootdown*, which costs "thousands of cycles". The kernel also evicts pages with a single process, `kswapd`. Comparing `mmap` with `fio`, a benchmark tool that reads the SSDs directly, the authors found that "mmap performs well only on a single SSD during the initial loading phase. Once page eviction begins or when using multiple SSDs, mmap is 2–20× worse than fio."

**The hints don't fix it.** `madvise` (tell the kernel how pages will be read), `mlock` (stop pages from being evicted) and `msync` (write pages out now) exist, but CMU's database course concludes that "Using these syscalls to get the OS to behave correctly is just as onerous as managing memory yourself."

The paper's conclusion includes: "When you should not use mmap in your DBMS: You need to perform updates in a transactionally safe fashion."
