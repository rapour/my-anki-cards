Why is summing a `Vec<i32>` usually faster than summing a `LinkedList<i32>`, as far as the TLB is concerned?

```rust
fn sum_vec(v: &Vec<i32>) -> i64 {
    v.iter().map(|&x| x as i64).sum()
}
fn sum_list(l: &LinkedList<i32>) -> i64 {
    l.iter().map(|&x| x as i64).sum()
}
```

---

A `Vec` is one block of memory. One TLB lookup serves 1024 reads (4096 bytes ÷ 4 bytes per `i32`).

A `LinkedList` node is a separate allocation, and nodes can land on many different pages. Each `next` pointer may need a new translation, and the CPU cannot guess the next address in advance.

- The same reasoning applies to other node-based containers, such as trees.
- Prefer flat arrays and read them in order when speed matters.
