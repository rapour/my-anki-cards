How many multiplications does binary exponentiation need for `n = 10¹⁸`, compared with the plain loop?

---

`10¹⁸` has **60 bits**, because 2⁶⁰ ≈ 1.15 · 10¹⁸. Binary exponentiation does:

- one squaring per bit except the last: **59** squarings,
- one multiplication per `1` bit: `10¹⁸` has **24** of them.

That is about **83** multiplications. The plain loop needs `10¹⁸ − 1`.

In general: at most about `2 · log₂ n` multiplications, so `O(log n)`.
