Why would translating a virtual address be slow if the CPU had no TLB?

---

The page table is stored in RAM. Translating one address needs a **page walk**: several table reads, one after another, before the CPU can even start reading your data.

<div class="diagram">
<svg viewBox="0 0 520 130" width="100%" style="max-width:520px" role="img" aria-label="A page walk reads four tables one after another before the data read">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="10" y="30" width="88" height="50" rx="6" class="r"/>
<text x="54.0" y="51.5" text-anchor="middle">Table 1</text>
<text x="54.0" y="67.5" text-anchor="middle" class="m">memory read</text>
<rect x="114" y="30" width="88" height="50" rx="6" class="r"/>
<text x="158.0" y="51.5" text-anchor="middle">Table 2</text>
<text x="158.0" y="67.5" text-anchor="middle" class="m">memory read</text>
<rect x="218" y="30" width="88" height="50" rx="6" class="r"/>
<text x="262.0" y="51.5" text-anchor="middle">Table 3</text>
<text x="262.0" y="67.5" text-anchor="middle" class="m">memory read</text>
<rect x="322" y="30" width="88" height="50" rx="6" class="r"/>
<text x="366.0" y="51.5" text-anchor="middle">Table 4</text>
<text x="366.0" y="67.5" text-anchor="middle" class="m">memory read</text>
<rect x="426" y="30" width="88" height="50" rx="6" class="g"/>
<text x="470.0" y="51.5" text-anchor="middle">Your data</text>
<text x="470.0" y="67.5" text-anchor="middle" class="m">finally</text>
<line x1="98" y1="55" x2="114" y2="55" class="ln" marker-end="url(#ah)"/>
<line x1="202" y1="55" x2="218" y2="55" class="ln" marker-end="url(#ah)"/>
<line x1="306" y1="55" x2="322" y2="55" class="ln" marker-end="url(#ah)"/>
<line x1="410" y1="55" x2="426" y2="55" class="ln" marker-end="url(#ah)"/>
<line x1="10" y1="98" x2="410" y2="98" class="ln"/>
<text x="210" y="118" text-anchor="middle" class="m">page walk (4 levels on x86-64): each read waits for the one before it</text>
</svg>
</div>

- On x86-64 there are normally four levels, so four table reads come before the real read.
- Each read depends on the one before it, so they cannot run side by side.
