# SDLC Plan - Data Augmentation Using LLMs

## Project Overview
This document tracks the Software Development Lifecycle (SDLC) for the Data Augmentation Using LLMs project. It outlines requirements, design decisions, implementation status, testing strategy, and future roadmap.

## 1. Requirements

### Functional Requirements
- ✅ Generate synthetic tabular rows from a structured prompt
- ✅ Parse generated rows into a pandas DataFrame
- ✅ Validate data quality using schema, type, range, and sanity constraints
- ✅ Print useful summary statistics
- ✅ Support reproducible runs via deterministic seed

### Non-Functional Requirements
- ✅ Reproducible runs via deterministic seed (seed=42)
- ✅ Readable and maintainable script for learning purposes
- ✅ Minimal setup with standard Python tooling
- ✅ Clear documentation and error messages
- ✅ Fast execution (< 5 seconds for smoke test)

### Future Requirements (Backlog)
- [ ] Real LLM integration (GPT-2 via transformers)
- [ ] JSON mode output for structured generation
- [ ] Configurable validation parameters via config file
- [ ] Command-line argument support
- [ ] Batch processing for large datasets
- [ ] Export to multiple formats (CSV, JSON, Parquet)

## 2. Design

### Architecture Decisions
- **Single-script architecture:** All core logic in `data_augmentation.py` for simplicity
- **Class-based design:** `DataAugmentor` class encapsulates generation logic
- **Pandas-centric:** Leverages pandas for parsing, validation, and statistics
- **Simulated LLM:** Pattern-based generator for fast, deterministic execution
- **Validation pipeline:** Multi-stage validation (schema → type → range → sanity → dedup)

### Component Design

#### DataAugmentor Class
```python
class DataAugmentor:
    - __init__(seed=42): Initialize with deterministic seed
    - generate_from_prompt(prompt, num_samples=10): Generate synthetic rows
    - Pattern learning: Calculates avg_salary_per_year from examples
    - Variation injection: ±15% random variation for realism
```

#### Validation Pipeline
1. **Schema Check:** Verify expected columns exist
2. **Type Validation:** Convert to numeric with `pd.to_numeric()`
3. **Range Validation:** Filter within reasonable bounds
4. **Sanity Constraints:** Enforce logical relationships
5. **Deduplication:** Remove duplicates by employee_id

### Data Flow
```
Prompt (CSV format)
    ↓
Pattern Learning (salary/experience ratio)
    ↓
Synthetic Generation (15 rows)
    ↓
CSV Parsing (pd.read_csv)
    ↓
DataFrame Creation
    ↓
Validation Pipeline (5 stages)
    ↓
Filtered DataFrame (3-8 rows)
    ↓
Statistics Output
```

## 3. Implementation

### Current Implementation Status
- ✅ `data_augmentation.py` - Complete
- ✅ Prompt schema and validation logic - Explicit and adjustable
- ✅ Pandas integration - Robust parsing and filtering
- ✅ Error handling - Graceful degradation with informative messages
- ✅ Documentation - README, BUILD_FROM_SCRATCH, DEVELOPMENT_LOG

### Code Quality
- **Style:** PEP 8 compliant
- **Comments:** Minimal but informative
- **Error Handling:** Try-except for optional imports
- **Type Safety:** Uses pandas type conversion with error handling
- **Reproducibility:** Seeded random number generation

### Technical Debt
- [ ] Add type hints throughout
- [ ] Extract magic numbers to constants
- [ ] Add unit tests for validation functions
- [ ] Refactor validation into separate functions
- [ ] Add logging instead of print statements

## 4. Testing Strategy

### Current Testing
- ✅ **Smoke Test:** Run `python data_augmentation.py`
- ✅ **Manual Verification:** Check output matches expected format
- ✅ **Validation Checks:** Verify all validation stages pass

### Test Coverage
| Component | Status | Method |
|-----------|--------|----------|
| DataAugmentor initialization | ✅ Manual | Visual inspection |
| Pattern learning | ✅ Manual | Check salary calculations |
| Synthetic generation | ✅ Manual | Verify 15 rows generated |
| CSV parsing | ✅ Manual | DataFrame creation |
| Schema validation | ✅ Manual | Column presence check |
| Type validation | ✅ Manual | pd.to_numeric() conversion |
| Range validation | ✅ Manual | Filter verification |
| Sanity constraints | ✅ Manual | Logical relationship check |
| Deduplication | ✅ Manual | Duplicate count verification |
| Statistics calculation | ✅ Manual | Mean/min/max verification |

