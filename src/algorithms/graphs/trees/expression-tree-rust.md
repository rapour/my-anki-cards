Write a Rust evaluator for rules like `amount>500ANDamount<2000`, with `AND`, `OR` and the operators `> < >= <= == !=`. Build an expression tree and evaluate it with DFS.

---

`Expr` is the tree. `parse` splits on `OR`, then `AND`, then at the comparison operator. `evaluate` is the post-order DFS: it calls itself on the children and combines their answers. A comparison on two numbers is done numerically, otherwise as text (where only `==` and `!=` make sense). A field missing from the payment makes its comparison false.

```rust
use std::collections::HashMap;

enum Expr {
    Compare { field: String, op: String, value: String },
    And(Vec<Expr>),
    Or(Vec<Expr>),
}

fn parse(rule: &str) -> Expr {
    // OR has the lowest precedence, so it sits at the top of the tree
    Expr::Or(rule.split("OR").map(parse_and).collect())
}

fn parse_and(part: &str) -> Expr {
    Expr::And(part.split("AND").map(parse_compare).collect())
}

fn parse_compare(text: &str) -> Expr {
    // two-character operators first, or ">=" would be read as ">"
    for op in [">=", "<=", "==", "!=", ">", "<"] {
        if let Some((field, value)) = text.split_once(op) {
            return Expr::Compare {
                field: field.to_string(),
                op: op.to_string(),
                value: value.to_string(),
            };
        }
    }
    panic!("no comparison operator in {text:?}");
}

fn evaluate(expr: &Expr, payment: &HashMap<&str, &str>) -> bool {
    match expr {
        // any() and all() stop early: short-circuiting
        Expr::Or(parts) => parts.iter().any(|part| evaluate(part, payment)),
        Expr::And(parts) => parts.iter().all(|part| evaluate(part, payment)),
        Expr::Compare { field, op, value } => {
            let Some(actual) = payment.get(field.as_str()) else {
                return false; // the payment has no such field
            };
            match (actual.parse::<i64>(), value.parse::<i64>()) {
                (Ok(a), Ok(b)) => match op.as_str() {
                    ">" => a > b,
                    "<" => a < b,
                    ">=" => a >= b,
                    "<=" => a <= b,
                    "==" => a == b,
                    "!=" => a != b,
                    _ => false,
                },
                _ => match op.as_str() {
                    "==" => *actual == value.as_str(),
                    "!=" => *actual != value.as_str(),
                    _ => false, // ordering text makes no sense here
                },
            }
        }
    }
}

fn main() {
    let rule = parse("amount>500ANDamount<2000");
    let small = HashMap::from([("amount", "250")]);
    let medium = HashMap::from([("amount", "1000")]);
    assert!(!evaluate(&rule, &small));
    assert!(evaluate(&rule, &medium));

    // AND binds tighter than OR: country==US OR (amount>500 AND amount<2000)
    let rule = parse("country==USORamount>500ANDamount<2000");
    let us_small = HashMap::from([("country", "US"), ("amount", "5")]);
    let uk_small = HashMap::from([("country", "UK"), ("amount", "5")]);
    assert!(evaluate(&rule, &us_small));
    assert!(!evaluate(&rule, &uk_small));
    println!("rule evaluator works");
}
```

Caution: splitting on the raw letters `OR` or `AND` would cut a field name such as `ORDER_ID` in half. A production parser first splits the text into tokens. For an interview with the exact input format given, splitting on the keywords is usually accepted.
