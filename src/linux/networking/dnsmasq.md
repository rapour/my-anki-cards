What does **dnsmasq** do in this config, and why `bind-dynamic` rather than `bind-interfaces`?

```text
interface=wlp0s20f3
bind-dynamic
no-resolv
server=10.8.0.1
```

---

**dnsmasq** is a small DNS forwarder, also able to hand out DHCP addresses. Devices send it their DNS questions; it answers from its cache or asks an upstream server. This config makes a laptop answer DNS for devices on its Wi-Fi and pass every question on to a VPN's resolver:

| Line | Meaning |
|---|---|
| `interface=wlp0s20f3` | answer only on the Wi-Fi interface (dnsmasq also adds the loopback interface) |
| `bind-dynamic` | listen on that interface's own addresses, and follow them as they appear or change |
| `no-resolv` | ignore `/etc/resolv.conf`, so the upstream comes only from this file |
| `server=10.8.0.1` | send every question to 10.8.0.1, the resolver the VPN provides, reached through the tunnel |

Save it as a file in `/etc/dnsmasq.d/` and run `sudo systemctl restart dnsmasq`. It then listens on specific addresses only:

```text
$ sudo ss -lunp 'sport = :53'
127.0.0.1:53
192.168.1.7:53
```

**Why `bind-dynamic`.** Without a bind option, dnsmasq listens on *every* address (`0.0.0.0:53`). Ubuntu's own resolver, systemd-resolved, already listens on 127.0.0.53, so that clashes. Tested with something on 127.0.0.53:53:

```text
default:       dnsmasq: failed to create listening socket for port 53: Address already in use
bind-dynamic:  starts and runs
```

`bind-interfaces` also binds specific addresses, but only those present **at start**. If the Wi-Fi gets its address late at boot, dnsmasq refuses to start, while `bind-dynamic` waits for it. Tested on an interface, `lan1`, whose address was added after dnsmasq started:

```text
bind-interfaces: dnsmasq: unknown interface lan1
bind-dynamic:    answer after the address appeared: '203.0.113.7'
```

A related error, from `listen-address=` naming an address the machine doesn't have:

```text
dnsmasq: failed to create listening socket for 192.168.1.50: Cannot assign requested address
```
