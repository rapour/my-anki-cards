What are the iTLB and the dTLB?

---

The TLB (translation lookaside buffer) is the CPU's small cache of address translations from pages to page frames. Most CPUs have two of them:

- **iTLB** (instruction TLB): translates addresses of code the CPU is about to run.
- **dTLB** (data TLB): translates addresses of data the program reads and writes.

`perf` has a separate event for each: `iTLB-load-misses` and `dTLB-load-misses`.
