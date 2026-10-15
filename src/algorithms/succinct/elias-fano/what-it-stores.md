How does Elias-Fano store a sorted list of `n` numbers, all smaller than `u`, in few bits?

---

It splits every number `x` into a **low part** and a **high part**, and stores the two parts in different ways.

1. Choose `l = floor(log2(u / n))`.
2. The **low part** is the lowest `l` bits of `x`. These are stored as they are, `l` bits per number.
3. The **high part** is `x >> l`. Think of it as a *bucket* number: numbers with the same high part share a bucket. The high parts go into one bit array, the **high bits**. Each bucket, in order, writes one `1` for every number in it, then a `0` to close the bucket.

Because the list is sorted, the high parts never go down, so counting 1s and 0s is enough to get them back. Number `i` (counting from 0) has its `1` at position `high + i`: one `0` for each bucket closed before it, and one `1` for each of the `i` numbers before it.

Example: 3, 4, 7, 13, 14, 15, 21, 43 with `u = 44`, so `l = floor(log2(5.5)) = 2`.

<div class="diagram">
<svg viewBox="0 0 640 260" width="100%" style="max-width:640px" role="img" aria-label="Each number is split into a high part and a low part. The low parts are stored as they are. The high parts become a bit array with one 1 per number and one 0 closing each bucket.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}</style>
<text x="166" y="24" text-anchor="end" class="m">index</text>
<text x="166" y="50" text-anchor="end">number</text>
<text x="166" y="82" text-anchor="end">high = x &gt;&gt; 2</text>
<text x="166" y="112" text-anchor="end">low = x &amp; 3</text>
<text x="196" y="24" text-anchor="middle" class="m">0</text>
<text x="196" y="50" text-anchor="middle">3</text>
<rect x="174" y="66" width="44" height="24" rx="6" class="g"/>
<text x="196.0" y="82.5" text-anchor="middle">0</text>
<rect x="174" y="96" width="44" height="24" rx="6" class="r"/>
<text x="196.0" y="112.5" text-anchor="middle">3</text>
<text x="254" y="24" text-anchor="middle" class="m">1</text>
<text x="254" y="50" text-anchor="middle">4</text>
<rect x="232" y="66" width="44" height="24" rx="6" class="g"/>
<text x="254.0" y="82.5" text-anchor="middle">1</text>
<rect x="232" y="96" width="44" height="24" rx="6" class="r"/>
<text x="254.0" y="112.5" text-anchor="middle">0</text>
<text x="312" y="24" text-anchor="middle" class="m">2</text>
<text x="312" y="50" text-anchor="middle">7</text>
<rect x="290" y="66" width="44" height="24" rx="6" class="g"/>
<text x="312.0" y="82.5" text-anchor="middle">1</text>
<rect x="290" y="96" width="44" height="24" rx="6" class="r"/>
<text x="312.0" y="112.5" text-anchor="middle">3</text>
<text x="370" y="24" text-anchor="middle" class="m">3</text>
<text x="370" y="50" text-anchor="middle">13</text>
<rect x="348" y="66" width="44" height="24" rx="6" class="g"/>
<text x="370.0" y="82.5" text-anchor="middle">3</text>
<rect x="348" y="96" width="44" height="24" rx="6" class="r"/>
<text x="370.0" y="112.5" text-anchor="middle">1</text>
<text x="428" y="24" text-anchor="middle" class="m">4</text>
<text x="428" y="50" text-anchor="middle">14</text>
<rect x="406" y="66" width="44" height="24" rx="6" class="g"/>
<text x="428.0" y="82.5" text-anchor="middle">3</text>
<rect x="406" y="96" width="44" height="24" rx="6" class="r"/>
<text x="428.0" y="112.5" text-anchor="middle">2</text>
<text x="486" y="24" text-anchor="middle" class="m">5</text>
<text x="486" y="50" text-anchor="middle">15</text>
<rect x="464" y="66" width="44" height="24" rx="6" class="g"/>
<text x="486.0" y="82.5" text-anchor="middle">3</text>
<rect x="464" y="96" width="44" height="24" rx="6" class="r"/>
<text x="486.0" y="112.5" text-anchor="middle">3</text>
<text x="544" y="24" text-anchor="middle" class="m">6</text>
<text x="544" y="50" text-anchor="middle">21</text>
<rect x="522" y="66" width="44" height="24" rx="6" class="g"/>
<text x="544.0" y="82.5" text-anchor="middle">5</text>
<rect x="522" y="96" width="44" height="24" rx="6" class="r"/>
<text x="544.0" y="112.5" text-anchor="middle">1</text>
<text x="602" y="24" text-anchor="middle" class="m">7</text>
<text x="602" y="50" text-anchor="middle">43</text>
<rect x="580" y="66" width="44" height="24" rx="6" class="g"/>
<text x="602.0" y="82.5" text-anchor="middle">10</text>
<rect x="580" y="96" width="44" height="24" rx="6" class="r"/>
<text x="602.0" y="112.5" text-anchor="middle">3</text>
<text x="166" y="144" text-anchor="end" class="m">low parts, 2 bits each:</text>
<text x="174" y="144" text-anchor="start" class="to">3 0 3 1 2 3 1 3 (stored as they are)</text>
<text x="100" y="195" text-anchor="end">high bits</text>
<text x="122.5" y="172" text-anchor="middle" class="m">0</text>
<rect x="111" y="178" width="23" height="24" rx="2" class="cg"/>
<text x="122.5" y="195" text-anchor="middle">1</text>
<text x="147.5" y="172" text-anchor="middle" class="m">1</text>
<rect x="136" y="178" width="23" height="24" rx="2" class="c"/>
<text x="147.5" y="195" text-anchor="middle">0</text>
<text x="172.5" y="172" text-anchor="middle" class="m">2</text>
<rect x="161" y="178" width="23" height="24" rx="2" class="cg"/>
<text x="172.5" y="195" text-anchor="middle">1</text>
<text x="197.5" y="172" text-anchor="middle" class="m">3</text>
<rect x="186" y="178" width="23" height="24" rx="2" class="cg"/>
<text x="197.5" y="195" text-anchor="middle">1</text>
<text x="222.5" y="172" text-anchor="middle" class="m">4</text>
<rect x="211" y="178" width="23" height="24" rx="2" class="c"/>
<text x="222.5" y="195" text-anchor="middle">0</text>
<text x="247.5" y="172" text-anchor="middle" class="m">5</text>
<rect x="236" y="178" width="23" height="24" rx="2" class="c"/>
<text x="247.5" y="195" text-anchor="middle">0</text>
<text x="272.5" y="172" text-anchor="middle" class="m">6</text>
<rect x="261" y="178" width="23" height="24" rx="2" class="cg"/>
<text x="272.5" y="195" text-anchor="middle">1</text>
<text x="297.5" y="172" text-anchor="middle" class="m">7</text>
<rect x="286" y="178" width="23" height="24" rx="2" class="cg"/>
<text x="297.5" y="195" text-anchor="middle">1</text>
<text x="322.5" y="172" text-anchor="middle" class="m">8</text>
<rect x="311" y="178" width="23" height="24" rx="2" class="cg"/>
<text x="322.5" y="195" text-anchor="middle">1</text>
<text x="347.5" y="172" text-anchor="middle" class="m">9</text>
<rect x="336" y="178" width="23" height="24" rx="2" class="c"/>
<text x="347.5" y="195" text-anchor="middle">0</text>
<text x="372.5" y="172" text-anchor="middle" class="m">10</text>
<rect x="361" y="178" width="23" height="24" rx="2" class="c"/>
<text x="372.5" y="195" text-anchor="middle">0</text>
<text x="397.5" y="172" text-anchor="middle" class="m">11</text>
<rect x="386" y="178" width="23" height="24" rx="2" class="cg"/>
<text x="397.5" y="195" text-anchor="middle">1</text>
<text x="422.5" y="172" text-anchor="middle" class="m">12</text>
<rect x="411" y="178" width="23" height="24" rx="2" class="c"/>
<text x="422.5" y="195" text-anchor="middle">0</text>
<text x="447.5" y="172" text-anchor="middle" class="m">13</text>
<rect x="436" y="178" width="23" height="24" rx="2" class="c"/>
<text x="447.5" y="195" text-anchor="middle">0</text>
<text x="472.5" y="172" text-anchor="middle" class="m">14</text>
<rect x="461" y="178" width="23" height="24" rx="2" class="c"/>
<text x="472.5" y="195" text-anchor="middle">0</text>
<text x="497.5" y="172" text-anchor="middle" class="m">15</text>
<rect x="486" y="178" width="23" height="24" rx="2" class="c"/>
<text x="497.5" y="195" text-anchor="middle">0</text>
<text x="522.5" y="172" text-anchor="middle" class="m">16</text>
<rect x="511" y="178" width="23" height="24" rx="2" class="c"/>
<text x="522.5" y="195" text-anchor="middle">0</text>
<text x="547.5" y="172" text-anchor="middle" class="m">17</text>
<rect x="536" y="178" width="23" height="24" rx="2" class="cg"/>
<text x="547.5" y="195" text-anchor="middle">1</text>
<text x="572.5" y="172" text-anchor="middle" class="m">18</text>
<rect x="561" y="178" width="23" height="24" rx="2" class="c"/>
<text x="572.5" y="195" text-anchor="middle">0</text>
<text x="597.5" y="172" text-anchor="middle" class="m">19</text>
<rect x="586" y="178" width="23" height="24" rx="2" class="c"/>
<text x="597.5" y="195" text-anchor="middle">0</text>
<text x="100" y="224" text-anchor="end" class="m">bucket</text>
<line x1="113" y1="210" x2="157" y2="210" class="ln"/>
<text x="135.0" y="224" text-anchor="middle" class="m">0</text>
<line x1="163" y1="210" x2="232" y2="210" class="ln"/>
<text x="197.5" y="224" text-anchor="middle" class="m">1</text>
<line x1="238" y1="210" x2="257" y2="210" class="ln"/>
<text x="247.5" y="224" text-anchor="middle" class="m">2</text>
<line x1="263" y1="210" x2="357" y2="210" class="ln"/>
<text x="310.0" y="224" text-anchor="middle" class="m">3</text>
<line x1="363" y1="210" x2="382" y2="210" class="ln"/>
<text x="372.5" y="224" text-anchor="middle" class="m">4</text>
<line x1="388" y1="210" x2="432" y2="210" class="ln"/>
<text x="410.0" y="224" text-anchor="middle" class="m">5</text>
<line x1="438" y1="210" x2="457" y2="210" class="ln"/>
<text x="447.5" y="224" text-anchor="middle" class="m">6</text>
<line x1="463" y1="210" x2="482" y2="210" class="ln"/>
<text x="472.5" y="224" text-anchor="middle" class="m">7</text>
<line x1="488" y1="210" x2="507" y2="210" class="ln"/>
<text x="497.5" y="224" text-anchor="middle" class="m">8</text>
<line x1="513" y1="210" x2="532" y2="210" class="ln"/>
<text x="522.5" y="224" text-anchor="middle" class="m">9</text>
<line x1="538" y1="210" x2="582" y2="210" class="ln"/>
<text x="560.0" y="224" text-anchor="middle" class="m">10</text>
<line x1="588" y1="210" x2="607" y2="210" class="ln"/>
<text x="597.5" y="224" text-anchor="middle" class="m">11</text>
<text x="320" y="250" text-anchor="middle" class="m">number i puts its 1 at position high + i; every bucket ends with a 0</text>
</svg>
</div>

