A laptop forwards a phone's traffic (192.168.1.60) into a VPN tunnel, `tun0`. Why does it also need `iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE`, and what does that rule do?

---

**Without it, replies have nowhere to go.** Forwarding passes the phone's packets into the tunnel unchanged, still carrying the source address 192.168.1.60. That is a private address on the laptop's Wi-Fi. The VPN server has no route back to it, so its replies are lost.

**MASQUERADE** rewrites the source address of packets leaving `tun0` to the address `tun0` has right now, here 192.168.169.103. The kernel's *connection tracking* remembers each rewrite, so when a reply comes back to 192.168.169.103 it changes the destination back to 192.168.1.60 and forwards it to the phone. This is **NAT**, network address translation.

The three stages, tested. `1.1.1.1` is a test server that answers with the address it sees:

```text
ip_forward = 0:           phone fetches 1.1.1.1 → (timed out)
forwarding, no NAT:       packets leave tun0 as 192.168.1.60.43194 > 1.1.1.1.80 [SYN], twice
                          vpn side: ip route get 192.168.1.60 → Network is unreachable
                          phone → (timed out)
with MASQUERADE on tun0:  you are 192.168.169.103 (seen by the vpn side)
```

| Part | Meaning |
|---|---|
| `-t nat` | the table for address changes |
| `-A POSTROUTING` | the last step before a packet leaves, after routing has chosen the interface |
| `-o tun0` | only packets leaving through the tunnel |
| `-j MASQUERADE` | use whatever address `tun0` has when the packet leaves |

NAT rules see **only the first packet of each connection**. Connection tracking translates the rest, so the rule's counter stays small:

```text
$ sudo iptables -t nat -vnL POSTROUTING
 pkts bytes target     prot opt in     out     source               destination
    1    60 MASQUERADE  0    --  *      tun0    0.0.0.0/0            0.0.0.0/0
```

`SNAT --to-source ADDRESS` does the same with a fixed address. MASQUERADE suits a VPN, whose tunnel address can change at every reconnection.
