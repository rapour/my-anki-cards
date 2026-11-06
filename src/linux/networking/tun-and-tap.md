What are **TUN** and **TAP** devices, how do they differ, and which one does a VPN such as OpenVPN usually use?

---

Both are **virtual network interfaces whose other end is a program** rather than a cable. The kernel treats them like any network card: it routes packets to them and receives packets from them. What would go onto the wire is instead handed to the program that opened the device through `/dev/net/tun`, and what that program writes comes in as if it had arrived from the network.

| | TUN (`tun0`) | TAP (`tap0`) |
|---|---|---|
| Carries | **IP packets** (layer 3) | **Ethernet frames** (layer 2) |
| Has a MAC address | no (`link/none`) | yes (`link/ether …`) |
| ARP, broadcasts | no | yes, like a real network card |
| Typical use | VPNs that route IP traffic: OpenVPN's default `dev tun`, and the userspace WireGuard, `wireguard-go` | bridging a VPN or a virtual machine into an Ethernet network |

The kernel shows the difference:

```text
$ sudo ip tuntap add dev tun0 mode tun
$ sudo ip tuntap add dev tap0 mode tap
$ ip link show tun0
5: tun0: <POINTOPOINT,MULTICAST,NOARP> mtu 1500 qdisc noop state DOWN ...
    link/none
$ ip link show tap0
6: tap0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN ...
    link/ether 6e:8b:42:8b:7c:81 brd ff:ff:ff:ff:ff:ff
```

**What the program reads.** A small Python program opened each device, gave it the address 10.99.0.1/24, and pinged 10.99.0.2 through it:

```text
tun: read 84 bytes, first 16: 45 00 00 54 fe 41 40 00 40 01 27 9f 0a 63 00 01
  IPv4 packet, protocol 1 (1 = ICMP), 10.99.0.1 -> 10.99.0.2
tap: read 42 bytes, first 16: ff ff ff ff ff ff da 3a b7 cc d0 10 08 06 00 01
  Ethernet frame, dst ff:ff:ff:ff:ff:ff src da:3a:b7:cc:d0:10 type 0806 (0806 = ARP)
  ARP: who has 10.99.0.2 tell 10.99.0.1
```

Through TUN, the program got the ping itself: a bare IPv4 packet, starting with `45`. Through TAP, it first got an Ethernet broadcast asking for 10.99.0.2's MAC address, because the kernel treats a TAP device as Ethernet. A VPN program encrypts what it reads, sends it to the VPN server, and writes the server's replies back into the device.

How a program attaches, in Python:

```text
fd = os.open("/dev/net/tun", os.O_RDWR)
flags = IFF_TUN | IFF_NO_PI          # IFF_TAP for a TAP device
fcntl.ioctl(fd, TUNSETIFF, struct.pack("16sH", b"demo0", flags))
packet = os.read(fd, 2048)           # one packet (TUN) or frame (TAP)
```
