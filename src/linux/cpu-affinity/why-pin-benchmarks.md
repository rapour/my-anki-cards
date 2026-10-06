Why pin a benchmark to one core type with `taskset` before running `perf stat` on a hybrid Intel CPU?

---

So every thread runs on the same kind of core, which makes counts and IPC comparable between runs.

- Unpinned, the scheduler moves threads between P-cores and E-cores. `perf` then splits each event into `cpu_core` and `cpu_atom` rows and scales up partial counts, so the totals are estimates.
- P-cores and E-cores have different designs, so their IPC can't be compared or averaged.
- Pinning is not isolation: other processes can still run on the same CPUs. Close busy programs and repeat the measurement, for example with `perf stat -r 5`, to see the spread.
