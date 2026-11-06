A laptop sends a phone's traffic through a VPN. If the phone's DNS server is the home router (192.168.1.1), how do its DNS lookups **leak** past the VPN, and how do you stop that?

---

**How it leaks.** The phone and the router are on the same Wi-Fi network, so the phone sends DNS questions to the router **directly**. They never pass through the laptop and never enter the tunnel. The router then asks the internet provider's resolver, which sees every name the phone looks up, while the web traffic itself goes through the VPN.

Tested with two resolvers that give different answers for `example.test`, logging who asks:

```text
phone asks the laptop:  203.0.113.7    VPN resolver's log: query[A] example.test from 192.168.169.103
phone asks the router:  198.51.100.9   ISP resolver's log: query[A] example.test from 192.168.1.60
```

Through the laptop, the VPN's resolver answers and sees only the tunnel's address. Through the router, the internet provider's resolver sees the phone itself.

**Fix 1: a DNS forwarder on the laptop.** Run dnsmasq on the laptop's Wi-Fi address, forwarding to the VPN's resolver. Then set the phone's DNS to the laptop, 192.168.1.7. Find the resolver the VPN pushes, most reliable first:

1. `resolvectl status tun0 | grep -i 'DNS Server'`
2. `grep dhcp-option /etc/openvpn/*.conf`
3. the `PUSH_REPLY` line in the OpenVPN log, where the server lists `dhcp-option DNS …`

If none shows one, use a public resolver such as `server=9.9.9.9` in dnsmasq. Questions still travel through the tunnel, just not to the provider's own resolver.

**Fix 2: no forwarder.** Give the phone a public resolver directly, such as 9.9.9.9 or 1.1.1.1. It isn't on the local network, so the phone sends those questions to its gateway, the laptop, and they go through the tunnel like any other traffic.

**Check:** a DNS leak test site in the phone's browser should list only the VPN's resolvers, never the internet provider's.
