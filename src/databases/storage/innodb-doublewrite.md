How does InnoDB's **doublewrite buffer** stop a crash from leaving a half-written page in MySQL's data files, and why doesn't writing every page twice double the I/O cost?

---

**The problem.** InnoDB, MySQL's storage engine, stores data in 16 KiB pages. A disk usually guarantees only 4 KiB at a time to be written all or nothing. A crash in the middle of a page write can leave a **torn page**: part new, part old. InnoDB's redo log records only changes to pages, and a change can't be applied to a page that is half one version and half another.

**The fix.** The MySQL manual: "The doublewrite buffer is a storage area where InnoDB writes pages flushed from the buffer pool before writing the pages to their proper positions in the InnoDB data files." Despite its name it is on disk. The *buffer pool* is InnoDB's cache of pages in memory. Flushing changed pages takes two steps:

1. write the pages to the doublewrite area, and `fsync` (wait until they are really on disk);
2. then write each page to its own place in the data files.

<div class="diagram">
<svg viewBox="0 0 640 188" width="100%" style="max-width:640px" role="img" aria-label="InnoDB&#x27;s doublewrite buffer: pages go first to the doublewrite area in one sequential write, then to their places. If a page is torn in its place, recovery copies the complete version from the doublewrite area.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .bolt{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="do" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="dg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<rect x="20" y="30" width="150" height="56" rx="6" class="k"/>
<text x="95.0" y="54.5" text-anchor="middle">buffer pool</text>
<text x="95.0" y="70.5" text-anchor="middle" class="m">dirty 16 KiB pages</text>
<rect x="245" y="30" width="160" height="56" rx="6" class="g"/>
<text x="325.0" y="54.5" text-anchor="middle">doublewrite area</text>
<text x="325.0" y="70.5" text-anchor="middle" class="m">one sequential write + fsync</text>
<rect x="470" y="30" width="150" height="56" rx="6" class="k"/>
<text x="545.0" y="54.5" text-anchor="middle">data files</text>
<text x="545.0" y="70.5" text-anchor="middle" class="m">each page in its place</text>
<path d="M172 58 H243" class="pg" marker-end="url(#dg)"/>
<text x="207" y="50" text-anchor="middle" class="tg">1</text>
<path d="M407 58 H468" class="pg" marker-end="url(#dg)"/>
<text x="437" y="50" text-anchor="middle" class="tg">2</text>
<path d="M325 88 V112 H545 V90" class="pg" marker-end="url(#dg)"/>
<text x="435" y="128" text-anchor="middle" class="tg">3. after a crash: recovery copies the good page back</text>
<text x="320" y="156" text-anchor="middle" class="to">crash during step 2: a data page is torn, but its copy in the doublewrite area is complete</text>
<text x="320" y="176" text-anchor="middle" class="m">crash during step 1: the copy may be torn, but the data page was not touched yet</text>
</svg>
</div>

**After a crash**, InnoDB checks each page with the checksum stored in it. One step is always intact:

- crash during step 2: the page in its place may be torn, but its copy in the doublewrite area is complete. Recovery copies it back. In the manual's words, "InnoDB can find a good copy of the page from the doublewrite buffer during crash recovery."
- crash during step 1: the copy may be torn, but the page in its place hasn't been touched yet. It is still the complete old version, and the redo log brings it up to date.

**A simulation in Rust.** A disk that writes 4 KiB sectors one at a time and loses power after `budget` of them. The test cuts the power at every point of a page write:

