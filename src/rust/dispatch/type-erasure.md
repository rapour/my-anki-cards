What is type erasure, and where does it happen in Rust?

---

Forgetting the concrete type at compile time and keeping only what a trait promises. In Rust it happens when a pointer to a concrete type becomes a `dyn Trait` pointer:

```rust
let c: Box<Circle> = Box::new(Circle { r: 1.0 });
let s: Box<dyn Shape> = c; // the type Circle is erased here
```

<div class="diagram">
<svg viewBox="0 0 520 150" width="100%" style="max-width:520px" role="img" aria-label="Coercing Box&lt;Circle&gt; to Box&lt;dyn Shape&gt; forgets the type Circle and keeps only the Shape methods">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="20" y="35" width="170" height="58" rx="6" class="k"/>
<text x="105.0" y="60.5" text-anchor="middle">Box&lt;Circle&gt;</text>
<text x="105.0" y="76.5" text-anchor="middle" class="m">the compiler knows: Circle</text>
<line x1="190" y1="64" x2="330" y2="64" class="ln" marker-end="url(#ah)"/>
<text x="260" y="54" text-anchor="middle" class="m">coerce</text>
<rect x="330" y="35" width="170" height="58" rx="6" class="g"/>
<text x="415.0" y="60.5" text-anchor="middle">Box&lt;dyn Shape&gt;</text>
<text x="415.0" y="76.5" text-anchor="middle" class="m">the compiler knows: Shape</text>
<text x="260" y="124" text-anchor="middle" class="m">same value on the heap, plus a vtable pointer</text>
</svg>
</div>

- The vtable remembers how to call the `Shape` methods. Nothing else about `Circle` is available, so you cannot read `r` through `s`.
- This conversion is called an *unsized coercion*.
