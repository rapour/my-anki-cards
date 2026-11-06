What does the Linux setting `net.ipv4.ip_forward` control, and how do you turn it on so that it survives a reboot?

---

It decides whether Linux **passes on packets addressed to other machines.** At `0`, the default, Linux behaves as an ordinary host and drops any packet that isn't for one of its own addresses. At `1` it acts as a **router**: it looks the destination up in its routing table and sends the packet on.

A laptop meant to be a phone's gateway is useless without it. In a test with the phone pointed at the laptop:

```text
$ sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 0
phone: curl http://1.1.1.1/   →   (timed out)
```

With `1`, plus the address translation the phone also needs, the same request went through.

**Making it permanent.** Settings under `/proc/sys` (*sysctls*) reset at every boot. Put them in a file under `/etc/sysctl.d/`, which systemd applies at boot, and apply it now with `sysctl --system`:

```sh
sudo tee /etc/sysctl.d/99-vpn-gw.conf >/dev/null <<'EOF'
net.ipv4.ip_forward=1
EOF
sudo sysctl --system
sysctl net.ipv4.ip_forward
```

| Command | Effect |
|---|---|
| `sysctl NAME` | shows the current value: `net.ipv4.ip_forward = 1` |
| `sudo sysctl -w NAME=VALUE` | changes it until the next reboot |
| `sudo sysctl --system` | applies every file under `/etc/sysctl.d/` and the other sysctl folders |

Files apply in name order, and a later file wins, which is why custom files often start with `99-`. For IPv6 the setting is `net.ipv6.conf.all.forwarding=1`.

Forwarding only lets packets through the kernel. A firewall can still drop them in its **FORWARD** chain, and private addresses still need **NAT** to get replies back.
