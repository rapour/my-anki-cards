When a program prints the address of a variable, is that the real location in RAM?

---

No. It is a **virtual address**. The CPU's **MMU** (memory management unit) turns it into a **physical address**, using the **page table** that the operating system keeps.

```rust
let x = 42;
println!("{:p}", &x); // a virtual address, not a spot in RAM
```

<div class="diagram">
<svg viewBox="0 0 520 165" width="100%" style="max-width:520px" role="img" aria-label="A program uses a virtual address; the MMU uses the page table in RAM to find the physical address">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="10" y="35" width="130" height="60" rx="6" class="k"/>
<text x="75.0" y="61.5" text-anchor="middle">Your program</text>
<text x="75.0" y="77.5" text-anchor="middle" class="m">virtual address</text>
<line x1="140" y1="65" x2="190" y2="65" class="ln" marker-end="url(#ah)"/>
<rect x="190" y="35" width="140" height="60" rx="6" class="g"/>
<text x="260.0" y="61.5" text-anchor="middle">MMU</text>
<text x="260.0" y="77.5" text-anchor="middle" class="m">inside the CPU</text>
<line x1="330" y1="65" x2="380" y2="65" class="ln" marker-end="url(#ah)"/>
<rect x="380" y="35" width="130" height="60" rx="6" class="k"/>
<text x="445.0" y="61.5" text-anchor="middle">RAM</text>
<text x="445.0" y="77.5" text-anchor="middle" class="m">physical address</text>
<line x1="260" y1="95" x2="260" y2="120" class="ln" marker-end="url(#ah)"/>
<rect x="170" y="120" width="180" height="32" rx="6" class="k"/>
<text x="260.0" y="140.5" text-anchor="middle">Page table (stored in RAM)</text>
</svg>
</div>

- Every program gets its own private set of virtual addresses. RAM only understands physical ones.
- Think of the virtual address as a name, the physical address as GPS coordinates, and the page table as the directory that links them.
