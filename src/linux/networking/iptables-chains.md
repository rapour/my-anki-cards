How are `iptables` rules organised into **tables** and **chains**, in what order does a packet meet them, and how do you see which rule a packet hit?

---

`iptables` configures **netfilter**, the Linux kernel's packet filter. Rules live in **chains**, and chains are grouped into **tables** by the kind of job they do:

| Table | Job | Chains used on a gateway |
|---|---|---|
| `filter` (the default) | accept or drop | `INPUT`, `FORWARD`, `OUTPUT` |
| `nat` | change addresses, for the first packet of each connection | `PREROUTING`, `POSTROUTING` |
| `mangle` | change other header fields | `FORWARD` (for example the TCP MSS) |

Each chain is a fixed point in a packet's path:

<div class="diagram">
<svg viewBox="0 0 640 298" width="100%" style="max-width:640px" role="img" aria-label="Incoming packets pass PREROUTING, then a routing decision. Packets for another host go through FORWARD and POSTROUTING and out; packets for this host go to INPUT. The gateway&#x27;s ACCEPT and DROP rules are in filter FORWARD, MASQUERADE in nat POSTROUTING, the MSS clamp in mangle FORWARD, and Squid&#x27;s REDIRECT in nat PREROUTING.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .zone{fill:rgba(127,127,127,.07);stroke:currentColor;stroke-width:1;stroke-dasharray:5 4}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="no" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="ng" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="20" y="24" text-anchor="start">A packet&#x27;s path through the kernel, with the table.chain each gateway rule lives in</text>
<rect x="10" y="60" width="90" height="50" rx="6" class="k"/>
<text x="55.0" y="81.5" text-anchor="middle">packet in</text>
<text x="55.0" y="97.5" text-anchor="middle" class="m">wlp0s20f3</text>
<rect x="114" y="60" width="132" height="50" rx="6" class="k"/>
<text x="180.0" y="81.5" text-anchor="middle">PREROUTING</text>
<text x="180.0" y="97.5" text-anchor="middle" class="m">nat: REDIRECT (Squid)</text>
<rect x="260" y="60" width="110" height="50" rx="6" class="k"/>
<text x="315.0" y="81.5" text-anchor="middle">routing</text>
<text x="315.0" y="97.5" text-anchor="middle" class="m">for this host?</text>
<rect x="390" y="60" width="130" height="50" rx="6" class="g"/>
<text x="455.0" y="81.5" text-anchor="middle">FORWARD</text>
<text x="455.0" y="97.5" text-anchor="middle" class="m">filter: ACCEPT/DROP</text>
<rect x="540" y="60" width="90" height="50" rx="6" class="k"/>
<text x="585.0" y="81.5" text-anchor="middle">packet out</text>
<text x="585.0" y="97.5" text-anchor="middle" class="m">tun0</text>
<line x1="102" y1="85" x2="118" y2="85" class="ln" marker-end="url(#ah)"/>
<line x1="242" y1="85" x2="258" y2="85" class="ln" marker-end="url(#ah)"/>
<line x1="372" y1="85" x2="388" y2="85" class="ln" marker-end="url(#ah)"/>
<text x="380" y="80" text-anchor="middle" class="m">no</text>
<rect x="390" y="130" width="130" height="50" rx="6" class="g"/>
<text x="455.0" y="151.5" text-anchor="middle">POSTROUTING</text>
<text x="455.0" y="167.5" text-anchor="middle" class="m">nat: MASQUERADE</text>
<line x1="455" y1="112" x2="455" y2="128" class="ln" marker-end="url(#ah)"/>
<line x1="522" y1="155" x2="584" y2="112" class="ln" marker-end="url(#ah)"/>
<text x="455" y="196" text-anchor="middle" class="m">mangle FORWARD: TCPMSS clamp</text>
<rect x="260" y="210" width="110" height="50" rx="6" class="k"/>
<text x="315.0" y="231.5" text-anchor="middle">INPUT</text>
<text x="315.0" y="247.5" text-anchor="middle" class="m">to a local program</text>
<line x1="315" y1="112" x2="315" y2="208" class="ln" marker-end="url(#ah)"/>
<text x="325" y="160" text-anchor="start" class="m">yes</text>
<rect x="120" y="210" width="120" height="50" rx="6" class="k"/>
<text x="180.0" y="231.5" text-anchor="middle">local program</text>
<text x="180.0" y="247.5" text-anchor="middle" class="m">e.g. dnsmasq</text>
<line x1="258" y1="235" x2="242" y2="235" class="ln" marker-end="url(#ah)"/>
<text x="320" y="286" text-anchor="middle" class="m">Rules run in order inside each chain; the first ACCEPT or DROP ends the walk. If none matches, the chain&#x27;s policy decides.</text>
</svg>
</div>

**How a chain is read:**

- Rules run **top to bottom**. The first rule whose conditions match and whose target is final (`ACCEPT`, `DROP`, `REJECT`) ends the walk.
- A jump to another chain, such as UFW's `ufw-before-forward`, runs that chain and comes back if nothing in it decided.
- If no rule decides, the chain's **policy** does: `ACCEPT` or `DROP`.
- `-A` **appends** a rule at the bottom, and `-I` **inserts** it at the top (or at a given position). Order is meaning: an early `DROP` hides every rule after it.

**Which rule did a packet hit?** List with counters (`-v`), numeric addresses (`-n`) and positions:

```text
$ sudo iptables -vnL FORWARD --line-numbers
Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination
1        7   442 ACCEPT     0    --  wlp0s20f3 tun0    0.0.0.0/0            0.0.0.0/0
2        5   428 ACCEPT     0    --  tun0   wlp0s20f3  0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
3        0     0 DROP       0    --  wlp0s20f3 *       0.0.0.0/0            0.0.0.0/0
```

Run a test, then look for the counter that moved. `sudo iptables -Z` resets the counters. `-t nat` (or `-t mangle`) selects another table: `sudo iptables -t nat -vnL POSTROUTING`. `sudo iptables-save` prints every table as the commands that would rebuild it.
