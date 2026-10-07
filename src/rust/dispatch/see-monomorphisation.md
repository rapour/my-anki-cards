How can you check that the compiler made one copy of a generic function per type?

---

Build with optimisations and list the symbols in the binary:

```sh
cargo build --release
nm -C target/release/my_program | grep largest
```

```
0000000000014f60 t my_program::largest::<f64>
0000000000015020 t my_program::largest::<i32>
```

- Two types used, two copies.
- Put `#[inline(never)]` on the function. Otherwise the compiler may inline it and the copies disappear from the list.
- `cargo asm` shows the assembly of each copy.
