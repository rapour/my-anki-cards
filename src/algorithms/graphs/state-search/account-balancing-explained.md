Explain the **Optimal Account Balancing** problem (the minimum number of transactions to settle a group's debts) and how backtracking with DFS solves it.

---

**The problem.** A group of friends have lent each other money, for example "Alice paid Bob 10" and "Carol paid Alice 5". You want to settle everything with as few payments as possible.

**Step 1: forget who owes whom, keep only net balances.** For each person add up everything they received and subtract everything they paid. A positive balance means the group owes that person money. A negative balance means that person owes the group. All balances add up to zero. People whose balance is zero are already settled, so drop them.

**Step 2: search.** Take the first person with a non-zero balance. Someone has to settle with them, and it only makes sense to pair them with a person of the **opposite sign**. Try each such person in turn:

1. Move the first person's whole balance onto that person (one payment). This leaves the first person settled.
2. Recursively settle the remaining balances. Count this payment plus whatever the recursion needs.
3. **Undo** the move, and try the next candidate.

The smallest total over all candidates is the answer. Because you try an option and then undo it, this is **backtracking**, which is DFS over a tree of choices rather than over a graph you were given.

**Two pruning tricks that make it fast enough:**

- If a candidate's balance is exactly the opposite of the first person's, the pair cancels perfectly. That is always at least as good as any other choice, so take it and stop trying others.
- Skip candidates that have the same balance as one you already tried at this step.

The search is exponential in the number of people with non-zero balances, which is fine because the inputs are small. (This is LeetCode 465.)
