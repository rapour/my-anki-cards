What are the iTLB and the dTLB?

---

Most CPUs have two TLBs:

- **iTLB** (instruction TLB): translates addresses of code the CPU is about to run.
- **dTLB** (data TLB): translates addresses of data the program reads and writes.

`perf` has a separate event for each: `iTLB-load-misses` and `dTLB-load-misses`.
