How does PostgreSQL's `full_page_writes` setting protect against **torn pages** (pages left half new and half old by a crash during their write)? Why is it enough to act only on the first change to a page after a checkpoint, and what does it cost?

---

Two terms first:

- **WAL**, the *write-ahead log*: the file where PostgreSQL records each change before the changed page may be written to disk. After a crash it *replays* the WAL to redo the changes.
- **checkpoint**: a moment by which every changed page in memory has been written to disk. Replay starts from the last checkpoint, because everything before it is already safely on disk.

With `full_page_writes = on`, the default, the **first change to a page after each checkpoint** writes a copy of the whole page into the WAL: a *full-page image*. Later changes to that page, until the next checkpoint, log only the change.

<div class="diagram">
<svg viewBox="0 0 640 228" width="100%" style="max-width:640px" role="img" aria-label="PostgreSQL full-page writes: the first change to a page after a checkpoint puts the whole page into the WAL. After a crash, replay starts at the checkpoint, writes that image over the possibly torn page, then applies later changes.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .bolt{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="do" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="dg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<line x1="30" y1="70" x2="610" y2="70" class="ln"/>
<circle cx="60" cy="70" r="6" class="c"/>
<text x="60" y="50" text-anchor="middle">checkpoint</text>
<text x="60" y="94" text-anchor="middle" class="m">redo starts here</text>
<circle cx="190" cy="70" r="6" class="cg"/>
<text x="190" y="50" text-anchor="middle" class="tg">change 1</text>
<text x="190" y="94" text-anchor="middle" class="m">WAL: whole page, 6,381 B</text>
<circle cx="350" cy="70" r="6" class="c"/>
<text x="350" y="50" text-anchor="middle">change 2</text>
<text x="350" y="94" text-anchor="middle" class="m">WAL: the change, 82 B</text>
<circle cx="490" cy="70" r="6" class="cr"/>
<text x="490" y="50" text-anchor="middle" class="to">crash</text>
<text x="490" y="94" text-anchor="middle" class="m">page on disk torn</text>
<text x="320" y="130" text-anchor="middle">recovery replays the WAL from the checkpoint:</text>
<rect x="40" y="146" width="250" height="46" rx="6" class="g"/>
<text x="165.0" y="165.5" text-anchor="middle">1. write the image of change 1</text>
<text x="165.0" y="181.5" text-anchor="middle" class="m">the whole page, torn or not, is replaced</text>
<path d="M292 169 H346" class="pg" marker-end="url(#dg)"/>
<rect x="350" y="146" width="250" height="46" rx="6" class="k"/>
<text x="475.0" y="165.5" text-anchor="middle">2. apply change 2 on top</text>
<text x="475.0" y="181.5" text-anchor="middle" class="m">and every later change to the page</text>
<text x="320" y="216" text-anchor="middle" class="m">only the first change after each checkpoint carries an image, so WAL replay always finds one</text>
</svg>
</div>

**Why once per checkpoint is enough.** A page can only be torn by a write that happens after the last checkpoint, since every earlier write had finished. A page is only written because it was changed, and the first change after the checkpoint logged an image. Replay meets that image first and writes it over the page, torn or not, without reading the page from disk. Then it applies the later changes on top. The documentation:

> Because WAL replay always starts from a checkpoint, it is sufficient to do this during the first change of each page after a checkpoint.

**Measured** on PostgreSQL 16, with 8 KiB pages and a table `t` of 40 rows on one page:

```sql
CHECKPOINT;
UPDATE t SET v = 'first change' WHERE id = 1;
UPDATE t SET v = 'second change' WHERE id = 2;
```

`pg_waldump` prints WAL records. The two updates, shortened:

```text
rmgr: Heap  len (rec/tot): 65/ 6381, desc: HOT_UPDATE ... blk 0 FPW
rmgr: Heap  len (rec/tot): 82/   82, desc: HOT_UPDATE ... blk 0
```

- The first update after the checkpoint: 65 bytes for the change, 6,381 in total. `FPW` marks the page image. It is smaller than 8 KiB because the image leaves out the page's unused middle.
- The second update to the same page: 82 bytes.

**It repairs a torn page.** In the same setup, update all 40 rows, crash the server before it writes the page, and put a torn page in the file: the first 4 KiB new, the last 4 KiB old. After a restart:

| `full_page_writes` | Result |
|---|---|
| `on` | 40 rows, all with the new value |
| `off`, data checksums on | recovery stops: `FATAL: invalid page in block 0` |
| `off`, no checksums | 67 rows: 27 old versions came back beside the 40 new ones |

The documentation warns of exactly these two failures: "Turning this parameter off speeds normal operation, but might lead to either unrecoverable data corruption, or silent data corruption, after a system failure." It should be turned off only in the circumstances in which turning off `fsync` would be safe.

**With data checksums on**, even a change that only sets *hint bits* (status flags that a read stores in a row's header) logs a full-page image, as a record called `FPI_FOR_HINT`. Hint bits are not otherwise logged, so a torn page that differed only in them would fail its checksum and there would be nothing to repair it from.

**The cost** is WAL volume: right after each checkpoint, almost every page touched adds a whole page image to the WAL. Ways to reduce it:

- checkpoints further apart (`checkpoint_timeout`, `max_wal_size`), at the price of a longer replay after a crash;
- `wal_compression`, which compresses the images.
