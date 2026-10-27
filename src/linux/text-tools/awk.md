What does `awk` do, and how do you read this command?

```sh
awk -F': ' '$1 == "Suites" {print $2}' /etc/apt/sources.list.d/example.sources
```

---

**`awk`** reads its input one line at a time and splits each line into **fields**. It then runs a small program of `pattern {action}` rules on every line. Where `grep` picks lines and `sed` rewrites text, `awk` understands **columns** and can **calculate**.

How a line is handled:

- The fields are `$1`, `$2`, … and the whole line is `$0`. By default fields are separated by spaces or tabs. `-F` sets another separator.
- For each rule, if the **pattern** is true for this line, the **action** in `{ }` runs.
- A rule with no pattern runs on every line. A rule with no action prints the line.

The command above uses `': '` (a colon and a space) as the separator. So the line `Suites: noble` has `$1 = "Suites"` and `$2 = "noble"`, and only on that line is the pattern `$1 == "Suites"` true. It prints:

```text
noble
```

**Building blocks**

| Name | Meaning |
|---|---|
| `NR` | the number of the current line, counting from 1 |
| `NF` | the number of fields on this line, so `$NF` is the last field |
| `BEGIN {…}` | runs once, before the first line |
| `END {…}` | runs once, after the last line |
| `OFS` | the separator `print` puts between items; a space unless you set it |
| variables | need no declaration and start as 0 or empty text |
| arrays | indexed by any text, for example `n[$3]++` |

**Examples**, on this `requests.log` (method, path, status, bytes):

```text
GET /index.html 200 512
GET /missing 404 0
POST /login 200 128
GET /admin 403 64
GET /index.html 200 512
```

Print chosen columns, and only on some lines:

```sh
$ awk '$3 == 404 {print $2}' requests.log
/missing
$ awk '{printf "%-12s %s\n", $2, $3}' requests.log | head -2
/index.html  200
/missing     404
```

Add up a column, and print the total once the input ends:

```sh
$ awk '{bytes += $4} END {print bytes}' requests.log
1216
```

Count lines by status with an array. `for (s in n)` visits the keys in no fixed order, so sort the result:

```sh
$ awk '{n[$3]++} END {for (s in n) print s, n[s]}' requests.log | sort
200 3
403 1
404 1
```

A comma-separated file with a header line: skip it with `NR > 1`, then average a column. `-F,` makes the comma the separator:

```sh
$ cat prices.csv
item,price
tea,3
coffee,4
cake,6
$ awk -F, 'NR > 1 {sum += $2} END {print sum / (NR - 1)}' prices.csv
4.33333
$ awk -F, 'BEGIN {OFS = " = "} NR > 1 {print $1, $2}' prices.csv
tea = 3
coffee = 4
cake = 6
```

`NF` is the number of fields, so `$NF` is the last one:

```sh
$ echo 'a b c' | awk '{print NF, $NF}'
3 c
```

The same edit the `sed` command `s/^Suites: noble$/Suites: resolute/` plus `/^Enabled: no$/d` makes to an apt source. The first rule changes field 2 on the `Suites:` line. The second rule has only a pattern, so it prints every line except `Enabled: no`:

```sh
$ awk '$1 == "Suites:" {$2 = "resolute"} $0 != "Enabled: no"' example.sources
Types: deb
URIs: https://vendor.example.com/repo
Suites: resolute
Components: main
Signed-By: /usr/share/keyrings/example.gpg
```

Standard `awk` can't edit a file in place. Write to a new file and move it back: `awk '…' f > f.new && mv f.new f`. Ubuntu's `awk` is `mawk`. GNU awk (`gawk`, a separate package) adds extras such as `-i inplace`.
