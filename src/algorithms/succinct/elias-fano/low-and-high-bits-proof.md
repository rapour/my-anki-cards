Prove that for a non-negative integer `x`, the `l` lowest bits of `x`, read as a number, equal `x mod 2^l`, and the remaining bits, read as a number, equal `x >> l = floor(x / 2^l)`. (`x >> l` shifts the bits of `x` right by `l` places, dropping the `l` lowest.)

---

**Idea.** Cutting the binary digits of $x$ after the $l$ lowest ones writes $x = 2^l \cdot H + \mathrm{Lo}$, where $H$ is the high bits read as a number and $\mathrm{Lo}$ is the low bits read as a number, with $0 \le \mathrm{Lo} < 2^l$. Dividing by $2^l$ has only one answer of that shape, so $H$ is the quotient and $\mathrm{Lo}$ is the remainder.

**Example.** $x = 45$, which is `101101` in binary, and $l = 2$.

<div class="diagram">
<svg viewBox="0 0 580 220" width="100%" style="max-width:580px" role="img" aria-label="45 in binary is 101101. Splitting it after the two lowest bits gives the high bits 1011, which is 11, and the low bits 01, which is 1. 45 equals 4 times 11 plus 1.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}</style>
<text x="100" y="38" text-anchor="end" class="m">position k</text>
<text x="100" y="77" text-anchor="end">bit b_k</text>
<text x="100" y="116" text-anchor="end" class="m">worth 2^k</text>
<text x="139.0" y="38" text-anchor="middle" class="m">5</text>
<rect x="113" y="52" width="52" height="40" rx="6" class="g"/>
<text x="139.0" y="76.5" text-anchor="middle">1</text>
<text x="139.0" y="116" text-anchor="middle" class="m">32</text>
<text x="197.0" y="38" text-anchor="middle" class="m">4</text>
<rect x="171" y="52" width="52" height="40" rx="6" class="g"/>
<text x="197.0" y="76.5" text-anchor="middle">0</text>
<text x="197.0" y="116" text-anchor="middle" class="m">16</text>
<text x="255.0" y="38" text-anchor="middle" class="m">3</text>
<rect x="229" y="52" width="52" height="40" rx="6" class="g"/>
<text x="255.0" y="76.5" text-anchor="middle">1</text>
<text x="255.0" y="116" text-anchor="middle" class="m">8</text>
<text x="313.0" y="38" text-anchor="middle" class="m">2</text>
<rect x="287" y="52" width="52" height="40" rx="6" class="g"/>
<text x="313.0" y="76.5" text-anchor="middle">1</text>
<text x="313.0" y="116" text-anchor="middle" class="m">4</text>
<text x="371.0" y="38" text-anchor="middle" class="m">1</text>
<rect x="345" y="52" width="52" height="40" rx="6" class="r"/>
<text x="371.0" y="76.5" text-anchor="middle">0</text>
<text x="371.0" y="116" text-anchor="middle" class="m">2</text>
<text x="429.0" y="38" text-anchor="middle" class="m">0</text>
<rect x="403" y="52" width="52" height="40" rx="6" class="r"/>
<text x="429.0" y="76.5" text-anchor="middle">1</text>
<text x="429.0" y="116" text-anchor="middle" class="m">1</text>
<line x1="342" y1="26" x2="342" y2="126" class="ln" stroke-dasharray="4 4"/>
<text x="342" y="22" text-anchor="middle" class="m">split at l = 2</text>
<line x1="114" y1="136" x2="336" y2="136" class="ln"/>
<line x1="348" y1="136" x2="454" y2="136" class="ln"/>
<text x="226.0" y="156" text-anchor="middle" class="tg">H = 1011 = 11</text>
<text x="226.0" y="174" text-anchor="middle" class="m">high terms: 32 + 8 + 4 = 44 = 2^2 · 11</text>
<text x="400.0" y="156" text-anchor="middle" class="to">Lo = 01 = 1</text>
<text x="400.0" y="174" text-anchor="middle" class="m">low terms: 1</text>
<text x="290" y="206" text-anchor="middle">45 = 2^2 · 11 + 1 with 0 ≤ 1 &lt; 4, so 45 &gt;&gt; 2 = 11 and 45 mod 4 = 1</text>
</svg>
</div>

**Proof.** Let $x$ have the binary digits $b_{L-1} \dots b_1 b_0$, so $L$ is the number of digits and each $b_k$ is 0 or 1.

**1. Write $x$ as a sum of its bits.** Bit $k$ is worth $2^k$:

$$
x = \sum_{k=0}^{L-1} b_k \, 2^k
$$

**2. Split the sum at position $l$.** Every term with $k \ge l$ contains $2^l$, so take it out of those terms:

$$
x = \sum_{k=l}^{L-1} b_k \, 2^k + \sum_{k=0}^{l-1} b_k \, 2^k = 2^l \cdot H + \mathrm{Lo}
$$

$$
\text{where} \quad H = \sum_{k=l}^{L-1} b_k \, 2^{k-l} \quad \text{and} \quad \mathrm{Lo} = \sum_{k=0}^{l-1} b_k \, 2^k
$$

- $H$ is the high bits $b_{L-1} \dots b_l$ read as a number: bit $k$ now counts as $2^{k-l}$, as if it sat at position $k - l$. Every exponent $k - l$ is 0 or more, so $H$ is a whole number.
- $\mathrm{Lo}$ is the low bits $b_{l-1} \dots b_0$ read as a number.

