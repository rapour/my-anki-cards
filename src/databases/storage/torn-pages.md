What is a **torn page** in a database, how does a crash create one, and what does PostgreSQL do when it finds one and has nothing to repair it with?

---

A **torn page** is a database page on disk that is **part new and part old**, because a crash interrupted its write.

**How it happens.** A PostgreSQL page is 8 KiB, but a disk usually guarantees only 4 KiB at a time to be written all or nothing. So writing one page is two device writes. If power fails after the first, the page on disk has a new first half and an old second half.

<div class="diagram">
<svg viewBox="0 0 640 204" width="100%" style="max-width:640px" role="img" aria-label="A torn page: the page on disk was old, the new version was being written, and power failed after the first 4 KiB. The page on disk is now half new and half old.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .bolt{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="do" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="dg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="158" y="44" text-anchor="end">on disk before</text>
<rect x="171" y="24" width="198" height="30" rx="2" class="c"/>
<text x="270.0" y="44" text-anchor="middle">old (first 4 KiB)</text>
<rect x="371" y="24" width="198" height="30" rx="2" class="c"/>
<text x="470.0" y="44" text-anchor="middle">old (second 4 KiB)</text>
<text x="158" y="94" text-anchor="end">in memory, to write</text>
<rect x="171" y="74" width="198" height="30" rx="2" class="cg"/>
<text x="270.0" y="94" text-anchor="middle">new (first 4 KiB)</text>
<rect x="371" y="74" width="198" height="30" rx="2" class="cg"/>
<text x="470.0" y="94" text-anchor="middle">new (second 4 KiB)</text>
<text x="158" y="144" text-anchor="end">on disk after the crash</text>
<rect x="171" y="124" width="198" height="30" rx="2" class="cg"/>
<text x="270.0" y="144" text-anchor="middle">new (first 4 KiB)</text>
<rect x="371" y="124" width="198" height="30" rx="2" class="cr"/>
<text x="470.0" y="144" text-anchor="middle">old (second 4 KiB)</text>
<path d="M370 114 l-7 14 h6 l-4 12 l12 -16 h-6 l5 -10 z" class="bolt"/>
<text x="370" y="176" text-anchor="middle" class="to">the header and checksum belong to the new page, half the rows to the old one</text>
<text x="370" y="194" text-anchor="middle" class="m">checksum on: the page fails verification. checksum off: wrong data, no error</text>
</svg>
</div>

**Why the log can't simply redo it.** PostgreSQL records every change in its *write-ahead log* (WAL) before the changed page may reach the disk. After a crash it *replays* the WAL, redoing each change. Usually a WAL record holds only the change itself, such as "row 1 on page 0 now has this value". Applying that needs a page that is consistent to start with. A torn page isn't: its header, written in the new half, describes rows the old half doesn't hold.

**An experiment** with PostgreSQL 16, with `full_page_writes` off so that nothing repairs the page:

1. Create table `t` with 40 rows, each with `v = repeat('x', 120)`. They fill most of one 8 KiB page. `CHECKPOINT` writes that page to disk.
2. `UPDATE t SET v = repeat('y', 120)` changes every row, in memory.
3. Crash the server before it writes the page (`pg_ctl stop -m immediate`). Then write a torn page into the table's file by hand: the first 4 KiB of the new page, then the last 4 KiB of the old one.
4. Start the server again.

**With data checksums on** (each page stores a checksum of its contents, checked on every read), recovery finds the damage and stops. The server does not start:

```text
WARNING:  page verification failed, calculated checksum 46616 but expected 61972
FATAL:  invalid page in block 0 of relation base/5/16429
```

**Without checksums**, it starts and gives wrong answers, with no error at all:

```sql
SELECT left(v, 3) AS v, count(*) FROM t GROUP BY 1 ORDER BY 1;
```

```text
  v  | count
-----+-------
 xxx |    27
 yyy |    40
```

That's 67 rows in a table of 40. An `UPDATE` doesn't overwrite a row: it writes a new version of the row and marks the old version as replaced, in that old version's header. 27 of the old versions had their headers in the second half of the page. The torn page kept the old second half, so it lost those 27 marks, and the 27 old rows came back beside their new versions.

**The lesson:** a checksum can **detect** a torn page but can't **repair** it. Repair needs a complete copy of the page kept somewhere else:

- PostgreSQL's **full-page writes** put a copy of the whole page in the WAL;
- InnoDB's **doublewrite buffer** (MySQL) writes each page to a separate area before writing it in its place.

The alternative is a page no bigger than what the device writes all or nothing.
