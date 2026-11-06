An Ubuntu laptop is set up to forward a phone's traffic into a VPN tunnel, but nothing the phone sends comes out of the VPN. How does **UFW**, Ubuntu's firewall front end, cause that, and what are the two fixes?

---

**The cause.** UFW sets the policy of the `FORWARD` chain, which decides about every packet the laptop passes on, to **DROP**. It comes from this line in `/etc/default/ufw`:

```text
DEFAULT_FORWARD_POLICY="DROP"
```

Any forwarded packet that no rule explicitly accepts is dropped. Tested, with UFW on and no forwarding rules:

```text
phone fetches 1.1.1.1 → (timed out)
```

**Fix 1: let forwarding through by default.**

```sh
sudo sed -i 's/^DEFAULT_FORWARD_POLICY=.*/DEFAULT_FORWARD_POLICY="ACCEPT"/' /etc/default/ufw
sudo ufw reload
```

Then your own `FORWARD` rules decide, including a kill switch that drops traffic not going into the tunnel.

**Fix 2: keep DROP and allow only the tunnel path.** A UFW *route* rule allows forwarding between two interfaces:

```text
$ sudo ufw route allow in on wlp0s20f3 out on tun0
Rule added
$ sudo ufw status
To                         Action      From
--                         ------      ----
Anywhere on tun0           ALLOW FWD   Anywhere on wlp0s20f3
```

Tested, this also makes the DROP policy the kill switch. With the tunnel down, the phone's traffic would leave by the Wi-Fi instead, matches no rule, and is dropped.

**Rules added outside UFW.** Rules appended with `iptables -A FORWARD` still run, *after* UFW's own chains, which only accept or return. In a test, appended ACCEPT rules worked with UFW active. But whenever they are missing, for example after a reboot if they weren't saved, the DROP policy silently blocks everything forwarded.

Check the policy with `sudo iptables -vnL FORWARD | head -1`. Docker also sets this policy to DROP, but its own chains return traffic that isn't for containers, so explicit ACCEPT rules still apply.
