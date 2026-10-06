On a hybrid Intel CPU under Linux, which file lists the logical CPU numbers of the P-cores?

---

`/sys/devices/cpu_core/cpus`

```sh
cat /sys/devices/cpu_core/cpus    # P-cores, for example 0-11
cat /sys/devices/cpu_atom/cpus    # E-cores, for example 12-19
```

- `cpu_core` and `cpu_atom` are the perf PMUs for each core type. They are why `perf stat` prints separate `cpu_core/…/` and `cpu_atom/…/` rows.
- The output is a CPU list (`0-11`, `0-5,8`), the same format `taskset -c` takes.
- The numbers are logical CPUs: with Hyper-Threading each P-core appears twice.
- On a non-hybrid CPU neither file exists; the single PMU is `/sys/devices/cpu`.
