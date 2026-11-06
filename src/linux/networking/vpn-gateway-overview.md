How do you turn an Ubuntu laptop that is connected to OpenVPN into a gateway that sends an Android phone's traffic through the VPN, with no VPN app on the phone? List the steps in order and what each one is for.

---

The laptop becomes the phone's **default gateway** on the home Wi-Fi. It passes the phone's packets into its tunnel `tun0` and translates their source address. To the phone it is just an ordinary gateway.

<div class="diagram">
<svg viewBox="0 0 640 348" width="100%" style="max-width:640px" role="img" aria-label="The phone sends everything to the laptop. The laptop&#x27;s FORWARD chain lets it into tun0, MASQUERADE gives it the tunnel&#x27;s address, and it leaves through the VPN. DNS goes to dnsmasq on the laptop, which forwards it through the tunnel to the VPN&#x27;s resolver.">
<style>svg text{fill:currentColor;font-size:13px}svg .m{font-size:11px;opacity:.7}svg .k{fill:rgba(127,127,127,.14);stroke:currentColor;stroke-width:1.5}svg .g{fill:rgba(0,122,102,.18);stroke:#007A66;stroke-width:1.5}svg .r{fill:rgba(250,100,25,.18);stroke:#FA6419;stroke-width:1.5}svg .c{fill:rgba(127,127,127,.14);stroke:rgba(127,127,127,.6);stroke-width:1}svg .cr{fill:rgba(250,100,25,.55);stroke:#FA6419;stroke-width:1}svg .cg{fill:rgba(0,122,102,.55);stroke:#007A66;stroke-width:1}svg .ln{stroke:currentColor;stroke-width:1.5;fill:none}.nightMode svg .g,.night_mode svg .g{fill:rgba(20,193,160,.22);stroke:#14C1A0}.nightMode svg .cg,.night_mode svg .cg{fill:rgba(20,193,160,.6);stroke:#14C1A0}</style>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<style>svg .tg{fill:#007A66}svg .to{fill:#FA6419}svg .po{stroke:#FA6419;stroke-width:2;fill:none}svg .pg{stroke:#007A66;stroke-width:2;fill:none}svg .fo{fill:#FA6419}svg .fg{fill:#007A66}svg .zone{fill:rgba(127,127,127,.07);stroke:currentColor;stroke-width:1;stroke-dasharray:5 4}.nightMode svg .tg,.night_mode svg .tg{fill:#14C1A0}.nightMode svg .pg,.night_mode svg .pg{stroke:#14C1A0}.nightMode svg .fg,.night_mode svg .fg{fill:#14C1A0}</style><defs><marker id="no" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fo"/></marker><marker id="ng" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="fg"/></marker></defs>
<text x="14" y="26" text-anchor="start">The phone sees an ordinary gateway; the laptop does the tunnelling</text>
<rect x="186" y="56" width="268" height="232" rx="8" class="zone"/>
<text x="320" y="74" text-anchor="middle" class="m">Ubuntu laptop: wlp0s20f3 192.168.1.7 and tun0</text>
<rect x="14" y="110" width="150" height="64" rx="6" class="k"/>
<text x="89.0" y="130.5" text-anchor="middle">Android phone</text>
<text x="89.0" y="146.5" text-anchor="middle" class="m">192.168.1.60, static</text>
<text x="89.0" y="162.5" text-anchor="middle" class="m">gateway and DNS: .1.7</text>
<rect x="200" y="90" width="240" height="52" rx="6" class="k"/>
<text x="320.0" y="112.5" text-anchor="middle">1. FORWARD chain</text>
<text x="320.0" y="128.5" text-anchor="middle" class="m">allow LAN → tun0; drop the rest (kill switch)</text>
<rect x="200" y="158" width="240" height="52" rx="6" class="g"/>
<text x="320.0" y="180.5" text-anchor="middle">2. MASQUERADE on tun0</text>
<text x="320.0" y="196.5" text-anchor="middle" class="m">new source 192.168.169.103, MSS clamped</text>
<rect x="200" y="226" width="240" height="52" rx="6" class="k"/>
<text x="320.0" y="248.5" text-anchor="middle">dnsmasq on 192.168.1.7:53</text>
<text x="320.0" y="264.5" text-anchor="middle" class="m">forwards to the VPN&#x27;s resolver</text>
<rect x="490" y="126" width="136" height="52" rx="6" class="g"/>
<text x="558.0" y="148.5" text-anchor="middle">VPN exit</text>
<text x="558.0" y="164.5" text-anchor="middle" class="m">then the internet</text>
<path d="M166 136 H198" class="pg" marker-end="url(#ng)"/>
<path d="M320 144 V156" class="pg" marker-end="url(#ng)"/>
<path d="M442 184 H488" class="pg" marker-end="url(#ng)"/>
<path d="M90 176 V252 H198" class="pg" marker-end="url(#ng)"/>
<path d="M442 252 H558 V180" class="pg" marker-end="url(#ng)"/>
<text x="452" y="270" text-anchor="start" class="m">DNS goes through the tunnel too</text>
<rect x="14" y="300" width="150" height="40" rx="6" class="k"/>
<text x="89.0" y="316.5" text-anchor="middle">Router 192.168.1.1</text>
<text x="89.0" y="332.5" text-anchor="middle" class="m">carries only the tunnel</text>
<text x="176" y="318" text-anchor="start" class="m">The router never sees the phone&#x27;s traffic in the clear, only the laptop&#x27;s encrypted tunnel.</text>
<text x="176" y="334" text-anchor="start" class="m">The phone runs no VPN app: to it, the laptop is just a gateway on the Wi-Fi.</text>
</svg>
</div>

| Device | Address | Role |
|---|---|---|
| laptop `wlp0s20f3` | 192.168.1.7/24 | the Wi-Fi side, facing the phone and the router |
| laptop `tun0` | 192.168.169.103/22 | the OpenVPN tunnel, the way out |
| router | 192.168.1.1 | carries only the laptop's encrypted tunnel |
| phone | 192.168.1.60 | static, with gateway and DNS 192.168.1.7 |

**The steps:**

1. **Check the prerequisite.** `ip route get 1.1.1.1` must show `dev tun0`. If it doesn't, the client profile needs `redirect-gateway def1`.
2. **Kernel forwarding.** Put `net.ipv4.ip_forward=1` in `/etc/sysctl.d/`, so the laptop passes on packets for other machines. Turn **ICMP redirects** off too (`send_redirects=0`, also for `wlp0s20f3`), so the laptop never tells the phone to use the router directly.
3. **UFW.** Its default `FORWARD` policy is DROP. Set it to ACCEPT, or allow the path with `ufw route allow in on wlp0s20f3 out on tun0`.
4. **NAT, kill switch and MSS.** MASQUERADE on `tun0`, so replies come back. ACCEPT Wi-Fi → `tun0`, ACCEPT established replies back, then DROP everything else from the Wi-Fi, so a dropped tunnel blocks instead of leaking. Clamp the TCP MSS to the tunnel's MTU, so HTTPS doesn't hang.
5. **Persistence.** `iptables-persistent`, then inspect with `iptables-save` and run `netfilter-persistent save`. The sysctl, UFW and dnsmasq files persist on their own.
6. **DNS.** Run dnsmasq on the laptop (`interface=wlp0s20f3`, `bind-dynamic`, `no-resolv`, `server=` the VPN's resolver), or give the phone a public resolver. A DNS server of 192.168.1.1 would leak every lookup to the internet provider.
7. **Pin the laptop's address,** with `nmcli … ipv4.method manual` or a DHCP reservation, so the phone's typed-in gateway stays valid.
8. **The phone.** Static IP 192.168.1.60, gateway and DNS 192.168.1.7. Check Android's adaptive connectivity and automatic switching to mobile data.
9. **IPv6.** If the tunnel is IPv4 only, make sure nothing advertises IPv6 to the phone, or it bypasses the laptop.
10. **Verify** with mobile data off: a public-IP website in the phone's browser must show the VPN's address.

**Alternative:** a hotspot on a second Wi-Fi radio (`nmcli device wifi hotspot`) replaces steps 7 and 8 and closes the IPv6 hole.
