What does a **transparent Squid proxy** add to a Linux gateway, how is web traffic sent to it, and why should you not intercept HTTPS (port 443)?

---

**Squid** is a web proxy: it fetches pages on behalf of clients and can cache and log them. It adds **nothing to routing**: forwarding, NAT and the VPN work the same with or without it. Add it only to cache or log plain-HTTP requests.

*Transparent*, or *intercepting*, means the clients aren't configured to use a proxy. The gateway quietly redirects their web traffic into Squid.

Squid config (`/etc/squid/squid.conf`):

```text
http_port 3128
http_port 3129 intercept
acl localnet src 192.168.1.0/24
http_access allow localnet
```

- `3128`: the normal port, for clients configured to use the proxy;
- `3129 intercept`: the port for redirected traffic. `intercept` tells Squid to read the real destination from the redirected connection;
- `acl` and `http_access`: only devices on 192.168.1.0/24 may use it.

Redirect the phone's plain HTTP into it:

```sh
sudo iptables -t nat -A PREROUTING -i wlp0s20f3 -s 192.168.1.0/24 \
  -p tcp --dport 80 -j REDIRECT --to-ports 3129
```

`PREROUTING` runs before the routing decision, and `REDIRECT` turns a packet for any outside address into a packet for this machine's port 3129.

**Why not port 443.** To read HTTPS, Squid must decrypt it (*SSL bump*) and re-encrypt it with a certificate signed by its own certificate authority (CA). The phone would have to trust that CA. Apps that target Android 7 or later **ignore user-installed CAs** unless they explicitly opt in, so most apps would just fail. Let HTTPS pass through the NAT untouched.
