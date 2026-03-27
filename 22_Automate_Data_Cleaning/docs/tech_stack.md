# Tech Stack — Data Cleaner

## Overview

This document details the technology choices for the Data Cleaner project, including the rationale behind each decision.

---

## Core Technologies

### Programming Language: Rust

| Attribute | Value |
|-----------|-------|
| **Version** | 1.94.0 (stable) |
| **Source** | rustup |
| **Compilation Target** | Native binary (x86_64-unknown-linux-gnu) |

#### Why Rust?

**Decision**: Use Rust as the primary programming language.

**Rationale**:
1. **Performance**: Compiled to native code with zero-cost abstractions
2. **Memory Safety**: Ownership system prevents memory leaks and data races at compile time
3. **Type Safety**: Strong static typing catches errors before runtime
4. **Modern Tooling**: Cargo provides excellent package management and build system
5. **Learning Opportunity**: Demonstrates systems programming concepts

**Alternatives Considered**:
- **Python with Pandas**: Easier to write but slower and requires Python interpreter
- **Go**: Good for concurrency but less mature data processing libraries

**Trade-offs**:
- Pros: Speed, safety, standalone binaries, modern language features
- Cons: Steeper learning curve, stricter compiler, longer compilation times

**When to Re-evaluate**:
- If team lacks Rust expertise for maintenance
- If rapid prototyping is prioritized over performance

---

### DataFrame Library: Polars

| Attribute | Value |
|-----------|-------|
| **Version** | 0.32.1 |
| **Source** | crates.io |
| **Features Used** | lazy, csv, dtype-categorical |

#### Why Polars?

**Decision**: Use Polars for DataFrame operations.

**Rationale**:
1. **Performance**: Written in Rust, optimized for speed
2. **API Familiarity**: Similar to pandas for easier adoption
3. **Lazy Evaluation**: Query optimization through Lazy API
4. **Memory Efficient**: Apache Arrow backend
5. **Active Development**: Modern, actively maintained library

**Alternatives Considered**:
- **Manual Implementation**: Too time-consuming and error-prone
- **DataFusion**: More focused on SQL queries, overkill for simple cleaning

**Trade-offs**:
- Pros: Blazing fast, expressive API, perfect Rust integration
- Cons: Large dependency, increases compile time and binary size

**Version Selection**:
- Started with v0.34.2 — encountered compilation errors
- Tested v0.52.0 — polars-expr compilation issues
- Tested v0.41.3 — HashMap method compatibility issues
- **Final**: v0.32.1 — Most stable version without errors

**When to Upgrade**:
- Monitor for v0.33+ with confirmed stability
- Test thoroughly before upgrading in production

---

### Build Tool: Cargo

| Attribute | Value |
|-----------|-------|
| **Version** | 1.94.0 |
| **Source** | Bundled with Rust |

#### Why Cargo?

**Decision**: Use Cargo as the build tool and package manager.

**Rationale**:
1. **Standard Tool**: Official Rust build system
2. **Dependency Management**: Automatic crate downloads from crates.io
3. **Build Profiles**: Debug and release configurations
4. **Workspace Support**: Multi-crate projects
5. **Integration**: Works with rustfmt, clippy, and other tools

**Key Commands**:
```bash
cargo build          # Development build
cargo build --release  # Optimized release build
cargo run            # Build and run
cargo test           # Run tests
cargo check          # Fast syntax/type check
cargo fmt            # Auto-format code
cargo clippy         # Run linter
```

---

### Data Format: CSV

| Attribute | Value |
|-----------|-------|
| **Format** | Comma-separated values |
| **Encoding** | UTF-8 |
| **Line Endings** | Unix (LF) |

#### Why CSV?

**Decision**: Use CSV as the input/output format.

**Rationale**:
1. **Universal**: Supported by virtually all data tools
2. **Human Readable**: Easy to inspect and debug
3. **Simple**: No complex parsing requirements
4. **Polars Support**: Native CSV support in Polars

**Limitations**:
- No type information (everything is string initially)
- No compression (larger file sizes)
- No schema enforcement

**Future Considerations**:
- Parquet for compressed columnar storage
- JSON for nested data structures

---

## Development Tools

