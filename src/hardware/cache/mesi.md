Each core keeps its own copies of memory in its private caches. How do the caches keep one consistent view when two cores read and write the same line? Explain the **MESI** protocol's four states, and what a **read for ownership** is.

---

**MESI** is a *cache coherence protocol*: each line in each core's cache is in one of four states. Drepper's definitions:

| State | Meaning |
|---|---|
| **M**odified | "The local processor has modified the cache line. This also implies it is the only copy in any cache." Memory is out of date |
| **E**xclusive | "The cache line is not modified but known to not be loaded into any other processor's cache." |
| **S**hared | "The cache line is not modified and might exist in another processor's cache." |
| **I**nvalid | "The cache line is invalid, i.e., unused." |

**The rules:**

- **Read miss:** load the line. If no other cache has it, it becomes **E**; otherwise all copies become **S**. If another core holds it **M**, that core first supplies its changed line.
- **Write:** a core may only write a line nobody else holds. In **M** or **E** it writes at once, with no messages: from **E** the line just becomes **M**. In **S** it must first invalidate the other copies. In **I** it sends a **read for ownership** (RFO): "give me the line, and drop your copies". Drepper calls it "the infamous 'Request For Ownership' (RFO) operation".

<div class="diagram">
<svg viewBox="0 0 640 262" width="100%" style="max-width:640px" role="img" aria-label="MESI states of one cache line in two cores over six steps: read gives Exclusive, write gives Modified silently, the other core&#x27;s read makes both Shared, a write invalidates the other copy, and alternating writes need a read for ownership each time.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .dsh{stroke:currentColor;stroke-width:1.2;fill:none;stroke-dasharray:4 4;opacity:.6}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="co" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="cgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="190" y="22" text-anchor="middle">core 0</text>
<text x="300" y="22" text-anchor="middle">core 1</text>
<text x="370" y="22" text-anchor="start">messages between the cores</text>
<text x="120" y="52" text-anchor="end">core 0 reads</text>
<rect x="140" y="34" width="100" height="26" rx="6" class="g"/>
<text x="190.0" y="51.5" text-anchor="middle">Exclusive</text>
<rect x="250" y="34" width="100" height="26" rx="6" class="c"/>
<text x="300.0" y="51.5" text-anchor="middle">Invalid</text>
<text x="370" y="52" text-anchor="start">read from memory</text>
<text x="120" y="86" text-anchor="end">core 0 writes</text>
<rect x="140" y="68" width="100" height="26" rx="6" class="r"/>
<text x="190.0" y="85.5" text-anchor="middle">Modified</text>
<rect x="250" y="68" width="100" height="26" rx="6" class="c"/>
<text x="300.0" y="85.5" text-anchor="middle">Invalid</text>
<text x="370" y="86" text-anchor="start" class="m">none: no one else has it</text>
<text x="120" y="120" text-anchor="end">core 1 reads</text>
<rect x="140" y="102" width="100" height="26" rx="6" class="k"/>
<text x="190.0" y="119.5" text-anchor="middle">Shared</text>
<rect x="250" y="102" width="100" height="26" rx="6" class="k"/>
<text x="300.0" y="119.5" text-anchor="middle">Shared</text>
<text x="370" y="120" text-anchor="start">core 0 sends its changed line</text>
<text x="120" y="154" text-anchor="end">core 1 writes</text>
<rect x="140" y="136" width="100" height="26" rx="6" class="c"/>
<text x="190.0" y="153.5" text-anchor="middle">Invalid</text>
<rect x="250" y="136" width="100" height="26" rx="6" class="r"/>
<text x="300.0" y="153.5" text-anchor="middle">Modified</text>
<text x="370" y="154" text-anchor="start">invalidate core 0&#x27;s copy</text>
<text x="120" y="188" text-anchor="end">core 0 writes</text>
<rect x="140" y="170" width="100" height="26" rx="6" class="r"/>
<text x="190.0" y="187.5" text-anchor="middle">Modified</text>
<rect x="250" y="170" width="100" height="26" rx="6" class="c"/>
<text x="300.0" y="187.5" text-anchor="middle">Invalid</text>
<text x="370" y="188" text-anchor="start" class="to">read for ownership (RFO)</text>
<text x="120" y="222" text-anchor="end">core 1 writes</text>
<rect x="140" y="204" width="100" height="26" rx="6" class="c"/>
<text x="190.0" y="221.5" text-anchor="middle">Invalid</text>
<rect x="250" y="204" width="100" height="26" rx="6" class="r"/>
<text x="300.0" y="221.5" text-anchor="middle">Modified</text>
<text x="370" y="222" text-anchor="start" class="to">read for ownership (RFO)</text>
<text x="320" y="250" text-anchor="middle" class="m">the last two rows repeat for as long as the two cores take turns writing</text>
</svg>
</div>

