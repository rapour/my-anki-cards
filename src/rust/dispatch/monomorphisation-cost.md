What does monomorphisation cost?

---

More machine code, because there is one copy of the function for every type.

- The binary gets bigger.
- Compile times get longer.
- Many copies of similar code can crowd the CPU's instruction cache (its small, fast memory for the code it is running).

`dyn Trait` avoids this: the function is compiled once, and the right method is looked up at run time in a *vtable*, a table of function addresses.
