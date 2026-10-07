What is the difference between static dispatch and dynamic dispatch in Rust?

---

*Dispatch* means choosing which function runs when you call a trait method.

- **Static dispatch:** the compiler knows the concrete type, so it picks the function at compile time. You get it with generics and `impl Trait`.
- **Dynamic dispatch:** the concrete type is only known at run time, so the program looks the function up in a vtable. You get it with `dyn Trait`.

<div class="diagram">
<svg viewBox="0 0 520 215" width="100%" style="max-width:520px" role="img" aria-label="Static dispatch jumps straight to the function; dynamic dispatch reads its address from the vtable first">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<text x="130" y="18" text-anchor="middle">Static (generics)</text>
<text x="390" y="18" text-anchor="middle">Dynamic (dyn Trait)</text>
<rect x="30" y="30" width="200" height="38" rx="6" class="k"/>
<text x="130.0" y="53.5" text-anchor="middle">shape.area()</text>
<line x1="130" y1="68" x2="130" y2="150" class="ln" marker-end="url(#ah)"/>
<text x="145" y="114" text-anchor="start" class="m">direct jump</text>
<rect x="30" y="150" width="200" height="38" rx="6" class="g"/>
<text x="130.0" y="173.5" text-anchor="middle">Circle::area</text>
<text x="130" y="208" text-anchor="middle" class="m">address fixed at compile time</text>
<rect x="290" y="30" width="200" height="38" rx="6" class="k"/>
<text x="390.0" y="53.5" text-anchor="middle">shape.area()</text>
<line x1="390" y1="68" x2="390" y2="90" class="ln" marker-end="url(#ah)"/>
<rect x="290" y="90" width="200" height="38" rx="6" class="r"/>
<text x="390.0" y="113.5" text-anchor="middle">read address from vtable</text>
<line x1="390" y1="128" x2="390" y2="150" class="ln" marker-end="url(#ah)"/>
<rect x="290" y="150" width="200" height="38" rx="6" class="g"/>
<text x="390.0" y="173.5" text-anchor="middle">Circle::area</text>
<text x="390" y="208" text-anchor="middle" class="m">address found at run time</text>
</svg>
</div>
