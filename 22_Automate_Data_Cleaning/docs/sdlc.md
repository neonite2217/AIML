# SDLC — Data Cleaner

## Software Development Life Cycle Tracking

This document tracks the progress of the Data Cleaner project through all phases of the SDLC.

---

## 1. Requirements

### 1.1 Functional Requirements

- [x] **FR-001**: Read CSV files from disk
  - Input: CSV file path
  - Output: In-memory DataFrame representation

- [x] **FR-002**: Standardize column names
  - Convert to lowercase
  - Replace spaces with underscores
  - Trim whitespace

- [x] **FR-003**: Remove duplicate rows
  - Keep first occurrence
  - Discard subsequent duplicates

- [x] **FR-004**: Trim whitespace from string values
  - Remove leading/trailing whitespace
  - Apply to specified columns

- [x] **FR-005**: Write cleaned data to CSV
  - Output: New CSV file with transformations applied
  - Preserve data integrity

### 1.2 Non-Functional Requirements

- [x] **NFR-001**: Performance
  - Process files with up to 10,000 rows in under 5 seconds
  - Memory efficient for typical use cases

- [x] **NFR-002**: Reliability
  - Handle missing input file gracefully
  - No data loss during transformation

- [x] **NFR-003**: Usability
  - Single command execution (`cargo run`)
  - Clear console output showing transformations

- [x] **NFR-004**: Maintainability
  - Clean, modular code structure
  - Well-documented functions

### 1.3 User Personas

**Primary User**: Data Analyst
- Needs quick data cleaning for analysis
- Familiar with command-line tools
- Values performance and reliability

**Secondary User**: Developer
- Extends the tool with custom cleaning operations
- Needs well-structured, documented codebase

---

## 2. Design

### 2.1 Architecture Design

- [x] **ADR-001**: Pipeline Architecture Selected
  - Linear data flow from input to output
  - Each transformation as a discrete step
  - Easy to extend and debug

### 2.2 Tech Stack Finalization

- [x] **Language**: Rust (v1.94.0)
- [x] **DataFrame Library**: Polars (v0.32.1)
- [x] **Build Tool**: Cargo
- [x] **Data Format**: CSV

### 2.3 Component Design

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ CSV Reader  │───▶│ Transform   │───▶│ CSV Writer  │
└─────────────┘    │ Pipeline    │    └─────────────┘
                   └─────────────┘
```

- [x] Input component: `CsvReader`
- [x] Processing component: Transformation functions
- [x] Output component: `CsvWriter`

### 2.4 Data Flow Design

- [x] Data ingestion: File → DataFrame
- [x] Transformation: In-place modifications with clones where needed
- [x] Data export: DataFrame → File

---

## 3. Development

### 3.1 Coding Standards

- [x] Follow Rust naming conventions (snake_case)
- [x] Use idiomatic error handling (`Result` + `?`)
- [x] Document public functions
- [x] No `unwrap()` in production paths (handled via `?`)

### 3.2 Feature Branches

- [x] Main branch contains working v0.1
- [x] No feature branches for v0.1 (single developer)
- [ ] Future: Use feature branches for v0.2 and beyond

### 3.3 Code Review

- [x] Self-review completed
- [ ] Peer review pending (for team development)

---

## 4. Testing

### 4.1 Unit Tests

- [ ] Test `standardize_column_names` function
- [ ] Test `drop_duplicates` function
- [ ] Test `trim_whitespace` function
- [ ] **Coverage Target**: >70%

### 4.2 Integration Tests

- [x] **Smoke Test**: Application builds and runs
- [x] **End-to-End**: Input CSV → Cleaned CSV
- [ ] Test with various CSV formats
- [ ] Test error handling (missing files, malformed data)

### 4.3 Manual Testing

- [x] Test case 1: Standard CSV with duplicates
- [x] Test case 2: CSV with whitespace issues
- [x] Test case 3: Edge case - empty file handling

#### Manual Test Results

| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| Standard | loan-recovery.csv (4 rows, 1 duplicate) | 3 rows, no duplicates | ✅ PASS |
| Whitespace | Columns with spaces, values with padding | Clean column names, trimmed values | ✅ PASS |
| Missing file | Non-existent file | Auto-generates test data | ✅ PASS |

### 4.4 Edge Cases

- [x] Empty CSV files
- [x] CSV with only headers
- [x] All duplicate rows
- [x] No duplicates
- [x] Large whitespace variations

---

## 5. Deployment

### 5.1 Environment Variables

- [x] Not applicable for v0.1 (no env vars required)
- [ ] Future: Add configuration via env vars for v1.0

### 5.2 Deployment Guide

#### Local Development Deployment

```bash
# 1. Clone repository
git clone <repository-url>
cd Automate_Data_Cleaning

# 2. Install Rust (if not present)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

# 3. Build
cargo build --release

# 4. Run
./target/release/data_cleaner
```

#### Binary Distribution

- [ ] Create release binaries for Linux
- [ ] Create release binaries for macOS
- [ ] Create release binaries for Windows
- [ ] Package with sample data files

### 5.3 Rollback Plan

- **Method**: Git version control
- **Command**: `git checkout v0.1.0` to rollback
- **Backup**: Each commit is a potential rollback point

### 5.4 CI/CD Pipeline

- [ ] Set up GitHub Actions for automated builds
- [ ] Run tests on pull requests
- [ ] Build release artifacts on tags
- [ ] Code quality checks (clippy, fmt)

---

## 6. Maintenance

### 6.1 Changelog

- [x] CHANGELOG.md created
- [ ] Keep updated with each release

### 6.2 Known Issues

| Issue | Priority | Status | Notes |
|-------|----------|--------|-------|
| Memory usage scales with file size | Medium | Open | Will address with streaming API |
| Hardcoded column name for trim | Low | Open | Will make configurable |
| No command-line arguments | Medium | Open | Planned for v0.2 |

### 6.3 Agent Log

- [x] docs/agent_log.md created
- [ ] Log all development sessions

### 6.4 Future Enhancements

| Feature | Priority | Target Version |
|---------|----------|----------------|
| Command-line argument parsing | High | v0.2 |
| Config file support | High | v0.2 |
| Additional cleaning operations | Medium | v0.3 |
| Streaming API for large files | High | v1.0 |
| Unit tests >70% coverage | High | v0.2 |
| Data profiling reports | Low | v1.0 |

---

## Phase Status Summary

| Phase | Status | Completion % | Notes |
|-------|--------|--------------|-------|
| Requirements | Completed | 100% | All core requirements defined |
| Design | Completed | 100% | Architecture finalized |
| Development | Completed | 100% | v0.1 code complete |
| Testing | In Progress | 60% | Manual tests pass, unit tests pending |
| Deployment | In Progress | 30% | Manual deployment works, CI/CD pending |
| Maintenance | Not Started | 0% | Documentation created, ongoing tasks |

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| v0.1.0 | 2026-01-30 | Initial release - Core functionality working |
| v0.1.1 | 2026-03-23 | Documentation complete - README, SDLC, Architecture |

---

**Last Updated**: 2026-03-23
**Current Version**: 0.1.1
**SDLC Phase**: Testing/Deployment
