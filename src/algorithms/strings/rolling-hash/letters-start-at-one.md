Why should letters map to 1, 2, 3, ... and not to 0, 1, 2, ...?

---

If `a = 0`, a letter `a` adds nothing to the hash, so strings that differ only by letters `a` can look the same. With the degree-0 term last:

- `"a"`, `"aa"` and `"aaa"` all hash to `0`.
- `"ab"` and `"b"` both hash to `1`, because the leading `a` contributes `0 · p`.

With `a = 1, b = 2, ...` every letter contributes something, so these strings get different hashes.
