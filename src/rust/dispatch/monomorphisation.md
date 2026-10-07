What is monomorphisation?

---

How the compiler handles generic code: it makes a separate copy of the generic function for every concrete type that is used. (*mono* = one, *morph* = form.)

```rust
fn largest<T: PartialOrd + Copy>(items: &[T]) -> T {
    let mut best = items[0];
    for &item in items {
        if item > best {
            best = item;
        }
    }
    best
}

largest(&[1, 5, 3]);   // the compiler makes largest::<i32>
largest(&[1.5, 0.5]);  // the compiler makes largest::<f64>
```

<div class="diagram">
<svg viewBox="0 0 520 180" width="100%" style="max-width:520px" role="img" aria-label="One generic function becomes three separate compiled copies, one per type">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect x="20" y="60" width="150" height="56" rx="6" class="k"/>
<text x="95.0" y="84.5" text-anchor="middle">fn largest&lt;T&gt;</text>
<text x="95.0" y="100.5" text-anchor="middle" class="m">one generic source</text>
<line x1="170" y1="88" x2="330" y2="33" class="ln" marker-end="url(#ah)"/>
<line x1="170" y1="88" x2="330" y2="88" class="ln" marker-end="url(#ah)"/>
<line x1="170" y1="88" x2="330" y2="143" class="ln" marker-end="url(#ah)"/>
<rect x="330" y="12" width="170" height="42" rx="6" class="g"/>
<text x="415.0" y="29.5" text-anchor="middle">largest::&lt;i32&gt;</text>
<text x="415.0" y="45.5" text-anchor="middle" class="m">copy for i32</text>
<rect x="330" y="67" width="170" height="42" rx="6" class="g"/>
<text x="415.0" y="84.5" text-anchor="middle">largest::&lt;f64&gt;</text>
<text x="415.0" y="100.5" text-anchor="middle" class="m">copy for f64</text>
<rect x="330" y="122" width="170" height="42" rx="6" class="g"/>
<text x="415.0" y="139.5" text-anchor="middle">largest::&lt;char&gt;</text>
<text x="415.0" y="155.5" text-anchor="middle" class="m">copy for char</text>
<text x="175" y="172" text-anchor="middle" class="m">the compiler writes one copy for every type you use</text>
</svg>
</div>

This happens at compile time, so it is the way generics get static dispatch.
