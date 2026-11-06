Through a VPN gateway, DNS works and pings work, but HTTPS pages and apps hang. Why is that usually an **MTU** problem, and what does this rule fix?

```sh
sudo iptables -t mangle -A FORWARD -o tun0 -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
```

---

**The MTU** is the largest packet an interface carries. Wi-Fi carries 1500 bytes, but a VPN tunnel wraps every packet in its own headers and encryption, so `tun0` carries less, say 1400. A full-size packet doesn't fit.

**Why only some traffic breaks.** Small packets fit: DNS answers, pings, the start of a TCP connection. Large ones don't, such as the certificate in a TLS handshake or a page's first big chunk. Normally the sender learns to send less from ICMP "packet too big" messages (*path MTU discovery*). When something on the way blocks those messages, large packets vanish silently and the connection hangs. That looks like a routing fault, but it's an MTU fault.

**The MSS** (maximum segment size) is the largest chunk of data each side of a TCP connection agrees to send in one packet. Each side announces it in the first packet of the connection, the `SYN`, usually as its MTU minus 40 bytes of IP and TCP headers.

**The rule** rewrites the MSS in every TCP `SYN` the gateway forwards into the tunnel, down to what the tunnel can carry. The two ends then never send packets too big for it, and no ICMP is needed.

| Part | Meaning |
|---|---|
| `-t mangle -A FORWARD` | change headers of forwarded packets |
| `-o tun0 -p tcp` | TCP packets leaving through the tunnel |
| `--tcp-flags SYN,RST SYN` | of the flags SYN and RST, only SYN is set: the opening packet of a connection |
| `-j TCPMSS --clamp-mss-to-pmtu` | set the MSS to the route's MTU minus 40 |

Tested with a 1400-byte tunnel, capturing the phone's `SYN` as it leaves `tun0`:

```text
no clamp:   IP 192.168.169.103.40270 > 1.1.1.1.80: Flags [S], ... options [mss 1460
with clamp: IP 192.168.169.103.40282 > 1.1.1.1.80: Flags [S], ... options [mss 1360
```

The phone announced 1460, from its 1500-byte Wi-Fi. The gateway lowered it to 1360, which is 1400 − 40.

To check the sizes, compare `ip link show tun0` with the Wi-Fi's 1500. The clamp is worth adding even when everything seems to work, since the failures it prevents look random.