### Required Tools

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| rustc | 1.94.0 | Rust compiler | rustup |
| cargo | 1.94.0 | Build tool | rustup |
| rustfmt | latest | Code formatting | rustup component |
| clippy | latest | Linting | rustup component |

### Optional Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| cargo-edit | Dependency management | Adding crates to Cargo.toml |
| cargo-watch | Auto-rebuild on changes | Development workflow |
| cargo-expand | Macro expansion | Debugging macros |

---

## Dependencies

### Direct Dependencies

| Crate | Version | Features | Purpose |
|-------|---------|----------|---------|
| polars | 0.32.1 | lazy, csv, dtype-categorical | DataFrame operations |

### Transitive Dependencies (Selected)

| Crate | Purpose |
|-------|---------|
| arrow2 | Apache Arrow implementation |
| chrono | Date/time handling |
| rayon | Data parallelism |
| serde | Serialization framework |
| tokio | Async runtime (via Polars) |

### Dependency Tree Size

- **Direct**: 1 crate
- **Total**: ~120 crates (including transitive)
- **Compile Time**: ~1-2 minutes (clean), <1 second (incremental)

---

## Environment

### Development Environment

| Component | Requirement |
|-----------|-------------|
| OS | Linux (primary), macOS, Windows WSL |
| Shell | bash, zsh |
| Terminal | Any |
| IDE | VS Code with rust-analyzer, IntelliJ with Rust plugin |

### Build Environment

| Component | Value |
|-----------|-------|
| Target | x86_64-unknown-linux-gnu |
| Profile | dev (debug) / release (optimized) |
| Optimization | Level 3 (release) |
| LTO | Disabled (dev), Thin (release) |

---

## Architecture Patterns

### Design Patterns Used

1. **Pipeline Pattern**: Linear data transformation flow
2. **Result Type**: Error handling through Rust's Result
3. **Builder Pattern**: CsvReader configuration
4. **Iterator Pattern**: Column name transformations

### Memory Management

- **Ownership**: Rust's compile-time ownership tracking
- **Borrowing**: Immutable borrows for reading, mutable for writing
- **Cloning**: Explicit cloning where needed (column names)
- **No GC**: Deterministic memory management

### Concurrency

- **Current**: Single-threaded
- **Polars**: Automatic parallelism for DataFrame operations
- **Future**: Consider rayon for explicit parallelization

---

## Performance Characteristics

### Compilation

| Metric | Debug | Release |
|--------|-------|---------|
| Time | ~1-2 min | ~2-3 min |
| Binary Size | ~50MB | ~5MB |
| Optimizations | None | Full |
| Debug Info | Full | None |

### Runtime

| Metric | Expected |
|--------|----------|
| Startup | <100ms |
| Memory Usage | ~2-3x input file size |
| Processing | O(n) for n rows |
| I/O | Disk-bound for large files |

---

## Security Considerations

### Dependencies

- No network-dependent crates in runtime
- All dependencies from official crates.io
- Regular security audits: `cargo audit`

### Input Handling

- CSV parsing handled by Polars (validated)
- Path traversal prevented (no .. in paths)
- No execution of untrusted data

### Output

- Non-destructive (creates new file)
- No temporary files left behind
- Proper file permissions respected

---

## Migration Path

### Upgrading Polars

1. Check CHANGELOG for breaking changes
2. Update version in Cargo.toml
3. Run `cargo update`
4. Fix compilation errors
5. Run full test suite
6. Update documentation

### Future Technology Evaluations

| Technology | Evaluation Criteria | Timeline |
|------------|---------------------|----------|
| Polars v1.0 | Stability, performance | Monitor |
| Arrow2 v0.18 | Memory efficiency | As needed |
| Clap v4 | CLI parsing | v0.2 |
| Serde YAML | Config files | v0.2 |

---

## References

- [Rust Book](https://doc.rust-lang.org/book/)
- [Polars Documentation](https://docs.rs/polars/)
- [Cargo Guide](https://doc.rust-lang.org/cargo/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Polars User Guide](https://pola-rs.github.io/polars-book/)

---

**Last Updated**: 2026-03-23
**Version**: 1.0
**Maintainer**: Project Team
