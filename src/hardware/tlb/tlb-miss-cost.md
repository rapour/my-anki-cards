Does a TLB miss always mean a slow read from main memory (DRAM)?

---

No. Page table entries are ordinary data, so they are often found in the L1, L2 or L3 caches. The miss then costs only a few extra cycles.

- A real DRAM access costs hundreds of cycles, which is far more.
- A single miss is cheap. The damage comes from many misses in a row (see TLB thrashing).
