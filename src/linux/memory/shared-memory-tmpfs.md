Linux has four ways for processes to share memory that isn't an ordinary file on disk: `mmap` with `MAP_SHARED | MAP_ANONYMOUS`, POSIX `shm_open`, `memfd_create`, and System V `shmget`. How does the kernel implement all four, and what follows from that?

---

**All four are files on tmpfs.** *tmpfs* is a file system that keeps its files only in memory: their pages live in the *page cache* (the kernel's copy of file data in RAM) with no disk file behind them. The kernel calls this kind of memory *shmem*. Each interface creates a tmpfs file in its own way:

| Interface | The tmpfs file | Name in `/proc/<pid>/maps` |
|---|---|---|
| `mmap(MAP_SHARED | MAP_ANONYMOUS)` | hidden, on the kernel's internal tmpfs mount | `/dev/zero (deleted)` |
| `shm_open("/demo-shm")` | an ordinary file in `/dev/shm`, a tmpfs mount | `/dev/shm/demo-shm` |
| `memfd_create("demo")` | hidden; you get a file descriptor to it | `/memfd:demo (deleted)` |
| `shmget` + `shmat` | hidden, named after the segment's key | `/SYSV00000000 (deleted)` |

*(deleted)* means the file has no name in any directory, so no other process can open it by name.

<div class="diagram">
<svg viewBox="0 0 640 272" width="100%" style="max-width:640px" role="img" aria-label="Shared anonymous mappings, POSIX shm_open, memfd_create and System V shared memory all create a file on tmpfs, a file system that keeps its files in memory. Their pages are counted as Shmem and can only be moved to swap.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="mo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="mg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="145" y="22" text-anchor="middle" class="m">interface, and its name in /proc/&lt;pid&gt;/maps</text>
<rect x="10" y="34" width="272" height="42" rx="6" class="k"/>
<text x="146.0" y="51.5" text-anchor="middle">mmap(MAP_SHARED|MAP_ANONYMOUS)</text>
<text x="146.0" y="67.5" text-anchor="middle" class="m">/dev/zero (deleted)</text>
<line x1="284" y1="55" x2="326" y2="135" class="pg" marker-end="url(#mg)"/>
<rect x="10" y="86" width="272" height="42" rx="6" class="k"/>
<text x="146.0" y="103.5" text-anchor="middle">shm_open(&quot;/demo-shm&quot;)  (POSIX)</text>
<text x="146.0" y="119.5" text-anchor="middle" class="m">/dev/shm/demo-shm</text>
<line x1="284" y1="107" x2="326" y2="135" class="pg" marker-end="url(#mg)"/>
<rect x="10" y="138" width="272" height="42" rx="6" class="k"/>
<text x="146.0" y="155.5" text-anchor="middle">memfd_create(&quot;demo&quot;)</text>
<text x="146.0" y="171.5" text-anchor="middle" class="m">/memfd:demo (deleted)</text>
<line x1="284" y1="159" x2="326" y2="135" class="pg" marker-end="url(#mg)"/>
<rect x="10" y="190" width="272" height="42" rx="6" class="k"/>
<text x="146.0" y="207.5" text-anchor="middle">shmget + shmat  (System V)</text>
<text x="146.0" y="223.5" text-anchor="middle" class="m">/SYSV00000000 (deleted)</text>
<line x1="284" y1="211" x2="326" y2="135" class="pg" marker-end="url(#mg)"/>
<rect x="328" y="95" width="150" height="80" rx="6" class="g"/>
<text x="403.0" y="123.5" text-anchor="middle">a file on tmpfs</text>
<text x="403.0" y="139.5" text-anchor="middle" class="m">a file system that keeps</text>
<text x="403.0" y="155.5" text-anchor="middle" class="m">its files only in memory</text>
<rect x="505" y="64" width="115" height="48" rx="6" class="k"/>
<text x="562.5" y="84.5" text-anchor="middle">RAM</text>
<text x="562.5" y="100.5" text-anchor="middle" class="m">counted as Shmem</text>
<rect x="505" y="158" width="115" height="48" rx="6" class="r"/>
<text x="562.5" y="178.5" text-anchor="middle">swap</text>
<text x="562.5" y="194.5" text-anchor="middle" class="m">when RAM is short</text>
<line x1="480" y1="125" x2="503" y2="92" class="pg" marker-end="url(#mg)"/>
<line x1="480" y1="148" x2="503" y2="178" class="po" marker-end="url(#mo)"/>
<text x="320" y="260" text-anchor="middle" class="m">No disk file is behind them, so under memory pressure their pages can only go to swap, never be dropped.</text>
</svg>
</div>

```sh
$ stat -fc %T /dev/shm
tmpfs
```

**The proof in Rust.** The program makes 16 MiB of each kind, writes to every page, and reads `RssShmem` from `/proc/self/status`: how much shmem this process has in memory. Private anonymous memory is the control case: it is ordinary memory, not shmem.

```rust
use std::fs;

extern "C" {
    fn mmap(
        addr: *mut u8,
        len: usize,
        prot: i32,
        flags: i32,
        fd: i32,
        offset: i64,
    ) -> *mut u8;
    fn shm_open(name: *const i8, oflag: i32, mode: u32) -> i32;
    fn shm_unlink(name: *const i8) -> i32;
    fn memfd_create(name: *const i8, flags: u32) -> i32;
    fn ftruncate(fd: i32, len: i64) -> i32;
    fn shmget(key: i32, size: usize, flags: i32) -> i32;
    fn shmat(id: i32, addr: *const u8, flags: i32) -> *mut u8;
    fn shmctl(id: i32, cmd: i32, buf: *mut u8) -> i32;
}
// Linux values of the flags
const PROT_READ_WRITE: i32 = 0x1 | 0x2;
const MAP_SHARED: i32 = 0x01;
const MAP_PRIVATE: i32 = 0x02;
const MAP_ANONYMOUS: i32 = 0x20;
const O_RDWR_CREAT: i32 = 0o2 | 0o100;
const IPC_PRIVATE: i32 = 0;
const IPC_RMID: i32 = 0;
const LEN: usize = 16 << 20; // 16 MiB

fn map(flags: i32, fd: i32) -> *mut u8 {
    let p = unsafe {
        mmap(std::ptr::null_mut(), LEN, PROT_READ_WRITE, flags, fd, 0)
    };
    assert_ne!(p as isize, -1, "mmap failed");
    p
}

/// Give a file descriptor a size of LEN and map it shared.
fn map_fd(fd: i32) -> *mut u8 {
    assert!(fd >= 0);
    assert_eq!(unsafe { ftruncate(fd, LEN as i64) }, 0);
    map(MAP_SHARED, fd)
}

/// A field of /proc/self/status, in KiB, such as "RssShmem:".
fn status_kib(field: &str) -> usize {
    let status = fs::read_to_string("/proc/self/status").unwrap();
    let line = status.lines().find(|l| l.starts_with(field)).unwrap();
    line.split_whitespace().nth(1).unwrap().parse().unwrap()
}

/// The path column of the /proc/self/maps line that starts at `p`.
fn maps_path(p: *mut u8) -> String {
    let start = format!("{:x}-", p as usize);
    let maps = fs::read_to_string("/proc/self/maps").unwrap();
    let line = maps.lines().find(|l| l.starts_with(&start)).unwrap();
    line.split_whitespace().skip(5).collect::<Vec<_>>().join(" ")
}

/// Touch every page of a new mapping and report how much this
/// process's resident *shared* memory (RssShmem) grew.
fn report(kind: &str, p: *mut u8) -> usize {
    let before = status_kib("RssShmem:");
    unsafe { p.write_bytes(1, LEN) };
    let grew = status_kib("RssShmem:") - before;
    println!("{kind:<17} +{grew:>5} KiB  {}", maps_path(p));
    grew
}

fn main() {
    let private = map(MAP_PRIVATE | MAP_ANONYMOUS, -1);
    assert_eq!(report("private anonymous", private), 0);

    let shared = map(MAP_SHARED | MAP_ANONYMOUS, -1);
    assert_eq!(report("shared anonymous", shared), LEN >> 10);

    let name = c"/demo-shm";
    let fd = unsafe { shm_open(name.as_ptr(), O_RDWR_CREAT, 0o600) };
    assert_eq!(report("POSIX shm_open", map_fd(fd)), LEN >> 10);
    // an ordinary file on the tmpfs mounted at /dev/shm
    let size = fs::metadata("/dev/shm/demo-shm").unwrap().len();
    assert_eq!(size, LEN as u64);
    unsafe { shm_unlink(name.as_ptr()) };

    let fd = unsafe { memfd_create(c"demo".as_ptr(), 0) };
    assert_eq!(report("memfd_create", map_fd(fd)), LEN >> 10);

    let id = unsafe { shmget(IPC_PRIVATE, LEN, 0o600) };
    assert!(id >= 0);
    let p = unsafe { shmat(id, std::ptr::null(), 0) };
    assert_eq!(report("System V shmget", p), LEN >> 10);
    unsafe { shmctl(id, IPC_RMID, std::ptr::null_mut()) };
}
```

```text
private anonymous +    0 KiB
shared anonymous  +16384 KiB  /dev/zero (deleted)
POSIX shm_open    +16384 KiB  /dev/shm/demo-shm
memfd_create      +16384 KiB  /memfd:demo (deleted)
System V shmget   +16384 KiB  /SYSV00000000 (deleted)
```

**What follows from it:**

1. **It's counted as shared memory, not as a cache.** It shows as `Shmem` in `/proc/meminfo`, in the "shared" column of `free`, and as `RssShmem` for each process. Unlike a file's pages, these pages can't simply be dropped when memory is short: there's no file to read them back from. They can only go to swap, and with no swap they stay in RAM.
2. **A tmpfs mount has a size limit.** tmpfs defaults to half of RAM, and `/dev/shm` may be mounted smaller, in a container for example. Writing to a page that tmpfs has no room for, through a mapping, kills the process with `SIGBUS` instead of returning an error. PostgreSQL's source code (`dsm_impl.c`) explains why it allocates its segments up front: "On Linux, a shm_open fd is backed by a tmpfs file. … Accessing memory backed by a hole causes tmpfs to allocate pages, which fails with SIGBUS if there is no more tmpfs space available. So we ask tmpfs to allocate pages here, so we can fail gracefully with ENOSPC now rather than risking SIGBUS later."
3. **Lifetimes differ.** Shared anonymous and memfd memory disappear when the last process using them unmaps or closes them. A POSIX shared memory file stays in `/dev/shm` until `shm_unlink`, even after every process has exited. A System V segment stays until it is removed with `IPC_RMID`; `ipcs -m` lists the segments. A crashed program can leak either kind.

PostgreSQL uses two of these by default on Linux: an anonymous shared `mmap` for its main shared memory, including its cache of pages, and `shm_open` for the extra segments that parallel queries use.
