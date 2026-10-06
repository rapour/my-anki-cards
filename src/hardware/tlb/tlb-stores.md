What does the TLB store: your data, or something else?

---

Not your data. It stores recent **mappings from a page to its page frame** (copies of page table entries).

- TLB stands for Translation Lookaside Buffer. It is a small, very fast cache inside the CPU.
- If the mapping is in the TLB, the CPU skips the page walk.
- Your data is kept in the L1, L2 and L3 caches. The TLB only helps find where it is.
