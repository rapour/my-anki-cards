What does the response header `Strict-Transport-Security: max-age=31536000; includeSubDomains` tell a browser, and how does it stop SSL stripping (an attacker keeping the victim on plain HTTP)?

---

It says: **"for the next `max-age` seconds, contact this host over HTTPS only."** That is **HSTS**, HTTP Strict Transport Security. The browser stores the host as an HSTS host and, until that expires:

1. **Rewrites every `http://` address for the host to `https://` inside the browser**, before anything is sent. There is no plain-text request left for an attacker to answer. Chrome's developer tools show this step as `307 Internal Redirect`.
2. **Treats any certificate error on the host as fatal.** There is no "proceed anyway" button, so an attacker can't fall back to a fake certificate and hope the user clicks through.

<div class="diagram">
<svg viewBox="0 0 640 224" width="100%" style="max-width:640px" role="img" aria-label="Without HSTS the first request goes out as plain HTTP and only then is redirected. With HSTS the browser rewrites the address to https itself, so the first request is already encrypted, and certificate errors cannot be clicked through.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .life{stroke:currentColor;stroke-width:1;stroke-dasharray:4 4;opacity:.5}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="mo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="mg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="20" y="22" text-anchor="start">Without HSTS</text>
<rect x="20" y="32" width="150" height="44" rx="6" class="k"/>
<text x="95.0" y="50.5" text-anchor="middle">user types</text>
<text x="95.0" y="66.5" text-anchor="middle" class="m">bank.example</text>
<line x1="172" y1="54" x2="206" y2="54" class="po" marker-end="url(#mo)"/>
<rect x="208" y="32" width="190" height="44" rx="6" class="r"/>
<text x="303.0" y="50.5" text-anchor="middle">GET http://bank.example/</text>
<text x="303.0" y="66.5" text-anchor="middle" class="m">plain text: can be intercepted</text>
<line x1="400" y1="54" x2="434" y2="54" class="po" marker-end="url(#mo)"/>
<rect x="436" y="32" width="184" height="44" rx="6" class="k"/>
<text x="528.0" y="50.5" text-anchor="middle">301 to https://…</text>
<text x="528.0" y="66.5" text-anchor="middle" class="m">if the real site answers</text>
<text x="20" y="110" text-anchor="start" class="tg">With HSTS: the browser stored &quot;bank.example: HTTPS only, until …&quot;</text>
<rect x="20" y="120" width="150" height="44" rx="6" class="k"/>
<text x="95.0" y="138.5" text-anchor="middle">user types</text>
<text x="95.0" y="154.5" text-anchor="middle" class="m">bank.example</text>
<line x1="172" y1="142" x2="206" y2="142" class="pg" marker-end="url(#mg)"/>
<rect x="208" y="120" width="190" height="44" rx="6" class="g"/>
<text x="303.0" y="138.5" text-anchor="middle">rewritten inside the browser</text>
<text x="303.0" y="154.5" text-anchor="middle" class="m">Chrome shows 307 Internal Redirect</text>
<line x1="400" y1="142" x2="434" y2="142" class="pg" marker-end="url(#mg)"/>
<rect x="436" y="120" width="184" height="44" rx="6" class="g"/>
<text x="528.0" y="138.5" text-anchor="middle">GET https://bank.example/</text>
<text x="528.0" y="154.5" text-anchor="middle" class="m">TLS from the first byte</text>
<text x="320" y="194" text-anchor="middle" class="m">Nothing is ever sent in plain text, so there is no request to strip.</text>
<text x="320" y="212" text-anchor="middle" class="m">A certificate error on this host blocks the page: there is no &quot;proceed anyway&quot;.</text>
</svg>
</div>

| Directive | Meaning |
|---|---|
| `max-age=31536000` | required. How long to remember, in seconds (31,536,000 is 365 days), counted from the latest response that carried the header. `max-age=0` deletes the stored policy |
| `includeSubDomains` | the rule also covers every subdomain, such as `api.bank.example` |
| `preload` | asks to be added to the list of HSTS hosts built into browsers. Not part of the RFC; the preload list's site uses it |

Rules from the standard, RFC 6797:

- The header counts only when it **arrives over HTTPS** without certificate errors. Over plain HTTP the browser ignores it; otherwise an attacker could add or delete it.
- It applies to host names, **not IP addresses**.

**Seen with curl**, which implements HSTS when given a cache file with `--hsts` (real output, October 2026):

```sh
$ curl -s -o /dev/null -D - --hsts hsts.txt https://en.wikipedia.org/ | grep -i '^strict'
strict-transport-security: max-age=106384710; includeSubDomains; preload
$ grep wikipedia hsts.txt
.en.wikipedia.org "20300312 22:19:17"
$ curl -sv -o /dev/null --hsts hsts.txt http://en.wikipedia.org/ 2>&1 | grep HSTS
* Switched from HTTP to HTTPS due to HSTS => https://en.wikipedia.org/
```

The first response stored the policy. The leading dot in `.en.wikipedia.org` means `includeSubDomains`, and the date is the moment of the request plus `max-age`. After that, a request written as `http://` went out as HTTPS without a single plain-text byte.
