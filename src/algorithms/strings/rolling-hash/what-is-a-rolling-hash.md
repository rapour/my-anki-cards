What is a polynomial rolling hash of a string, and what is it good for?

---

It turns a string into a number (a sum of the letters, each multiplied by a power of a base `p`, and kept below a modulus `m`), so that comparing two strings costs one number comparison instead of a letter-by-letter comparison. Two rules:

- **Equal strings always have equal hashes.**
- Equal hashes **probably** mean equal strings, but not for sure. When two different strings share a hash, that is a **collision**.

*Rolling* means the hash of a window of letters can be updated in `O(1)` as the window slides along the text, and the hash of any substring can be read off in `O(1)` after one `O(n)` pass.

Kattis *String Hashing* is exactly this: given a string of up to 300,000 letters and up to 300,000 queries `(L, R)`, print a number for each substring `s[L..R)` so that equal substrings get equal numbers.
