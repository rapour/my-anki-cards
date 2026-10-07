What do you gain from monomorphisation?

---

Speed. Each copy knows its exact type, so:

- The call is direct, with no lookup.
- The compiler can **inline** the function (paste its body into the caller) and optimise it for that one type, for example by using SIMD instructions for `f32`.

This is why Rust calls generics a *zero-cost abstraction*: the generic version runs as fast as code you wrote by hand for each type.
