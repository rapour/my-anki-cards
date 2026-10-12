Write the Gift Boxes solution in Rust: count the boxes packed when items arrive one by one and every run of the pattern at the end of the belt is removed.

---

`hashes[i]` is the hash of the first `i` items that are on the belt right now. A new item extends the list by one entry. When the newest `k` items match the pattern, `truncate` removes them.

```rust
const P: u64 = 31;
const M: u64 = 1_000_000_007;

fn value(byte: u8) -> u64 {
    (byte - b'a' + 1) as u64
}

/// Items arrive one by one. Whenever the newest items spell
/// `pattern`,
/// they are removed
/// and one gift box is packed. Returns the number of boxes.
fn gift_boxes(pattern: &str, belt: &str) -> usize {
    let k = pattern.len();
    let target = pattern.bytes().fold(0, |h, b| (h * P + value(b)) % M);
    let power_k = (0..k).fold(1, |acc, _| acc * P % M); // P^k

    // hashes[i] = hash of the first i items that are on the belt
    // right
    // now
    let mut hashes = vec![0u64];
    let mut boxes = 0;

    for byte in belt.bytes() {
        // put the new item on the belt
        let next = (hashes.last().unwrap() * P + value(byte)) % M;
        hashes.push(next);
        // number of items on the belt
        let len = hashes.len() - 1;

        if len >= k {
            // hash of the last k items on the belt
            let newest = (next + M - hashes[len - k] * power_k % M) % M;
            if newest == target {
                // pack the box: these k items leave the belt
                hashes.truncate(len - k + 1);
                boxes += 1;
            }
        }
    }
    boxes
}

fn gift_boxes_slowly(pattern: &str, belt: &str) -> usize {
    let mut on_belt = String::new();
    let mut boxes = 0;
    for ch in belt.chars() {
        on_belt.push(ch);
        if on_belt.ends_with(pattern) {
            on_belt.truncate(on_belt.len() - pattern.len());
            boxes += 1;
        }
    }
    boxes
}

fn main() {
    assert_eq!(gift_boxes("ab", "abab"), 2);
    // after the first "ab" leaves, a new "ab" forms
    assert_eq!(gift_boxes("ab", "aabb"), 2);
    assert_eq!(gift_boxes("ab", "aaa"), 0);

    // compare with the slow method on pseudo-random belts
    let mut x: u64 = 7;
    let mut next = || {
        x = x
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        (x >> 33) as usize
    };
    for _ in 0..500 {
        let belt: String = (0..60)
            .map(|_| (b'a' + (next() % 2) as u8) as char)
            .collect();
        let pattern: String = (0..1 + next() % 4)
            .map(|_| (b'a' + (next() % 2) as u8) as char)
            .collect();
        assert_eq!(
            gift_boxes(&pattern, &belt),
            gift_boxes_slowly(&pattern, &belt)
        );
    }
}
```

- The slow version builds the belt as a `String` and uses `ends_with`. The program compares the two on 500 random belts.
- Only the hashes are kept, not the letters, so memory is `O(n)` `u64`s.
- To be certain, keep the letters too and compare the last `k` of them when the hashes agree.
