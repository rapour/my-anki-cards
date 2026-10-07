Which of these functions use static dispatch, and which use dynamic dispatch?

```rust
fn a(shape: &impl Shape) -> f64 { shape.area() }
fn b<T: Shape>(shape: &T) -> f64 { shape.area() }
fn c(shape: &dyn Shape) -> f64 { shape.area() }
```

---

`a` and `b` use **static** dispatch. `c` uses **dynamic** dispatch.

- `impl Shape` in an argument is shorthand for a generic like `b`'s `T: Shape`.
- Only `c` has a type the compiler does not know: `dyn Shape` stands for "some type that implements `Shape`".
