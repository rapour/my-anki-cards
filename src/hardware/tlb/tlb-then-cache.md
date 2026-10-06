What question does the TLB answer, and what question does the L1/L2 cache answer?

---

- **TLB:** "Where is the memory?" It gives the physical address.
- **Cache:** "Do I already have the contents?" It gives the data.

<div class="diagram">
<svg viewBox="0 0 520 120" width="100%" style="max-width:520px" role="img" aria-label="The TLB turns a virtual address into a physical address, then the L1 cache looks for the data">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="21" y="25" width="90" height="44" rx="6" class="k"/>
<text x="66.0" y="43.5" text-anchor="middle">Virtual</text>
<text x="66.0" y="59.5" text-anchor="middle">address</text>
<line x1="111" y1="47" x2="133" y2="47" class="ln" marker-end="url(#ah)"/>
<rect x="133" y="25" width="60" height="44" rx="6" class="g"/>
<text x="163.0" y="51.5" text-anchor="middle">TLB</text>
<line x1="193" y1="47" x2="215" y2="47" class="ln" marker-end="url(#ah)"/>
<rect x="215" y="25" width="100" height="44" rx="6" class="k"/>
<text x="265.0" y="43.5" text-anchor="middle">Physical</text>
<text x="265.0" y="59.5" text-anchor="middle">address</text>
<line x1="315" y1="47" x2="337" y2="47" class="ln" marker-end="url(#ah)"/>
<rect x="337" y="25" width="80" height="44" rx="6" class="g"/>
<text x="377.0" y="51.5" text-anchor="middle">L1 cache</text>
<line x1="417" y1="47" x2="439" y2="47" class="ln" marker-end="url(#ah)"/>
<rect x="439" y="25" width="60" height="44" rx="6" class="k"/>
<text x="469.0" y="51.5" text-anchor="middle">Data</text>
<text x="163" y="92" text-anchor="middle" class="m">answers: where</text>
<text x="163" y="106" text-anchor="middle" class="m">is the memory?</text>
<text x="377" y="92" text-anchor="middle" class="m">answers: do I already</text>
<text x="377" y="106" text-anchor="middle" class="m">have the contents?</text>
</svg>
</div>

- The address must be translated before the cache lookup can finish, so the TLB comes first.
- Modern CPUs overlap the two steps to hide most of this delay.
