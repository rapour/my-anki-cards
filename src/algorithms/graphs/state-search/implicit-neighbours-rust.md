Credit Card Redaction part 4 asks you to recover the original card number when a single digit has been corrupted. How is that a "graph search over states", and what does a Rust implementation look like?

---

Sometimes the graph is never written down. Instead, you have a way to **generate the neighbours of any state on demand**. Such a graph is called *implicit*.

Here each possible card number is a **state**, and two states are neighbours if they differ in exactly one digit. You never build the whole graph (there are far too many card numbers). You just ask "what are all the one-digit changes of this number?", which is a function that produces neighbours.

Searching one step away from the damaged number is **a single layer of BFS**. You look at every neighbour, and keep only those that pass the validity rules:

- the **Luhn checksum** (a formula every genuine card number satisfies), and
- the **brand prefix** (a Visa number starts with 4).

If more than one candidate survives, the problem's extra rules decide between them. Luhn catches every single-digit error, but it usually leaves several digit positions that could be "repaired", which is why the extra filters matter.

This is a looser fit for BFS and DFS than the other cards. Use it for the idea that a graph can be explored without ever being stored.

```rust
fn luhn_valid(number: &str) -> bool {
    let mut sum = 0;
    for (i, ch) in number.chars().rev().enumerate() {
        let Some(mut digit) = ch.to_digit(10) else {
            return false;
        };
        if i % 2 == 1 {
            digit *= 2; // double every second digit from the right
            if digit > 9 {
                digit -= 9;
            }
        }
        sum += digit;
    }
    sum % 10 == 0
}

/// Every number one digit away from `number` that is a valid card with the given prefix.
fn single_digit_repairs(number: &str, prefix: &str) -> Vec<String> {
    let digits: Vec<char> = number.chars().collect();
    let mut repairs = Vec::new();

    for position in 0..digits.len() {
        for replacement in '0'..='9' {
            if replacement == digits[position] {
                continue; // that is the number we started with
            }
            let mut candidate = digits.clone();
            candidate[position] = replacement; // generate one neighbour
            let candidate: String = candidate.into_iter().collect();
            if candidate.starts_with(prefix) && luhn_valid(&candidate) {
                repairs.push(candidate);
            }
        }
    }
    repairs
}

fn main() {
    assert!(luhn_valid("4111111111111111")); // a standard Visa test number

    // the 12th digit was damaged: 1 became 2
    let damaged = "4111111111121111";
    let repairs = single_digit_repairs(damaged, "4");
    assert!(repairs.contains(&"4111111111111111".to_string()));
    println!("{} candidates: {repairs:?}", repairs.len());
}
```
