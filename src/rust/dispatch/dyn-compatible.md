Why does `Box<dyn Clone>` not compile?

---

A trait can only be used as `dyn Trait` if it is **dyn compatible**, which means the compiler can build a *vtable* (a table of function addresses) for it. `Clone` is not dyn compatible. The error says: *the trait `Clone` is not dyn compatible*. (Older Rust called this *object safe*.)

`clone(&self) -> Self` returns `Self`, the concrete type. Behind a `dyn`, the concrete type is forgotten (*erased*), so the caller has no idea how big `Self` is and cannot make room for the result.

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
