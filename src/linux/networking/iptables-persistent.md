Rules added with `iptables` disappear at reboot. How do you make them permanent on Ubuntu, and what should you check before saving?

---

`iptables` changes only the rules in the running kernel. Settings files survive reboots, such as `/etc/sysctl.d/`, `/etc/default/ufw` and dnsmasq's config, but iptables rules don't.

Install the saver, inspect, then save:

```sh
sudo apt install iptables-persistent
sudo iptables-save | less
sudo netfilter-persistent save
```

- **`iptables-persistent`** installs a boot service, `netfilter-persistent`, that loads `/etc/iptables/rules.v4` (and `rules.v6` for `ip6tables`) at boot.
- **`netfilter-persistent save`** writes **whatever rules are loaded right now** to those files.
- **`iptables-save`** prints every table as the commands that rebuild it, so you can read exactly what will be saved.

**Inspect first.** Experiments and leftovers from troubleshooting are saved too, and will come back at every boot. A VPN gateway's saved rules look like this (the chain header lines are left out):

```text
*mangle
-A FORWARD -o tun0 -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
COMMIT
*filter
-A FORWARD -i wlp0s20f3 -o tun0 -j ACCEPT
-A FORWARD -i tun0 -o wlp0s20f3 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i wlp0s20f3 -j DROP
COMMIT
*nat
-A POSTROUTING -o tun0 -j MASQUERADE
COMMIT
```

**An interface that doesn't exist yet is fine.** Rules naming `-o tun0` are loaded at boot before OpenVPN creates `tun0`. They compare the name when each packet passes, so they do nothing until the interface appears, then work.

To undo a stray rule, delete it by position, for example `sudo iptables -D FORWARD 3` (see positions with `--line-numbers`), then save again.
