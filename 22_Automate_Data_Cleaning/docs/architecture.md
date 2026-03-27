# Architecture — Data Cleaner

## System Overview

The Data Cleaner is a command-line application built in Rust that automates common data cleaning tasks on CSV files. It uses the Polars DataFrame library to provide high-performance data manipulation. The system follows a simple pipeline architecture where data flows through sequential transformation steps.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Data Cleaner Application                │
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Input      │───▶│   Cleaning   │───▶│    Output    │   │
│  │   Reader     │    │   Pipeline   │    │   Writer     │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│         │                   │                   │             │
│         ▼                   ▼                   ▼             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │  CSV File    │    │ Transformers │    │ Cleaned CSV  │   │
│  │  (Disk)      │    │              │    │  (Disk)      │   │
│  └──────────────┘    │ • Standardize│    └──────────────┘   │
│                      │ • Deduplicate│                         │
│                      │ • Trim       │                         │
│                      └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        DATA FLOW                             │
└─────────────────────────────────────────────────────────────┘

    [loan-recovery.csv]
           │
           │ 1. Read
           ▼
    ┌──────────────┐
    │ CsvReader    │
    │ Polars       │
    └──────────────┘
           │
           │ 2. Parse
           ▼
    ┌──────────────┐
    │ DataFrame    │
    │ (In-Memory)  │
    └──────────────┘
           │
           │ 3. Transform
           ▼
    ┌──────────────────────────────────┐
    │      Cleaning Pipeline         │
    │  ┌──────────────────────────┐  │
    │  │ standardize_column_names │  │
    │  │  • lowercase             │  │
    │  │  • trim whitespace       │  │
    │  │  • replace spaces        │  │
    │  └──────────────────────────┘  │
    │               │                 │
    │  ┌──────────────────────────┐  │
    │  │ drop_duplicates          │  │
    │  │  • keep first occurrence │  │
    │  └──────────────────────────┘  │
    │               │                 │
    │  ┌──────────────────────────┐  │
    │  │ trim_whitespace          │  │
    │  │  • Lazy API              │  │
    │  │  • string operations     │  │
    │  └──────────────────────────┘  │
    └──────────────────────────────────┘
           │
           │ 4. Output
           ▼
    ┌──────────────┐
    │ CsvWriter    │
    │ Polars       │
    └──────────────┘
           │
           │ 5. Write
           ▼
    [cleaned_loan_recovery.csv]
```

## Key Design Decisions

### 1. Pipeline Architecture

**Decision**: Use a linear data transformation pipeline.

**Rationale**:
- Simple to understand and debug
- Each step is independent and testable
- Natural fit for data processing tasks
- Easy to extend with additional cleaning operations

**Trade-offs**:
- Pros: Clarity, maintainability, ease of testing
- Cons: Entire dataset must fit in memory (addressed in future with streaming API)

### 2. In-Memory Processing

**Decision**: Load entire CSV into memory as a DataFrame.

**Rationale**:
- Polars is optimized for in-memory operations
- Fast random access for transformations
- Simpler implementation for v0.1

**Trade-offs**:
- Pros: High performance, simple code
- Cons: Memory limitations for very large files

**Future Consideration**: For files > available RAM, implement streaming API using `scan_csv` instead of `read_csv`.

### 3. Error Handling with `Result` and `?`

**Decision**: Use Rust's `Result` type with `?` operator for error propagation.

**Rationale**:
- Idiomatic Rust error handling
- Clean error propagation without nested match statements
- Type-safe error handling at compile time

**Implementation**:
```rust
fn main() -> Result<(), PolarsError> {
    let df = CsvReader::from_path("file.csv")?.finish()?;
    // Errors automatically propagated
    Ok(())
}
```

### 4. Polars Lazy API for Transformations

**Decision**: Use Polars Lazy API for string operations.

**Rationale**:
- Better performance through query optimization
- Reduced memory allocation
- Polars can parallelize operations

**Example**:
```rust
df = df.lazy().with_column(col("loan_id").str().strip(None)).collect()?;
```

## External Dependencies

| Dependency | Version | Purpose | Source |
|------------|---------|---------|--------|
| polars | 0.32.1 | DataFrame operations | crates.io |
| Rust Standard Library | 1.94.0 | File I/O, path handling | Built-in |

### Polars Features Used

- `lazy` - Lazy evaluation for performance
- `csv` - CSV reading and writing
- `dtype-categorical` - Categorical data types

## Module Structure

```
src/
└── main.rs
    ├── Imports
    │   ├── polars::prelude::*    # DataFrame operations
    │   └── std::fs::File         # File I/O
    │
    ├── create_dummy_data()        # Helper: Generate test data
    │   └── Creates loan-recovery.csv if missing
    │
    └── main()                     # Application entry point
        ├── Load CSV              # CsvReader::from_path()
        ├── Print original        # println!()
        ├── Standardize names     # Iterator transformations
        ├── Remove duplicates     # DataFrame::unique()
        ├── Trim whitespace       # Lazy API with_column()
        ├── Print cleaned         # println!()
        └── Write output          # CsvWriter
```

## Entry Points

| Function | Purpose | Location |
|----------|---------|----------|
| `main` | Application entry point | `src/main.rs:19` |
| `create_dummy_data` | Generate test data if missing | `src/main.rs:6` |

## Data Structures

### Core Types

- `DataFrame` - Polars DataFrame (in-memory tabular data)
- `LazyFrame` - Polars lazy representation (query plan)
- `PolarsError` - Error type for Polars operations
- `UniqueKeepStrategy` - Enum for deduplication strategy

### Column Types Supported

- `Utf8` (String)
- `Int64` (Integer)
- Other types supported by Polars

## Performance Considerations

### Current Implementation

- **Time Complexity**: O(n) for most operations where n = number of rows
- **Space Complexity**: O(n) - entire dataset in memory
- **Compile Time**: ~1-2 minutes for initial build, ~1 second for incremental

### Optimization Strategies

1. **Polars Lazy API**: Used for string operations
2. **Iterator chains**: Efficient column name transformations
3. **Zero-copy operations**: Where possible, Polars avoids copying data

### Scalability Limits

| Resource | Current Limit | Mitigation Strategy |
|----------|---------------|---------------------|
| Memory | Available RAM | Streaming API in v1.0 |
| File Size | ~50% of RAM | Chunked processing |
| Compilation | ~2 minutes | Incremental builds |

## Security Considerations

- **No network access** - Purely local file processing
- **No secrets** - No API keys or credentials required
- **Input validation** - Polars handles CSV parsing safely
- **Output sanitization** - Clean data written to new file (non-destructive)

## Monitoring Points

For production deployment, monitor:

1. **Memory usage** - Peak heap consumption
2. **Processing time** - Total execution duration
3. **I/O throughput** - Read/write operations per second
4. **Error rates** - Failed parsing or write operations

## Extension Points

Future enhancements can be added as pipeline stages:

```rust
// Current pipeline
df = standardize_column_names(df)?;
df = drop_duplicates(df)?;
df = trim_whitespace(df)?;

// Potential additions
df = handle_missing_values(df)?;
df = detect_outliers(df)?;
df = normalize_dates(df)?;
df = type_conversion(df)?;
```

---

**Last Updated**: 2026-03-23
**Version**: 0.1.0
**Author**: Project Team
