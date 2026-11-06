Why do setup scripts write a root-owned file with `sudo tee FILE >/dev/null` instead of `sudo echo … > FILE`? What does each part do?

```sh
sudo tee /etc/sysctl.d/99-vpn-gw.conf >/dev/null <<'EOF'
net.ipv4.ip_forward=1
EOF
```

---

Because **`>` is done by your own shell, not by the command.** The shell opens the target file before it starts `sudo`, using *your* permissions. In `sudo echo x > /etc/f`, only `echo` runs as root, and the shell, as you, fails to open `/etc/f`: `Permission denied`.

You can see the shell doing it: when the target can't be opened, the error comes from `bash`, not from `echo`.

```sh
$ bash -c 'echo hello > ./no-such-dir/out.conf'
bash: line 1: ./no-such-dir/out.conf: No such file or directory
```

**`tee FILE`** copies its standard input to `FILE` *and* to standard output. With `sudo tee`, it is `tee`, running as root, that opens the file, so the write works.

| Part | Job |
|---|---|
| `sudo tee FILE` | root opens `FILE` and writes the input into it, replacing what was there |
| `>/dev/null` | throws away the copy `tee` also prints, so the content doesn't scroll past |
| `<<'EOF' … EOF` | the input: the lines up to `EOF`, kept exactly as written |
| `tee -a FILE` | **a**ppends instead of replacing |

```sh
$ echo 'net.ipv4.ip_forward=1' | tee gw.conf
net.ipv4.ip_forward=1
$ echo 'net.ipv4.ip_forward=1' | tee gw.conf >/dev/null
$ echo 'net.ipv4.conf.all.send_redirects=0' | tee -a gw.conf >/dev/null
$ cat gw.conf
net.ipv4.ip_forward=1
net.ipv4.conf.all.send_redirects=0
```

The other common fix is to run the whole redirect as root: `sudo sh -c 'echo x > /etc/f'`.
