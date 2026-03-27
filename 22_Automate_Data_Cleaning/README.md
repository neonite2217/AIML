# Data Cleaner
> A high-performance command-line data cleaning tool built in Rust using the Polars DataFrame library.

## Tech Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Rust | 1.94.0 | Systems programming with memory safety |
| DataFrame Library | Polars | 0.32.1 | High-performance data manipulation |
| Build Tool | Cargo | 1.94.0 | Package management and compilation |
| Format | CSV | - | Input/Output data format |

## Prerequisites

Before building and running this project, ensure you have the following installed:

- **Rust** (version 1.60 or higher recommended)
  - Install via [rustup](https://rustup.rs/): `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- **Cargo** (comes bundled with Rust)
- **Git** (for cloning the repository)

### System Requirements

- Linux, macOS, or Windows (WSL recommended for Windows)
- At least 2GB RAM (for compilation)
- 500MB disk space

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Automate_Data_Cleaning
```

### Step 2: Verify Rust Installation

```bash
rustc --version  # Should show 1.60.0 or higher
cargo --version
```

If Rust is not installed, run:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
```

### Step 3: Build the Project

```bash
# Development build (unoptimized, includes debug info)
cargo build

# Release build (optimized for performance)
cargo build --release
```

The compiled binary will be located at:
- **Development**: `target/debug/data_cleaner`
- **Release**: `target/release/data_cleaner`

### Step 4: Run the Application

```bash
# Using cargo
cargo run

# Or run the compiled binary directly
./target/debug/data_cleaner
```

## Usage

### Basic Usage

The application automatically processes the `loan-recovery.csv` file and outputs `cleaned_loan_recovery.csv`:

```bash
cargo run
```

### Input Data Format

The application expects a CSV file with the following characteristics:

```csv
Loan_ID, Recovery_Amount, Last_Contact_Date
LP001,1000,2023-01-15
LP002, 2000, 2023-01-16
LP003,1500,
```

### Cleaning Operations Performed

1. **Column Name Standardization**: Converts to lowercase, removes whitespace, replaces spaces with underscores
   - `Loan_ID` → `loan_id`
   - ` Recovery_Amount` → `recovery_amount`

2. **Duplicate Removal**: Removes duplicate rows, keeping the first occurrence

3. **Whitespace Trimming**: Trims leading/trailing whitespace from string columns

### Output

The application will:
- Print the original and cleaned DataFrames to the console
- Create a new file `cleaned_loan_recovery.csv` with the cleaned data

### Example Output

```
Original DataFrame:
shape: (4, 3)
┌─────────┬──────────────────┬────────────────────┐
│ Loan_ID ┆  Recovery_Amount ┆  Last_Contact_Date │
│ ---     ┆ ---              ┆ ---                │
│ str     ┆ i64              ┆ str                │
╞═════════╪══════════════════╪════════════════════╡
│ LP001   ┆ 1000             ┆ 2023-01-15         │
│ LP002   ┆ 2000             ┆  2023-01-16        │
│ LP003   ┆ 1500             ┆                    │
│ LP001   ┆ 1000             ┆ 2023-01-15         │
└─────────┴──────────────────┴────────────────────┘

Cleaned DataFrame:
shape: (3, 3)
┌─────────┬─────────────────┬───────────────────┐
│ loan_id ┆ recovery_amount ┆ last_contact_date│
│ ---     ┆ ---             ┆ ---              │
│ str     ┆ i64             ┆ str              │
╞═════════╪═════════════════╪═══════════════════╡
│ LP002   ┆ 2000            ┆  2023-01-16      │
│ LP001   ┆ 1000            ┆ 2023-01-15       │
│ LP003   ┆ 1500            ┆                  │
└─────────┴─────────────────┴───────────────────┘
```

## Project Structure

```
Automate_Data_Cleaning/
├── Cargo.toml                    # Rust package configuration
├── Cargo.lock                    # Dependency lock file
├── README.md                     # This file
├── RULES.md                      # Agent operating rules
├── BUILD_LOG.md                  # Development log
├── ENGINEERING_DECISIONS.md       # Key engineering decisions
├── guide.txt                     # Detailed implementation guide
├── loan-recovery.csv             # Sample input data file
├── cleaned_loan_recovery.csv     # Generated output file
├── src/
│   └── main.rs                   # Main application source code
├── target/                       # Build artifacts (auto-generated)
│   └── debug/
│       └── data_cleaner          # Compiled binary
└── docs/                         # Documentation directory
    ├── agent_log.md              # Agent session log
    ├── architecture.md           # System architecture
    ├── CHANGELOG.md              # Version history
    ├── sdlc.md                   # SDLC tracking
    ├── tasks.md                  # Task backlog
    └── tech_stack.md             # Technology decisions
```

### File Descriptions

| File | Purpose |
|------|---------|
| `Cargo.toml` | Defines project metadata and dependencies |
| `src/main.rs` | Main source file containing the data cleaning pipeline |
| `loan-recovery.csv` | Sample messy data with duplicates and formatting issues |
| `BUILD_LOG.md` | Detailed build process and troubleshooting |
| `ENGINEERING_DECISIONS.md` | Rationale for technology choices |

## Architecture Overview

This project follows a simple **pipeline architecture** where data flows through sequential transformation steps:

```
[Input CSV]
    │
    ▼
[CSV Reader] → Polars DataFrame
    │
    ▼
[Cleaning Pipeline]
    ├─ Standardize column names
    ├─ Remove duplicates
    └─ Trim whitespace
    │
    ▼
[CSV Writer] → Output file
```

### Key Components

1. **Data Ingestion**: Uses Polars `CsvReader` to load CSV into memory
2. **Transformation Layer**: Applies cleaning functions using DataFrame operations
3. **Data Export**: Writes cleaned data back to CSV using `CsvWriter`

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Environment Variables

Currently, this project does not use environment variables. All configuration is handled through the source code.

## Running Tests

### Smoke Test

Verify the application builds and runs correctly:

```bash
# Build the project
cargo build

# Run the application
cargo run

# Verify output file exists
ls -la cleaned_loan_recovery.csv
```

### Manual Testing

Create custom test files to verify the cleaning operations:

```bash
# Create a test file
cat > test_input.csv << EOF
ID, Name, Value
1, " Alice ", 100
1, "Alice", 100
2, "  Bob", 200
EOF

# Modify src/main.rs to use test_input.csv temporarily
# Run and verify output
cargo run
```

## SDLC Status

**Current Phase**: Development (v0.1)

| Phase | Status | Notes |
|-------|--------|-------|
| Requirements | Completed | Core data cleaning requirements defined |
| Design | Completed | Pipeline architecture implemented |
| Development | Completed | v0.1 core functionality working |
| Testing | In Progress | Manual testing implemented |
| Deployment | Pending | Standalone binary distribution |
| Maintenance | Not Started | Future enhancements planned |

See [docs/sdlc.md](docs/sdlc.md) for full SDLC documentation.

## Troubleshooting

### Build Errors

#### Error: `cargo: command not found`

**Cause**: Rust/Cargo is not installed or not in PATH.

**Solution**:
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Source the environment
source "$HOME/.cargo/env"

# Verify installation
rustc --version
cargo --version
```

#### Error: `feature 'csv-file' not found` or Polars compilation errors

**Cause**: Incompatible Polars version.

**Solution**: The project uses Polars v0.32.1 which is stable. Do not modify the version in `Cargo.toml`.

#### Error: Borrowing/ownership errors

**Cause**: Rust's strict ownership system.

**Solution**: The codebase already handles this correctly. If modifying code, ensure you clone data structures when needed:
```rust
let old_columns: Vec<String> = df.get_column_names().iter().map(|s| s.to_string()).collect();
```

### Runtime Errors

#### Error: `No such file or directory` (loan-recovery.csv)

**Cause**: Running from wrong directory or file missing.

**Solution**:
```bash
# Ensure you're in the project root
cd Automate_Data_Cleaning

# Verify file exists
ls -la loan-recovery.csv

# If missing, the app will auto-generate it on first run
```

#### Error: Permission denied

**Cause**: Insufficient permissions to write output file.

**Solution**:
```bash
# Check permissions
ls -la .

# Fix if needed
chmod 755 .
```

### Performance Issues

#### Slow compilation

**Cause**: Polars is a large dependency.

**Solution**: 
- First compile takes ~1-2 minutes (normal)
- Subsequent compiles are fast (~1 second)
- Use `cargo build` instead of `cargo run` to just compile

#### Out of memory during build

**Cause**: Compilation requires significant RAM.

**Solution**: 
- Close other applications
- Use release mode for lower memory usage: `cargo build --release`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes following Rust style guidelines
4. Test thoroughly: `cargo run`
5. Commit with descriptive messages
6. Push and create a pull request

### Code Style

- Follow Rust naming conventions (snake_case for functions/variables)
- Use `cargo fmt` to auto-format code
- Use `cargo clippy` for linting
- Keep functions small and focused

## Future Enhancements

- [ ] Command-line argument parsing for input/output files
- [ ] Configuration file support (YAML/TOML)
- [ ] Additional cleaning operations (outlier detection, type conversion)
- [ ] Streaming API for large files
- [ ] Unit tests with >70% coverage
- [ ] Data profiling report generation
- [ ] Support for additional file formats (Parquet, JSON)

## License

This project is for educational purposes. See LICENSE file for details.

## Additional Resources

- [Rust Book](https://doc.rust-lang.org/book/)
- [Polars Documentation](https://docs.rs/polars/)
- [Cargo Guide](https://doc.rust-lang.org/cargo/)
- [BUILD_LOG.md](BUILD_LOG.md) - Detailed build process log
- [ENGINEERING_DECISIONS.md](ENGINEERING_DECISIONS.md) - Why Rust and Polars were chosen

---

**Last Updated**: 2026-03-23
**Version**: 0.1.0
**Maintainer**: Project Owner
