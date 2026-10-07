Why does `Box<dyn Clone>` not compile?

---

`Clone` is not **dyn compatible**, so the compiler cannot build a vtable for it. The error says: *the trait `Clone` is not dyn compatible*. (Older Rust called this *object safe*.)

`clone(&self) -> Self` returns `Self`. Once the type is erased, the caller has no idea how big `Self` is, so it cannot make room for the result.

Three things stop a trait from being dyn compatible:

- A method that returns `Self`.
- A method with its own generic type parameter.
- A method with no `self` argument.

You can opt a method out with `where Self: Sized`. The trait can then be used as `dyn`, but that method cannot be called on a trait object:

```rust
trait Make {
    fn make() -> Self where Self: Sized;
    fn name(&self) -> String;
}
```
