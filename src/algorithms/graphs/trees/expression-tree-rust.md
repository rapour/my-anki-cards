A rule is text such as `amount>500ANDamount<2000`, using `AND`, `OR` and the operators `> < >= <= == !=`, and a payment is a set of named values. Write a Rust evaluator that builds an *expression tree* from the rule and evaluates it with DFS.

---

`Expr` is the expression tree: its leaves are single comparisons, and its inner nodes are `AND` or `OR`. `parse` splits on `OR`, then `AND`, then at the comparison operator, and trims any spaces. `evaluate` is the post-order DFS (children first, then the parent): it calls itself on the children and combines their answers. A comparison on two numbers is done numerically, otherwise as text (where only `==` and `!=` make sense). A field missing from the payment makes its comparison false.

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
                field: field.trim().to_string(),
                op: op.to_string(),
                value: value.trim().to_string(),
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

    // spaces around the keywords and operators make no difference
    let spaced = parse("country==US OR amount > 500 AND amount < 2000");
    assert!(evaluate(&spaced, &us_small));
    assert!(!evaluate(&spaced, &uk_small));
    println!("rule evaluator works");
}
```

Caution: splitting on the raw letters `OR` or `AND` would cut a field name such as `ORDER_ID` in half. A robust parser first splits the text into tokens (words and symbols). Splitting on the keywords is fine when the input format is fixed and field names cannot contain them.
