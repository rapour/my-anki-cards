What happens on a TLB hit, and what happens on a TLB miss?

---

- **Hit:** the mapping is in the TLB, so the CPU goes straight to fetching the data.
- **Miss:** the mapping is not there. The CPU does a page walk, saves the result in the TLB, then fetches the data.

<div class="diagram">
<svg viewBox="0 0 520 212" width="100%" style="max-width:520px" role="img" aria-label="On a TLB hit the frame is found at once; on a miss the CPU does a page walk and saves the result">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="190" y="8" width="140" height="30" rx="6" class="k"/>
<text x="260.0" y="27.5" text-anchor="middle">Virtual address</text>
<line x1="260" y1="38" x2="260" y2="58" class="ln" marker-end="url(#ah)"/>
<rect x="190" y="58" width="140" height="30" rx="6" class="g"/>
<text x="260.0" y="77.5" text-anchor="middle">TLB lookup</text>
<line x1="235" y1="88" x2="100" y2="118" class="ln" marker-end="url(#ah)"/>
<text x="150" y="98" text-anchor="middle" class="m">hit</text>
<line x1="285" y1="88" x2="420" y2="118" class="ln" marker-end="url(#ah)"/>
<text x="385" y="98" text-anchor="middle" class="m">miss</text>
<rect x="20" y="118" width="160" height="32" rx="6" class="g"/>
<text x="100.0" y="138.5" text-anchor="middle">Hit: frame found</text>
<rect x="340" y="118" width="160" height="32" rx="6" class="r"/>
<text x="420.0" y="138.5" text-anchor="middle">Miss: page walk</text>
<line x1="100" y1="150" x2="100" y2="168" class="ln" marker-end="url(#ah)"/>
<line x1="420" y1="150" x2="420" y2="168" class="ln" marker-end="url(#ah)"/>
<rect x="20" y="168" width="160" height="32" rx="6" class="k"/>
<text x="100.0" y="188.5" text-anchor="middle">Fetch the data</text>
<rect x="335" y="168" width="170" height="32" rx="6" class="k"/>
<text x="420.0" y="188.5" text-anchor="middle">Save in TLB, fetch data</text>
</svg>
</div>
