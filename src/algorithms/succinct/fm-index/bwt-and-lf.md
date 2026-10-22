What is the **Burrows-Wheeler transform** (BWT) of a text, and what property of it lets you walk through the text backwards, one character at a time?

---

**The BWT.** Add an end marker `$` that is smaller than every letter, write down all rotations of the text, and sort them. The BWT is the **last column `L`** of the sorted rotations. The first column, `F`, is just the text's characters in sorted order.

For `abracadabra$`, `L = ard$rcaaaabb` and `F = $aaaaabbcdrr`.

**The property (LF mapping).** For every character `c`, the `k`-th `c` in `L` and the `k`-th `c` in `F` are **the same character of the text**. In the table below, the a's in `L`, top to bottom, are the text positions 10, 7, 0, 3, 5, and the a's in `F` are the same positions in the same order.

<div class="diagram">
<svg viewBox="0 0 640 280" width="100%" style="max-width:640px" role="img" aria-label="The sorted rotations of abracadabra$. The a&#x27;s in the last column L appear in the same order as the a&#x27;s in the first column F.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .nt{fill:#007A66;font-size:11px}svg .cl{fill:rgba(250,100,25,.22);stroke:#FA6419;stroke-width:1}svg .pth{fill:none;stroke:#007A66;stroke-width:2;stroke-dasharray:5 3}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}svg .dim{opacity:.35}.nightMode svg .tg,.night_mode svg .tg,.nightMode svg .nt,.night_mode svg .nt{fill:#14C1A0}.nightMode svg .pth,.night_mode svg .pth{stroke:#14C1A0}</style>
<text x="20" y="26" text-anchor="middle" class="m">row</text>
<text x="113.0" y="26" text-anchor="middle" class="tg">F</text>
<text x="311.0" y="26" text-anchor="middle" class="to">L</text>
<text x="20" y="53" text-anchor="middle" class="m">0</text>
<rect x="105" y="41" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="54" text-anchor="middle" class="mono">$</text>
<text x="131.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="54" text-anchor="middle" class="mono">b</text>
<text x="167.0" y="54" text-anchor="middle" class="mono">r</text>
<text x="185.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="54" text-anchor="middle" class="mono">c</text>
<text x="221.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="54" text-anchor="middle" class="mono">d</text>
<text x="257.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="54" text-anchor="middle" class="mono">b</text>
<text x="293.0" y="54" text-anchor="middle" class="mono">r</text>
<rect x="303" y="41" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="54" text-anchor="middle" class="mono">a</text>
<text x="326" y="53" text-anchor="start" class="to">pos 10</text>
<text x="20" y="72" text-anchor="middle" class="m">1</text>
<rect x="105" y="60" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="73" text-anchor="middle" class="mono">$</text>
<text x="149.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="73" text-anchor="middle" class="mono">b</text>
<text x="185.0" y="73" text-anchor="middle" class="mono">r</text>
<text x="203.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="73" text-anchor="middle" class="mono">c</text>
<text x="239.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="73" text-anchor="middle" class="mono">d</text>
<text x="275.0" y="73" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="73" text-anchor="middle" class="mono">b</text>
<rect x="303" y="60" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="73" text-anchor="middle" class="mono">r</text>
<text x="98" y="72" text-anchor="end" class="tg">pos 10</text>
<text x="20" y="91" text-anchor="middle" class="m">2</text>
<rect x="105" y="79" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="92" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="92" text-anchor="middle" class="mono">b</text>
<text x="149.0" y="92" text-anchor="middle" class="mono">r</text>
<text x="167.0" y="92" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="92" text-anchor="middle" class="mono">$</text>
<text x="203.0" y="92" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="92" text-anchor="middle" class="mono">b</text>
<text x="239.0" y="92" text-anchor="middle" class="mono">r</text>
<text x="257.0" y="92" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="92" text-anchor="middle" class="mono">c</text>
<text x="293.0" y="92" text-anchor="middle" class="mono">a</text>
<rect x="303" y="79" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="92" text-anchor="middle" class="mono">d</text>
<text x="98" y="91" text-anchor="end" class="tg">pos 7</text>
<text x="20" y="110" text-anchor="middle" class="m">3</text>
<rect x="105" y="98" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="111" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="111" text-anchor="middle" class="mono">b</text>
<text x="149.0" y="111" text-anchor="middle" class="mono">r</text>
<text x="167.0" y="111" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="111" text-anchor="middle" class="mono">c</text>
<text x="203.0" y="111" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="111" text-anchor="middle" class="mono">d</text>
<text x="239.0" y="111" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="111" text-anchor="middle" class="mono">b</text>
<text x="275.0" y="111" text-anchor="middle" class="mono">r</text>
<text x="293.0" y="111" text-anchor="middle" class="mono">a</text>
<rect x="303" y="98" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="111" text-anchor="middle" class="mono">$</text>
<text x="98" y="110" text-anchor="end" class="tg">pos 0</text>
<text x="20" y="129" text-anchor="middle" class="m">4</text>
<rect x="105" y="117" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="130" text-anchor="middle" class="mono">c</text>
<text x="149.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="130" text-anchor="middle" class="mono">d</text>
<text x="185.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="130" text-anchor="middle" class="mono">b</text>
<text x="221.0" y="130" text-anchor="middle" class="mono">r</text>
<text x="239.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="130" text-anchor="middle" class="mono">$</text>
<text x="275.0" y="130" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="130" text-anchor="middle" class="mono">b</text>
<rect x="303" y="117" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="130" text-anchor="middle" class="mono">r</text>
<text x="98" y="129" text-anchor="end" class="tg">pos 3</text>
<text x="20" y="148" text-anchor="middle" class="m">5</text>
<rect x="105" y="136" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="149" text-anchor="middle" class="mono">a</text>
<text x="131.0" y="149" text-anchor="middle" class="mono">d</text>
<text x="149.0" y="149" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="149" text-anchor="middle" class="mono">b</text>
<text x="185.0" y="149" text-anchor="middle" class="mono">r</text>
<text x="203.0" y="149" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="149" text-anchor="middle" class="mono">$</text>
<text x="239.0" y="149" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="149" text-anchor="middle" class="mono">b</text>
<text x="275.0" y="149" text-anchor="middle" class="mono">r</text>
<text x="293.0" y="149" text-anchor="middle" class="mono">a</text>
<rect x="303" y="136" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="149" text-anchor="middle" class="mono">c</text>
<text x="98" y="148" text-anchor="end" class="tg">pos 5</text>
<text x="20" y="167" text-anchor="middle" class="m">6</text>
<rect x="105" y="155" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="168" text-anchor="middle" class="mono">b</text>
<text x="131.0" y="168" text-anchor="middle" class="mono">r</text>
<text x="149.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="168" text-anchor="middle" class="mono">$</text>
<text x="185.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="168" text-anchor="middle" class="mono">b</text>
<text x="221.0" y="168" text-anchor="middle" class="mono">r</text>
<text x="239.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="257.0" y="168" text-anchor="middle" class="mono">c</text>
<text x="275.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="168" text-anchor="middle" class="mono">d</text>
<rect x="303" y="155" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="168" text-anchor="middle" class="mono">a</text>
<text x="326" y="167" text-anchor="start" class="to">pos 7</text>
<text x="20" y="186" text-anchor="middle" class="m">7</text>
<rect x="105" y="174" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="187" text-anchor="middle" class="mono">b</text>
<text x="131.0" y="187" text-anchor="middle" class="mono">r</text>
<text x="149.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="167.0" y="187" text-anchor="middle" class="mono">c</text>
<text x="185.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="187" text-anchor="middle" class="mono">d</text>
<text x="221.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="187" text-anchor="middle" class="mono">b</text>
<text x="257.0" y="187" text-anchor="middle" class="mono">r</text>
<text x="275.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="187" text-anchor="middle" class="mono">$</text>
<rect x="303" y="174" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="187" text-anchor="middle" class="mono">a</text>
<text x="326" y="186" text-anchor="start" class="to">pos 0</text>
<text x="20" y="205" text-anchor="middle" class="m">8</text>
<rect x="105" y="193" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="206" text-anchor="middle" class="mono">c</text>
<text x="131.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="206" text-anchor="middle" class="mono">d</text>
<text x="167.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="206" text-anchor="middle" class="mono">b</text>
<text x="203.0" y="206" text-anchor="middle" class="mono">r</text>
<text x="221.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="206" text-anchor="middle" class="mono">$</text>
<text x="257.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="206" text-anchor="middle" class="mono">b</text>
<text x="293.0" y="206" text-anchor="middle" class="mono">r</text>
<rect x="303" y="193" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="206" text-anchor="middle" class="mono">a</text>
<text x="326" y="205" text-anchor="start" class="to">pos 3</text>
<text x="20" y="224" text-anchor="middle" class="m">9</text>
<rect x="105" y="212" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="225" text-anchor="middle" class="mono">d</text>
<text x="131.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="225" text-anchor="middle" class="mono">b</text>
<text x="167.0" y="225" text-anchor="middle" class="mono">r</text>
<text x="185.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="203.0" y="225" text-anchor="middle" class="mono">$</text>
<text x="221.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="225" text-anchor="middle" class="mono">b</text>
<text x="257.0" y="225" text-anchor="middle" class="mono">r</text>
<text x="275.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="293.0" y="225" text-anchor="middle" class="mono">c</text>
<rect x="303" y="212" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="225" text-anchor="middle" class="mono">a</text>
<text x="326" y="224" text-anchor="start" class="to">pos 5</text>
<text x="20" y="243" text-anchor="middle" class="m">10</text>
<rect x="105" y="231" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="244" text-anchor="middle" class="mono">r</text>
<text x="131.0" y="244" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="244" text-anchor="middle" class="mono">$</text>
<text x="167.0" y="244" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="244" text-anchor="middle" class="mono">b</text>
<text x="203.0" y="244" text-anchor="middle" class="mono">r</text>
<text x="221.0" y="244" text-anchor="middle" class="mono">a</text>
<text x="239.0" y="244" text-anchor="middle" class="mono">c</text>
<text x="257.0" y="244" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="244" text-anchor="middle" class="mono">d</text>
<text x="293.0" y="244" text-anchor="middle" class="mono">a</text>
<rect x="303" y="231" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="244" text-anchor="middle" class="mono">b</text>
<text x="20" y="262" text-anchor="middle" class="m">11</text>
<rect x="105" y="250" width="16" height="17" rx="2" class="cg"/>
<text x="113.0" y="263" text-anchor="middle" class="mono">r</text>
<text x="131.0" y="263" text-anchor="middle" class="mono">a</text>
<text x="149.0" y="263" text-anchor="middle" class="mono">c</text>
<text x="167.0" y="263" text-anchor="middle" class="mono">a</text>
<text x="185.0" y="263" text-anchor="middle" class="mono">d</text>
<text x="203.0" y="263" text-anchor="middle" class="mono">a</text>
<text x="221.0" y="263" text-anchor="middle" class="mono">b</text>
<text x="239.0" y="263" text-anchor="middle" class="mono">r</text>
<text x="257.0" y="263" text-anchor="middle" class="mono">a</text>
<text x="275.0" y="263" text-anchor="middle" class="mono">$</text>
<text x="293.0" y="263" text-anchor="middle" class="mono">a</text>
<rect x="303" y="250" width="16" height="17" rx="2" class="cr"/>
<text x="311.0" y="263" text-anchor="middle" class="mono">b</text>
<text x="386" y="60" text-anchor="start" class="to">a&#x27;s in L, top to bottom: rows 0, 6, 7, 8, 9</text>
<text x="386" y="80" text-anchor="start" class="to">text positions 10, 7, 0, 3, 5</text>
<text x="386" y="112" text-anchor="start" class="tg">a&#x27;s in F, top to bottom: rows 1 to 5</text>
<text x="386" y="132" text-anchor="start" class="tg">text positions 10, 7, 0, 3, 5</text>
<text x="386" y="164" text-anchor="start">the same order, so the k-th a in L</text>
<text x="386" y="184" text-anchor="start">is the k-th a in F</text>
</svg>
</div>

