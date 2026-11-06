A laptop is meant to forward a phone's traffic (192.168.1.60, arriving on `wlp0s20f3`) into a VPN tunnel `tun0`, but the phone's traffic doesn't come out of the VPN. In what order do you check, and what does each check isolate?

---

**Work outward from the laptop, one hop at a time:**

```sh
ip route get 1.1.1.1                                    # 1. the laptop's own route
ip route get 1.1.1.1 from 192.168.1.60 iif wlp0s20f3    # 2. the route for forwarded traffic
sudo tcpdump -ni wlp0s20f3 'host 192.168.1.60 and not arp'   # 3. does the phone's traffic arrive?
sudo iptables -vnL FORWARD --line-numbers               # 4. which rule takes it?
sudo iptables -t nat -vnL POSTROUTING                   # 5. is it translated on the way out?
```

1. Must say `dev tun0`. If it says `dev wlp0s20f3`, the VPN isn't the default route: the client profile lacks `redirect-gateway def1`.
2. The same, for a packet *from the phone*. Needs forwarding on (`net.ipv4.ip_forward=1`).
3. Shows whether the phone sends to the laptop at all. Nothing means the phone's static settings didn't take. `-n` skips name lookups, `-i` picks the interface, and `not arp` hides address-resolution chatter.
4. Run a test, then see which counter moved. A DROP counter rising, or a UFW chain taking the packets, means the firewall blocks it.
5. The MASQUERADE counter should rise with each new connection.

Healthy output, from a test copy of this setup:

```text
1.1.1.1 from 192.168.1.60 via 192.168.168.1 dev tun0
IP 192.168.1.60.53852 > 1.1.1.1.80: Flags [S], seq 3463936289, win 64240, options [mss 1460,sackOK,TS val 2322202007 ecr 0,nop,wscale 10], length 0
IP 1.1.1.1.80 > 192.168.1.60.53852: Flags [S.], seq 12642551, ack 3463936290, win 64704, options [mss 1360,sackOK,TS val 1394157489 ecr 2322202007,nop,wscale 10], length 0
```

| Symptom | Likely cause | Check |
|---|---|---|
| no traffic from the phone at all | the phone's static IP settings didn't take | `tcpdump` on the Wi-Fi interface |
| packets arrive, nothing leaves the tunnel | UFW or another rule drops them first | `iptables -vnL FORWARD` counters |
| DNS and ping work, HTTPS hangs | the tunnel's MTU is smaller | compare `ip link show tun0` with 1500, add MSS clamping |
| the phone has an IPv6 address | something on the network advertises a prefix | `ip -6 route show`, and the router's IPv6 settings |

**The final check is on the phone:** a website that shows your public IP address must show the VPN's address, never your internet provider's.
