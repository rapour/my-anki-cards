Does Rust erase generic types the way Java does?

---

No.

- **Java:** one compiled copy of a generic method. The type parameter is erased, and values are handled as plain objects.
- **Rust generics:** monomorphised. There is a real copy for each type, and no type is forgotten.
- **Rust `dyn Trait`:** this is where Rust erases a type, and only because you asked for it.
