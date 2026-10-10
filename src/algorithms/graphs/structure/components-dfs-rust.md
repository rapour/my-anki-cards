Write a Rust function that groups records into connected components (entities), given the list of matching pairs. Use DFS with an explicit stack.

---

First we turn the list of pairs into neighbour lists. The pairs are undirected ("A matches B" works both ways), so each pair adds an edge in both directions. Then we scan the records, and for each unassigned one we start a new group and flood-fill outwards.

This version uses an explicit `stack` (a `Vec`) rather than recursion, which avoids any risk of overflowing the program's call stack on long chains of matches.

```rust
fn components(records: usize, matches: &[(usize, usize)]) -> Vec<usize> {
    let mut neighbours = vec![Vec::new(); records];
    for &(a, b) in matches {
        neighbours[a].push(b);
        neighbours[b].push(a); // a match works both ways
    }

    const UNASSIGNED: usize = usize::MAX;
    let mut group = vec![UNASSIGNED; records];
    let mut next_group = 0;

    for start in 0..records {
        if group[start] != UNASSIGNED {
            continue; // already part of an earlier group
        }
        group[start] = next_group;
        let mut stack = vec![start];
        while let Some(node) = stack.pop() {
            for &next in &neighbours[node] {
                if group[next] == UNASSIGNED {
                    group[next] = next_group;
                    stack.push(next);
                }
            }
        }
        next_group += 1;
    }
    group
}

fn main() {
    // records 0..5: 0 matches 1, 1 matches 2, and 3 matches 4. Record 5 matches nobody.
    let group = components(6, &[(0, 1), (1, 2), (3, 4)]);
    assert_eq!(group, vec![0, 0, 0, 1, 1, 2]);
    // 0 and 2 were never compared directly, yet they share a group
    assert_eq!(group[0], group[2]);
    println!("{group:?}");
}
```
