# Changelog

All notable changes to the Data Cleaner project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Command-line argument parsing (planned)
- Configuration file support (planned)
- Unit tests with >70% coverage (planned)
- Additional cleaning operations: date normalization, missing value handling

### Changed
- Refactor monolithic main.rs into modular functions (planned)

### Fixed
- Memory optimization for large files using streaming API (planned)

---

## [0.1.1] - 2026-03-23

### Added
- Comprehensive README.md with:
  - Tech stack documentation
  - Installation instructions
  - Usage guide
  - Project structure
  - Troubleshooting section
- docs/ directory with full documentation suite:
  - architecture.md — System architecture and data flow
  - sdlc.md — Software Development Life Cycle tracking
  - tasks.md — MoSCoW prioritized task list
  - agent_log.md — Agent session log
  - tech_stack.md — Technology decisions and rationale
  - CHANGELOG.md — This file

### Fixed
- Documentation gaps identified in project review
- No code changes — documentation only release

---

## [0.1.0] - 2026-01-30

### Added
- Initial project setup with Cargo
- Core data cleaning functionality:
  - Column name standardization (lowercase, underscores, trim)
  - Duplicate row removal (keep first)
  - Whitespace trimming from string columns
- CSV I/O using Polars CsvReader and CsvWriter
- Sample data file: loan-recovery.csv
- Error handling using Result and ? operator
- Dummy data generation if input file missing

### Fixed
- Polars version compatibility — downgraded from v0.34.2 to v0.32.1
- Rust borrowing/ownership errors in column renaming logic
- Compilation errors in polars-expr crate

### Technical Details
- Language: Rust v1.93.0
- Dependencies: Polars v0.32.1 (features: lazy, csv, dtype-categorical)
- Build time: ~16 seconds (initial), <1 second (incremental)

---

## Notes

### Version Numbering

- **MAJOR**: Incompatible API changes or major feature additions
- **MINOR**: New functionality in a backward compatible manner
- **PATCH**: Backward compatible bug fixes

### Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Now removed features
- **Fixed**: Bug fixes
- **Security**: Security-related changes

---

**Last Updated**: 2026-03-23
**Current Version**: 0.1.1