Why: take the rows whose last character is `c`, and rotate each one right by one place. That moves the `c` to the front and gives exactly the rows that start with `c`. Their order doesn't change, because after the shared first `c` each one continues with the old row, and the old rows were already sorted.

**Walking backwards.** In row `i`, `L[i]` is the character just before the row's start in the text. That character's own row is

`LF(i) = C[c] + rank(c, i)`, with `c = L[i]`, where

- `C[c]` is the number of characters in the text smaller than `c`. The rows that start with `c` begin at row `C[c]`.
- `rank(c, i)` is how many times `c` appears in `L` above row `i`, so `L[i]` is the `c` with that number, counting from 0.

Example: row 7 (`bracadabra$a`) has `L[7] = a`. `C[a] = 1`, since only `$` is smaller, and `rank(a, 7) = 2`, because there are a's at rows 0 and 6. So `LF(7) = 3`, and row 3 is `abracadabra$`, the text starting with that `a`.

Starting at row 0, the row that begins with `$`, and following LF, reads the text backwards: `a, r, b, a, d, a, c, a, r, b, a`. So the BWT can be undone. It also tends to put equal characters next to each other (`aaaa`, `bb`), because rows that start with the same context sort together. That is why the compressor bzip2 uses it.

```rust
/// The BWT: the last column of the sorted rotations.
fn bwt(text: &[u8]) -> Vec<u8> {
    let n = text.len();
    let rotation = |s: usize| [&text[s..], &text[..s]].concat();
    let mut starts: Vec<usize> = (0..n).collect();
    starts.sort_by_key(|&s| rotation(s));
    starts.iter().map(|&s| text[(s + n - 1) % n]).collect()
}

/// C[c]: how many characters of the text are smaller than c.
fn smaller(text: &[u8], c: u8) -> usize {
    text.iter().filter(|&&x| x < c).count()
}

/// How many times c appears in l[..i].
fn rank(l: &[u8], c: u8, i: usize) -> usize {
    l[..i].iter().filter(|&&x| x == c).count()
}

fn main() {
    let text = b"abracadabra$";
    let l = bwt(text);
    assert_eq!(l, b"ard$rcaaaabb");

    // LF(7) = C[a] + rank(a, 7) = 1 + 2 = 3
    let lf = |i: usize| smaller(text, l[i]) + rank(&l, l[i], i);
    assert_eq!(lf(7), 3);

    // walk backwards from the row that starts with $
    let mut row = 0;
    let mut backwards = Vec::new();
    for _ in 0..text.len() - 1 {
        backwards.push(l[row]);
        row = lf(row);
    }
    backwards.reverse();
    assert_eq!(backwards, b"abracadabra");
}
```
