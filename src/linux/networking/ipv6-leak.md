A laptop forwards a phone's IPv4 traffic into an IPv4-only VPN tunnel. How could the phone's **IPv6** traffic bypass the laptop entirely, and why can't a firewall rule on the laptop stop it?

---

**IPv6 configures itself.** A router on the network sends **router advertisements** (RAs): "here is a network prefix, and I am a way out." Every device that hears one builds its own IPv6 address from the prefix (*SLAAC*, stateless address autoconfiguration) and uses that router for IPv6. Nothing has to be typed in, and a static IPv4 setting on the device doesn't stop it.

**The bypass.** The phone's typed-in gateway, the laptop, is an IPv4 setting. If the home router starts advertising an IPv6 prefix, for example after a firmware update, the phone takes an IPv6 address and sends IPv6 traffic **straight to the router**. Any site reachable over IPv6 is then reached outside the VPN.

**Why the laptop can't block it.** Those packets go from the phone to the router and never reach the laptop. An `ip6tables` rule on the laptop only sees packets that pass through the laptop.

**Check what exists today.** If the Wi-Fi interface and the tunnel have only link-local IPv6 addresses (`fe80::…`, valid only on the local link), no router is advertising a prefix and nothing is leaking yet:

```sh
ip -6 addr show dev tun0
ip -6 addr show dev wlp0s20f3
ip -6 route show
```

**Keep the phone off IPv6:**

- **Turn off router advertisements** (or IPv6 entirely) on the home router. It changes nothing today, but stops a later firmware update from quietly turning them on.
- **Or use a separate network for the phone,** such as a hotspot run by the laptop. There the laptop is the only router, so no other device can advertise a way out.

**Check on the phone:** a test site such as test-ipv6.com in its browser shows whether it has IPv6 and which address the world sees for each protocol.
