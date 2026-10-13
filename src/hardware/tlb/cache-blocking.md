What is cache blocking (also called tiling)?

---

Split a big job into small chunks, and finish all the steps on one chunk before moving to the next. The *L1 cache* is the CPU's smallest and fastest memory. The *TLB* is a small cache of address translations, and its *reach* is the amount of memory it can translate without a slow table lookup (number of entries × page size). A chunk that fits in the L1 cache and in the TLB's reach is served from fast memory every time it is read.

```rust
/// Two passes over the whole array: each pass touches every page.
fn two_passes(data: &mut [i32]) {
    for x in data.iter_mut() {
        *x += 1;
    }
    for x in data.iter_mut() {
        *x *= 2;
    }
}

/// Both steps on one 64 KB chunk, then on the next chunk.
fn blocked(data: &mut [i32]) {
    for chunk in data.chunks_mut(16 * 1024) {
        for x in chunk.iter_mut() {
            *x += 1;
        }
        for x in chunk.iter_mut() {
            *x *= 2;
        }
    }
}

fn main() {
    let mut a = vec![1i32; 1 << 20];
    let mut b = a.clone();
    two_passes(&mut a);
    blocked(&mut b);
    // same result, different memory access pattern
    assert_eq!(a, b);
}
```

- Choose the chunk size from your cache and TLB sizes, then measure.
