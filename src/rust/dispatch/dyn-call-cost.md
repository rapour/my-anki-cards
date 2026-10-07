Why is a call through a vtable usually slower than a static call?

---

- **Extra loads:** the program reads the vtable pointer and then the function address before it can call.
- **Indirect branch:** the CPU has to guess where the call goes. A wrong guess is a branch miss, like the ones `perf stat` counts.
- **No inlining:** the compiler usually cannot see which function runs, so it cannot paste the body into the caller or optimise across the call.

The cost of one call is small. It matters in hot loops that make millions of calls. The optimiser can sometimes work out the type and skip the lookup, which is called *devirtualisation*.
