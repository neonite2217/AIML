# SDLC — Text Classification Pipeline

## Project Overview

A text classification pipeline built in R using classical machine learning techniques. The project demonstrates the complete workflow from raw text data to trained classifier, including text preprocessing, feature extraction, model training, and evaluation.

---

## 1. Requirements

### 1.1 Functional Requirements

- [x] Load and parse text data from CSV format
- [x] Preprocess text (tokenization, punctuation removal, stopword removal)
- [x] Convert text to numerical features (Document-Feature Matrix)
- [x] Split data into training and testing sets (80/20 split)
- [x] Train a Naive Bayes classifier
- [x] Predict class labels for test data
- [x] Evaluate model performance (confusion matrix, accuracy)
- [x] Handle edge cases (minimum data requirements, empty test sets)

### 1.2 Non-Functional Requirements

- [x] **Performance**: Process small datasets (<1000 docs) in under 5 seconds
- [x] **Usability**: Single command execution (`Rscript text_classification.R`)
- [x] **Maintainability**: Clear code structure with comments
- [x] **Portability**: Works on any system with R installed
- [x] **Reproducibility**: Set random seed for consistent train/test splits

### 1.3 User Personas

1. **Data Science Students**: Learning text classification fundamentals
2. **ML Practitioners**: Quick baseline for text classification tasks
3. **Researchers**: Starting point for NLP experiments

---

## 2. Design

### 2.1 Architecture

See [architecture.md](architecture.md) for detailed system design.

**High-level flow:**
```
Data Ingestion → Text Preprocessing → Feature Extraction → 
Model Training → Prediction → Evaluation
```

### 2.2 Tech Stack

See [tech_stack.md](tech_stack.md) for technology decisions.

**Core Technologies:**
- R (programming language)
- quanteda (text processing)
- e1071 (Naive Bayes)
- tidyverse (data manipulation)

### 2.3 Data Schema

**Input Schema (newsgroups.csv):**
| Field | Type | Description |
|-------|------|-------------|
| text | string | Document content |
| topic | string | Class label |

**Output:**
- Confusion matrix (table)
- Accuracy score (float)

### 2.4 Algorithm Design

**Text Preprocessing:**
1. Create corpus from text data
2. Tokenize with punctuation/number/symbol removal
3. Remove English stopwords
4. Build Document-Feature Matrix

**Model:**
- Algorithm: Multinomial Naive Bayes
- Features: Word frequency counts (bag-of-words)
- Training: 80% of data
- Testing: 20% of data

---

## 3. Development

### 3.1 Coding Standards

- [x] Follow R style guidelines
- [x] Use meaningful variable names
- [x] Comment complex operations
- [x] Handle edge cases explicitly
- [x] Use consistent indentation (2 spaces)

### 3.2 Version Control

- Repository: Part of Super 30 series
- Branch: main
- Commits: Conventional commit format

### 3.3 Code Review

- Self-reviewed for R best practices
- Validated against quanteda documentation
- Tested with sample data

---

## 4. Testing

### 4.1 Unit Tests

**Test Cases:**
- [x] Data loading with existing file
- [x] Data generation when file missing
- [x] Corpus creation from data frame
- [x] DFM creation with preprocessing
- [x] Train/test split with sufficient data
- [x] Model training on training data
- [x] Prediction on test data
- [x] Confusion matrix calculation
- [x] Accuracy computation

### 4.2 Integration Tests

- [x] End-to-end pipeline execution
- [x] Package-optional execution path verified (base R fallback)
- [x] Data flow from input to output

### 4.3 Smoke Test

```bash
Rscript text_classification.R
```

**Expected Result:**
- Script runs without errors
- Confusion matrix displayed
- Accuracy score printed

**Actual Status**: ✅ PASSED (2026-03-25)
- **Command**: `Rscript text_classification.R`
- **Result**: Exit code 0, confusion matrix + accuracy printed
- **Runtime**: Base R fallback backend (no external package requirement)

### 4.4 Edge Cases

- [x] Empty dataset handling
- [x] Single document handling
- [x] Missing file handling (auto-generate sample data)
- [x] Class imbalance awareness

---

## 5. Deployment

### 5.1 Environment Setup

**Prerequisites:**
- R >= 4.0
- Optional packages for quanteda backend: quanteda, quanteda.textmodels

**Installation:**
```bash
# Install R (platform-specific)
# Optional package install for quanteda backend
R -e 'install.packages(c("quanteda", "quanteda.textmodels"))'
```

### 5.2 Deployment Guide

1. Clone/download project files
2. Install R (optional: quanteda backend packages)
3. Run: `Rscript text_classification.R`

### 5.3 Rollback Plan

- No persistent state to rollback
- Revert to previous git commit if needed
- Reinstall packages if corrupted

### 5.4 CI/CD

Not applicable for this standalone R script project.

---

## 6. Maintenance

### 6.1 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

### 6.2 Known Issues

| Issue | Severity | Workaround |
|-------|----------|------------|
| R not installed | High | Install R from cran.r-project.org |
| Package installation fails | Medium | Script auto-falls back to base R backend |
| Small dataset warning | Low | Add more sample data |

### 6.3 Agent Log

See [agent_log.md](agent_log.md) for development session history.

### 6.4 Future Enhancements

See [tasks.md](tasks.md) for planned improvements.

**Potential Enhancements:**
1. Support for larger datasets
2. Additional classifiers (SVM, Random Forest)
3. Cross-validation
4. Hyperparameter tuning
5. TF-IDF weighting
6. N-gram features
7. Model persistence (save/load)
8. Command-line arguments

---

## SDLC Phase Status Summary

| Phase | Status | Completion Date | Evidence |
|-------|--------|-----------------|----------|
| Requirements | ✅ Complete | 2026-03-17 | All functional requirements documented and implemented |
| Design | ✅ Complete | 2026-03-17 | Architecture documented in docs/architecture.md |
| Development | ✅ Complete | 2026-03-17 | text_classification.R implemented (69 lines) |
| Testing | ✅ Complete | 2026-03-25 | Smoke test passed (`Rscript text_classification.R`, exit 0) |
| Deployment | ✅ Complete | 2026-03-22 | Installation guide complete; R v4.5.3 installed |
| Maintenance | 🔄 Ongoing | 2026-03-22 | CHANGELOG.md, tasks.md created |

**Build Status**: R runtime verified (v4.5.3). Base-R pipeline runs without external dependencies; quanteda backend remains optional.

---

**Document Version**: 1.0.0  
**Last Updated**: 2026-03-25  
**Author**: Ansh
