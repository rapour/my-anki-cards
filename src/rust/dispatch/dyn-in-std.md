Which three trait objects do you meet most often in the standard library?

---

- `Box<dyn std::error::Error>`: any error type. It is what `?` converts errors into when a function returns `Result<T, Box<dyn Error>>`.
- `&mut dyn std::io::Write`: any writer, such as a file, stdout or a `Vec<u8>`.
- `Box<dyn Fn(i32) -> i32>`: any closure with that signature.
