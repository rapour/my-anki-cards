Which command starts `./bench` so that it may only run on logical CPUs 0 to 11?

---

`taskset -c 0-11 ./bench`

- `-c` (`--cpu-list`) takes a list: `0-11`, `0,2,4`, or `0-11:2` for every second CPU.
- Without `-c` the argument is a hex bitmask, so `taskset 0xfff ./bench` means the same.
- Threads and child processes that `./bench` starts are limited to the same CPUs, so a thread pool such as tokio's workers stays on them too.
- Pin to the P-cores without typing the range:

```sh
taskset -c "$(cat /sys/devices/cpu_core/cpus)" ./bench
```
