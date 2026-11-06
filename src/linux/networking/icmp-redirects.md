A Linux laptop is the gateway for a phone on the same Wi-Fi, and sends the phone's traffic into a VPN tunnel. Why turn off **ICMP redirects** on it, and which settings actually do that?

---

**What a redirect is.** When Linux forwards a packet **back out the same interface it arrived on**, it concludes that the sender could have reached the next hop directly. So it sends the sender an *ICMP redirect*: "for this destination, use 192.168.1.1 instead of me." A device that accepts it remembers that route for a while.

**Why it hurts here.** Normally the phone's packets go out through the tunnel interface, a different interface, so no redirect is sent. But while the tunnel is down, the laptop's route for the internet falls back to the router, on the same Wi-Fi interface. Then:

<div class="diagram">
<svg viewBox="0 0 640 230" width="100%" style="max-width:640px" role="img" aria-label="When the laptop would forward a phone packet back out the same Wi-Fi interface to the router, it sends the phone an ICMP redirect. The phone then sends that destination straight to the router, bypassing the laptop even after the tunnel returns.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .zone{fill:rgba(127,127,127,.07);stroke:currentColor;stroke-width:1;stroke-dasharray:5 4}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="no" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="ng" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<rect x="20" y="40" width="150" height="56" rx="6" class="k"/>
<text x="95.0" y="64.5" text-anchor="middle">Phone</text>
<text x="95.0" y="80.5" text-anchor="middle" class="m">192.168.1.60</text>
<rect x="245" y="40" width="150" height="56" rx="6" class="k"/>
<text x="320.0" y="64.5" text-anchor="middle">Laptop 192.168.1.7</text>
<text x="320.0" y="80.5" text-anchor="middle" class="m">tunnel briefly down</text>
<rect x="470" y="40" width="150" height="56" rx="6" class="k"/>
<text x="545.0" y="64.5" text-anchor="middle">Router 192.168.1.1</text>
<text x="545.0" y="80.5" text-anchor="middle" class="m">the ISP path</text>
<path d="M172 58 H243" class="pg" marker-end="url(#ng)"/>
<text x="207" y="50" text-anchor="middle" class="m">1. packet</text>
<path d="M243 82 H172" class="po" marker-end="url(#no)"/>
<text x="190" y="116" text-anchor="middle" class="to">2. ICMP redirect:</text>
<text x="190" y="132" text-anchor="middle" class="to">use .1.1 instead</text>
<text x="330" y="116" text-anchor="middle" class="m">same interface in and out,</text>
<text x="330" y="130" text-anchor="middle" class="m">so the kernel sends a redirect</text>
<path d="M70 98 V160 H545 V98" class="po" marker-end="url(#no)"/>
<text x="320" y="176" text-anchor="middle" class="to">3. from now on the phone sends that destination straight to the router,</text>
<text x="320" y="192" text-anchor="middle" class="to">even after the tunnel is back: it bypasses the laptop and the VPN</text>
<text x="320" y="218" text-anchor="middle" class="tg">Fix on the laptop: send_redirects=0 for all and for the Wi-Fi interface</text>
</svg>
</div>

Tested with a Linux "phone" that accepts redirects, as Linux does by default:

```text
send_redirects=1, tunnel down for a moment
  phone route: 1.1.1.1 via 192.168.1.1 dev eth0 src 192.168.1.60
  tunnel back up. laptop route: 1.1.1.1 via 192.168.168.1 dev tun0
  phone fetches: you are 192.168.1.60 (seen by the isp side)
send_redirects=0, same test
  phone route: 1.1.1.1 via 192.168.1.7 dev eth0 src 192.168.1.60
  phone fetches: you are 192.168.169.103 (seen by the vpn side)
```

With redirects on, the phone kept bypassing the VPN after the tunnel came back.

**Turn them off for the interface too.** The kernel sends redirects if `all` **or** the interface's own setting is `1`. `default` only applies to interfaces created *later*. Measured:

| `all` | `wlp0s20f3` | Redirects sent |
|---|---|---|
| 0 | 1 | 2 |
| 0 | 0 | 0 |
| 1 | 0 | 2 |

So name the interface as well. systemd also applies per-interface lines whenever that interface appears:

```sh
sudo tee -a /etc/sysctl.d/99-vpn-gw.conf >/dev/null <<'EOF'
net.ipv4.conf.all.send_redirects=0
net.ipv4.conf.default.send_redirects=0
net.ipv4.conf.wlp0s20f3.send_redirects=0
EOF
sudo sysctl --system
```

Check with `nstat -az IcmpOutRedirects`: the count must stop rising.
