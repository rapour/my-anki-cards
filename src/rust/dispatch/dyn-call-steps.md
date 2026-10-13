`Shape` is a trait with an `area` method. What happens at run time when you call `shape.area()` and `shape` is a `&dyn Shape` (a reference to any value that implements `Shape`)?

---

A `&dyn Shape` is a *fat pointer*: two pointers, one to the value (the **data pointer**) and one to its *vtable*, a table of function addresses for the value's type.

1. Read the **vtable pointer** from the fat pointer.
2. Load the address of `area` from the vtable.
3. Call that address, passing the **data pointer** as `self`.

That is an *indirect call*: the address to jump to is read from memory, not written into the code.
