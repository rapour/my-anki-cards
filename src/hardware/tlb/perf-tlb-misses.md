Which `perf stat` command counts how often the CPU's address-translation cache (the TLB) misses, for data and for instructions, while `./bench` runs?

---

```sh
perf stat -e dTLB-loads,dTLB-load-misses \
  -e iTLB-loads,iTLB-load-misses ./bench
```

- `dTLB` is the data TLB and `iTLB` is the instruction TLB. Miss rate = misses ÷ loads. A high dTLB rate points to data spread over many pages.
- An event can show `<not supported>` on some CPUs. Run `perf list | grep -i tlb` to see what yours offers.
- On a hybrid Intel CPU you get a row for each core type, like `cpu_core/dTLB-load-misses/`.
