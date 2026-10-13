How can binary exponentiation compute the `n`-th Fibonacci number in `O(log n)`?

---

The Fibonacci numbers are `F(0) = 0`, `F(1) = 1` and `F(n) = F(n−1) + F(n−2)`. One step of this rule can be written as a matrix times a pair of numbers:

`[F(n+1), F(n)] = [[1, 1], [1, 0]] · [F(n), F(n−1)]`

Doing it `n` times means multiplying by the matrix `n` times, so you need the matrix to the power `n`, which binary exponentiation gives in `O(log n)` matrix multiplications:

`[[1, 1], [1, 0]]ⁿ = [[F(n+1), F(n)], [F(n), F(n−1)]]`

so `F(n)` is the top right entry. The "1" for matrices is the **identity matrix** `[[1, 0], [0, 1]]`.

```rust
const MOD: u64 = 1_000_000_007;
type Matrix = [[u64; 2]; 2];

fn multiply(a: &Matrix, b: &Matrix) -> Matrix {
    let mut c = [[0; 2]; 2];
    for i in 0..2 {
        for j in 0..2 {
            for k in 0..2 {
                c[i][j] = (c[i][j] + a[i][k] * b[k][j]) % MOD;
            }
        }
    }
    c
}

fn matrix_power(mut base: Matrix, mut exp: u64) -> Matrix {
    // the identity matrix is the "1" of matrices
    let mut result = [[1, 0], [0, 1]];
    while exp > 0 {
        if exp & 1 == 1 {
            result = multiply(&result, &base);
        }
        base = multiply(&base, &base);
        exp >>= 1;
    }
    result
}

fn fib(n: u64) -> u64 {
    // [[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]
    matrix_power([[1, 1], [1, 0]], n)[0][1]
}

fn main() {
    assert_eq!(fib(0), 0);
    assert_eq!(fib(1), 1);
    assert_eq!(fib(10), 55);
    // F(50) = 12586269025, modulo 10^9 + 7
    assert_eq!(fib(50), 586_268_941);
    assert_eq!(fib(90), 210_345_902);
    assert_eq!(fib(1000), 517_691_607);
}
```

Problems usually ask for the answer modulo 10⁹ + 7, so every entry is reduced after each multiplication.
