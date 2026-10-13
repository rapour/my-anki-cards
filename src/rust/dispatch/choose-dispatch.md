When do you use generics (static dispatch), and when `dyn Trait` (dynamic dispatch)?

---

| | Generics (`T: Trait`) | `dyn Trait` |
|---|---|---|
| Function chosen | at compile time | at run time |
| Speed | fastest, can inline | indirect call |
| Binary size | grows with each type | one copy |
| Different types in one `Vec` | no | yes |
| Type known only at run time | no | yes |

- Pick generics for hot code (code that runs very often) where the types are known.
- Pick `dyn` for collections of mixed types, plugins, and when you want a smaller binary or faster builds.

**Terms**

- *Static dispatch*: the compiler knows the concrete type and picks the method at compile time.
- *Dynamic dispatch*: the method is looked up at run time through a *vtable*, a table of function addresses.
- *Inline*: the compiler pastes a function's body into the caller, which lets it optimise further.
- *Indirect call*: the address to jump to is read from memory instead of being written into the code.