```rust
/// Elias-Fano parts of a sorted list of numbers below `u`.
struct EliasFano {
    // how many low bits each number keeps
    l: u32,
    // the low part of every number (l bits each)
    low: Vec<u64>,
    // high parts: a 1 per number, a 0 closing each bucket
    high: Vec<bool>,
}

fn encode(values: &[u64], u: u64) -> EliasFano {
    let n = values.len() as u64;
    // floor(log2(u / n)), or 0 when n >= u
    let l = if u > n { (u / n).ilog2() } else { 0 };
    let mut high = vec![false; (n + (u >> l) + 1) as usize];
    let mut low = Vec::new();
    for (i, &x) in values.iter().enumerate() {
        // the l lowest bits
        low.push(x & ((1 << l) - 1));
        // bucket x >> l, moved right by the i earlier 1s
        high[(x >> l) as usize + i] = true;
    }
    EliasFano { l, low, high }
}

fn main() {
    let values = [3, 4, 7, 13, 14, 15, 21, 43];
    let ef = encode(&values, 44);

    // 44 / 8 = 5.5, and floor(log2(5.5)) = 2
    assert_eq!(ef.l, 2);
    assert_eq!(ef.low, vec![3, 0, 3, 1, 2, 3, 1, 3]);

    let bits: String =
        ef.high.iter().map(|&b| if b { '1' } else { '0' }).collect();
    assert_eq!(bits, "10110011100100000100");

    // 20 high bits + 8 * 2 low bits = 36 bits,
    // against 8 * 6 = 48 bits for plain 6-bit numbers
    assert_eq!(ef.high.len() + ef.low.len() * ef.l as usize, 36);
}
```

Repeated numbers are allowed: they share a bucket, and each still gets its own `1`.
