Write a **union-find** (disjoint-set union) structure in Rust, and use it to group records when matching pairs arrive one at a time.

---

Union-find keeps every record in a tree of "parents". The record at the top of a tree (the one that is its own parent) is the group's **representative**. Two records are in the same group exactly when they have the same representative.

- `find(x)`: follow parents up to the representative. **Path compression** re-points every record on the way directly at the representative, which keeps later searches very fast.
- `union(a, b)`: find both representatives, and if they differ, attach one tree under the other, merging the groups.

With path compression, each operation is close to constant time in practice.

```rust
struct UnionFind {
    parent: Vec<usize>,
}

impl UnionFind {
    fn new(size: usize) -> Self {
        // at the start every record is alone: its own parent
        Self { parent: (0..size).collect() }
    }

    fn find(&mut self, x: usize) -> usize {
        if self.parent[x] != x {
            let root = self.find(self.parent[x]);
            self.parent[x] = root; // path compression
        }
        self.parent[x]
    }

    fn union(&mut self, a: usize, b: usize) {
        let (root_a, root_b) = (self.find(a), self.find(b));
        if root_a != root_b {
            self.parent[root_a] = root_b;
        }
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

The recursion in `find` is shallow in practice because of path compression. In a worst case with a very long chain of parents you could switch it to a loop.
