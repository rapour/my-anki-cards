How do you make an Android phone send its traffic through a laptop that forwards it into a VPN, with no VPN app on the phone? Which Android behaviour can silently undo it?

---

**Set a static IP on the phone's Wi-Fi.** Settings, Wi-Fi, edit the network (long-press, or its gear icon), Advanced, IP settings, **Static**. Menu names vary by maker.

| Field | Value |
|---|---|
| IP address | 192.168.1.60: free, and outside the router's DHCP pool so the router never hands it out |
| Gateway | 192.168.1.7, the laptop |
| Network prefix length | 24, the same network as the router's 192.168.1.x |
| DNS 1 | 192.168.1.7 if the laptop runs a DNS forwarder, otherwise a public resolver such as 9.9.9.9 |

The phone sees an ordinary gateway on its Wi-Fi. It shows no VPN icon and has no way to tell that its traffic is tunnelled.

**What undoes it: the fallback to mobile data.** Android checks every Wi-Fi network by fetching a known web page. If the check fails, for example because the laptop's firewall drops forwarded traffic, Android marks the Wi-Fi as having no internet and quietly moves apps onto **mobile data**. Apps keep working, just not through the VPN. Two settings under Network can do this on their own; check them after the setup:

- **adaptive connectivity**, which switches networks based on quality;
- **switching to mobile data automatically** when the Wi-Fi is poor.

**The fastest test when unsure: turn mobile data off completely.**

- If apps lose their connection, forwarding through the laptop never worked.
- If they work and an IP-checking website shows the VPN's address, forwarding is fine and Android was simply preferring mobile data.

Check in a browser, against a site that shows your public IP address. Don't trust an app that shows your location, which can come from GPS or the phone network. Seeing your own internet provider's address means a leak.
