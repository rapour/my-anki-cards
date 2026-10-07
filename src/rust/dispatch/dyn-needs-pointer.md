Why does `Vec<dyn Shape>` not compile, and what do you write instead?

---

`dyn Shape` has no fixed size: a `Circle` and a `Square` take different amounts of memory. A `Vec` stores its items directly, so it needs every item to have a known size. The compiler says: *the size for values of type `dyn Shape` cannot be known at compilation time*.

Put the value behind a pointer. A pointer has a known size (16 bytes for a fat pointer):

```rust
let owned: Vec<Box<dyn Shape>> = Vec::new();    // owned values on the heap
let borrowed: &dyn Shape = &Circle { r: 1.0 };  // a borrowed value
```
