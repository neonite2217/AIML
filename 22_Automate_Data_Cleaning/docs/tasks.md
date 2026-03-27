# Tasks — Data Cleaner

Task tracking for the Data Cleaner project using MoSCoW prioritization.

---

## Must Have (Critical for v0.1)

- [x] Create basic project structure with Cargo
- [x] Implement CSV reader using Polars CsvReader
- [x] Implement column name standardization (lowercase, underscores)
- [x] Implement duplicate row removal
- [x] Implement whitespace trimming for string columns
- [x] Implement CSV writer using Polars CsvWriter
- [x] Create sample data file (loan-recovery.csv)
- [x] Fix Rust borrowing/ownership compilation errors
- [x] Resolve Polars version compatibility issues
- [x] Ensure application runs without panics

## Should Have (Important for v0.2)

- [ ] Add command-line argument parsing (clap crate)
- [ ] Allow custom input/output file paths
- [ ] Add configuration file support (YAML/TOML)
- [ ] Refactor code into modular functions
- [ ] Implement unit tests (>70% coverage)
- [ ] Add integration tests
- [ ] Create setup scripts (setup.sh, setup.ps1)
- [ ] Add logging framework (env_logger)

## Could Have (Nice to have for v1.0)

- [ ] Implement streaming API for large files
- [ ] Add more cleaning operations:
  - [ ] Date normalization
  - [ ] Missing value handling (fill with mean/median)
  - [ ] Outlier detection
  - [ ] Type conversion
- [ ] Generate data profiling reports
- [ ] Support additional file formats (Parquet, JSON)
- [ ] Parallel processing for multiple files
- [ ] Progress bar for large files
- [ ] Dry-run mode (preview changes)

## Won't Have (this release)

- [ ] GUI interface
- [ ] Database connectivity
- [ ] Real-time/streaming data processing
- [ ] Machine learning integration
- [ ] Cloud storage integration (S3, GCS)
- [ ] REST API server mode
- [ ] Authentication/authorization
- [ ] Multi-user support

---

## Done (Completed Tasks)

- [x] **Initial project setup** — 2026-01-30
  - Created Cargo.toml with Polars dependency
  - Set up basic project structure

- [x] **Core data cleaning implementation** — 2026-01-30
  - Implemented column standardization
  - Implemented duplicate removal
  - Implemented whitespace trimming

- [x] **Fix compilation issues** — 2026-01-30
  - Resolved Polars v0.32.1 compatibility
  - Fixed borrowing/ownership errors

- [x] **Build and runtime verification** — 2026-01-30
  - Application compiles successfully
  - Application runs and produces correct output

- [x] **Create comprehensive documentation** — 2026-03-23
  - README.md with full setup instructions
  - SDLC documentation
  - Architecture documentation
  - Troubleshooting guide
  - Tech stack documentation

---

## In Progress

- [ ] Unit testing framework setup
- [ ] CI/CD pipeline configuration

## Blocked

None currently.

---

## Task Details

### TD-001: Command-line Arguments

**Description**: Allow users to specify input/output files via CLI
**Priority**: High
**Estimated Effort**: 2 hours
**Dependencies**: None
**Notes**: Use `clap` crate for argument parsing

### TD-002: Unit Tests

**Description**: Write unit tests for each cleaning function
**Priority**: High
**Estimated Effort**: 4 hours
**Dependencies**: Modular refactoring
**Notes**: Target >70% code coverage

### TD-003: Configuration File

**Description**: Support YAML/TOML config for cleaning rules
**Priority**: Medium
**Estimated Effort**: 3 hours
**Dependencies**: TD-001 (CLI args)
**Notes**: Allow enabling/disabling specific cleaning steps

### TD-004: Streaming API

**Description**: Use Polars streaming for large files
**Priority**: High
**Estimated Effort**: 4 hours
**Dependencies**: None
**Notes**: Critical for production use with large datasets

---

**Last Updated**: 2026-03-23
**Maintainer**: Project Team
