How do you show, and then change, the CPU affinity of a running multithreaded process with PID 4242?

---

```sh
taskset -cp 4242           # show the current CPU list
taskset -acp 0-11 4242     # set it for every thread
```

- `-p` acts on an existing PID instead of starting a command. The CPU list comes before the PID.
- Without `-a` only the thread whose ID is 4242 changes; the other threads keep their old affinity.
- Changing another user's process needs `CAP_SYS_NICE`.
- Underneath, `taskset` calls `sched_getaffinity(2)` and `sched_setaffinity(2)`.
