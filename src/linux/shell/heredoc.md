What does a **here-document**, `<<'EOF' … EOF`, do in a shell command, and why does quoting the `'EOF'` matter?

---

It feeds the lines that follow, up to a line containing only `EOF`, to the command as its **standard input**, as if they came from a file. `EOF` is only a marker: any word works, as long as the closing line matches it exactly.

**Quoting the marker decides whether the shell changes the text:**

- `<<EOF` (unquoted): the shell first expands `$VARIABLE`, `$(command)` and backslashes inside the text.
- `<<'EOF'` (quoted): the text is passed on exactly as written.

```sh
$ cat <<EOF
home is $HOME, shell is $(basename $SHELL)
EOF
home is /root, shell is bash
$ cat <<'EOF'
home is $HOME, shell is $(basename $SHELL)
EOF
home is $HOME, shell is $(basename $SHELL)
```

Quote the marker when writing **config files or scripts**. A `$` meant for the file, such as `$LAN` in a script, would otherwise be replaced by the shell, usually with nothing.

A common pattern writes a root-owned file. `sudo tee` opens the file as root, and `>/dev/null` hides the copy `tee` prints:

```sh
sudo tee /etc/dnsmasq.d/vpn-gw.conf >/dev/null <<'EOF'
interface=wlp0s20f3
bind-dynamic
EOF
```

`<<-EOF` also strips leading **tab** characters (not spaces) from each line, so the text can be indented inside a script.
