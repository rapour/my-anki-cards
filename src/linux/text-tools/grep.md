What does `grep` do, and what do these two commands print?

```sh
grep -E '^(URIs|Suites|Enabled)' /etc/apt/sources.list.d/example.sources
sudo apt update 2>&1 | grep -iE 'example|^E:|^W:'
```

---

**`grep`** prints the lines of its input that match a pattern (a *regular expression*), and nothing else.

**First command.** It shows only three fields of the file:

```text
URIs: https://vendor.example.com/repo
Suites: noble
Enabled: no
```

- `^` matches the start of a line, so only lines that *begin* with a field name match.
- `(URIs|Suites|Enabled)` means "URIs or Suites or Enabled".
- `-E` turns on *extended* regular expressions, where `|` and `( )` work as written. Without `-E`, grep treats them as plain characters unless you write `\|` and `\( \)`, so `grep '^(URIs|Suites)'` finds nothing.

**Second command.** It keeps only the lines about the `example` source, plus any errors (`E:`) and warnings (`W:`).

- `-i` ignores case, so `Example` matches too. `-iE` is `-i` and `-E` together.
- `2>&1` matters. A program writes normal output to *standard output* (stdout) and errors to *standard error* (stderr). `|` only carries stdout, and apt prints its `E:` and `W:` lines on stderr. Without `2>&1` those lines skip `grep` entirely: they go straight to the screen, unfiltered and uncounted. `2>&1` sends stderr to the same place as stdout, into the pipe.

Real output from a source whose suite doesn't exist (here the made-up `nosuchsuite`, filtered with `archive` instead of `example`):

```text
Ign:1 http://archive.ubuntu.com/ubuntu nosuchsuite InRelease
Err:2 http://archive.ubuntu.com/ubuntu nosuchsuite Release
E: The repository 'http://archive.ubuntu.com/ubuntu nosuchsuite Release' does not have a Release file.
```

Without `2>&1`, the `E:` line never reaches `grep`.

**Options worth knowing**, on this `access.log`:

```text
GET /index.html 200
GET /missing 404
POST /login 200
get /Admin 403
GET /index.html 200
```

| Command | Prints | Option |
|---|---|---|
| `grep -v ' 200$' access.log` | `GET /missing 404`<br>`get /Admin 403` | `-v`: lines that do **not** match |
| `grep -c ' 200$' access.log` | `3` | `-c`: count matching lines |
| `grep -n index access.log` | `1:GET /index.html 200`<br>`5:GET /index.html 200` | `-n`: line numbers |
| `grep -i '^get' access.log` | the four GET lines, including `get /Admin 403` | `-i`: ignore case |
| `grep -oE '[0-9]{3}$' access.log` | `200`, `404`, `200`, `403`, `200` (one per line) | `-o`: only the matching part |
| `grep -A1 missing access.log` | `GET /missing 404`<br>`POST /login 200` | `-A1`: 1 line after each match (`-B` before, `-C` both) |

A few more:

- `-w` matches whole words only.
- `-r` searches every file in a folder, and `-l` prints only the names of files that match.
- `-F` searches for plain text, so `.` is just a dot instead of "any character".
- `-q` prints nothing. Its exit status says whether anything matched: 0 if it did, 1 if not. That makes it the form to use inside `if`.

```sh
$ printf 'cat\ncatalog\nthe cat sat\n' | grep -w cat
cat
the cat sat
$ grep -rl '^port=' conf/ | sort
conf/a.conf
conf/b.conf
$ printf 'a.b\naxb\n' | grep -F 'a.b'
a.b
$ if grep -q '^debug=true' conf/c.conf; then echo "debug is on"; fi
debug is on
```
