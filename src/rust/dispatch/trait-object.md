What is a trait object?

---

A value of type `dyn Trait` that you use through a pointer, such as `&dyn Shape` or `Box<dyn Shape>`. The compiler no longer knows the concrete type. It only knows that the type implements `Shape`.

```rust
let a: &dyn Shape = &Circle { r: 1.0 };
let b: Box<dyn Shape> = Box::new(Square { s: 2.0 });
```

Calls on a trait object use dynamic dispatch.
