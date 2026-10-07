`Circle` and `Square` both implement `trait Shape { fn area(&self) -> f64; }`. How do you keep one of each in the same `Vec` and add up their areas?

---

```rust
let shapes: Vec<Box<dyn Shape>> = vec![
    Box::new(Circle { r: 1.0 }),
    Box::new(Square { s: 2.0 }),
];
let total: f64 = shapes.iter().map(|s| s.area()).sum();
```

- Each item is a `Box<dyn Shape>`: a pointer to the value on the heap plus a vtable pointer.
- Each `area()` call goes through the vtable, so it runs the right method for each type.
- With generics (`Vec<T>`) all items would have to be the same type.
