Step by step, how does a memory read travel from the CPU through the TLB and the L1 cache, and what changes if the L1 cache misses?

---

<div class="diagram">
<svg viewBox="0 0 480 385" width="100%" style="max-width:480px" role="img" aria-label="A memory read: CPU to TLB to L1 cache, with an L1 hit returning data and an L1 miss going to main RAM">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<style>svg .lk{stroke:currentColor;stroke-width:2;fill:none}svg .lg{stroke:#007A66;stroke-width:2;fill:none}svg .lo{stroke:#FA6419;stroke-width:2;stroke-dasharray:6 4;fill:none}svg .los{stroke:#FA6419;stroke-width:2;fill:none}svg .mk{fill:currentColor}svg .mg{fill:#007A66}svg .mo{fill:#FA6419}svg .bk{fill:#555}svg .bg{fill:#007A66}svg .bo{fill:#FA6419}svg .bt{fill:#fff;font-size:11px;font-weight:700}svg .bto{fill:#111;font-size:11px;font-weight:700}svg .fr{fill:none;stroke:currentColor;stroke-opacity:.5;stroke-width:1.5;stroke-dasharray:6 4}svg .ttl{font-weight:700}.nightMode svg .lg,.night_mode svg .lg{stroke:#14C1A0}.nightMode svg .mg,.night_mode svg .mg{fill:#14C1A0}</style>
<defs><marker id="ak" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker><marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" class="mg"/></marker><marker id="ao" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" class="mo"/></marker></defs>
<rect x="40" y="10" width="140" height="50" rx="6" class="k"/>
<text x="110.0" y="39.5" text-anchor="middle">CPU core</text>
<rect x="40" y="100" width="140" height="50" rx="6" class="g"/>
<text x="110.0" y="121.5" text-anchor="middle">TLB</text>
<text x="110.0" y="137.5" text-anchor="middle" class="m">address cache</text>
<rect x="40" y="190" width="140" height="50" rx="6" class="g"/>
<text x="110.0" y="211.5" text-anchor="middle">L1 cache</text>
<text x="110.0" y="227.5" text-anchor="middle" class="m">data cache</text>
<rect x="40" y="290" width="140" height="50" rx="6" class="k"/>
<text x="110.0" y="311.5" text-anchor="middle">Main RAM</text>
<text x="110.0" y="327.5" text-anchor="middle" class="m">far away</text>
<polyline points="110,60 110,100" class="lk" marker-end="url(#ak)"/>
<rect x="100.5" y="71" width="19" height="18" rx="9" class="bk"/><text x="110" y="84" text-anchor="middle" class="bt">1</text>
<text x="128" y="84" text-anchor="start">virtual address</text>
<polyline points="110,150 110,190" class="lk" marker-end="url(#ak)"/>
<rect x="100.5" y="161" width="19" height="18" rx="9" class="bk"/><text x="110" y="174" text-anchor="middle" class="bt">2</text>
<text x="128" y="174" text-anchor="start">physical address</text>
<polyline points="110,240 110,290" class="lo" marker-end="url(#ao)"/>
<rect x="100.5" y="256" width="19" height="18" rx="9" class="bo"/><text x="110" y="269" text-anchor="middle" class="bto">4</text>
<text x="128" y="269" text-anchor="start">L1 miss: ask RAM</text>
<polyline points="180,215 290,215 290,35 180,35" class="lg" marker-end="url(#ag)"/>
<rect x="280.5" y="116" width="19" height="18" rx="9" class="bg"/><text x="290" y="129" text-anchor="middle" class="bt">3</text>
<text x="306" y="112" text-anchor="start">L1 hit:</text>
<text x="306" y="128" text-anchor="start">data goes</text>
<text x="306" y="144" text-anchor="start">to the CPU</text>
<polyline points="180,315 430,315 430,22 180,22" class="los" marker-end="url(#ao)"/>
<rect x="420.5" y="161" width="19" height="18" rx="9" class="bo"/><text x="430" y="174" text-anchor="middle" class="bto">5</text>
<text x="195" y="336" text-anchor="start">RAM returns the 64-byte line (slow)</text>
<line x1="10" y1="368" x2="38" y2="368" class="lk"/><text x="46" y="372" text-anchor="start" class="m">request</text>
<line x1="105" y1="368" x2="133" y2="368" class="lg"/><text x="141" y="372" text-anchor="start" class="m">hit: fast path</text>
<line x1="225" y1="368" x2="253" y2="368" class="lo"/><text x="261" y="372" text-anchor="start" class="m">miss: slow path</text>
<line x1="355" y1="368" x2="383" y2="368" class="los"/><text x="391" y="372" text-anchor="start" class="m">RAM answer</text>
</svg>
</div>

1. The CPU sends a **virtual address** to the TLB.
2. The TLB returns the **physical address** (this assumes a TLB hit).
3. **L1 hit:** the L1 cache has that address, so the data goes straight back to the CPU. This is the fast path.
4. **L1 miss:** the request goes on to main RAM. On a real CPU it tries the L2 and L3 caches first.
5. RAM returns a 64-byte cache line. The L1 cache keeps a copy and the CPU gets its data. This is the slow path.

**Remember:** the TLB gives the address, the cache gives the data. A TLB miss is a separate case, covered on the next card.
