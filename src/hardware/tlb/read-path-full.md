What are all the steps of a memory read, including a TLB miss and a cache miss?

---

<div class="diagram">
<svg viewBox="0 0 560 390" width="100%" style="max-width:560px" role="img" aria-label="The full path of a memory read, including a TLB miss with a page walk and a cache miss that goes to RAM">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<style>svg .lk{stroke:currentColor;stroke-width:2;fill:none}svg .lg{stroke:#007A66;stroke-width:2;fill:none}svg .lo{stroke:#FA6419;stroke-width:2;stroke-dasharray:6 4;fill:none}svg .los{stroke:#FA6419;stroke-width:2;fill:none}svg .mk{fill:currentColor}svg .mg{fill:#007A66}svg .mo{fill:#FA6419}svg .bk{fill:#555}svg .bg{fill:#007A66}svg .bo{fill:#FA6419}svg .bt{fill:#fff;font-size:11px;font-weight:700}svg .bto{fill:#111;font-size:11px;font-weight:700}svg .fr{fill:none;stroke:currentColor;stroke-opacity:.5;stroke-width:1.5;stroke-dasharray:6 4}svg .ttl{font-weight:700}.nightMode svg .lg,.night_mode svg .lg{stroke:#14C1A0}.nightMode svg .mg,.night_mode svg .mg{fill:#14C1A0}</style>
<defs><marker id="ak" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker><marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" class="mg"/></marker><marker id="ao" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" class="mo"/></marker></defs>
<rect x="8" y="4" width="242" height="330" rx="12" class="fr"/>
<rect x="360" y="4" width="192" height="330" rx="12" class="fr"/>
<text x="129" y="22" text-anchor="middle" class="ttl">Inside the CPU</text>
<text x="456" y="22" text-anchor="middle" class="ttl">Main memory (RAM)</text>
<rect x="45" y="34" width="160" height="50" rx="6" class="k"/>
<text x="125.0" y="63.5" text-anchor="middle">CPU core</text>
<rect x="45" y="140" width="160" height="50" rx="6" class="g"/>
<text x="125.0" y="161.5" text-anchor="middle">TLB</text>
<text x="125.0" y="177.5" text-anchor="middle" class="m">address cache</text>
<rect x="45" y="260" width="160" height="50" rx="6" class="g"/>
<text x="125.0" y="281.5" text-anchor="middle">L1/L2 cache</text>
<text x="125.0" y="297.5" text-anchor="middle" class="m">data cache</text>
<rect x="375" y="140" width="160" height="50" rx="6" class="k"/>
<text x="455.0" y="161.5" text-anchor="middle">Page tables</text>
<text x="455.0" y="177.5" text-anchor="middle" class="m">virtual to physical map</text>
<rect x="375" y="260" width="160" height="50" rx="6" class="k"/>
<text x="455.0" y="281.5" text-anchor="middle">Physical data</text>
<text x="455.0" y="297.5" text-anchor="middle" class="m">your variables and arrays</text>
<polyline points="125,84 125,140" class="lk" marker-end="url(#ak)"/>
<rect x="115.5" y="103" width="19" height="18" rx="9" class="bk"/><text x="125" y="116" text-anchor="middle" class="bt">1</text>
<text x="142" y="116" text-anchor="start">virtual address</text>
<polyline points="125,190 125,260" class="lg" marker-end="url(#ag)"/>
<rect x="115.5" y="216" width="19" height="18" rx="9" class="bg"/><text x="125" y="229" text-anchor="middle" class="bt">2</text>
<text x="142" y="221" text-anchor="start">TLB hit:</text>
<text x="142" y="237" text-anchor="start">physical address</text>
<polyline points="205,150 375,150" class="lo" marker-end="url(#ao)"/>
<text x="305" y="120" text-anchor="middle" class="m">TLB miss:</text>
<text x="305" y="134" text-anchor="middle" class="m">page walk</text>
<rect x="292.0" y="141" width="26" height="18" rx="9" class="bo"/><text x="305" y="154" text-anchor="middle" class="bto">2a</text>
<polyline points="375,175 205,175" class="los" marker-end="url(#ao)"/>
<rect x="292.0" y="166" width="26" height="18" rx="9" class="bo"/><text x="305" y="179" text-anchor="middle" class="bto">2b</text>
<text x="305" y="198" text-anchor="middle" class="m">mapping returned</text>
<polyline points="205,270 375,270" class="lo" marker-end="url(#ao)"/>
<text x="305" y="240" text-anchor="middle" class="m">cache miss:</text>
<text x="305" y="254" text-anchor="middle" class="m">fetch the line</text>
<rect x="292.0" y="261" width="26" height="18" rx="9" class="bo"/><text x="305" y="274" text-anchor="middle" class="bto">3a</text>
<polyline points="375,295 205,295" class="los" marker-end="url(#ao)"/>
<rect x="292.0" y="286" width="26" height="18" rx="9" class="bo"/><text x="305" y="299" text-anchor="middle" class="bto">3b</text>
<text x="305" y="318" text-anchor="middle" class="m">64-byte cache line</text>
<polyline points="45,285 26,285 26,59 45,59" class="lg" marker-end="url(#ag)"/>
<rect x="16.5" y="163" width="19" height="18" rx="9" class="bg"/><text x="26" y="176" text-anchor="middle" class="bt">3</text>
<line x1="20" y1="362" x2="48" y2="362" class="lk"/><text x="56" y="366" text-anchor="start" class="m">request</text>
<line x1="140" y1="362" x2="168" y2="362" class="lg"/><text x="176" y="366" text-anchor="start" class="m">hit: fast path</text>
<line x1="270" y1="362" x2="298" y2="362" class="lo"/><text x="306" y="366" text-anchor="start" class="m">miss: slow path</text>
<line x1="400" y1="362" x2="428" y2="362" class="los"/><text x="436" y="366" text-anchor="start" class="m">RAM answer</text>
</svg>
</div>

1. The CPU sends a **virtual address** to the TLB.
2. The TLB looks for the mapping of that page.
    - **Hit:** the TLB sends the physical address to the cache (arrow 2).
    - **Miss:** the CPU walks the page tables in RAM (2a). The mapping comes back (2b) and is saved in the TLB, which then sends the physical address to the cache.
3. The cache looks for the data at that physical address.
    - **Hit:** the data goes back to the CPU (arrow 3).
    - **Miss:** the request goes to RAM (3a). RAM returns a 64-byte cache line (3b). The cache keeps a copy and the CPU gets its data.

**Best case:** TLB hit and cache hit. **Worst case:** both miss, so one page walk and one RAM fetch.

Page table entries can themselves be found in the L1, L2 or L3 caches, so a page walk is not always a full trip to RAM.
