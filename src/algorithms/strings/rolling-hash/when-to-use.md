What signs in a problem tell you to use a rolling hash, and when should you pick something else?

---

Look for **many comparisons of substrings** (equal? same as a prefix? a palindrome?) on a string that is too long to compare letter by letter every time.

| Sign in the problem | Example |
|---|---|
| a number for each substring, equal substrings equal | Kattis String Hashing |
| find every occurrence of a pattern | SPOJ NHAY, Rabin–Karp |
| a pattern is removed from the end as it appears | HackerRank Gift Boxes |
| count distinct substrings | Codeforces 271D Good Substrings |
| palindromes among substrings or prefixes | Codeforces 835D, Codeforces 7D |
| a prefix that is also a suffix and appears inside | Codeforces 126B Password |

**Hashing is probabilistic.** If you need a guaranteed answer, use KMP or the Z-function for pattern matching and suffix structures for distinct substrings. Hashing wins when it is simpler to write, and a tiny collision risk is acceptable.