**A simulation in Rust** of one line and two cores:

```rust
use State::*;

/// The MESI state of one cache line in one core's cache.
#[derive(Clone, Copy, Debug, PartialEq)]
enum State {
    Modified,  // changed here; the only copy; memory is out of date
    Exclusive, // unchanged; no other cache has it
    Shared,    // unchanged; other caches may have it too
    Invalid,   // not usable
}

/// One cache line as two cores see it, and a log of the messages
/// the cores had to send each other.
struct Line {
    state: [State; 2],
    log: Vec<&'static str>,
}

impl Line {
    fn read(&mut self, me: usize) {
        let other = 1 - me;
        match (self.state[me], self.state[other]) {
            (Invalid, Invalid) => {
                self.log.push("read from memory");
                self.state[me] = Exclusive;
            }
            (Invalid, Modified) => {
                self.log.push("other core sends its changed line");
                self.state = [Shared, Shared];
            }
            (Invalid, _) => {
                self.log.push("read a copy");
                self.state = [Shared, Shared];
            }
            _ => {} // a hit in M, E or S: no messages at all
        }
    }

    fn write(&mut self, me: usize) {
        match self.state[me] {
            Modified | Exclusive => {} // no other copy: no messages
            Shared => self.log.push("invalidate the other copy"),
            Invalid => self.log.push("RFO: read for ownership"),
        }
        self.state[1 - me] = Invalid;
        self.state[me] = Modified;
    }
}

fn step(l: &mut Line, core: usize, op: &str, want: [State; 2]) {
    let before = l.log.len();
    if op == "read" {
        l.read(core);
    } else {
        l.write(core);
    }
    assert_eq!(l.state, want);
    let msgs = &l.log[before..];
    println!("core {core} {op:<5} {:?} {msgs:?}", l.state);
}

fn main() {
    let mut l = Line { state: [Invalid, Invalid], log: vec![] };
    step(&mut l, 0, "read", [Exclusive, Invalid]);
    step(&mut l, 0, "write", [Modified, Invalid]); // silent
    step(&mut l, 1, "read", [Shared, Shared]);
    step(&mut l, 1, "write", [Invalid, Modified]);
    step(&mut l, 0, "write", [Modified, Invalid]); // ping...
    step(&mut l, 1, "write", [Invalid, Modified]); // ...pong
    assert_eq!(l.log.len(), 5);
}
```

```text
core 0 read  [Exclusive, Invalid] ["read from memory"]
core 0 write [Modified, Invalid] []
core 1 read  [Shared, Shared] ["other core sends its changed line"]
core 1 write [Invalid, Modified] ["invalidate the other copy"]
core 0 write [Modified, Invalid] ["RFO: read for ownership"]
core 1 write [Invalid, Modified] ["RFO: read for ownership"]
```

**Why it matters:**

- the **E** state makes the common case cheap: data only one core uses can be written with no messages at all;
- when cores take turns writing one line, **every** write is an RFO, a round trip between cores. That is why writing shared data from many threads doesn't scale, even with no locks.

Real CPUs use extended versions with an extra state, such as Intel's MESIF and AMD's MOESI.