```rust
// The disk writes 4 KiB at a time, all or nothing; an InnoDB page is
// 16 KiB, so writing one page takes 4 separate sector writes.
const SECTOR: usize = 4096;
const PAGE: usize = 16384;

/// A disk that loses power after `budget` more sector writes.
struct Disk {
    bytes: Vec<u8>,
    budget: usize,
}

impl Disk {
    /// Write sector by sector; Err if the power went out part-way.
    fn write(&mut self, at: usize, data: &[u8]) -> Result<(), ()> {
        for (i, sector) in data.chunks(SECTOR).enumerate() {
            if self.budget == 0 {
                return Err(());
            }
            self.budget -= 1;
            let start = at + i * SECTOR;
            self.bytes[start..start + SECTOR].copy_from_slice(sector);
        }
        Ok(())
    }
}

/// FNV-1a hash of the page body; the page's last 4 bytes store it.
fn checksum(body: &[u8]) -> u32 {
    let mut h = 0x811c_9dc5u32;
    for &b in body {
        h = (h ^ b as u32).wrapping_mul(0x0100_0193);
    }
    h
}

fn make_page(fill: u8) -> Vec<u8> {
    let mut page = vec![fill; PAGE];
    let sum = checksum(&page[..PAGE - 4]);
    page[PAGE - 4..].copy_from_slice(&sum.to_le_bytes());
    page
}

fn page_ok(page: &[u8]) -> bool {
    let stored = &page[PAGE - 4..];
    checksum(&page[..PAGE - 4]).to_le_bytes() == stored
}

// disk layout: [doublewrite area: one page][data file: one page]
const DOUBLEWRITE: usize = 0;
const DATA: usize = PAGE;

/// Write a page the InnoDB way: first to the doublewrite area,
/// then to its real place. (InnoDB also fsyncs between the two.)
fn write_page(disk: &mut Disk, page: &[u8]) -> Result<(), ()> {
    disk.write(DOUBLEWRITE, page)?;
    disk.write(DATA, page)
}

/// Crash recovery: a torn data page is replaced by the copy in the
/// doublewrite area, if that copy is complete.
fn recover(disk: &mut Disk) {
    let (dw, data) = disk.bytes.split_at_mut(DATA);
    if !page_ok(data) && page_ok(dw) {
        data.copy_from_slice(dw);
    }
}

fn main() {
    let (old, new) = (make_page(b'o'), make_page(b'n'));
    let both_old = [old.clone(), old.clone()].concat();

    // Without doublewrite: power fails after 2 of the 4 sectors.
    let mut disk = Disk { bytes: both_old.clone(), budget: 2 };
    assert!(disk.write(DATA, &new).is_err());
    let data = &disk.bytes[DATA..];
    // half new, half old: torn, and the checksum shows it
    assert_eq!((data[0], data[PAGE - 5]), (b'n', b'o'));
    assert!(!page_ok(data));

    // With doublewrite: power fails after any of the 8 sector writes.
    for budget in 0..=8 {
        let mut disk = Disk { bytes: both_old.clone(), budget };
        let _ = write_page(&mut disk, &new);
        recover(&mut disk);
        let data = &disk.bytes[DATA..];
        // never torn: either the whole old page or the whole new one
        assert!(page_ok(data));
        let state = if data[0] == b'n' { "new" } else { "old" };
        assert_eq!(state, if budget <= 4 { "old" } else { "new" });
        println!("power lost after {budget} sector writes: {state}");
    }
}
```

It prints, and the assertions check:

```text
power lost after 0 sector writes: old
power lost after 1 sector writes: old
power lost after 2 sector writes: old
power lost after 3 sector writes: old
power lost after 4 sector writes: old
power lost after 5 sector writes: new
power lost after 6 sector writes: new
power lost after 7 sector writes: new
power lost after 8 sector writes: new
```

Writes 1 to 4 fill the doublewrite area, 5 to 8 the data page. Without the doublewrite step, the same power cut after 2 sectors leaves a torn page that fails its checksum. With it, the data page is always a whole page: the old one if the copy wasn't finished, the new one otherwise.

**Why it isn't twice the cost.** The manual: "Although data is written twice, the doublewrite buffer does not require twice as much I/O overhead or twice as many I/O operations. Data is written to the doublewrite buffer in a large sequential chunk, with a single `fsync()` call to the operating system." Many pages go to the doublewrite area together, as one sequential write. The scattered writes to their places would happen anyway.

**Settings:** `innodb_doublewrite` is `ON` by default. `DETECT_ONLY` writes no page contents to the doublewrite area, so it can only detect incomplete page writes, not fix them. `OFF` removes the protection; the manual suggests it for when performance matters more than data integrity, such as benchmarks.

PostgreSQL solves the same problem differently: it puts a copy of the whole page in its write-ahead log, the first time the page changes after each checkpoint.
