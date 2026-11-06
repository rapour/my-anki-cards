Why does a database engine keep its own cache of pages in memory, a **buffer pool**, instead of leaving caching to the operating system's page cache? Give the main reasons, and work through an example where the operating system's usual policy fails.

---

- The **OS page cache** is the kernel's copy of recently used file data in RAM. All programs share it, and the kernel runs it with one general policy: roughly, evict the *least recently used* (LRU) page.
- A **buffer pool** is memory the database engine manages itself, divided into *frames* of one page each. The engine decides which pages stay, which to read early and when changed pages go to disk.

**The reasons**, from Michael Stonebraker's paper *Operating System Support for Database Management* (1981):

1. **Replacement.** "Although the folklore indicates that LRU is a generally good tactic for buffer management, it appears to perform only marginally in a database environment." The engine knows its query plan. A page read once by a large scan won't be needed again; the root page of an index will be needed constantly.
2. **Prefetch.** The kernel reads ahead only when it sees a program reading a file in order. The engine knows which pages it will need next, even when they are scattered, such as the leaf pages of an index.
3. **Write order.** Crash recovery depends on order: the log record must reach the disk before the page it describes, and the commit record after everything the transaction wrote. In the scheme Stonebraker describes, a transaction first writes an *intentions list* (the changes it will make) and then a commit flag, and he asks for "a selected force out which would push the intentions list and the commit flag to disk in the proper order. Such a service is not present in any buffer manager known to us."
4. **Pinning.** A page the engine is working on must not be evicted until it says so.

Ramakrishnan and Gehrke's *Database Management Systems* sums it up: a DBMS "needs features not found in many OS's, e.g., forcing a page to disk, controlling the order of page writes to disk, files spanning disks, ability to control pre-fetching and page replacement policy based on predictable access patterns".

**Worked example: sequential flooding.** A table of 11 pages is scanned from start to end again and again, through a cache of 10 frames. This happens, for example, in a *nested-loop join*, which reads the inner table once for each row of the outer one.

<div class="diagram">
<svg viewBox="0 0 640 196" width="100%" style="max-width:640px" role="img" aria-label="Sequential flooding: with 10 frames and an 11-page table, LRU evicts the page the next scan needs first, so every request misses.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .bolt{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="do" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="dg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="20" y="22" text-anchor="start">LRU buffer pool with 10 frames, a table of 11 pages scanned again and again</text>
<rect x="21" y="40" width="40" height="30" rx="2" class="cr"/>
<text x="41.0" y="60" text-anchor="middle">1</text>
<rect x="65" y="40" width="40" height="30" rx="2" class="c"/>
<text x="85.0" y="60" text-anchor="middle">2</text>
<rect x="109" y="40" width="40" height="30" rx="2" class="c"/>
<text x="129.0" y="60" text-anchor="middle">3</text>
<rect x="153" y="40" width="40" height="30" rx="2" class="c"/>
<text x="173.0" y="60" text-anchor="middle">4</text>
<rect x="197" y="40" width="40" height="30" rx="2" class="c"/>
<text x="217.0" y="60" text-anchor="middle">5</text>
<rect x="241" y="40" width="40" height="30" rx="2" class="c"/>
<text x="261.0" y="60" text-anchor="middle">6</text>
<rect x="285" y="40" width="40" height="30" rx="2" class="c"/>
<text x="305.0" y="60" text-anchor="middle">7</text>
<rect x="329" y="40" width="40" height="30" rx="2" class="c"/>
<text x="349.0" y="60" text-anchor="middle">8</text>
<rect x="373" y="40" width="40" height="30" rx="2" class="c"/>
<text x="393.0" y="60" text-anchor="middle">9</text>
<rect x="417" y="40" width="40" height="30" rx="2" class="c"/>
<text x="437.0" y="60" text-anchor="middle">10</text>
<text x="468" y="54" text-anchor="start" style="font-size:11px">scan asks for page 11:</text>
<text x="468" y="69" text-anchor="start" class="to" style="font-size:11px">miss, evict page 1</text>
<rect x="21" y="88" width="40" height="30" rx="2" class="cr"/>
<text x="41.0" y="108" text-anchor="middle">2</text>
<rect x="65" y="88" width="40" height="30" rx="2" class="c"/>
<text x="85.0" y="108" text-anchor="middle">3</text>
<rect x="109" y="88" width="40" height="30" rx="2" class="c"/>
<text x="129.0" y="108" text-anchor="middle">4</text>
<rect x="153" y="88" width="40" height="30" rx="2" class="c"/>
<text x="173.0" y="108" text-anchor="middle">5</text>
<rect x="197" y="88" width="40" height="30" rx="2" class="c"/>
<text x="217.0" y="108" text-anchor="middle">6</text>
<rect x="241" y="88" width="40" height="30" rx="2" class="c"/>
<text x="261.0" y="108" text-anchor="middle">7</text>
<rect x="285" y="88" width="40" height="30" rx="2" class="c"/>
<text x="305.0" y="108" text-anchor="middle">8</text>
<rect x="329" y="88" width="40" height="30" rx="2" class="c"/>
<text x="349.0" y="108" text-anchor="middle">9</text>
<rect x="373" y="88" width="40" height="30" rx="2" class="c"/>
<text x="393.0" y="108" text-anchor="middle">10</text>
<rect x="417" y="88" width="40" height="30" rx="2" class="c"/>
<text x="437.0" y="108" text-anchor="middle">11</text>
<text x="468" y="102" text-anchor="start" style="font-size:11px">next scan asks for page 1:</text>
<text x="468" y="117" text-anchor="start" class="to" style="font-size:11px">miss, evict page 2</text>
<text x="20" y="140" text-anchor="start" class="m">frames in LRU order, oldest on the left; the orange page is evicted next</text>
<text x="320" y="166" text-anchor="middle">each scan evicts exactly the page the next scan needs first: every request misses</text>
<text x="320" y="184" text-anchor="middle" class="m">simulated: 0 hits of 110 requests with LRU, 90 with MRU</text>
</svg>
</div>

