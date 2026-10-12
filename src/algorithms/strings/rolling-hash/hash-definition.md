In the version where the degree-0 term comes **last**, how is the hash of a string defined, and how do you compute it in one pass?

---

For a string `s` of length `n`, with each letter turned into a number:

`hash(s) = s[0]·p^(n−1) + s[1]·p^(n−2) + ... + s[n−1]·p⁰  (mod m)`

The **last** letter has weight `p⁰ = 1`, and the first letter has the highest power.

<div class="diagram">
<svg viewBox="0 0 520 180" width="100%" style="max-width:520px" role="img" aria-label="In the hash of abc the letter a gets weight p squared, b gets p, and c gets p to the power 0">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<text x="260" y="22" text-anchor="middle">hash of  abc  with the degree-0 term last</text>
<rect x="150" y="40" width="80" height="44" rx="6" class="k"/>
<text x="190.0" y="58.5" text-anchor="middle">a</text>
<text x="190.0" y="74.5" text-anchor="middle" class="m">value 1</text>
<rect x="250" y="40" width="80" height="44" rx="6" class="k"/>
<text x="290.0" y="58.5" text-anchor="middle">b</text>
<text x="290.0" y="74.5" text-anchor="middle" class="m">value 2</text>
<rect x="350" y="40" width="80" height="44" rx="6" class="g"/>
<text x="390.0" y="58.5" text-anchor="middle">c</text>
<text x="390.0" y="74.5" text-anchor="middle" class="m">value 3</text>
<line x1="190" y1="84" x2="190" y2="106" class="ln" marker-end="url(#ah)"/>
<line x1="290" y1="84" x2="290" y2="106" class="ln" marker-end="url(#ah)"/>
<line x1="390" y1="84" x2="390" y2="106" class="ln" marker-end="url(#ah)"/>
<text x="190" y="124" text-anchor="middle">× p²</text>
<text x="290" y="124" text-anchor="middle">× p¹</text>
<text x="390" y="124" text-anchor="middle">× p⁰ = 1</text>
<text x="260" y="160" text-anchor="middle">hash = 1·p² + 2·p¹ + 3·p⁰  (mod m)</text>
</svg>
</div>

Compute it in one pass: for each letter, multiply the hash so far by `p` (this moves every earlier letter up one power) and add the new letter:

```rust
const P: u64 = 31;
const M: u64 = 1_000_000_007;

fn hash(s: &str) -> u64 {
    let mut h = 0;
    for byte in s.bytes() {
        // a = 1, b = 2, ..., z = 26
        let value = (byte - b'a' + 1) as u64;
        // move everything so far up one power of P, then add the
        // letter
        h = (h * P + value) % M;
    }
    h
}

fn main() {
    // a * 31^2 + b * 31 + c = 1 * 961 + 2 * 31 + 3
    assert_eq!(hash("abc"), 1026);
    assert_eq!(hash("ab"), 33); // 1 * 31 + 2
    assert_eq!(hash("a"), 1);
    assert_eq!(hash(""), 0);
    // equal strings always give equal hashes
    assert_eq!(hash("hello"), hash("hello"));
}
```

- `p` is the base and `m` is the modulus (see the card on choosing them).
- Adding a letter at the **right** end is just `h · p + c`. That is why this form suits belts, windows and stacks.
- Some sources, such as the cp-algorithms article on string hashing, write the first letter at `p⁰` instead. This deck uses the order above.
