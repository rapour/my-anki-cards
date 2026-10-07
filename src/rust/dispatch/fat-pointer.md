How big is a `&dyn Shape` on a 64-bit machine, and what does it hold?

---

**16 bytes**: two pointers.

1. A **data pointer** to the value.
2. A **vtable pointer** to the table of methods for that value's type.

```rust
assert_eq!(size_of::<&i32>(), 8);
assert_eq!(size_of::<&dyn Shape>(), 16);
```

<div class="diagram">
<svg viewBox="0 0 520 160" width="100%" style="max-width:520px" role="img" aria-label="A reference to a value is one pointer; a reference to a trait object is two pointers">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<text x="10" y="40" text-anchor="start">&amp;i32</text>
<text x="10" y="58" text-anchor="start" class="m">8 bytes</text>
<rect x="150" y="20" width="120" height="38" rx="6" class="k"/>
<text x="210.0" y="43.5" text-anchor="middle">data pointer</text>
<text x="285" y="43" text-anchor="start" class="m">points at the value</text>
<text x="10" y="110" text-anchor="start">&amp;dyn Shape</text>
<text x="10" y="128" text-anchor="start" class="m">16 bytes</text>
<rect x="150" y="90" width="120" height="38" rx="6" class="k"/>
<text x="210.0" y="113.5" text-anchor="middle">data pointer</text>
<rect x="270" y="90" width="120" height="38" rx="6" class="g"/>
<text x="330.0" y="113.5" text-anchor="middle">vtable pointer</text>
<text x="400" y="106" text-anchor="start" class="m">the value</text>
<text x="400" y="122" text-anchor="start" class="m">and its methods</text>
</svg>
</div>

- `Box<dyn Shape>` is also 16 bytes. `Box<Circle>` is 8, because its type is known.
- A pointer that is bigger than a normal one is called a **fat pointer**. `&[T]` and `&str` are fat too: a pointer plus a length.
