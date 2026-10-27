After an Ubuntu release upgrade, for example from 24.04 (`noble`) to 26.04 (`resolute`), a package you installed from a third-party apt source stops getting updates. Here the package is `examplepkg`, from `/etc/apt/sources.list.d/example.sources`. Why does this happen, and how do you fix it?

---

**Why.** The release upgrader, `do-release-upgrade`, only trusts Ubuntu's own mirrors to publish the new release. It switches every other source off with `Enabled: no`, and leaves its `Suites` at the old name, `noble`, because it can't know whether the vendor publishes `resolute`. The package stays installed, but no enabled source offers it any more. It is **stranded**: no updates, and no security fixes.

The fix: find it, see where it came from, ask the vendor whether it publishes the new release, then **keep**, **remove** or **replace** it.

<div class="diagram">
<svg viewBox="0 0 640 404" width="100%" style="max-width:640px" role="img" aria-label="Flow: a stranded package. If the vendor publishes the new release and you want the package, re-point the source and upgrade. Otherwise check what needs it: if nothing, purge it and its source; if something does, install Ubuntu&#x27;s own build. Then check again.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}</style>
<rect x="20" y="10" width="600" height="40" rx="6" class="r"/>
<text x="320.0" y="26.5" text-anchor="middle">examplepkg is stranded: pro security-status --unavailable lists it</text>
<text x="320.0" y="42.5" text-anchor="middle" class="m">apt policy shows only /var/lib/dpkg/status; its source says Suites: noble, Enabled: no</text>
<line x1="320" y1="52" x2="320" y2="74" class="ln" marker-end="url(#ah)"/>
<rect x="120" y="76" width="400" height="34" rx="6" class="k"/>
<text x="320.0" y="97.5" text-anchor="middle">curl …/dists/resolute/Release: does the vendor publish?</text>
<line x1="220" y1="112" x2="150" y2="148" class="ln" marker-end="url(#ah)"/>
<text x="152" y="132" text-anchor="end" class="tg">200, and you want it</text>
<line x1="420" y1="112" x2="470" y2="148" class="ln" marker-end="url(#ah)"/>
<text x="452" y="132" text-anchor="start" class="to">404, or you don&#x27;t want it</text>
<rect x="20" y="150" width="270" height="76" rx="6" class="g"/>
<text x="155.0" y="168.5" text-anchor="middle">Keep it</text>
<text x="155.0" y="184.5" text-anchor="middle" class="m">sed: Suites: resolute, delete Enabled: no</text>
<text x="155.0" y="200.5" text-anchor="middle" class="m">apt update (no E: or W: lines)</text>
<text x="155.0" y="216.5" text-anchor="middle" class="m">apt full-upgrade</text>
<rect x="330" y="150" width="290" height="58" rx="6" class="k"/>
<text x="475.0" y="167.5" text-anchor="middle">Who needs it?</text>
<text x="475.0" y="183.5" text-anchor="middle" class="m">apt -s purge examplepkg (preview only)</text>
<text x="475.0" y="199.5" text-anchor="middle" class="m">apt rdepends --installed examplepkg</text>
<line x1="400" y1="210" x2="372" y2="252" class="ln" marker-end="url(#ah)"/>
<text x="380" y="236" text-anchor="end" class="m">nothing</text>
<line x1="560" y1="210" x2="578" y2="252" class="ln" marker-end="url(#ah)"/>
<text x="576" y="236" text-anchor="start" class="m">something</text>
<rect x="250" y="254" width="200" height="76" rx="6" class="r"/>
<text x="350.0" y="272.5" text-anchor="middle">Remove it</text>
<text x="350.0" y="288.5" text-anchor="middle" class="m">apt purge examplepkg</text>
<text x="350.0" y="304.5" text-anchor="middle" class="m">rm example.sources</text>
<text x="350.0" y="320.5" text-anchor="middle" class="m">apt autoremove --purge</text>
<rect x="462" y="254" width="158" height="76" rx="6" class="g"/>
<text x="541.0" y="272.5" text-anchor="middle">Use Ubuntu&#x27;s build</text>
<text x="541.0" y="288.5" text-anchor="middle" class="m">apt install</text>
<text x="541.0" y="304.5" text-anchor="middle" class="m">--allow-downgrades</text>
<text x="541.0" y="320.5" text-anchor="middle" class="m">examplepkg=&lt;version&gt;</text>
<line x1="155" y1="228" x2="155" y2="360" class="ln" marker-end="url(#ah)"/>
<line x1="350" y1="332" x2="330" y2="360" class="ln" marker-end="url(#ah)"/>
<line x1="540" y1="332" x2="500" y2="360" class="ln" marker-end="url(#ah)"/>
<rect x="120" y="362" width="400" height="34" rx="6" class="g"/>
<text x="320.0" y="383.5" text-anchor="middle">pro security-status --unavailable: examplepkg is gone</text>
</svg>
</div>

