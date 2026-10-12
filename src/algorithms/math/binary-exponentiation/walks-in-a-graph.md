How do you count the walks with exactly `k` edges between every pair of nodes in a graph?

---

A **walk** is a route that may visit the same node more than once. Write the graph as an **adjacency matrix** `A`, where `A[i][j] = 1` if there is an edge from `i` to `j`. Then `(Aᵏ)[i][j]` is the number of walks with exactly `k` edges from `i` to `j`.

**Why:** `(A²)[i][j] = Σ A[i][m] · A[m][j]`. Each term is 1 exactly when `i → m → j` is a walk, so the sum counts all two-edge walks. Every extra factor of `A` adds one more edge.

The cost is `O(n³ log k)` for `n` nodes. For shortest walks with exactly `k` edges on weighted graphs, replace multiplication with addition and addition with `min`.

```rust
type Matrix = Vec<Vec<u64>>;

fn multiply(a: &Matrix, b: &Matrix) -> Matrix {
    let n = a.len();
    let mut c = vec![vec![0; n]; n];
    for i in 0..n {
        for k in 0..n {
            for j in 0..n {
                c[i][j] += a[i][k] * b[k][j];
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

/// Slow check: count walks edge by edge.
fn count_walks(
    graph: &Matrix,
    from: usize,
    to: usize,
    edges: u64,
) -> u64 {
    if edges == 0 {
        return (from == to) as u64;
    }
    (0..graph.len())
        .filter(|&next| graph[from][next] == 1)
        .map(|next| count_walks(graph, next, to, edges - 1))
        .sum()
}

fn main() {
    // edges: 0 -> 1, 0 -> 2, 1 -> 2, 2 -> 0
    let graph: Matrix =
        vec![vec![0, 1, 1], vec![0, 0, 1], vec![1, 0, 0]];

    // 2 edges from 0 back to 0: only 0 -> 2 -> 0
    assert_eq!(matrix_power(graph.clone(), 2)[0][0], 1);
    // 3 edges starting at 0: 0>1>2>0, 0>2>0>1 and 0>2>0>2 end at
    // nodes 0,
    // 1 and 2
    assert_eq!(matrix_power(graph.clone(), 3)[0], vec![1, 1, 1]);

    // compare every pair of nodes with the slow count
    for k in 0..=6u64 {
        let by_matrix = matrix_power(graph.clone(), k);
        for i in 0..3 {
            for j in 0..3 {
                assert_eq!(
                    by_matrix[i][j],
                    count_walks(&graph, i, j, k)
                );
            }
        }
    }
}
```
