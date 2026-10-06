What does `cat /sys/devices/cpu_core/cpus` print?

---

The CPU numbers of the fast cores (P-cores), for example `0-11`.

- It only exists on Intel CPUs that mix fast cores with slow ones (E-cores). `/sys/devices/cpu_atom/cpus` lists the slow ones.
- Use it to run a benchmark on the fast cores only:

```sh
taskset -c "$(cat /sys/devices/cpu_core/cpus)" ./bench
```
