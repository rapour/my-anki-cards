Which `ip` commands answer "where will a packet to this address go?" and "what does this interface look like?", and how do you read their output?

---

`ip`, from the **iproute2** package, is Linux's tool for interfaces, addresses and routes. It replaces the older `ifconfig` and `route`. Its subcommands can be shortened: `ip r` for `ip route`, `ip a` for `ip addr`, `ip l` for `ip link`.

**Where will it go?** `ip route get` asks the kernel to make the routing decision for one address, without sending anything:

```text
$ ip route get 1.1.1.1
1.1.1.1 via 192.168.168.1 dev tun0 src 192.168.169.103 uid 0
```

- `via`: the next hop, the machine the packet is handed to;
- `dev`: the interface it leaves by;
- `src`: the source address this machine would put on it.

To test traffic this machine **forwards** for another one, describe where it comes from. Here the packet comes from a phone at 192.168.1.60 on the Wi-Fi interface:

```text
$ ip route get 1.1.1.1 from 192.168.1.60 iif wlp0s20f3
1.1.1.1 from 192.168.1.60 via 192.168.168.1 dev tun0
```

**The whole table**, `ip route`. The most specific matching route wins:

```text
$ ip route
0.0.0.0/1 via 192.168.168.1 dev tun0
default via 192.168.1.1 dev wlp0s20f3 metric 600
128.0.0.0/1 via 192.168.168.1 dev tun0
192.168.1.0/24 dev wlp0s20f3 proto kernel scope link src 192.168.1.7
192.168.168.0/22 dev tun0 proto kernel scope link src 192.168.169.103
```

**The interface itself**: flags, MTU (the largest packet it carries) and state. Here is a TUN device held open by a program, the way OpenVPN holds `tun0`:

```text
$ ip link show tun9
13: tun9: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1400 qdisc pfifo_fast state UNKNOWN mode DEFAULT group default qlen 500
    link/none
$ ip -4 addr show dev tun9
13: tun9: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1400 qdisc pfifo_fast state UNKNOWN group default qlen 500
    inet 192.168.169.103/22 scope global tun9
```

`UP` means switched on, and `LOWER_UP` means the other end is connected (for TUN, a program holds it). `state UNKNOWN` is normal for TUN devices, which have no cable to sense.

| Command | Shows |
|---|---|
| `ip addr` (or `ip -6 addr show dev tun0`) | the addresses on each interface |
| `ip -6 route show` | the IPv6 routing table |
| `ip addr add 192.168.1.7/24 dev wlp0s20f3` | adds an address, until the next reboot |
| `ip link set tun0 up` | brings an interface up |

The route outputs come from a test copy of a laptop that sends a phone's traffic into a VPN tunnel, `tun0`.
