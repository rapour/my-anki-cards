How should you choose the base `p` and the modulus `m`?

---

- **Base `p`:** a number larger than the number of different letters. A prime such as `31` works for the 26 lowercase letters.
- **Modulus `m`:** a large prime, about 10⁹, such as `1_000_000_007`. For two different strings the chance of a collision is roughly `1/m`, so bigger is safer.
- **Size of the product:** `(m − 1)²` must fit in a `u64`. That holds for `m` below 2³², so `m ≈ 10⁹` is comfortable.
- **Do not use `m = 2⁶⁴`** (letting the `u64` wrap around). There are known strings, the Thue–Morse strings, that collide for **every** base.
- A base chosen at random when the program starts also defeats test data written to break a fixed base.
