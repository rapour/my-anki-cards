What does monomorphisation cost?

---

More machine code, because there is one copy of the function for every type.

- The binary gets bigger.
- Compile times get longer.
- Many copies of similar code can crowd the CPU's instruction cache.

`dyn Trait` avoids this: the function is compiled once, and the vtable picks the right method at run time.