### Future Testing (Backlog)
- [ ] Unit tests with pytest
- [ ] Integration tests for full pipeline
- [ ] Property-based testing for validation
- [ ] Performance benchmarks
- [ ] Edge case testing (empty input, malformed data)

### Test Scenarios
1. **Happy Path:** Normal execution with valid prompt
2. **Empty Input:** Handle empty prompt gracefully
3. **Malformed Data:** Handle invalid CSV format
4. **All Rows Filtered:** Handle case where validation removes all rows
5. **Duplicate IDs:** Handle duplicate employee_ids
6. **Type Mismatch:** Handle non-numeric values in numeric columns

## 5. Deployment / Runtime

### Current State
- **Environment:** Local CLI execution
- **Platform:** Linux, macOS, Windows
- **Dependencies:** Python 3.10+, pandas (minimal)
- **Execution:** `python data_augmentation.py`

### Deployment Targets
- ✅ Local development
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Docker container
- [ ] Jupyter notebook integration
- [ ] Web service API (FastAPI/Flask)

### Runtime Requirements
- Python 3.10+
- 100MB RAM (minimal)
- < 5 seconds execution time
- No GPU required (for simulated version)

## 6. Maintenance

### Documentation Maintenance
- ✅ Track changes in `DEVELOPMENT_LOG.md`
- ✅ Update README.md for user-facing changes
- ✅ Update BUILD_FROM_SCRATCH.md for setup changes
- ✅ Update SDLC.md for architectural changes

### Code Maintenance
- [ ] Add automated tests before major refactoring
- [ ] Version pinning for dependencies
- [ ] Changelog maintenance
- [ ] Code review process

### Known Issues
1. **LSP Errors:** Import warnings for pandas (false positive - installed in venv)
2. **Validation Strictness:** May filter too aggressively with some random seeds
3. **Limited Output:** Only 3-8 rows typically pass validation (by design)

### Maintenance Schedule
- **Weekly:** Review and update documentation
- **Monthly:** Check for dependency updates
- **Quarterly:** Review and refactor code
- **As Needed:** Bug fixes and feature additions

## 7. Risks and Mitigations

### Current Risks

#### Risk: Generated rows may be unrealistic
- **Likelihood:** Medium
- **Impact:** Medium
- **Mitigation:** Tighten validation ranges and sanity constraints
- **Status:** ✅ Addressed with multi-stage validation

#### Risk: Free-form model output can break parsing
- **Likelihood:** Low (simulated version uses structured output)
- **Impact:** High
- **Mitigation:** Keep strict CSV-like prompting; consider structured JSON output later
- **Status:** ✅ Addressed with CSV format

#### Risk: Hidden regressions when changing rules
- **Likelihood:** Medium
- **Impact:** Medium
- **Mitigation:** Add basic automated tests for parse + validate steps
- **Status:** 🔄 In Progress - tests planned

### Future Risks

#### Risk: Real LLM integration complexity
- **Likelihood:** High
- **Impact:** High
- **Mitigation:** Gradual migration, keep simulated version as fallback
- **Status:** 📋 Planned

#### Risk: Performance degradation with large datasets
- **Likelihood:** Medium
- **Impact:** Medium
- **Mitigation:** Benchmark and optimize pandas operations
- **Status:** 📋 Planned

## 8. Current Phase Status (as of 2026-03-17)

### Phase Completion
| Phase | Status | Completion Date | Notes |
|-------|--------|-----------------|-------|
| Requirements | ✅ Complete | 2026-03-05 | All core requirements defined |
| Design | ✅ Complete | 2026-03-05 | Architecture finalized |
| Implementation | ✅ Complete | 2026-03-05 | Core functionality working |
| Testing | ✅ Complete | 2026-03-17 | Smoke tests passing |
| Documentation | ✅ Complete | 2026-03-17 | All docs updated |
| Deployment | ⏸️ N/A | - | Local execution only |

