Does Rust erase generic types the way Java does?

---

No. *Type erasure* means forgetting a value's concrete type at compile time.

- **Java:** one compiled copy of a generic method. The type parameter is erased, and values are handled as plain objects.
- **Rust generics:** *monomorphised*: the compiler makes a separate copy of the generic code for each concrete type, so no type is forgotten.
- **Rust `dyn Trait`:** this is where Rust erases a type, and only because you asked for it.
