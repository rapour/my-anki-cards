Instead of giving the phone a static IP that points at the laptop, the laptop can run its own **Wi-Fi hotspot** for the phone. How do you start one with `nmcli`, and what does it fix compared with the static-IP setup?

---

```sh
nmcli device wifi hotspot ifname wlan1 ssid gw-ap password 'yourpassword'
```

It needs a **second Wi-Fi radio**, here `wlan1`, for example a USB Wi-Fi adapter, because the built-in one is busy carrying the laptop's own connection and VPN tunnel.

NetworkManager then does the routine work by itself:

- hands out addresses by DHCP, with the laptop as the gateway and DNS server;
- turns on forwarding;
- adds a masquerade (NAT) rule for the hotspot's network.

**What you still add:**

- the **kill switch**: a `FORWARD` rule that drops the hotspot's traffic unless it goes into `tun0`, so a dropped tunnel doesn't leak through the laptop's normal connection;
- NAT that sends the traffic out through **`tun0`**. Check that the shared connection's masquerade doesn't use another way out.

**What it fixes, compared with a phone pointed at the laptop on the home Wi-Fi:**

| Problem with the static-IP setup | With the hotspot |
|---|---|
| every phone needs its IP, gateway and DNS typed in | the phone just joins `gw-ap` |
| if the laptop's address changes, the phone's typed-in gateway goes stale | the phone learns the gateway from DHCP every time |
| router advertisements for IPv6 from the laptop reach every device on the home Wi-Fi | they stay on the hotspot's own network |
| the home router could advertise IPv6 and let the phone bypass the laptop | the laptop is the only router on the hotspot, so there is nothing to bypass it with |
