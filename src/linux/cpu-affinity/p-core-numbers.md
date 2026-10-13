What does `cat /sys/devices/cpu_core/cpus` print?

---

The numbers of the logical CPUs (the units the operating system schedules programs on) that belong to the fast cores, called P-cores (*performance* cores), for example `0-11`.

- It only exists on Intel CPUs that mix fast cores with slow ones (E-cores, the *efficiency* cores). `/sys/devices/cpu_atom/cpus` lists the slow ones.
- Use it with `taskset`, a command that limits which CPUs a program may run on, to run a benchmark on the fast cores only:

```sh
taskset -c "$(cat /sys/devices/cpu_core/cpus)" ./bench
```
