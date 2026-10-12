Why is it safe to take the remainder after every multiplication, and why do you have to?

---

**Safe:** the remainder of a product only depends on the remainders of the factors:

`(a · b) mod m = ((a mod m) · (b mod m)) mod m`

Example with `m = 5`: `7 · 8 = 56` and `56 mod 5 = 1`. Using remainders first: `(7 mod 5) · (8 mod 5) = 2 · 3 = 6`, and `6 mod 5 = 1`. Same answer.

**Necessary:** without it the numbers explode. `3^18132` has about 8,650 digits. With a remainder after each step every number stays below `m`.

**Watch the size of the product.** Two numbers below `m` multiply to less than `m²`. That fits in a `u64` when `m` is at most about 4 billion (2³²). For bigger `m`, widen to `u128`.
