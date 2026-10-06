How many 64-byte cache lines fit in one 4 KB page?

---

**64**, because 4096 bytes ÷ 64 bytes = 64.

<div class="diagram">
<svg viewBox="0 0 520 215" width="100%" style="max-width:520px" role="img" aria-label="A 4 KB page drawn as an 8 by 8 grid of 64 cache lines">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="20" y="15" width="20" height="20" rx="2" class="c"/>
<rect x="43" y="15" width="20" height="20" rx="2" class="c"/>
<rect x="66" y="15" width="20" height="20" rx="2" class="c"/>
<rect x="89" y="15" width="20" height="20" rx="2" class="c"/>
<rect x="112" y="15" width="20" height="20" rx="2" class="c"/>
<rect x="135" y="15" width="20" height="20" rx="2" class="c"/>
<rect x="158" y="15" width="20" height="20" rx="2" class="c"/>
<rect x="181" y="15" width="20" height="20" rx="2" class="c"/>
<rect x="20" y="38" width="20" height="20" rx="2" class="c"/>
<rect x="43" y="38" width="20" height="20" rx="2" class="c"/>
<rect x="66" y="38" width="20" height="20" rx="2" class="c"/>
<rect x="89" y="38" width="20" height="20" rx="2" class="c"/>
<rect x="112" y="38" width="20" height="20" rx="2" class="c"/>
<rect x="135" y="38" width="20" height="20" rx="2" class="c"/>
<rect x="158" y="38" width="20" height="20" rx="2" class="c"/>
<rect x="181" y="38" width="20" height="20" rx="2" class="c"/>
<rect x="20" y="61" width="20" height="20" rx="2" class="c"/>
<rect x="43" y="61" width="20" height="20" rx="2" class="c"/>
<rect x="66" y="61" width="20" height="20" rx="2" class="c"/>
<rect x="89" y="61" width="20" height="20" rx="2" class="c"/>
<rect x="112" y="61" width="20" height="20" rx="2" class="c"/>
<rect x="135" y="61" width="20" height="20" rx="2" class="c"/>
<rect x="158" y="61" width="20" height="20" rx="2" class="c"/>
<rect x="181" y="61" width="20" height="20" rx="2" class="c"/>
<rect x="20" y="84" width="20" height="20" rx="2" class="c"/>
<rect x="43" y="84" width="20" height="20" rx="2" class="c"/>
<rect x="66" y="84" width="20" height="20" rx="2" class="c"/>
<rect x="89" y="84" width="20" height="20" rx="2" class="c"/>
<rect x="112" y="84" width="20" height="20" rx="2" class="cg"/>
<rect x="135" y="84" width="20" height="20" rx="2" class="c"/>
<rect x="158" y="84" width="20" height="20" rx="2" class="c"/>
<rect x="181" y="84" width="20" height="20" rx="2" class="c"/>
<rect x="20" y="107" width="20" height="20" rx="2" class="c"/>
<rect x="43" y="107" width="20" height="20" rx="2" class="c"/>
<rect x="66" y="107" width="20" height="20" rx="2" class="c"/>
<rect x="89" y="107" width="20" height="20" rx="2" class="c"/>
<rect x="112" y="107" width="20" height="20" rx="2" class="c"/>
<rect x="135" y="107" width="20" height="20" rx="2" class="c"/>
<rect x="158" y="107" width="20" height="20" rx="2" class="c"/>
<rect x="181" y="107" width="20" height="20" rx="2" class="c"/>
<rect x="20" y="130" width="20" height="20" rx="2" class="c"/>
<rect x="43" y="130" width="20" height="20" rx="2" class="c"/>
<rect x="66" y="130" width="20" height="20" rx="2" class="c"/>
<rect x="89" y="130" width="20" height="20" rx="2" class="c"/>
<rect x="112" y="130" width="20" height="20" rx="2" class="c"/>
<rect x="135" y="130" width="20" height="20" rx="2" class="c"/>
<rect x="158" y="130" width="20" height="20" rx="2" class="c"/>
<rect x="181" y="130" width="20" height="20" rx="2" class="c"/>
<rect x="20" y="153" width="20" height="20" rx="2" class="c"/>
<rect x="43" y="153" width="20" height="20" rx="2" class="c"/>
<rect x="66" y="153" width="20" height="20" rx="2" class="c"/>
<rect x="89" y="153" width="20" height="20" rx="2" class="c"/>
<rect x="112" y="153" width="20" height="20" rx="2" class="c"/>
<rect x="135" y="153" width="20" height="20" rx="2" class="c"/>
<rect x="158" y="153" width="20" height="20" rx="2" class="c"/>
<rect x="181" y="153" width="20" height="20" rx="2" class="c"/>
<rect x="20" y="176" width="20" height="20" rx="2" class="c"/>
<rect x="43" y="176" width="20" height="20" rx="2" class="c"/>
<rect x="66" y="176" width="20" height="20" rx="2" class="c"/>
<rect x="89" y="176" width="20" height="20" rx="2" class="c"/>
<rect x="112" y="176" width="20" height="20" rx="2" class="c"/>
<rect x="135" y="176" width="20" height="20" rx="2" class="c"/>
<rect x="158" y="176" width="20" height="20" rx="2" class="c"/>
<rect x="181" y="176" width="20" height="20" rx="2" class="c"/>
<text x="235" y="62" text-anchor="start">One page = 4096 bytes</text>
<text x="235" y="92" text-anchor="start">Each square = one cache line = 64 bytes</text>
<text x="235" y="122" text-anchor="start">8 × 8 = 64 cache lines per page</text>
<text x="235" y="152" text-anchor="start">One TLB entry covers all 64 of them</text>
</svg>
</div>

- So one TLB entry, which maps one page, covers 64 cache lines.
- This assumes 4 KB pages and 64-byte lines. Check the manual for your CPU.
