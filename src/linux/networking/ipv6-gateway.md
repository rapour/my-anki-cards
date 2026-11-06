A Linux laptop forwards a phone's traffic into a VPN tunnel that also carries IPv6. What does it take to give the phone IPv6 through the laptop, and why will the phone still use IPv4 for almost everything?

---

**1. Forwarding, without losing the laptop's own IPv6.** Turning IPv6 forwarding on makes Linux, by default, stop accepting router advertisements (RAs), which would remove the laptop's own IPv6 connection. `accept_ra=2` means "accept them even while forwarding":

```sh
sudo tee -a /etc/sysctl.d/99-vpn-gw.conf >/dev/null <<'EOF'
net.ipv6.conf.all.forwarding=1
net.ipv6.conf.wlp0s20f3.accept_ra=2
EOF
sudo sysctl --system
sudo ip -6 addr add fd00:1337::1/64 dev wlp0s20f3
```

`fd00:1337::/64` is a **ULA**, a unique local address range: private, like 192.168.x.x in IPv4.

**2. Advertise the prefix to the phone, with dnsmasq:**

```text
enable-ra
dhcp-range=fd00:1337::,ra-only,64,12h
dhcp-option=option6:dns-server,[fd00:1337::1]
```

`ra-only` means: send router advertisements only, and let devices build their own addresses (SLAAC), with no DHCPv6. Android doesn't take addresses from DHCPv6, so a DHCPv6-only setup would leave it with none.

**3. NAT and the kill switch, for IPv6:**

```sh
sudo ip6tables -t nat -A POSTROUTING -s fd00:1337::/64 -o tun0 -j MASQUERADE
sudo ip6tables -A FORWARD -i wlp0s20f3 -o tun0 -j ACCEPT
sudo ip6tables -A FORWARD -i tun0 -o wlp0s20f3 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo ip6tables -A FORWARD -i wlp0s20f3 -j DROP
```

Don't block ICMPv6 on `INPUT`. IPv6 finds neighbours and path sizes with it, so filtering it the way people filter IPv4's ICMP breaks the link in confusing ways.

**Why IPv6 will sit idle.** Devices choose source and destination addresses by the rules of **RFC 6724**, which Android follows. One rule prefers a source and destination of the same kind. A ULA source paired with a public IPv6 destination loses to IPv4, so the phone keeps using IPv4 for nearly everything. Real use needs a public IPv6 prefix delegated by the VPN server, which few providers offer.

Also, RAs go to the whole Wi-Fi, so **every** device there will start treating the laptop as an IPv6 router.
