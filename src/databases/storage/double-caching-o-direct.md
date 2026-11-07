What is **double caching** in a database server, how does opening files with `O_DIRECT` avoid it, and what does `O_DIRECT` demand in return? How do InnoDB (MySQL) and PostgreSQL differ here?

---

**Double caching.** A database engine keeps recently used pages in memory in its own cache, its *buffer pool*. An ordinary `read()` first copies the page from disk into the kernel's *page cache* (the kernel's copy of file data in RAM), then into the buffer pool. The same page now sits in RAM **twice**, and memory used by one copy is memory the other cache can't use.

<div class="diagram">
<svg viewBox="0 0 640 236" width="100%" style="max-width:640px" role="img" aria-label="With buffered I/O a page can sit both in the database&#x27;s cache and in the OS page cache. With O_DIRECT the database reads and writes the disk directly, so only its own cache holds the page.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .bolt{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="do" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="dg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="160" y="22" text-anchor="middle">PostgreSQL: buffered I/O</text>
<text x="480" y="22" text-anchor="middle">InnoDB: O_DIRECT</text>
<rect x="20" y="34" width="280" height="40" rx="6" class="g"/>
<text x="160.0" y="50.5" text-anchor="middle">shared_buffers</text>
<text x="160.0" y="66.5" text-anchor="middle" class="m">page 42 cached here</text>
<rect x="20" y="100" width="280" height="40" rx="6" class="r"/>
<text x="160.0" y="116.5" text-anchor="middle">OS page cache</text>
<text x="160.0" y="132.5" text-anchor="middle" class="m">page 42 cached here too</text>
<rect x="20" y="166" width="280" height="36" rx="6" class="k"/>
<text x="160.0" y="188.5" text-anchor="middle">disk</text>
<line x1="160" y1="76" x2="160" y2="98" class="ln" marker-end="url(#ah)"/>
<line x1="160" y1="142" x2="160" y2="164" class="ln" marker-end="url(#ah)"/>
<rect x="340" y="34" width="280" height="40" rx="6" class="g"/>
<text x="480.0" y="50.5" text-anchor="middle">buffer pool</text>
<text x="480.0" y="66.5" text-anchor="middle" class="m">page 42 cached here only</text>
<rect x="340" y="100" width="280" height="40" rx="6" class="c" stroke-dasharray="5 4"/>
<text x="465" y="124" text-anchor="middle" class="m">OS page cache: bypassed</text>
<rect x="340" y="166" width="280" height="36" rx="6" class="k"/>
<text x="480.0" y="188.5" text-anchor="middle">disk</text>
<path d="M600 76 V164" class="pg" marker-end="url(#dg)"/>
<text x="320" y="226" text-anchor="middle" class="m">buffered: memory holds two copies; O_DIRECT: one copy, but I/O must be aligned</text>
</svg>
</div>

**`O_DIRECT`** is a flag for `open()` that makes reads and writes go straight between the disk and the program's own memory, skipping the page cache.

**A demonstration** on Linux. `fincore` reports how much of a file is in the page cache. `dd` with `oflag=direct` or `iflag=direct` opens the file with `O_DIRECT`:

```sh
$ dd if=/dev/urandom of=normal.dat bs=1M count=32 status=none
$ dd if=/dev/urandom of=direct.dat bs=1M count=32 oflag=direct status=none
$ fincore normal.dat direct.dat
  RES PAGES SIZE FILE
  32M  8192  32M normal.dat
   0B     0  32M direct.dat
$ dd if=direct.dat of=/dev/null bs=1M iflag=direct status=none
$ fincore direct.dat
RES PAGES SIZE FILE
 0B     0  32M direct.dat
$ cat direct.dat > /dev/null
$ fincore direct.dat
  RES PAGES SIZE FILE
  32M  8192  32M direct.dat
```

- the ordinary write left all 8,192 pages (32 MiB) of `normal.dat` in the page cache;
- writing and reading `direct.dat` with `O_DIRECT` left none;
- one ordinary read with `cat` put the whole file there.

**What `O_DIRECT` demands.**

**1. Alignment.** The file offset, the length and the address of the memory buffer must be multiples of the disk's logical block size, typically 512 bytes. Otherwise the call fails. Reading 1,000 bytes fails, reading 512 succeeds:

```sh
$ dd if=direct.dat of=/dev/null bs=1000 count=1 iflag=direct status=none
dd: error reading 'direct.dat': Invalid argument
$ dd if=direct.dat of=/dev/null bs=512 count=1 iflag=direct status=none
```

Database pages are powers of two from 4 KiB up, so they meet this naturally.

**2. No help from the kernel.** No caching and no read-ahead: every page the engine doesn't hold itself is a disk read, so its own buffer pool must be large and it must do its own prefetching.

**3. Still `fsync`.** `O_DIRECT` skips the page cache, but doesn't promise the data is on stable storage: the drive may still hold it in its own write cache. The engine still has to call `fsync`.

**InnoDB** uses `O_DIRECT` by default on Linux (`innodb_flush_method`). The manual: "InnoDB uses O_DIRECT ... to open the data files, and uses fsync() to flush both the data and log files", and "O_DIRECT can help to avoid double buffering between the InnoDB buffer pool and the operating system file system cache." It also says that on dedicated servers "up to 80% of physical memory is often assigned to the buffer pool."

**PostgreSQL** reads through the page cache, so a page can be in both caches. It accepts this and keeps its own cache, `shared_buffers`, moderate: "a reasonable starting value for shared_buffers is 25% of the memory in your system", and "because PostgreSQL also relies on the operating system cache, it is unlikely that an allocation of more than 40% of RAM to shared_buffers will work better than a smaller amount." The kernel's page cache then uses much of the remaining memory as a second level of cache.
