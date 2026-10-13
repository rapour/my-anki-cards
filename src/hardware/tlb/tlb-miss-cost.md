Does a TLB miss always mean a slow read from main memory (DRAM)?

---

No. Page table entries are ordinary data, so they are often found in the L1, L2 or L3 caches (the CPU's small, fast caches). The miss then costs only a little extra time.

- A real DRAM access costs far more: typically hundreds of CPU cycles.
- A single miss is cheap. The damage comes from many misses in a row, which happens when a program keeps using more pages than the TLB can hold (*TLB thrashing*).
