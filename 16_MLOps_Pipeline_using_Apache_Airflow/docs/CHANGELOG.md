# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Unit tests with pytest (>70% coverage)
- MLflow integration for experiment tracking
- Docker containerization
- CI/CD pipeline with GitHub Actions
- Data validation with Great Expectations
- Model registry integration

## [1.0.0] - 2026-03-25

### Added
- Complete MLOps pipeline DAG (`mlops_pipeline_screentime`)
- Data creation task with synthetic screentime data generation
- Preprocessing task with feature engineering and StandardScaler
- Model training task using RandomForestRegressor
- Comprehensive evaluation metrics (MAE, MSE, RMSE, R2)
- Metrics artifact generation to `artifacts/metrics.json`
- Model serialization support (optional, requires joblib)
- Professional DAG documentation and docstrings
- Comprehensive README with installation and usage instructions
- Architecture documentation with diagrams
- SDLC documentation tracking all phases
- Technology stack documentation
- Setup scripts for automated installation (Unix/Linux and Windows)
- Environment variable configuration template
- Troubleshooting guide with common issues and solutions
- Project structure compliant with RULES.md standards

### Changed
- Enhanced DAG from simple proof-of-concept to production-grade
- Improved error handling and logging throughout pipeline
- Updated task dependencies for proper execution flow
- Restructured project for professional development standards

### Fixed
- Proper module imports and dependencies
- Task context passing for XCom data sharing
- Path handling for cross-platform compatibility

## [0.1.0] - 2026-03-20

### Added
- Initial proof-of-concept DAG with basic functionality
- Simple data preprocessing function
- Random Forest model training
- Basic MAE calculation

---

**Last Updated**: 2026-03-25
**Maintainer**: MLOps Team
