`Circle` and `Square` both implement the trait `Shape`. A function must return a circle or a square, depending on a `bool`. Why does `-> impl Shape` fail, and what do you write instead?

---

`impl Shape` means *one* hidden concrete type, chosen at compile time (static dispatch: the compiler picks the method). The two branches return different types, so the compiler reports: *`if` and `else` have incompatible types*.

Return a trait object instead:

```rust
fn make(round: bool) -> Box<dyn Shape> {
    if round {
        Box::new(Circle { r: 1.0 })
    } else {
        Box::new(Square { s: 2.0 })
    }
}
```

- `-> impl Shape`: one type, no pointer, direct calls.
- `-> Box<dyn Shape>`: any type, one heap allocation, calls through the vtable.
