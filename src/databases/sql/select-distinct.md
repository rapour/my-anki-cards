What does `SELECT DISTINCT` do?

---

Removes duplicate rows from the result set. Two rows are duplicates when every selected column is equal.

```sql
SELECT DISTINCT country FROM customers;
```
