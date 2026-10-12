What is binary exponentiation, and how many multiplications does it need to compute `aⁿ`?

---

A fast way to compute `aⁿ`, also called *exponentiation by squaring*. It needs about `log₂ n` squarings, plus at most that many extra multiplications, instead of the `n − 1` multiplications of the plain loop.

**The idea.** Write the exponent in binary. Every `1` bit adds one factor `a^(2^k)`, where `k` is the position of that bit. Each of these powers is the square of the one before it, so they are cheap to produce.

Example: 13 is `1101` in binary, which is 8 + 4 + 1, so

`3¹³ = 3⁸ · 3⁴ · 3¹ = 6561 · 81 · 3 = 1,594,323`

<div class="diagram">
<svg viewBox="0 0 520 180" width="100%" style="max-width:520px" role="img" aria-label="The exponent 13 is 1101 in binary, so 3 to the 13 is 3 to the 8 times 3 to the 4 times 3 to the 1">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<text x="10" y="58" text-anchor="start" class="m">bit position k</text>
<text x="10" y="93" text-anchor="start" class="m">bit of 13</text>
<text x="10" y="141" text-anchor="start" class="m">3^(2^k)</text>
<text x="190" y="58" text-anchor="middle" class="m">3</text>
<text x="280" y="58" text-anchor="middle" class="m">2</text>
<text x="370" y="58" text-anchor="middle" class="m">1</text>
<text x="460" y="58" text-anchor="middle" class="m">0</text>
<rect x="150" y="70" width="80" height="36" rx="6" class="g"/>
<text x="190.0" y="92.5" text-anchor="middle">1</text>
<rect x="240" y="70" width="80" height="36" rx="6" class="g"/>
<text x="280.0" y="92.5" text-anchor="middle">1</text>
<rect x="330" y="70" width="80" height="36" rx="6" class="k"/>
<text x="370.0" y="92.5" text-anchor="middle">0</text>
<rect x="420" y="70" width="80" height="36" rx="6" class="g"/>
<text x="460.0" y="92.5" text-anchor="middle">1</text>
<rect x="150" y="118" width="80" height="36" rx="6" class="g"/>
<text x="190.0" y="140.5" text-anchor="middle">3^8 = 6561</text>
<rect x="240" y="118" width="80" height="36" rx="6" class="g"/>
<text x="280.0" y="140.5" text-anchor="middle">3^4 = 81</text>
<rect x="330" y="118" width="80" height="36" rx="6" class="k"/>
<text x="370.0" y="140.5" text-anchor="middle">3^2 = 9</text>
<rect x="420" y="118" width="80" height="36" rx="6" class="g"/>
<text x="460.0" y="140.5" text-anchor="middle">3^1 = 3</text>
<text x="260" y="176" text-anchor="middle">3^13 = 6561 × 81 × 3 = 1,594,323   (green = used)</text>
</svg>
</div>

The powers 3, 9, 81, 6561 come from squaring: 3² = 9, 9² = 81, 81² = 6561. The bit for `3²` is `0`, so that power is skipped.