**1. Find the stranded packages.**

```sh
pro security-status --unavailable
```

`pro` is the Ubuntu Pro client, part of a standard Ubuntu install. `--unavailable` lists installed packages that no enabled source offers.

**2. See where one came from.**

```sh
apt policy examplepkg
grep -E '^(URIs|Suites|Enabled)' /etc/apt/sources.list.d/example.sources
```

`apt policy` shows that the only place `examplepkg` exists is `100 /var/lib/dpkg/status`, the record of installed packages. `grep` prints the source's address, its old suite and the switch: `URIs: https://vendor.example.com/repo`, `Suites: noble`, `Enabled: no`.

**3. Ask whether the vendor publishes the new release.** A repository has a release when it has the file `dists/<release>/Release`:

```sh
curl -s -o /dev/null -w '%{http_code}\n' \
  https://vendor.example.com/repo/dists/resolute/Release
```

200 means yes. 404 means no, or not yet.

**4a. Keep it** (200, and you want the package). Point the source at the new release and switch it back on:

```sh
sudo sed -i \
  -e 's/^Suites: noble$/Suites: resolute/' \
  -e '/^Enabled: no$/d' \
  /etc/apt/sources.list.d/example.sources
sudo apt update 2>&1 | grep -iE 'example|^E:|^W:'
sudo apt full-upgrade
```

`sed` rewrites the line that is exactly `Suites: noble` and deletes the line that is exactly `Enabled: no`. The filtered `apt update` should show the vendor's `resolute` index being fetched and no `E:` (error) or `W:` (warning) lines. `2>&1` is needed because apt prints those on stderr, which a pipe alone doesn't carry. `full-upgrade` installs the new version, adding or removing other packages if the new version needs it.

If the source's suite is a fixed name such as `stable` rather than a release name, leave `Suites` as it is and only delete the `Enabled: no` line. Check for `dists/stable/Release` in step 3.

**4b. Remove it** (you don't want it, or the vendor returned 404). First check what removing it would take:

```sh
sudo apt -s purge examplepkg
apt rdepends --installed examplepkg
```

`-s` *simulates*: it prints what would be removed and changes nothing. `rdepends --installed` lists installed packages that depend on `examplepkg` directly. Trust the simulation for the full picture: on Ubuntu 24.04, `apt rdepends --installed sed` names one package, but `apt -s purge sed` would remove five, because packages that depend on *those* go too.

If nothing depends on it:

```sh
sudo apt purge examplepkg
sudo rm /etc/apt/sources.list.d/example.sources
sudo apt autoremove --purge
```

`purge` removes the package together with its system-wide settings files. Deleting the `.sources` file removes the dead source. `autoremove --purge` then removes packages that were installed only to support it and are no longer needed.

**4c. Replace it** (something depends on it). Ubuntu may ship its own build of the same package. `apt policy examplepkg` then also lists a version from the Ubuntu archive:

```text
 *** 2.4.1-1 100
        100 /var/lib/dpkg/status
     2.2.0-3 500
        500 http://archive.ubuntu.com/ubuntu resolute/universe amd64 Packages
```

```sh
sudo apt install --allow-downgrades examplepkg=2.2.0-3
```

`name=version` picks that exact version. `--allow-downgrades` is needed because the vendor's version is usually newer than Ubuntu's. The vendor's switched-off source file can then be deleted too.

**5. Check.** Run `pro security-status --unavailable` again; `examplepkg` should no longer appear.

**Next time.** `sudo do-release-upgrade --allow-third-party` keeps third-party sources. It moves those whose suite is a release name to the new release when the vendor has a `Release` file for it, and still switches off the rest.
