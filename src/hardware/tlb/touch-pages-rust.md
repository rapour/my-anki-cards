Both calls do 10 million increments. Which one is slower, and why?

```rust
const INTS_PER_PAGE: usize = 4096 / size_of::<i32>(); // 1024

fn touch_pages(pages: usize, total: usize) {
    let mut memory = vec![0i32; pages * INTS_PER_PAGE];
    for _ in 0..total / pages {
        for page in 0..pages {
            memory[page * INTS_PER_PAGE] += 1; // one int per page
        }
    }
    std::hint::black_box(&memory); // keeps the work alive
}

touch_pages(32, 10_000_000);
touch_pages(2048, 10_000_000);
```

---

A *page* is the 4 KB block of memory that the CPU's address translation works on. The *TLB* is the small cache of those translations, and it holds only a limited number of entries (often 64 to 128 for the first level, depending on the CPU).

The second one (2048 pages, 8 MB). The first loops over only 32 pages (128 KB), which fits in the TLB. The second loops over far more pages than the TLB holds, so the TLB thrashes and most accesses need a page walk.

- Build with `cargo build --release`. A debug build hides the effect.
- The 8 MB also falls out of the L1 and L2 caches, so part of the slowdown is cache misses. Count `dTLB-load-misses` with `perf stat` to see the TLB part on its own.
