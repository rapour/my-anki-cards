What is a vtable?

---

A table of function pointers that the compiler builds for each (type, trait) pair, such as `(Circle, Shape)`. It holds:

1. How to drop the value.
2. The value's size.
3. The value's alignment.
4. One pointer for each trait method, such as `area`.

<div class="diagram">
<svg viewBox="0 0 520 255" width="100%" style="max-width:520px" role="img" aria-label="A &amp;dyn Shape holds a data pointer to the Circle and a vtable pointer to the table for Circle and Shape">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<text x="10" y="18" text-anchor="start">shape: &amp;dyn Shape</text>
<rect x="10" y="28" width="130" height="36" rx="6" class="k"/>
<text x="75.0" y="50.5" text-anchor="middle">data pointer</text>
<rect x="10" y="64" width="130" height="36" rx="6" class="g"/>
<text x="75.0" y="86.5" text-anchor="middle">vtable pointer</text>
<text x="300" y="18" text-anchor="start">the value</text>
<rect x="300" y="28" width="200" height="36" rx="6" class="k"/>
<text x="400.0" y="50.5" text-anchor="middle">Circle { r: 2.0 }</text>
<line x1="140" y1="46" x2="300" y2="46" class="ln" marker-end="url(#ah)"/>
<text x="300" y="98" text-anchor="start">vtable for (Circle, Shape)</text>
<rect x="300" y="106" width="200" height="28" rx="6" class="k"/>
<text x="400.0" y="124.5" text-anchor="middle">drop_in_place::&lt;Circle&gt;</text>
<rect x="300" y="134" width="200" height="28" rx="6" class="k"/>
<text x="400.0" y="152.5" text-anchor="middle">size: 8</text>
<rect x="300" y="162" width="200" height="28" rx="6" class="k"/>
<text x="400.0" y="180.5" text-anchor="middle">align: 8</text>
<rect x="300" y="190" width="200" height="28" rx="6" class="g"/>
<text x="400.0" y="208.5" text-anchor="middle">Shape::area</text>
<line x1="140" y1="82" x2="300" y2="120" class="ln" marker-end="url(#ah)"/>
<text x="260" y="244" text-anchor="middle" class="m">one vtable per (type, trait) pair, shared by every Circle</text>
</svg>
</div>

- Every `Circle` used as a `dyn Shape` shares the same vtable.
- This is the layout rustc uses today. The language does not promise it.
