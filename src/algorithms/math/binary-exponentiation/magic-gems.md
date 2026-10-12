Codeforces 1117D *Magic Gems*: a gem takes 1 unit of space, or `M` units when it is split. How many ways are there to fill exactly `N` units, with `N` up to 10¹⁸ and `M` up to 100, modulo 10⁹ + 7?

---

Think of it as laying pieces in a row. Each piece is a whole gem (size 1) or a split gem (size `M`). Let `f(n)` be the number of ways to fill `n` units. The last piece is either 1 unit or `M` units:

`f(n) = f(n−1) + f(n−M)`, with `f(0) = 1`

Example, `M = 2`, `N = 4`: `1+1+1+1`, `1+1+2`, `1+2+1`, `2+1+1`, `2+2`, so `f(4) = 5`.

`N` is too big to loop over, but this is a **linear recurrence**, so a matrix can do one step. Keep the last `M` values as the state `[f(i), f(i−1), ..., f(i−M+1)]`:

- the new first entry is `f(i) + f(i−M+1)`,
- every other entry is the old entry one place to the left.

That is an `M × M` matrix. Raise it to the power `N`: the cost is `O(M³ log N)`.

```rust
const MOD: u64 = 1_000_000_007;
type Matrix = Vec<Vec<u64>>;

fn multiply(a: &Matrix, b: &Matrix) -> Matrix {
    let n = a.len();
    let mut c = vec![vec![0; n]; n];
    for i in 0..n {
        for k in 0..n {
            for j in 0..n {
                c[i][j] = (c[i][j] + a[i][k] * b[k][j]) % MOD;
            }
        }
    }
    c
}

fn matrix_power(mut base: Matrix, mut exp: u64) -> Matrix {
    let n = base.len();
    let mut result: Matrix = (0..n)
        .map(|i| (0..n).map(|j| (i == j) as u64).collect())
        .collect();
    while exp > 0 {
        if exp & 1 == 1 {
            result = multiply(&result, &base);
        }
        base = multiply(&base, &base);
        exp >>= 1;
    }
    result
}

/// Ways to fill `n` units with pieces of size 1 (a whole gem) or
/// `m` (a
/// split gem).
fn magic_gems(n: u64, m: usize) -> u64 {
    // state = [f(i), f(i-1), ..., f(i-m+1)] and f(i+1) = f(i) +
    // f(i+1-m)
    let mut step = vec![vec![0; m]; m];
    step[0][0] = 1; // f(i)
    step[0][m - 1] += 1; // f(i+1-m)
    for row in 1..m {
        // shift every other entry down by one place
        step[row][row - 1] = 1;
    }
    // the start state is [f(0), 0, ..., 0] = [1, 0, ..., 0], so
    // f(n) is
    // the top left entry
    matrix_power(step, n)[0][0]
}

fn main() {
    assert_eq!(magic_gems(4, 2), 5);
    assert_eq!(magic_gems(3, 2), 3);
    assert_eq!(magic_gems(10, 3), 28);
    assert_eq!(magic_gems(60, 5), 10_730_820);

    // compare with the simple recurrence for small inputs
    for m in 2..=6usize {
        let mut f = vec![1u64];
        for i in 1..=40usize {
            f.push(f[i - 1] + if i >= m { f[i - m] } else { 0 });
            assert_eq!(magic_gems(i as u64, m), f[i] % MOD);
        }
    }
}
```
