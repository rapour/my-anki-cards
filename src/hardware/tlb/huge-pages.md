How do huge pages change the TLB reach of a TLB with 64 entries?

---

With 2 MB pages instead of 4 KB: 64 × 2 MB = **128 MB**, instead of 256 KB. That is 512 times more reach from the same 64 entries.

<div class="diagram">
<svg viewBox="0 0 520 190" width="100%" style="max-width:520px" role="img" aria-label="With 2 MB huge pages the same 64 entries reach 128 MB instead of 256 KB">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="10" y="15" width="130" height="50" rx="6" class="k"/>
<text x="75.0" y="36.5" text-anchor="middle">64</text>
<text x="75.0" y="52.5" text-anchor="middle" class="m">TLB entries</text>
<text x="160" y="47" text-anchor="middle" style="font-size:20px">×</text>
<rect x="180" y="15" width="130" height="50" rx="6" class="k"/>
<text x="245.0" y="36.5" text-anchor="middle">4 KB</text>
<text x="245.0" y="52.5" text-anchor="middle" class="m">normal page</text>
<text x="330" y="47" text-anchor="middle" style="font-size:20px">=</text>
<rect x="350" y="15" width="160" height="50" rx="6" class="k"/>
<text x="430.0" y="36.5" text-anchor="middle">256 KB</text>
<text x="430.0" y="52.5" text-anchor="middle" class="m">TLB reach</text>
<rect x="10" y="95" width="130" height="50" rx="6" class="k"/>
<text x="75.0" y="116.5" text-anchor="middle">64</text>
<text x="75.0" y="132.5" text-anchor="middle" class="m">TLB entries</text>
<text x="160" y="127" text-anchor="middle" style="font-size:20px">×</text>
<rect x="180" y="95" width="130" height="50" rx="6" class="k"/>
<text x="245.0" y="116.5" text-anchor="middle">2 MB</text>
<text x="245.0" y="132.5" text-anchor="middle" class="m">huge page</text>
<text x="330" y="127" text-anchor="middle" style="font-size:20px">=</text>
<rect x="350" y="95" width="160" height="50" rx="6" class="g"/>
<text x="430.0" y="116.5" text-anchor="middle">128 MB</text>
<text x="430.0" y="132.5" text-anchor="middle" class="m">TLB reach</text>
<text x="260" y="175" text-anchor="middle" class="m">512 times more reach from the same 64 entries</text>
</svg>
</div>

- On x86-64 the huge page sizes are 2 MB and 1 GB.
- Fewer misses for programs that use a lot of memory spread over many pages.
