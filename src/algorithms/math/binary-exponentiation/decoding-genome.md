Codeforces 222E *Decoding Genome*: count the valid DNA chains of length `n` (a huge number) when some pairs of nucleotides may not follow each other. How?

---

Turn the rules into a graph. Each nucleotide is a node, and there is an edge `a → b` when `b` is allowed to come right after `a`. Put it in a matrix `A` with `A[a][b] = 1` for an allowed pair.

A chain of `n` nucleotides is a **walk with `n − 1` edges** that may start anywhere. So the answer is the sum of **all entries** of `A^(n−1)`.

Example with three letters `a b c`, where `ab` and `cc` are forbidden: the rows of `A` are `a: [1, 0, 1]`, `b: [1, 1, 1]` and `c: [1, 1, 0]`.

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

/// Strings of length `n` where `allowed[a][b]` is 1 if letter b
/// may come
/// right after letter a.
fn count_strings(n: u64, allowed: &Matrix) -> u64 {
    // a string of n letters is a walk of n - 1 steps that may
    // start on
    // any letter
    let walks = matrix_power(allowed.clone(), n - 1);
    walks.iter().flatten().fold(0, |sum, &x| (sum + x) % MOD)
}

fn main() {
    // 3 letters: a, b, c. Forbidden neighbours: "ab" and "cc"
    let allowed: Matrix =
        vec![vec![1, 0, 1], vec![1, 1, 1], vec![1, 1, 0]];

    // brute force: try every string of length n
    for n in 1..=7u32 {
        let mut count = 0;
        for x in 0..3u64.pow(n) {
            let letters: Vec<usize> = (0..n)
                .map(|i| (x / 3u64.pow(i) % 3) as usize)
                .collect();
            if letters.windows(2).all(|w| allowed[w[0]][w[1]] == 1) {
                count += 1;
            }
        }
        assert_eq!(count_strings(n as u64, &allowed), count);
    }
}
```

The program also checks every chain of length up to 7 by brute force.
