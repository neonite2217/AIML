# Engineering Decisions Log

This document records the key decisions made during the development of the Automated Data Cleaning project.

---

### Decision 1: Choice of Language (Rust)

*   **Problem:** We need to build a command-line tool for data processing. What language should we use?
*   **Options Considered:**
    1.  **Python with Pandas/Polars:** This is the most common choice for data work. It's easy to write and has a massive ecosystem. However, it can be slow for very large datasets and requires a Python interpreter to be installed on the user's machine.
    2.  **Go:** A compiled language known for simplicity and good concurrency support. Its data manipulation libraries are less mature than Python's.
    3.  **Rust:** A compiled language known for performance, memory safety, and a powerful type system. Its `polars` library is a modern, high-performance DataFrame library inspired by pandas.
*   **Final Choice:** **Rust**.
*   **Trade-offs:**
    *   **Pros:** Produces a single, fast, standalone binary that can be easily distributed. Rust's safety guarantees prevent entire classes of bugs. It's a great opportunity to learn a modern systems language.
    *   **Cons:** Rust has a steeper learning curve than Python, especially regarding its ownership and borrowing rules. The compilation process can be slower than scripting.

---

### Decision 2: Choice of DataFrame Library (Polars)

*   **Problem:** We need a robust and performant library for data manipulation in Rust.
*   **Options Considered:**
    1.  **Manual Implementation:** We could write our own data structures and functions to parse and manipulate CSV data. This would be incredibly time-consuming and error-prone.
    2.  **Polars:** A modern, extremely fast DataFrame library written in Rust. It leverages parallel processing and has an API that is familiar to users of Python's pandas/Polars.
    3.  **DataFusion:** Another powerful query engine, part of the Apache Arrow project. It's more focused on SQL-like queries and might be overkill for our simple cleaning tasks.
*   **Final Choice:** **Polars**.
*   **Trade-offs:**
    *   **Pros:** Blazing fast performance. The API is expressive and easy to use for those with prior DataFrame experience. It's written in Rust, so it integrates perfectly with our chosen language.
    *   **Cons:** Polars is a large dependency, which can increase compile times and the final binary size.

---

### Decision 3: Error Handling Strategy (`Result` and `?`)

*   **Problem:** Many of our operations (like reading a file or parsing a CSV) can fail. How should we handle these potential failures?
*   **Options Considered:**
    1.  **Panicking:** We could use `.unwrap()` or `.expect()` on our `Result` types. If an operation fails, the program will immediately crash (panic). This is easy to write but not robust.
    2.  **Explicit `match` statements:** We could write a `match` statement for every fallible operation to handle the `Ok` and `Err` cases. This is very verbose and can clutter the code.
    3.  **Using the `?` operator:** This operator provides a concise way to propagate errors. If a function returns a `Result`, using `?` after it will automatically return the `Err` value from the current function if the operation fails, or unwrap the `Ok` value if it succeeds. The function must have a `Result` return type to use this.
*   **Final Choice:** **Use the `?` operator**.
*   **Trade-offs:**
    *   **Pros:** Keeps the "happy path" code clean and readable, while still handling errors correctly. It's the idiomatic and recommended way to handle errors in Rust applications.
    *   **Cons:** Requires the function to return a `Result`, which adds a bit of ceremony to the function signature (`-> Result<(), PolarsError>`). It's a piece of syntactic sugar that can be slightly confusing for absolute beginners.
