How do you get the hash of `s[l..r)` from the prefix hashes with no division?

---

`hash(s[l..r)) = H[r] − H[l] · p^(r−l)  (mod m)`, where `H[i]` is the hash of the first `i` letters.

**Why:** `H[r]` is the hash of the first `l` letters followed by the `r − l` letters of the substring. Adding `r − l` letters at the right end shifted the first part up by `r − l` powers, so `H[r] = H[l] · p^(r−l) + hash(s[l..r))`. Move the first term to the other side.

<div class="diagram">
<svg viewBox="0 0 520 170" width="100%" style="max-width:520px" role="img" aria-label="The prefix hash H of r equals H of l shifted up by r minus l places plus the hash of the substring">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<line x1="20" y1="40" x2="400" y2="40" class="ln"/>
<line x1="20" y1="34" x2="20" y2="46" class="ln"/>
<line x1="400" y1="34" x2="400" y2="46" class="ln"/>
<text x="210" y="30" text-anchor="middle">H[r] = hash of the first r letters</text>
<rect x="20" y="56" width="190" height="36" rx="6" class="k"/>
<text x="115.0" y="78.5" text-anchor="middle">s[0..l)</text>
<rect x="210" y="56" width="190" height="36" rx="6" class="g"/>
<text x="305.0" y="78.5" text-anchor="middle">s[l..r)</text>
<text x="115" y="112" text-anchor="middle" class="m">this part is H[l], but shifted</text>
<text x="115" y="126" text-anchor="middle" class="m">up by r − l places: H[l]·p^(r−l)</text>
<text x="305" y="112" text-anchor="middle" class="m">hash of s[l..r)</text>
<text x="305" y="126" text-anchor="middle" class="m">(the part we want)</text>
<text x="210" y="156" text-anchor="middle">hash(s[l..r)) = H[r] − H[l]·p^(r−l)   (mod m)</text>
</svg>
</div>

- No modular inverse is needed. That is the advantage of this form.
- Add `m` before taking `% m` so the subtraction never goes negative with unsigned numbers.
- Kattis *String Hashing* is answered by `get(L, R)` for every query.
