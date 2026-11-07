Why does a CPU cache store and move memory in 64-byte **cache lines** instead of single bytes or words, and what does that mean for how you lay out and walk through data?

---

A **cache line** is the unit a CPU cache stores and moves: 64 bytes on x86-64 and on most ARM cores. Lines are aligned, so line *n* holds bytes 64*n* to 64*n* + 63. Reading a single byte brings its whole line into the cache.

```sh
$ getconf LEVEL1_DCACHE_LINESIZE
64
```

<div class="diagram">
<svg viewBox="0 0 640 204" width="100%" style="max-width:640px" role="img" aria-label="Memory is cached in 64-byte lines. An 8-byte value at offset 56 lies in one line; one at offset 124 straddles two lines.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<rect x="41.0" y="50" width="184.66666666666666" height="36" rx="2" class="c"/>
<text x="133.33333333333331" y="40" text-anchor="middle" class="m">line 0: bytes 0 to 63</text>
<rect x="227.66666666666666" y="50" width="184.66666666666666" height="36" rx="2" class="c"/>
<text x="320.0" y="40" text-anchor="middle" class="m">line 1: bytes 64 to 127</text>
<rect x="414.3333333333333" y="50" width="184.66666666666666" height="36" rx="2" class="c"/>
<text x="506.66666666666663" y="40" text-anchor="middle" class="m">line 2: bytes 128 to 191</text>
<rect x="203.33333333333331" y="50" width="23.333333333333332" height="36" rx="2" class="cg"/>
<rect x="401.66666666666663" y="50" width="23.333333333333332" height="36" rx="2" class="cr"/>
<line x1="215.0" y1="128" x2="215.0" y2="90" class="pg" marker-end="url(#cgm)"/>
<text x="215.0" y="144" text-anchor="middle" class="tg">8 bytes at 56: one line</text>
<line x1="413.3333333333333" y1="128" x2="413.3333333333333" y2="90" class="po" marker-end="url(#co)"/>
<text x="413.3333333333333" y="144" text-anchor="middle" class="to">8 bytes at 124: two lines</text>
<text x="320" y="176" text-anchor="middle" class="m">The cache moves whole 64-byte lines: reading one byte brings in all 64,</text>
<text x="320" y="192" text-anchor="middle" class="m">so its neighbours are then in the cache too.</text>
</svg>
</div>

**Why lines, not bytes:**

- **Tags cost space.** The cache must store, next to each block it holds, which address the block came from (its *tag*). Ulrich Drepper, in *What Every Programmer Should Know About Memory*: "Since for the tag, in addition to the actual memory, additional space is required, it is inefficient to chose a word as the granularity of the cache." One tag per 64 bytes is cheap.
- **Memory is faster in blocks.** RAM delivers a run of consecutive bytes much more efficiently than the same bytes one at a time.
- **Spatial locality.** Programs usually use nearby bytes soon: the next array element, the next field of a struct.

**What it means for your code:**

1. **Walk data in address order.** One line fetched serves 16 `u32`s or 8 `u64`s.
2. **Skipping doesn't save much.** Touching every 16th `u32` still loads every line, so it costs almost as much memory traffic as touching all of them.
3. **Keep things that are used together on the same line**, and don't let a value straddle two lines: then it costs two lines.
4. **Threads that write different variables on the same line slow each other down**, because the cores pass the whole line back and forth (*false sharing*).

**In Rust:**

```rust
use std::time::Instant;

const LINE: usize = 64;

/// How many 64-byte cache lines does the byte range
/// [addr, addr + len) touch?
fn lines_touched(addr: usize, len: usize) -> usize {
    (addr + len - 1) / LINE - addr / LINE + 1
}

/// Multiply every `step`-th u32 by 3 and return the time taken.
fn touch(data: &mut [u32], step: usize) -> std::time::Duration {
    let start = Instant::now();
    for i in (0..data.len()).step_by(step) {
        data[i] *= 3;
    }
    start.elapsed()
}

fn main() {
    // an 8-byte value at offset 56 of a line fits; at 60 it straddles
    assert_eq!(lines_touched(56, 8), 1);
    assert_eq!(lines_touched(60, 8), 2);
    // a 64-byte struct is one line only if it starts on a line
    assert_eq!(lines_touched(128, 64), 1);
    assert_eq!(lines_touched(130, 64), 2);

    // 64 MiB of u32: far bigger than the caches
    let mut data = vec![1u32; 16 << 20];
    touch(&mut data, 1); // first touch: let the OS allocate pages
    let every = touch(&mut data, 1); // 16,777,216 multiplications
    let every_16th = touch(&mut data, 16); // 1,048,576: one per line
    println!("every u32:     {every:?}");
    println!("every 16th:    {every_16th:?}");
    // 16 u32s fill one 64-byte line: both loops read every line
    assert_eq!(16 * std::mem::size_of::<u32>(), LINE);
}
```

One run:

```text
every u32:     7.350995ms
every 16th:    3.496318ms
```

The second loop does 16 times fewer multiplications but is only about twice as fast: both loops bring all 64 MiB through the cache, line by line.
