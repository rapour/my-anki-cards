Both sums read a `Vec<i32>` of about 10 million items. Why is each read in the second one more expensive?

```rust
let data = vec![1i32; 10_000_000];

let a: i64 = data.iter().map(|&x| x as i64).sum();
let b: i64 = data
    .iter()
    .step_by(1024)
    .map(|&x| x as i64)
    .sum();
```

---

`step_by(1024)` jumps 1024 × 4 bytes = 4096 bytes, exactly one page, on every read.

<div class="diagram">
<svg viewBox="0 0 520 165" width="100%" style="max-width:520px" role="img" aria-label="Reading one value per page touches one of the 64 cache lines in each page">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<text x="67" y="20" text-anchor="middle" class="m">page 1</text>
<text x="187" y="20" text-anchor="middle" class="m">page 2</text>
<text x="307" y="20" text-anchor="middle" class="m">page 3</text>
<rect x="20" y="30" width="10" height="10" rx="2" class="cr"/>
<rect x="32" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="44" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="56" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="68" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="80" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="92" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="104" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="20" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="32" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="44" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="56" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="68" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="80" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="92" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="104" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="20" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="32" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="44" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="56" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="68" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="80" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="92" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="104" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="20" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="32" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="44" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="56" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="68" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="80" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="92" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="104" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="20" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="32" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="44" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="56" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="68" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="80" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="92" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="104" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="20" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="32" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="44" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="56" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="68" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="80" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="92" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="104" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="20" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="32" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="44" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="56" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="68" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="80" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="92" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="104" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="20" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="32" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="44" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="56" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="68" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="80" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="92" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="104" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="140" y="30" width="10" height="10" rx="2" class="cr"/>
<rect x="152" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="164" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="176" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="188" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="200" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="212" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="224" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="140" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="152" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="164" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="176" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="188" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="200" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="212" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="224" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="140" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="152" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="164" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="176" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="188" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="200" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="212" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="224" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="140" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="152" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="164" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="176" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="188" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="200" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="212" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="224" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="140" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="152" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="164" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="176" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="188" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="200" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="212" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="224" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="140" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="152" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="164" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="176" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="188" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="200" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="212" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="224" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="140" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="152" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="164" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="176" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="188" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="200" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="212" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="224" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="140" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="152" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="164" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="176" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="188" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="200" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="212" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="224" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="260" y="30" width="10" height="10" rx="2" class="cr"/>
<rect x="272" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="284" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="296" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="308" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="320" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="332" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="344" y="30" width="10" height="10" rx="2" class="c"/>
<rect x="260" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="272" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="284" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="296" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="308" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="320" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="332" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="344" y="42" width="10" height="10" rx="2" class="c"/>
<rect x="260" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="272" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="284" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="296" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="308" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="320" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="332" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="344" y="54" width="10" height="10" rx="2" class="c"/>
<rect x="260" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="272" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="284" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="296" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="308" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="320" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="332" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="344" y="66" width="10" height="10" rx="2" class="c"/>
<rect x="260" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="272" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="284" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="296" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="308" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="320" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="332" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="344" y="78" width="10" height="10" rx="2" class="c"/>
<rect x="260" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="272" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="284" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="296" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="308" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="320" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="332" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="344" y="90" width="10" height="10" rx="2" class="c"/>
<rect x="260" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="272" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="284" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="296" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="308" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="320" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="332" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="344" y="102" width="10" height="10" rx="2" class="c"/>
<rect x="260" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="272" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="284" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="296" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="308" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="320" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="332" y="114" width="10" height="10" rx="2" class="c"/>
<rect x="344" y="114" width="10" height="10" rx="2" class="c"/>
<line x1="116" y1="78" x2="138" y2="78" class="ln" marker-end="url(#ah)"/>
<line x1="236" y1="78" x2="258" y2="78" class="ln" marker-end="url(#ah)"/>
<text x="375" y="60" text-anchor="start" class="m">orange = line read</text>
<text x="375" y="78" text-anchor="start" class="m">grey = 63 skipped</text>
<text x="240" y="150" text-anchor="middle" class="m">every read lands on a new page and uses 1 of its 64 cache lines</text>
</svg>
</div>

- Each read lands on a new page, so a TLB miss is likely.
- Each read uses only 1 of the 64 cache lines in its page. The other 63 are skipped, so memory bandwidth is wasted.
- Reading one item after another uses all 16 `i32`s in a cache line and 1024 reads per page.
