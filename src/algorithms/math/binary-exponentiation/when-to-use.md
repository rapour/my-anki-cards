What signs in a problem statement tell you to use binary exponentiation?

---

Look for **a step repeated a huge number of times**: an exponent or length up to 10¹⁵ or 10¹⁸, often with "modulo 10⁹ + 7".

| Sign in the problem | Example |
|---|---|
| `a^b mod m` with a huge `b` | UVa 374 Big Mod, UVa 1230 MODEX |
| digits of a huge power | SPOJ LASTDIG (last digit), UVa 11029 (first and last three) |
| count strings of length `n` where positions are independent | LeetCode 1922 Count Good Numbers |
| a recurrence with a huge `n` | Fibonacci, Codeforces 1117D Magic Gems (matrix) |
| count strings or walks of length `n` with forbidden neighbours | Codeforces 222E Decoding Genome (matrix) |
| the same shuffle repeated `k` times | permutation power |

If the repeated step is a matrix, the cost is `O(size³ log n)`, so check that the matrix is small.
