What is a page, and what is a page frame?

---

A **page** is a fixed-size chunk of *virtual* memory, usually 4 KB on x86. A **page frame** is a chunk of the same size in *physical* RAM. The page table says which frame holds each page.

<div class="diagram">
<svg viewBox="0 0 520 215" width="100%" style="max-width:520px" role="img" aria-label="Virtual pages are linked by the page table to page frames in RAM, in any order">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<text x="115" y="22" text-anchor="middle">Virtual pages (4 KB each)</text>
<text x="405" y="22" text-anchor="middle">Page frames in RAM (4 KB each)</text>
<rect x="40" y="35" width="150" height="32" rx="6" class="k"/>
<text x="115.0" y="55.5" text-anchor="middle">page 0</text>
<rect x="40" y="75" width="150" height="32" rx="6" class="k"/>
<text x="115.0" y="95.5" text-anchor="middle">page 1</text>
<rect x="40" y="115" width="150" height="32" rx="6" class="k"/>
<text x="115.0" y="135.5" text-anchor="middle">page 2</text>
<rect x="40" y="155" width="150" height="32" rx="6" class="k"/>
<text x="115.0" y="175.5" text-anchor="middle">page 3</text>
<rect x="330" y="35" width="150" height="32" rx="6" class="g"/>
<text x="405.0" y="55.5" text-anchor="middle">frame 5</text>
<rect x="330" y="75" width="150" height="32" rx="6" class="g"/>
<text x="405.0" y="95.5" text-anchor="middle">frame 2</text>
<rect x="330" y="115" width="150" height="32" rx="6" class="g"/>
<text x="405.0" y="135.5" text-anchor="middle">frame 9</text>
<rect x="330" y="155" width="150" height="32" rx="6" class="g"/>
<text x="405.0" y="175.5" text-anchor="middle">frame 0</text>
<line x1="190" y1="51" x2="330" y2="91" class="ln"/>
<line x1="190" y1="91" x2="330" y2="171" class="ln"/>
<line x1="190" y1="131" x2="330" y2="51" class="ln"/>
<line x1="190" y1="171" x2="330" y2="131" class="ln"/>
<text x="260" y="206" text-anchor="middle" class="m">the page table holds these links</text>
</svg>
</div>

- Pages that sit next to each other in virtual memory can sit in frames far apart in RAM.
- 4 KB is typical, but the size depends on the CPU and the operating system.
