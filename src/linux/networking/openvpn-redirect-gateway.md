What does OpenVPN's `redirect-gateway def1` do to the routing table, and how do you check that a machine's traffic really leaves through the tunnel?

---

It makes the VPN tunnel the route for **all** internet traffic. `def1` does it without deleting the normal default route: it adds two routes that each cover **half** of all IPv4 addresses, through the tunnel:

```text
$ ip route
0.0.0.0/1 via 192.168.168.1 dev tun0
default via 192.168.1.1 dev wlp0s20f3 metric 600
128.0.0.0/1 via 192.168.168.1 dev tun0
192.168.1.0/24 dev wlp0s20f3 proto kernel scope link src 192.168.1.7
192.168.168.0/22 dev tun0 proto kernel scope link src 192.168.169.103
```

**Why that works.** Linux picks the **most specific** matching route, the one with the longest prefix. `default` is `0.0.0.0/0`, prefix 0. Every address falls in one of the two `/1` halves, prefix 1, so the halves always win. When the tunnel closes, they disappear and the untouched default route takes over again. OpenVPN also adds a route to the VPN server itself through the old gateway, so the tunnel's own encrypted packets don't try to go through the tunnel.

**Checking it:**

```text
$ ip route get 1.1.1.1
1.1.1.1 via 192.168.168.1 dev tun0 src 192.168.169.103 uid 0
```

`dev tun0` means internet traffic goes into the tunnel. If it shows `dev wlp0s20f3`, the client profile is missing `redirect-gateway def1` (or the server didn't push it). Then only the VPN's own network goes through the tunnel, and anything built on top, such as sharing the tunnel with other devices, has nothing to work with.

The option goes in the client's `.ovpn` or `.conf` file as `redirect-gateway def1`, or the server sends it with `push "redirect-gateway def1"`. Add `ipv6` (`redirect-gateway def1 ipv6`) to take IPv6 traffic too.
