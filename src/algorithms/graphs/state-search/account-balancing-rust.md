Write a Rust function that returns the minimum number of transactions needed to settle a group's debts, given transactions `(from, to, amount)`. Use net balances and DFS backtracking.

---

Step one builds the net balance of each person. Step two, `settle`, takes the first unsettled person (`start`), tries to pass their balance to each later person of the opposite sign, recurses, and **undoes** the move afterwards.

Once a cancelling pair (`balances[i] + balances[start] == 0`) has been tried, the loop stops (`break`): settling two people with one payment cannot be beaten, so the remaining candidates are skipped. Only this first pruning trick is shown. The second one (skipping a candidate whose balance repeats one already tried) is left out to keep the code short.

```rust
use std::collections::HashMap;

fn min_transactions(transactions: &[(usize, usize, i32)]) -> usize {
    let mut net: HashMap<usize, i32> = HashMap::new();
    for &(from, to, amount) in transactions {
        *net.entry(from).or_insert(0) += amount; // paid out: now owed money
        *net.entry(to).or_insert(0) -= amount; // received: now owes money
    }
    let mut balances: Vec<i32> = net.into_values().filter(|&b| b != 0).collect();
    settle(&mut balances, 0)
}

fn settle(balances: &mut [i32], start: usize) -> usize {
    // skip people who are already settled
    let mut start = start;
    while start < balances.len() && balances[start] == 0 {
        start += 1;
    }
    if start == balances.len() {
        return 0; // everyone is settled
    }

    let mut best = usize::MAX;
    for i in start + 1..balances.len() {
        let opposite_sign = (balances[i] > 0) != (balances[start] > 0);
        if !opposite_sign {
            continue;
        }
        balances[i] += balances[start]; // one payment settles `start`
        best = best.min(1 + settle(balances, start + 1));
        balances[i] -= balances[start]; // undo, then try the next candidate

        if balances[i] + balances[start] == 0 {
            break; // a perfect cancel is always optimal
        }
    }
    best
}

fn main() {
    // person 0 paid 10 to person 1, person 2 paid 5 to person 0
    assert_eq!(min_transactions(&[(0, 1, 10), (2, 0, 5)]), 2);

    // everything nets out neatly: one payment settles all
    let chain = [(0, 1, 10), (1, 0, 1), (1, 2, 5), (2, 0, 5)];
    assert_eq!(min_transactions(&chain), 1);

    assert_eq!(min_transactions(&[(0, 1, 5), (1, 0, 5)]), 0); // already even
    println!("account balancing works");
}
```
