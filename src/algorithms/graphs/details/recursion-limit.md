Recursive DFS can crash on very large graphs or very long chains (for example a million rows that each depend on the next). Why does this happen in Python and in Rust, and what are the fixes?

---

Every time a function calls itself, the computer must remember where to return to and keep that call's local variables. It stores them in a fixed-size area of memory called the **call stack**. A chain of one million nested calls needs one million of these records at the same time, and the stack runs out of room.

**In Python:** the interpreter allows about 1000 nested calls by default. Go deeper and Python raises a `RecursionError`. You can raise the limit with `sys.setrecursionlimit`, but a very high limit can crash the whole interpreter instead.

**In Rust:** there is no friendly limit. The size of the stack depends on the thread. The main thread's stack is set by the operating system (commonly 8 MiB on Linux, 1 MiB on Windows), and threads you create yourself get 2 MiB by default. If you run out, the program is **aborted** with a message such as "has overflowed its stack". You cannot catch this error.

**Fix 1 (best): use an explicit stack.** Replace the recursion with a loop and a `Vec` that you push to and pop from. The `Vec` lives on the heap, which can grow to the size of available memory. For reachability, components and similar jobs this is a direct replacement.

**Fix 2: run the recursion on a thread with a bigger stack.** In Rust, `std::thread::Builder::new().stack_size(...)` lets you ask for hundreds of megabytes. The code stays simple, but you are still guessing how much is enough.

**A subtlety of fix 1.** A simple loop that pushes all neighbours on the stack visits nodes in a different order than true recursive DFS, and it does not tell you when a node is *finished*. That is fine for "can I reach it?" and "which group is it in?". For cycle detection with three states, or for topological order by post-order, store `(node, index of the next neighbour to try)` on the stack, so the loop can tell when a node has used up all its neighbours.

**Rule of thumb:** if the input could contain a chain of thousands of nodes, prefer the explicit stack, and mention it to the interviewer.