For 45: the high terms are $32 + 8 + 4 = 44 = 4 \cdot 11$, and the low terms add up to 1.

**3. $\mathrm{Lo}$ is smaller than $2^l$.** It is largest when all $l$ low bits are 1:

$$
0 \le \mathrm{Lo} \le \sum_{k=0}^{l-1} 2^k = 2^l - 1 < 2^l
$$

With $l = 2$, the largest is binary `11`, which is $3 = 2^2 - 1$.

**4. Division by $2^l$ has only one answer.** Dividing $x$ by $2^l$ means finding whole numbers $q$ (the quotient, $\lfloor x / 2^l \rfloor$) and $r$ (the remainder, $x \bmod 2^l$) such that

$$
x = q \cdot 2^l + r \quad \text{and} \quad 0 \le r < 2^l
$$

Suppose $(q, r)$ and $(q', r')$ both work. Subtracting one equation from the other gives $(q - q') \cdot 2^l = r' - r$. The right side lies between $-(2^l - 1)$ and $2^l - 1$. The left side is a multiple of $2^l$, and the only multiple of $2^l$ in that range is 0. So $q = q'$ and $r = r'$.

**Conclusion.** Steps 2 and 3 give one answer, $q = H$ and $r = \mathrm{Lo}$, and step 4 says there is no other. So $\mathrm{Lo} = x \bmod 2^l$ and $H = \lfloor x / 2^l \rfloor$, which is what `x >> l` computes. ∎

The edge cases fit too: with $l = 0$ there are no low bits, so $\mathrm{Lo} = 0$ and $H = x$. With $l \ge L$ there are no high bits, so $H = 0$ and $\mathrm{Lo} = x$.

**Why it matters for Elias-Fano.** Elias-Fano stores a sorted list of numbers by splitting each number `x` into a high part `x >> l` and a low part, its `l` lowest bits.

- **Nothing is lost.** `x == (h << l) | lo`. The `|` (bitwise OR) works like `+` here: `h << l` has 0s in its `l` lowest bits, and `lo` fits in exactly those bits, so no bits overlap and nothing carries. For 45: `(11 << 2) | 1 = 44 | 1 = 45`.
- **Sorted numbers have sorted high parts.** Write $H_x$ for the high part of $x$. If $x \le y$, then $H_x \cdot 2^l \le x \le y < (H_y + 1) \cdot 2^l$, so $H_x < H_y + 1$, that is $H_x \le H_y$. For 3, 4, 7, 13 with $l = 2$ the high parts are 0, 1, 1, 3.
- **So the high parts can be stored as counts.** In a bit array, each number writes one `1`, and a `0` closes each possible high part. Number `i` (counting from 0) then has its `1` at position $H + i$. Decoding finds $H$ as `select1(i) - i`, where `select1(i)` is the position of the `1` number `i`. The low parts go into a plain array of `l` bits each, and `x = (h << l) | lo` puts the number back together.

```rust
/// The l lowest bits of x, read as a number.
fn low_bits(x: u64, l: u32) -> u64 {
    // the mask has l 1s at the bottom
    x & ((1u64 << l) - 1)
}

/// Build H and Lo from the bits one by one, as in step 2.
fn split_by_sum(x: u64, l: u32) -> (u64, u64) {
    let (mut h, mut lo) = (0, 0);
    for k in 0..64 {
        let bit = (x >> k) & 1;
        if k >= l {
            // bit k counts as 2^(k - l) in H
            h += bit << (k - l);
        } else {
            lo += bit << k;
        }
    }
    (h, lo)
}

fn main() {
    // the example: 45 = 0b1011_01 with l = 2
    assert_eq!(split_by_sum(45, 2), (0b1011, 0b01));
    assert_eq!(45, 4 * 11 + 1);
    assert_eq!((45 >> 2, 45 % 4), (11, 1));

    // every x below 2^11 and every l from 0 to 15
    // (l = 0 and l above 11 are the edge cases)
    for x in 0..2048u64 {
        for l in 0..16u32 {
            let p = 1u64 << l;
            let (h, lo) = split_by_sum(x, l);
            // step 2: x = 2^l * H + Lo
            assert_eq!(x, p * h + lo);
            // step 3: Lo < 2^l
            assert!(lo < p);
            // step 4: exactly one q has 0 <= x - q * 2^l < 2^l
            let fits = |q: u64| q * p <= x && x - q * p < p;
            assert_eq!((0..=x / p + 1).filter(|&q| fits(q)).count(), 1);
            // conclusion
            assert_eq!((h, lo), (x / p, x % p));
            assert_eq!((h, lo), (x >> l, low_bits(x, l)));
            // | works like + because the bits do not overlap
            assert_eq!((h << l) | lo, (h << l) + lo);
        }
    }

    // sorted numbers have sorted high parts
    let sorted = [3u64, 4, 7, 13, 14, 15, 21, 43];
    let highs: Vec<u64> = sorted.iter().map(|&x| x >> 2).collect();
    assert_eq!(highs, vec![0, 1, 1, 3, 3, 3, 5, 10]);
    assert!(highs.windows(2).all(|w| w[0] <= w[1]));
}
```
