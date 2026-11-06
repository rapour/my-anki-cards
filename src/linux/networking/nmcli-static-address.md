A phone uses a laptop (192.168.1.7) as its gateway, typed into the phone by hand. Why must that laptop address be pinned, and how do you pin it with **nmcli**, NetworkManager's command-line tool?

---

**Why.** The laptop most likely got 192.168.1.7 from the router by **DHCP**, as a *lease* that can change on renewal or after a reboot. The phone has the old address typed in as its gateway, so if it changes, the phone sends everything to an address nobody answers on. It loses its connection with no obvious cause.

**Pin it on the laptop** by switching its Wi-Fi connection from DHCP to a fixed (manual) address:

```sh
nmcli con show                                    # find the connection's name
nmcli con mod "<connection-name>" ipv4.method manual \
  ipv4.addresses 192.168.1.7/24 \
  ipv4.gateway 192.168.1.1 \
  ipv4.dns 192.168.1.1
nmcli con up "<connection-name>"                  # reconnect with the new settings
```

| Setting | Meaning |
|---|---|
| `ipv4.method manual` | no DHCP: use the address given here |
| `ipv4.addresses 192.168.1.7/24` | the address, and its network (`/24` is 192.168.1.0 to 192.168.1.255) |
| `ipv4.gateway 192.168.1.1` | the router, still the laptop's own way out (it carries the VPN tunnel) |
| `ipv4.dns 192.168.1.1` | the laptop's own DNS server, until the VPN pushes its own |

`nmcli con mod` only changes the saved profile. `nmcli con up` applies it. The setting is stored with that Wi-Fi network's profile, so it applies only on that network.

**The other way: a DHCP reservation.** In the router's settings, reserve 192.168.1.7 for the laptop's MAC address (its network card's hardware address). The laptop keeps using DHCP but always gets the same address, and the router stays the only place addresses are managed. Pick an address outside the router's DHCP pool if you use the manual method, so the router never hands it to another device.

Either way works; doing neither is the mistake.
