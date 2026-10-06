What is cache blocking (also called tiling)?

---

Split a big job into small chunks, and finish all the steps on one chunk before moving to the next. A chunk that fits in the L1 cache and in the TLB's reach is read from fast memory every time.

```rust
// Two passes over everything: each pass touches all the pages.
for x in data.iter_mut() { *x += 1; }
for x in data.iter_mut() { *x *= 2; }

// Blocked: both steps on one 64 KB chunk, then the next chunk.
for chunk in data.chunks_mut(16 * 1024) {
    for x in chunk.iter_mut() { *x += 1; }
    for x in chunk.iter_mut() { *x *= 2; }
}
```

- Choose the chunk size from your cache and TLB sizes, then measure.
