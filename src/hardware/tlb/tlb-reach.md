What is TLB reach, and what is it for 64 entries and 4 KB pages?

---

TLB reach is the amount of memory the CPU can use without a page walk: **entries × page size**.

64 × 4 KB = **256 KB**

<div class="diagram">
<svg viewBox="0 0 520 90" width="100%" style="max-width:520px" role="img" aria-label="64 TLB entries times 4 KB per page gives a TLB reach of 256 KB">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="10" y="20" width="130" height="50" rx="6" class="k"/>
<text x="75.0" y="41.5" text-anchor="middle">64</text>
<text x="75.0" y="57.5" text-anchor="middle" class="m">TLB entries</text>
<text x="160" y="52" text-anchor="middle" style="font-size:20px">×</text>
<rect x="180" y="20" width="130" height="50" rx="6" class="k"/>
<text x="245.0" y="41.5" text-anchor="middle">4 KB</text>
<text x="245.0" y="57.5" text-anchor="middle" class="m">per page</text>
<text x="330" y="52" text-anchor="middle" style="font-size:20px">=</text>
<rect x="350" y="20" width="160" height="50" rx="6" class="g"/>
<text x="430.0" y="41.5" text-anchor="middle">256 KB</text>
<text x="430.0" y="57.5" text-anchor="middle" class="m">TLB reach</text>
</svg>
</div>

- A small L1 TLB often holds about 64 to 128 entries. The number depends on the CPU.
- Use more memory than the reach, spread over many pages, and the TLB starts missing.
