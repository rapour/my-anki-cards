Where does `apt` get packages from? Read a `.sources` entry, say which addresses apt downloads from it, and read the output of `apt policy`.

---

**Where.** apt's *sources* are files in `/etc/apt/sources.list.d/`. Since Ubuntu 24.04 they use the **deb822** format: `.sources` files made of `Field: value` lines, one block (a *stanza*) per source. Older one-line `.list` files still work. Ubuntu's own entry, from `ubuntu.sources`:

```text
Types: deb
URIs: http://archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

| Field | Meaning |
|---|---|
| `Types` | `deb` for ready-to-install packages, `deb-src` for source code |
| `URIs` | the repository's base address |
| `Suites` | which collection to use. Ubuntu names them after the release (`noble` is 24.04, `resolute` is 26.04); a vendor may use a release name or a fixed name such as `stable` |
| `Components` | parts of the suite, such as `main` and `universe` |
| `Signed-By` | the key the repository's index must be signed with. apt refuses an index whose signature doesn't check out |
| `Enabled` | optional. `Enabled: no` switches the stanza off without deleting it |

A vendor's entry in the old one-line format looks like this:

```text
deb [signed-by=/usr/share/keyrings/example.gpg] https://vendor.example.com/repo noble main
```

**Which addresses.** apt builds URLs from the fields:

<div class="diagram">
<svg viewBox="0 0 640 350" width="100%" style="max-width:640px" role="img" aria-label="A sources stanza gives a base URI, a suite and components. apt downloads URI/dists/suite/InRelease, then URI/dists/suite/component/binary-amd64/Packages, then the package files under URI/pool.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}</style>
<text x="20" y="20" text-anchor="start" class="m">example.sources</text>
<rect x="14" y="28" width="380" height="104" rx="6" class="k"/>
<text x="26" y="50" text-anchor="start" class="mono">Types: deb</text>
<text x="26" y="69" text-anchor="start" class="mono">URIs: <tspan class="tg">https://vendor.example.com/repo</tspan></text>
<text x="26" y="88" text-anchor="start" class="mono">Suites: <tspan class="to">noble</tspan></text>
<text x="26" y="107" text-anchor="start" class="mono">Components: main</text>
<text x="26" y="126" text-anchor="start" class="mono">Signed-By: /usr/share/keyrings/example.gpg</text>
<line x1="200" y1="134" x2="200" y2="154" class="ln" marker-end="url(#ah)"/>
<text x="210" y="148" text-anchor="start" class="m">apt update fetches 1 and 2; installing a package fetches 3</text>
<text x="20" y="172" text-anchor="start">1. the suite&#x27;s signed table of contents</text>
<text x="34" y="192" text-anchor="start" class="mono"><tspan class="tg">https://vendor.example.com/repo</tspan>/dists/<tspan class="to">noble</tspan>/InRelease</text>
<text x="20" y="228" text-anchor="start">2. the list of packages in each component</text>
<text x="34" y="248" text-anchor="start" class="mono"><tspan class="tg">https://vendor.example.com/repo</tspan>/dists/<tspan class="to">noble</tspan>/main/binary-amd64/Packages</text>
<text x="20" y="284" text-anchor="start">3. the package files, at the paths that list gives</text>
<text x="34" y="304" text-anchor="start" class="mono"><tspan class="tg">https://vendor.example.com/repo</tspan>/pool/main/e/examplepkg/…_amd64.deb</text>
<text x="20" y="338" text-anchor="start" class="m">A suite exists for a repository when its dists/&lt;suite&gt;/Release (or InRelease) file does.</text>
</svg>
</div>

So "does this repository publish for release X?" is the same as "does `URIs/dists/X/Release` exist?":

```sh
$ curl -s -o /dev/null -w '%{http_code}\n' http://archive.ubuntu.com/ubuntu/dists/noble/Release
200
$ curl -s -o /dev/null -w '%{http_code}\n' http://archive.ubuntu.com/ubuntu/dists/nosuchsuite/Release
404
```

`-s` hides progress, `-o /dev/null` throws the file away, and `-w '%{http_code}\n'` prints only the HTTP status: 200 means found, 404 means not found.

**`apt policy`** shows, for one package, which versions exist and where each comes from. Real output on Ubuntu 24.04:

```text
curl:
  Installed: 8.5.0-2ubuntu10.15
  Candidate: 8.5.0-2ubuntu10.16
  Version table:
     8.5.0-2ubuntu10.16 500
        500 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages
 *** 8.5.0-2ubuntu10.15 100
        100 /var/lib/dpkg/status
     8.5.0-2ubuntu10 500
        500 http://archive.ubuntu.com/ubuntu noble/main amd64 Packages
```

- **Installed** is the version you have, marked `***` in the table.
- **Candidate** is what an upgrade would install: the newest version from the highest-priority place.
- Each version lists where it is available, with a **priority**. 500 is a normal enabled source. 100 is `/var/lib/dpkg/status`, the record of what is installed on this machine.

If a package's only line is `100 /var/lib/dpkg/status`, it is installed but **no enabled source offers it**, so it will never be updated.
