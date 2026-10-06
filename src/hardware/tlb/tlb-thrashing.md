What is TLB thrashing?

---

The program uses more pages than the TLB can hold. The TLB keeps throwing out mappings that the program needs again soon, so almost every access misses and needs a page walk.

<div class="diagram">
<svg viewBox="0 0 520 190" width="100%" style="max-width:520px" role="img" aria-label="A toy TLB with 4 slots loops over 6 pages and misses on every access">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="20" y="15" width="44" height="28" rx="6" class="k"/>
<text x="42.0" y="33.5" text-anchor="middle">1</text>
<rect x="70" y="15" width="44" height="28" rx="6" class="k"/>
<text x="92.0" y="33.5" text-anchor="middle">2</text>
<rect x="120" y="15" width="44" height="28" rx="6" class="k"/>
<text x="142.0" y="33.5" text-anchor="middle">3</text>
<rect x="170" y="15" width="44" height="28" rx="6" class="k"/>
<text x="192.0" y="33.5" text-anchor="middle">4</text>
<text x="235" y="34" text-anchor="start">pages 1 to 4 fill the TLB</text>
<rect x="20" y="55" width="44" height="28" rx="6" class="r"/>
<text x="42.0" y="73.5" text-anchor="middle">5</text>
<rect x="70" y="55" width="44" height="28" rx="6" class="k"/>
<text x="92.0" y="73.5" text-anchor="middle">2</text>
<rect x="120" y="55" width="44" height="28" rx="6" class="k"/>
<text x="142.0" y="73.5" text-anchor="middle">3</text>
<rect x="170" y="55" width="44" height="28" rx="6" class="k"/>
<text x="192.0" y="73.5" text-anchor="middle">4</text>
<text x="235" y="74" text-anchor="start">page 5 arrives and pushes out page 1</text>
<rect x="20" y="95" width="44" height="28" rx="6" class="k"/>
<text x="42.0" y="113.5" text-anchor="middle">5</text>
<rect x="70" y="95" width="44" height="28" rx="6" class="r"/>
<text x="92.0" y="113.5" text-anchor="middle">6</text>
<rect x="120" y="95" width="44" height="28" rx="6" class="k"/>
<text x="142.0" y="113.5" text-anchor="middle">3</text>
<rect x="170" y="95" width="44" height="28" rx="6" class="k"/>
<text x="192.0" y="113.5" text-anchor="middle">4</text>
<text x="235" y="114" text-anchor="start">page 6 arrives and pushes out page 2</text>
<rect x="20" y="135" width="44" height="28" rx="6" class="k"/>
<text x="42.0" y="153.5" text-anchor="middle">5</text>
<rect x="70" y="135" width="44" height="28" rx="6" class="k"/>
<text x="92.0" y="153.5" text-anchor="middle">6</text>
<rect x="120" y="135" width="44" height="28" rx="6" class="r"/>
<text x="142.0" y="153.5" text-anchor="middle">1</text>
<rect x="170" y="135" width="44" height="28" rx="6" class="k"/>
<text x="192.0" y="153.5" text-anchor="middle">4</text>
<text x="235" y="154" text-anchor="start">page 1 is needed again: a miss</text>
<text x="260" y="182" text-anchor="middle" class="m">a toy TLB with 4 slots; real ones are bigger, the idea is the same</text>
</svg>
</div>
