# Changelog — Text Classification Pipeline

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- TF-IDF weighting support
- Cross-validation implementation
- Additional classifiers (SVM, Random Forest)
- Command-line argument support
- Docker containerization
- Hyperparameter tuning utilities

---

## [1.0.0] - 2026-03-22

### Added
- Initial release of Text Classification Pipeline
- Complete Naive Bayes text classifier implementation in R
- Document-Feature Matrix (DFM) creation using quanteda
- Text preprocessing pipeline (tokenization, stopword removal, punctuation removal)
- Train/test split functionality (80/20)
- Confusion matrix and accuracy metrics
- Sample dataset (newsgroups.csv) with 5 documents across 2 categories
- Auto-generation of sample data if CSV file missing
- Edge case handling for insufficient data
- Comprehensive documentation:
  - README.md with installation and usage instructions
  - docs/sdlc.md with full SDLC documentation
  - docs/architecture.md with component diagrams and data flow
  - docs/tech_stack.md with technology decisions
  - docs/CHANGELOG.md (this file)
  - docs/agent_log.md for development tracking
  - docs/tasks.md for future enhancements
- BUILD_LOG.md documenting the build process

### Features
- **Text Processing**: Punctuation, number, and symbol removal
- **Stopword Removal**: English stopwords filtered using quanteda
- **Feature Extraction**: Bag-of-words representation via DFM
- **Classification**: Multinomial Naive Bayes from e1071 package
- **Evaluation**: Confusion matrix and accuracy calculation
- **Reproducibility**: Fixed random seed (123) for consistent train/test splits

### Technical Details
- Language: R (version 4.0+)
- Dependencies: tidyverse, quanteda, e1071
- Dataset: 20 Newsgroups subset (comp.graphics, sci.space)
- Performance: ~2-5 seconds for small datasets

### Documentation
- Installation guide for Linux, macOS, and Windows
- Troubleshooting section with common issues and solutions
- Architecture overview with data flow diagrams
- SDLC compliance tracking
- Project structure documentation

---

## Notes

### Version History
- **v1.0.0** (2026-03-22): Initial release - Complete text classification pipeline

### Maintenance
See `docs/tasks.md` for planned improvements and enhancement ideas.

### Contributors
- Ansh (Initial implementation and documentation)

---

**Last Updated**: 2026-03-22
