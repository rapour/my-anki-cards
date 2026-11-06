A laptop forwards a phone's traffic from its Wi-Fi interface `wlp0s20f3` into a VPN tunnel `tun0`. Which `FORWARD` rules make up a **kill switch**, so the phone's traffic stops rather than leaking out unencrypted when the tunnel drops? Why does their order matter?

---

```sh
LAN=wlp0s20f3
sudo iptables -A FORWARD -i $LAN -o tun0 -j ACCEPT
sudo iptables -A FORWARD -i tun0 -o $LAN -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i $LAN -j DROP
```

| Rule | Job |
|---|---|
| in on the Wi-Fi, out on `tun0`: ACCEPT | lets the phone's traffic into the tunnel |
| in on `tun0`, out on the Wi-Fi, only `RELATED,ESTABLISHED`: ACCEPT | lets replies back. Connection tracking only marks a packet `ESTABLISHED` if it belongs to a connection the phone started, so nobody on the VPN side can open new connections to the phone |
| in on the Wi-Fi, anything else: DROP | **the kill switch** |

**Why the DROP is needed.** When the tunnel drops, `tun0` and its routes disappear, and the laptop's route for the internet falls back to the router on the Wi-Fi. Without the DROP, the phone's traffic would simply go that way, unencrypted. With it, that traffic matches no ACCEPT rule and dies. Tested with the tunnel down:

```text
phone fetches 1.1.1.1 → (timed out), twice
num   pkts bytes target     prot opt in     out
1        6   390 ACCEPT     0    --  wlp0s20f3 tun0
2        6   480 ACCEPT     0    --  tun0   wlp0s20f3  ctstate RELATED,ESTABLISHED
3        8   480 DROP       0    --  wlp0s20f3 *
```

The DROP counter is the blocked traffic. Without the DROP rule, the same test answered `you are 192.168.1.60 (seen by the isp side)`: a leak.

**Why the order matters.** Rules are read top to bottom, and `-A` adds each at the bottom. The DROP must come **last**. Added first, it would catch the phone's traffic before the ACCEPT rules ever see it.

The rules name `tun0` as text, so they work before the tunnel exists and keep working when OpenVPN recreates it.