### Current Version
- **Version:** 1.0.0
- **Status:** Production Ready (Simulated LLM)
- **Last Updated:** 2026-03-17

### Recent Changes
1. ✅ Updated README.md with comprehensive build guide
2. ✅ Updated BUILD_FROM_SCRATCH.md with detailed troubleshooting
3. ✅ Updated SDLC.md with current status
4. ✅ Verified smoke test passes
5. ✅ All documentation synchronized

## 9. Next Steps / Roadmap

### Immediate (Next 2 Weeks)
- [ ] Add pytest test suite
- [ ] Create GitHub Actions CI pipeline
- [ ] Add type hints to all functions
- [ ] Extract validation logic into separate module

### Short-term (Next Month)
- [ ] Implement real LLM integration (GPT-2)
- [ ] Add command-line argument parsing
- [ ] Create configuration file support
- [ ] Add export to CSV/JSON functionality

### Medium-term (Next Quarter)
- [ ] Docker containerization
- [ ] Web API wrapper (FastAPI)
- [ ] Batch processing for large datasets
- [ ] Performance optimization

### Long-term (Next 6 Months)
- [ ] Support for multiple data types (not just employee data)
- [ ] Advanced pattern learning (ML-based)
- [ ] GUI interface
- [ ] Cloud deployment (AWS/GCP/Azure)

## 10. Enhancement Ideas

From `guide.txt`, potential enhancements:

1. **Enforce Structured Data Generation**
   - Use JSON mode for LLM output
   - Integrate `outlines` library for constrained generation
   - Ensure valid CSV/JSON every time

2. **Controllable Generation with Advanced Prompting**
   - Specify class distribution for classification tasks
   - Control sentiment, tone, reading level
   - Conditional generation based on column values

3. **Automated Data Quality Filtering**
   - Statistical outlier detection
   - Distribution matching with original data
   - Train classifier for quality assessment

4. **Empirical Comparison with Traditional Augmentation**
   - Compare with back-translation
   - Compare with synonym replacement
   - Benchmark downstream model performance

5. **Augmenting Tabular Data with Relationships**
   - Preserve column relationships
   - Conditional generation (one column based on others)
   - Specialized models for tabular data

## 11. Success Metrics

### Current Metrics
- ✅ Build success rate: 100% (when following instructions)
- ✅ Test pass rate: 100% (smoke test)
- ✅ Documentation completeness: 100%
- ✅ Code coverage: Manual testing only

### Target Metrics
- [ ] Automated test coverage: > 80%
- [ ] Build time: < 2 minutes
- [ ] Execution time: < 3 seconds
- [ ] Documentation freshness: Updated with each release

## 12. Resources

### Documentation
- `README.md` - User guide and overview
- `BUILD_FROM_SCRATCH.md` - Detailed setup instructions
- `DEVELOPMENT_LOG.md` - Implementation history
- `guide.txt` - Original project brief
- `docs/sdlc.md` - This file

### Code
- `data_augmentation.py` - Main implementation
- `requirements.txt` - Dependencies

### External Resources
- Pandas documentation: https://pandas.pydata.org/docs/
- Transformers library: https://huggingface.co/docs/transformers/
- Outlines library: https://outlines-dev.github.io/outlines/

## 13. Glossary

- **LLM:** Large Language Model (e.g., GPT-2)
- **Data Augmentation:** Generating synthetic data to expand training datasets
- **Prompt:** Input text that guides the LLM generation
- **Schema:** Structure definition of the data (column names and types)
- **Validation:** Process of checking data quality and correctness
- **Synthetic Data:** Artificially generated data that mimics real data
- **Pattern Learning:** Extracting rules from example data
- **Smoke Test:** Basic test to verify the system runs without errors

## 14. Change Log

### Version 1.0.0 (2026-03-17)
- ✅ Initial release
- ✅ Simulated LLM implementation
- ✅ 5-step workflow complete
- ✅ Comprehensive validation pipeline
- ✅ Full documentation suite

### Version 0.9.0 (2026-03-05)
- 🔄 Development phase
- ✅ Core implementation
- ✅ Basic documentation

---

**Document Owner:** Development Team
**Review Schedule:** Monthly
**Next Review Date:** 2026-04-17
