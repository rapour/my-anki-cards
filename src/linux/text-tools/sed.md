What does `sed` do, and what exactly does this command change in the file?

```sh
sudo sed -i \
  -e 's/^Suites: noble$/Suites: resolute/' \
  -e '/^Enabled: no$/d' \
  /etc/apt/sources.list.d/example.sources
```

---

**`sed`** (*stream editor*) reads text one line at a time, runs a short script on each line, and prints the result. It suits edits you can state as a rule, such as "replace this" or "delete lines like that".

This command changes one line and deletes another:

| Part | Meaning |
|---|---|
| `-i` | edit the file **in place** instead of printing the result |
| `-e SCRIPT` | add a command. With several `-e`, every line goes through them in order |
| `s/^Suites: noble$/Suites: resolute/` | **s**ubstitute: where the pattern `^Suites: noble$` matches, put `Suites: resolute` |
| `/^Enabled: no$/d` | on every line that matches `^Enabled: no$`, run `d`, which **d**eletes the line |

The patterns are *regular expressions*. `^` matches the start of a line and `$` its end, so `^Suites: noble$` matches only a line that is exactly `Suites: noble`.

Before:

```text
Types: deb
URIs: https://vendor.example.com/repo
Suites: noble
Components: main
Signed-By: /usr/share/keyrings/example.gpg
Enabled: no
```

After: `Suites: resolute`, and the `Enabled: no` line is gone.

```text
Types: deb
URIs: https://vendor.example.com/repo
Suites: resolute
Components: main
Signed-By: /usr/share/keyrings/example.gpg
```

**Why the anchors matter.** Without `^` and `$`, `s/noble/resolute/` replaces the first `noble` on *every* line, even inside a URL:

```sh
$ echo 'URIs: https://mirror.example.com/noble/' | sed 's/noble/resolute/'
URIs: https://mirror.example.com/resolute/
```

The anchored pattern also leaves a line like `Suites: noble noble-updates` alone, so look at the file first.

**Everyday examples**, on this `notes.txt`:

```text
one cat, two cats
# a comment
port=8080
2026-10-27
```

Replace the first match on each line, or every match with `g`:

```sh
$ sed 's/cat/dog/' notes.txt | head -1
one dog, two cats
$ sed 's/cat/dog/g' notes.txt | head -1
one dog, two dogs
```

`-n` stops the automatic printing, and `p` prints on request:

```sh
$ sed -n '2,3p' notes.txt
# a comment
port=8080
$ sed -n 's/^port=//p' notes.txt
8080
```

Delete comment lines:

```sh
$ sed '/^#/d' notes.txt
one cat, two cats
port=8080
2026-10-27
```

`-E` turns on extended regular expressions. Groups in `( )` can then be reused as `\1`, `\2`, `\3`:

```sh
$ sed -E 's/([0-9]{4})-([0-9]{2})-([0-9]{2})/\3\/\2\/\1/' notes.txt | tail -1
27/10/2026
```

Any character can separate the parts of `s`, which is handy for paths:

```sh
$ echo /usr/local/bin | sed 's|/usr/local|/opt|'
/opt/bin
```

`-i.bak` edits in place but keeps the original as `notes.txt.bak`. On macOS, whose `sed` is the BSD version, write `-i ''` for no backup.