With LRU, the page evicted is always the one the scan will ask for soonest, so **every** request goes to disk. Evicting the *most* recently used page (MRU) instead keeps most of the table across scans. Ramakrishnan and Gehrke: "# buffer frames < # pages in file means each page request causes an I/O. MRU much better in this situation (but not in all situations, of course)."

```rust
use std::collections::VecDeque;

/// Run page requests through a buffer pool of `frames` pages and
/// count the hits (pages already in memory). `mru` picks the policy
/// that evicts the most recently used page instead of the least.
fn hits(requests: &[u32], frames: usize, mru: bool) -> usize {
    // pages in memory, least recently used first
    let mut pool: VecDeque<u32> = VecDeque::new();
    let mut hits = 0;
    for &page in requests {
        if let Some(i) = pool.iter().position(|&p| p == page) {
            hits += 1;
            pool.remove(i);
        } else if pool.len() == frames {
            if mru {
                pool.pop_back();
            } else {
                pool.pop_front();
            }
        }
        // the requested page is now the most recently used
        pool.push_back(page);
    }
    hits
}

fn main() {
    // a table of 11 pages, scanned from start to end 10 times
    let requests: Vec<u32> = (1..=11).cycle().take(11 * 10).collect();

    // 10 frames, one fewer than the table: LRU always evicts the
    // page the scan needs next, so every request goes to disk
    assert_eq!(hits(&requests, 10, false), 0);
    // MRU keeps most of the table across scans
    assert_eq!(hits(&requests, 10, true), 90);

    // with 11 frames the whole table fits: only the first scan misses
    assert_eq!(hits(&requests, 11, false), 99);
}
```

Real engines protect their caches from big scans in their own ways:

- **PostgreSQL** gives a large sequential scan a small *ring* of buffers of its own, instead of "blowing out the entire buffer cache" (from its source code's buffer manager notes). For sequential scans the ring is 256 KB.
- **InnoDB** (MySQL) puts a newly read page in the middle of its LRU list, not at the front: 3/8 of the way from the end, by default. A page moves to the front only if it is used again more than a second after it was first read (`innodb_old_blocks_time`, 1000 ms). A scan touches each page a few times in quick succession and never again, so its pages age out from the middle without pushing out the pages in frequent use.

Both policies depend on knowing which reads belong to a big scan, which only the engine knows.
