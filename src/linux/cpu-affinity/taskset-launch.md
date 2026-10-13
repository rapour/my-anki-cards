Which command starts the program `./bench` so that the operating system may only run it on logical CPUs 0 to 11 (a logical CPU is one unit that the operating system schedules programs on)?

---

`taskset -c 0-11 ./bench`

`taskset` limits which CPUs a program may run on.

- `-c` (`--cpu-list`) takes a list: `0-11`, `0,2,4`, or `0-11:2` for every second CPU.
- Without `-c` the argument is a hex bitmask, so `taskset 0xfff ./bench` means the same.
- Threads and child processes that `./bench` starts are limited to the same CPUs, so a thread pool (for example the worker threads of tokio, a Rust async runtime) stays on them too.
- Pin to the P-cores without typing the range:

```sh
taskset -c "$(cat /sys/devices/cpu_core/cpus)" ./bench
```
