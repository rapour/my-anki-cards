Write a **union-find** (disjoint-set union) structure in Rust, and use it to group records when matching pairs arrive one at a time.

---

Union-find keeps every record in a tree of "parents". The record at the top of a tree (the one that is its own parent) is the group's **representative**. Two records are in the same group exactly when they have the same representative.

- `find(x)`: follow parents up to the representative. **Path compression** re-points every record on the way directly at the representative, which keeps later searches very fast.
- `union(a, b)`: find both representatives. If they differ, hang the **smaller** tree under the bigger one (**union by size**), merging the groups and keeping the trees shallow.

With path compression and union by size together, each operation is close to constant time. (Strictly it grows like the inverse Ackermann function, which stays below 5 for any input you will ever meet.)

```rust
struct UnionFind {
    parent: Vec<usize>,
    size: Vec<usize>, // number of records under each representative
}

impl UnionFind {
    fn new(size: usize) -> Self {
        // at the start every record is alone: its own parent
        Self {
            parent: (0..size).collect(),
            size: vec![1; size],
        }
    }

    fn find(&mut self, x: usize) -> usize {
        if self.parent[x] != x {
            let root = self.find(self.parent[x]);
            self.parent[x] = root; // path compression
        }
        self.parent[x]
    }

    fn union(&mut self, a: usize, b: usize) {
        let (mut root_a, mut root_b) = (self.find(a), self.find(b));
        if root_a == root_b {
            return; // already in the same group
        }
        if self.size[root_a] < self.size[root_b] {
            std::mem::swap(&mut root_a, &mut root_b);
        }
        self.parent[root_b] = root_a; // smaller tree goes under the bigger one
        self.size[root_a] += self.size[root_b];
    }
}

fn main() {
    let mut groups = UnionFind::new(6);

    // matches arrive one at a time
    groups.union(0, 1);
    groups.union(1, 2);
    groups.union(3, 4);

    assert_eq!(groups.find(0), groups.find(2)); // linked through record 1
    assert_eq!(groups.find(3), groups.find(4));
    assert_ne!(groups.find(0), groups.find(3)); // separate entities
    assert_ne!(groups.find(5), groups.find(0)); // record 5 is alone
    println!("union-find works");
}
```

The recursion in `find` is shallow: union by size keeps every tree about `log2(n)` levels deep at most, so there is no risk of overflowing the stack.
