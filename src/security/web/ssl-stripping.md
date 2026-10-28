What is an **SSL stripping** attack, and why doesn't serving a site over HTTPS, with a redirect from HTTP, stop it?

---

An attacker who sits on the network path **keeps the victim on plain HTTP** while talking HTTPS to the real site. Everything passes through the attacker unencrypted, so they can read and change it.

**Why HTTPS alone doesn't stop it.** People rarely type `https://`. Typing `bank.example`, an old bookmark, or an `http://` link makes the browser's first request plain HTTP. The site answers with a redirect to `https://`, but that redirect *also* travels unencrypted. Whoever can intercept the first request can answer it instead of the site, and never send the redirect.

<div class="diagram">
<svg viewBox="0 0 640 398" width="100%" style="max-width:640px" role="img" aria-label="SSL stripping. The browser&#x27;s first request is plain HTTP, so the attacker answers it, fetches the real page over HTTPS, and sends it back over HTTP with the https links rewritten. The victim&#x27;s login then travels as plain text through the attacker.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .life{stroke:currentColor;stroke-width:1;stroke-dasharray:4 4;opacity:.5}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="mo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="mg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<rect x="15" y="10" width="150" height="40" rx="6" class="k"/>
<text x="90.0" y="34.5" text-anchor="middle">Victim&#x27;s browser</text>
<rect x="245" y="10" width="150" height="40" rx="6" class="r"/>
<text x="320.0" y="26.5" text-anchor="middle">Attacker</text>
<text x="320.0" y="42.5" text-anchor="middle" class="m">e.g. on the café Wi-Fi</text>
<rect x="475" y="10" width="150" height="40" rx="6" class="g"/>
<text x="550.0" y="34.5" text-anchor="middle">bank.example</text>
<line x1="90" y1="52" x2="90" y2="352" class="life"/>
<line x1="320" y1="52" x2="320" y2="352" class="life"/>
<line x1="550" y1="52" x2="550" y2="352" class="life"/>
<text x="205.0" y="78" text-anchor="middle" class="to">1. GET http://bank.example/</text>
<line x1="96" y1="86" x2="314" y2="86" class="po" marker-end="url(#mo)"/>
<text x="205.0" y="101" text-anchor="middle" class="m">plain text: the attacker answers it</text>
<text x="435.0" y="124" text-anchor="middle" class="tg">2. GET https://bank.example/</text>
<line x1="326" y1="132" x2="544" y2="132" class="pg" marker-end="url(#mg)"/>
<text x="435.0" y="147" text-anchor="middle" class="m">a normal TLS connection</text>
<text x="435.0" y="170" text-anchor="middle" class="tg">3. the login page</text>
<line x1="544" y1="178" x2="326" y2="178" class="pg" marker-end="url(#mg)"/>
<text x="205.0" y="216" text-anchor="middle" class="to">4. the same page, every https://</text>
<line x1="314" y1="224" x2="96" y2="224" class="po" marker-end="url(#mo)"/>
<text x="205.0" y="239" text-anchor="middle" class="m">link and redirect changed to http://</text>
<text x="205.0" y="262" text-anchor="middle" class="to">5. POST /login user=ann pass=…</text>
<line x1="96" y1="270" x2="314" y2="270" class="po" marker-end="url(#mo)"/>
<text x="205.0" y="285" text-anchor="middle" class="m">plain text: the attacker reads it</text>
<text x="435.0" y="308" text-anchor="middle" class="tg">6. POST /login (TLS)</text>
<line x1="326" y1="316" x2="544" y2="316" class="pg" marker-end="url(#mg)"/>
<text x="435.0" y="331" text-anchor="middle" class="m">the bank sees a normal login</text>
<line x1="20" y1="366" x2="50" y2="366" class="po"/>
<text x="56" y="370" text-anchor="start" class="m">plain HTTP: anyone on the path can read and change it</text>
<line x1="20" y1="384" x2="50" y2="384" class="pg"/>
<text x="56" y="388" text-anchor="start" class="m">TLS (HTTPS): encrypted, and the certificate proves who answers</text>
</svg>
</div>

1. The victim's browser sends `GET http://bank.example/` in plain text, and the attacker intercepts it.
2. The attacker requests the same page from the bank over HTTPS. The bank sees an ordinary visitor.
3. The bank sends the login page back to the attacker.
4. The attacker passes it to the victim over plain HTTP, after rewriting every `https://` link, form address and redirect to `http://`.
5. The victim logs in. The form goes to the attacker in plain text, so the attacker reads the password, and later the session cookie.
6. The attacker passes the login on over HTTPS. The bank sees a normal login, and nothing looks broken to the victim.

**Why the certificate doesn't save the victim.** TLS protects only connections made with TLS. Between the victim and the attacker there is no TLS at all, so no certificate is ever checked. The only signs are `http://` and "Not secure" in the address bar, which few people notice.

**Who can be "on the path":**

- a public Wi-Fi hotspot, or a fake one with the same name;
- a device on a local network that pretends to be the router (*ARP spoofing*);
- a compromised home or office router;
- anyone who can make a DNS lookup return their address.

The weak hop, as seen with `curl`: a plain-HTTP request whose answer is only a redirect.

```sh
$ curl -sI http://en.wikipedia.org/ | grep -iE '^(HTTP|location)'
HTTP/1.1 301 Moved Permanently
location: https://en.wikipedia.org/
```

Moxie Marlinspike presented the attack and his tool `sslstrip` in 2009. HSTS (RFC 6797, 2012) was designed as the answer: it makes the browser use HTTPS before it sends anything.
