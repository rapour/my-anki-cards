In the Radar Rule Evaluator problem you must decide whether a rule such as `amount>500ANDamount<2000` allows a payment. How is this a tree problem, and where does DFS come in?

---

A rule is a small formula, and a formula has a natural **tree shape**. Each leaf is a single comparison (`amount>500`), and each inner node combines the answers of its children with AND or OR.

For the rule `country==US OR amount>500 AND amount<2000` the tree looks like this:

```
          OR
        /    \
country==US   AND
             /   \
     amount>500   amount<2000
```

AND binds more tightly than OR, in the same way that multiplication binds more tightly than addition. So the AND is grouped first, and the OR sits at the top.

**Evaluating the tree is a DFS.** To get the answer for a node you first need the answers of its children, so you go *down* to the leaves, work out each comparison, and then pass the results back *up*: an OR node is true if any child is true, and an AND node is true only if all children are true. Doing the children first and the parent afterwards is called a **post-order** traversal.

**Short-circuiting.** As soon as an OR has one true child, or an AND has one false child, you can stop looking at the rest. This saves work, and it is built into Rust's `any` and `all`.

**Building the tree.** Split the text on `OR` first, because OR has the lowest precedence and so ends up at the top. Then split each piece on `AND`. Then each remaining piece is a comparison, which you split at its operator (`>=`, `<=`, `==`, `!=`, `>`, `<`). Try the two-character operators before `>` and `<`, otherwise `>=` would be misread as `>` followed by `=`.

Many solutions skip building the tree and just split and evaluate in one pass. That is the same DFS, done implicitly through nested loops.
