When do you use generics (static dispatch), and when `dyn Trait` (dynamic dispatch)?

---

| | Generics (`T: Trait`) | `dyn Trait` |
|---|---|---|
| Function chosen | at compile time | at run time |
| Speed | fastest, can inline | indirect call |
| Binary size | grows with each type | one copy |
| Different types in one `Vec` | no | yes |
| Type known only at run time | no | yes |

- Pick generics for hot code where the types are known.
- Pick `dyn` for collections of mixed types, plugins, and when you want a smaller binary or faster builds.
