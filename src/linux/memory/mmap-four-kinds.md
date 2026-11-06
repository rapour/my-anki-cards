`mmap` creates a memory mapping that is either **file-backed** or **anonymous**, and either **shared** or **private**. What does each of the four combinations do, what is each one used for, and how can you tell them apart in `/proc/<pid>/maps`?

---

`mmap` makes a range of a process's address space usable. It takes two independent choices:

- **Where the pages come from.** *File-backed*: from a file, through the *page cache* (the kernel's copy of file data in RAM). *Anonymous* (`MAP_ANONYMOUS`): from no file at all. The memory starts as zeros.
- **Who sees a write.** *Shared* (`MAP_SHARED`): there is one copy of each page, used by every process that maps it; for a file, writes reach the file. *Private* (`MAP_PRIVATE`): the first write to a page gives this process its own copy of that page, a technique called *copy on write*. Nobody else sees the write, and it never reaches the file.

<div class="diagram">
<svg viewBox="0 0 640 300" width="100%" style="max-width:640px" role="img" aria-label="The four kinds of mapping. Private file: reads the file, writes go to a private copy. Shared file: reads and writes the file&#x27;s pages in the page cache. Private anonymous: zero-filled memory of one process. Shared anonymous: zero-filled memory shared with child processes. /proc/pid/maps shows p or s for private or shared, and the file&#x27;s path.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="mo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="mg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="250.0" y="24" text-anchor="middle">private (MAP_PRIVATE)</text>
<text x="508.0" y="24" text-anchor="middle">shared (MAP_SHARED)</text>
<text x="113" y="92" text-anchor="end">file-backed</text>
<text x="113" y="108" text-anchor="end" class="m">fd of a file</text>
<text x="113" y="212" text-anchor="end">anonymous</text>
<text x="113" y="228" text-anchor="end" class="m">MAP_ANONYMOUS</text>
<rect x="125" y="40" width="250" height="110" rx="6" class="k"/>
<text x="250.0" y="67.5" text-anchor="middle">reads the file; a write copies the page</text>
<text x="250.0" y="83.5" text-anchor="middle" class="m">the copy is this process&#x27;s own,</text>
<text x="250.0" y="99.5" text-anchor="middle" class="m">never written to the file</text>
<text x="250.0" y="115.5" text-anchor="middle" class="m">used by: program code, shared libraries</text>
<text x="250.0" y="131.5" text-anchor="middle" class="m">maps: rw-p  /path/to/file</text>
<rect x="383" y="40" width="250" height="110" rx="6" class="g"/>
<text x="508.0" y="67.5" text-anchor="middle">reads and writes the file&#x27;s pages</text>
<text x="508.0" y="83.5" text-anchor="middle" class="m">in the page cache: writes reach the file</text>
<text x="508.0" y="99.5" text-anchor="middle" class="m">and every process mapping it sees them</text>
<text x="508.0" y="115.5" text-anchor="middle" class="m">used by: LMDB, files edited in place</text>
<text x="508.0" y="131.5" text-anchor="middle" class="m">maps: rw-s  /path/to/file</text>
<rect x="125" y="160" width="250" height="110" rx="6" class="k"/>
<text x="250.0" y="187.5" text-anchor="middle">zero-filled memory of one process</text>
<text x="250.0" y="203.5" text-anchor="middle" class="m">after fork, parent and child share it</text>
<text x="250.0" y="219.5" text-anchor="middle" class="m">until one writes: then it is copied</text>
<text x="250.0" y="235.5" text-anchor="middle" class="m">used by: the heap (malloc), thread stacks</text>
<text x="250.0" y="251.5" text-anchor="middle" class="m">maps: rw-p  (no path)</text>
<rect x="383" y="160" width="250" height="110" rx="6" class="g"/>
<text x="508.0" y="187.5" text-anchor="middle">zero-filled memory, shared</text>
<text x="508.0" y="203.5" text-anchor="middle" class="m">after fork, parent and child keep</text>
<text x="508.0" y="219.5" text-anchor="middle" class="m">using the same pages</text>
<text x="508.0" y="235.5" text-anchor="middle" class="m">used by: PostgreSQL&#x27;s shared buffers</text>
<text x="508.0" y="251.5" text-anchor="middle" class="m">maps: rw-s  /dev/zero (deleted)</text>
<text x="377" y="292" text-anchor="middle" class="m">the 4th letter of the permissions in /proc/&lt;pid&gt;/maps: p = private, s = shared</text>
</svg>
</div>

**Who uses which:**

| Mapping | Typical use |
|---|---|
| private, file-backed | the code and data of programs and shared libraries. A write to a global variable copies its page; the library file on disk never changes |
| shared, file-backed | a database that reads and writes its file through memory, such as LMDB; several processes sharing a file |
| private, anonymous | ordinary memory: `malloc` gets large blocks this way, and thread stacks are made this way |
| shared, anonymous | memory a process shares with the children it forks. PostgreSQL's main shared memory, which holds its cache of pages, is made this way by default on Linux |

**Telling them apart.** Each line of `/proc/<pid>/maps` describes one mapping: address range, permissions, offset in the file, device, inode and path. The 4th letter of the permissions is `p` for private or `s` for shared. A Rust program that makes one mapping of each kind and prints its own lines, without the address range:

```rust
use std::fs::{self, OpenOptions};
use std::os::fd::AsRawFd;

extern "C" {
    fn mmap(
        addr: *mut u8,
        len: usize,
        prot: i32,
        flags: i32,
        fd: i32,
        offset: i64,
    ) -> *mut u8;
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

/// The line of /proc/self/maps whose address range holds `p`,
/// without the range itself.
fn maps_line(p: *mut u8) -> String {
    let maps = fs::read_to_string("/proc/self/maps").unwrap();
    for line in maps.lines() {
        let (range, rest) = line.split_once(' ').unwrap();
        let (lo, hi) = range.split_once('-').unwrap();
        let lo = usize::from_str_radix(lo, 16).unwrap();
        let hi = usize::from_str_radix(hi, 16).unwrap();
        if (lo..hi).contains(&(p as usize)) {
            return rest
                .split_whitespace()
                .collect::<Vec<_>>()
                .join(" ");
        }
    }
    panic!("no mapping holds {p:?}");
}

fn main() {
    let path = std::env::temp_dir().join("kinds.dat");
    fs::write(&path, [b'x'; LEN]).unwrap();
    let file =
        OpenOptions::new().read(true).write(true).open(&path).unwrap();
    let fd = file.as_raw_fd();

    let kinds = [
        ("private file", map(MAP_PRIVATE, fd)),
        ("shared file", map(MAP_SHARED, fd)),
        ("private anonymous", map(MAP_PRIVATE | MAP_ANONYMOUS, -1)),
        ("shared anonymous", map(MAP_SHARED | MAP_ANONYMOUS, -1)),
    ];
    for (name, p) in kinds {
        let line = maps_line(p);
        println!("{name:<17} {line}");
        // the 4th letter of the permissions: p = private, s = shared
        let shared = name.starts_with("shared");
        assert!(line.starts_with(if shared { "rw-s" } else { "rw-p" }));
    }
}
```

```text
private file      rw-p 00000000 fe:00 681454 /tmp/kinds.dat
shared file       rw-s 00000000 fe:00 681454 /tmp/kinds.dat
private anonymous rw-p 00000000 00:00 0
shared anonymous  rw-s 00000000 00:01 24 /dev/zero (deleted)
```

- The file mappings show the file's device, inode and path.
- Private anonymous memory has no file: device `00:00`, inode 0, no path.
- Shared anonymous memory does have a file behind it: the kernel creates a hidden file on its internal *tmpfs*, a file system that keeps its files only in memory. That file is called `/dev/zero` and has already been deleted, so nothing else can open it.

The same in an ordinary program, here `awk` reading its own maps (field 2 is the permissions, field 6 the path):

```sh
$ awk '/libc|heap|stack/ {print $2, $6}' /proc/self/maps
rw-p [heap]
r--p /usr/lib/x86_64-linux-gnu/libc.so.6
r-xp /usr/lib/x86_64-linux-gnu/libc.so.6
r--p /usr/lib/x86_64-linux-gnu/libc.so.6
r--p /usr/lib/x86_64-linux-gnu/libc.so.6
rw-p /usr/lib/x86_64-linux-gnu/libc.so.6
rw-p [stack]
```

The C library is mapped five times, all private and file-backed: its code (`r-xp`, readable and executable), read-only data, and writable data (`rw-p`). The heap and the stack are private anonymous memory, which the kernel labels `[heap]` and `[stack]`.
