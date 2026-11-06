A database engine, the operating system and the storage device all work in units called "pages". What are these three kinds of page, how big is each one usually, and why does it matter that a database page is often bigger than the other two?

---

| Page | Used by | For | Usual size |
|---|---|---|---|
| **database page** | the database engine | reading, writing, caching and checksumming its files | PostgreSQL 8 KiB, InnoDB (MySQL) 16 KiB, SQLite 4 KiB |
| **OS page** | the kernel | virtual memory and the *page cache*, its copy of file data in RAM | 4 KiB on x86-64, plus *huge pages* of 2 MiB or 1 GiB |
| **hardware page** | the storage device | the largest write it guarantees is **all or nothing** | usually 4 KiB |

*All or nothing* means: if power fails during the write, the device afterwards holds either all the old bytes or all the new ones, never a mix. The CMU database course defines a hardware page as "the largest block of data that the storage device can guarantee failsafe writes".

The file system's block, the unit it gives out disk space in, is usually 4 KiB as well.

<div class="diagram">
<svg viewBox="0 0 640 242" width="100%" style="max-width:640px" role="img" aria-label="An 8 KiB database page covers two 4 KiB OS pages, file-system blocks and hardware pages, and sixteen 512-byte sectors. Only each 4 KiB hardware page is written all or nothing, so a crash can leave the database page half written.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .bolt{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="do" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="dg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="190" y="45" text-anchor="end" style="font-size:12px">database page</text>
<text x="190" y="59" text-anchor="end" class="m">8 KiB in PostgreSQL</text>
<rect x="201.0" y="30" width="418.0" height="30" rx="2" class="k"/>
<text x="410.0" y="50" text-anchor="middle">one database page</text>
<text x="190" y="93" text-anchor="end" style="font-size:12px">OS pages, file-system blocks</text>
<text x="190" y="107" text-anchor="end" class="m">4 KiB each</text>
<rect x="201.0" y="78" width="208.0" height="30" rx="2" class="c"/>
<rect x="411.0" y="78" width="208.0" height="30" rx="2" class="c"/>
<text x="190" y="141" text-anchor="end" style="font-size:12px">hardware pages</text>
<text x="190" y="155" text-anchor="end" class="m">usually 4 KiB, all or nothing</text>
<rect x="201.0" y="126" width="208.0" height="30" rx="2" class="cg"/>
<rect x="411.0" y="126" width="208.0" height="30" rx="2" class="cg"/>
<text x="190" y="189" text-anchor="end" style="font-size:12px">logical sectors</text>
<text x="190" y="203" text-anchor="end" class="m">512 B each</text>
<rect x="201.0" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="227.25" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="253.5" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="279.75" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="306.0" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="332.25" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="358.5" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="384.75" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="411.0" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="437.25" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="463.5" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="489.75" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="516.0" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="542.25" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="568.5" y="174" width="24.25" height="30" rx="2" class="c"/>
<rect x="594.75" y="174" width="24.25" height="30" rx="2" class="c"/>
<line x1="410.0" y1="66" x2="410.0" y2="212" class="po" stroke-dasharray="5 4"/>
<text x="410.0" y="230" text-anchor="middle" class="to">a crash can stop between the two 4 KiB halves: the page is then torn</text>
</svg>
</div>

**Why it matters.** If the database page is bigger than the hardware page, writing one database page takes several device writes. A crash between them leaves a **torn page**: part new and part old. So PostgreSQL and InnoDB, with 8 and 16 KiB pages, each need a way to repair one: PostgreSQL's *full-page writes* and InnoDB's *doublewrite buffer*. SQLite doesn't even trust a sector: its documentation says "SQLite has traditionally assumed that a sector write is not atomic."

The sizes are all powers of two, so a database page always covers whole OS pages and whole sectors, and never shares one with its neighbour.

**On a real machine** (Linux, ext4 on a virtual disk):

```sh
$ getconf PAGESIZE
4096
$ stat -fc %S /
4096
$ grep Hugepagesize /proc/meminfo
Hugepagesize:       2048 kB
$ lsblk -o NAME,LOG-SEC,PHY-SEC /dev/vda
NAME LOG-SEC PHY-SEC
vda      512    4096
```

- `getconf PAGESIZE`: the OS page.
- `stat -fc %S /`: the block size of the file system mounted at `/` (`-f` asks about the file system, `%S` prints its block size).
- `Hugepagesize`: the default huge page.
- `lsblk`: the disk accepts writes in 512-byte *logical* sectors, but stores data in 4 KiB *physical* sectors. A drive like this handles a smaller write by reading, changing and rewriting a whole 4 KiB sector.

And the database pages:

```sql
SHOW block_size;          -- PostgreSQL: 8192
PRAGMA page_size;         -- SQLite, new database: 4096
SELECT @@innodb_page_size; -- MySQL: 16384 by default
```

**Each one is fixed early.** PostgreSQL's page size is chosen when it is compiled. InnoDB's `innodb_page_size`, from 4 KiB to 64 KiB, is set once, when the MySQL instance is first initialised. SQLite's `PRAGMA page_size`, from 512 bytes to 64 KiB, takes effect only on a new database or after `VACUUM`.
