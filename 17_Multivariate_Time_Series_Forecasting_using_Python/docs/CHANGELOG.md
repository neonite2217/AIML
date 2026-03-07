# Changelog

## [Unreleased]
### Added
- Complete SDLC documentation (docs/sdlc.md)
- Architecture documentation (docs/architecture.md)
- Tech stack documentation (docs/tech_stack.md)
- Agent log documentation (docs/agent_log.md)
- Task backlog (docs/tasks.md)

### Changed
- Extended stocks.csv from 5 to 31 data points per ticker for better VAR model fitting
- Added forecast_standalone.py for verification without Docker

### Fixed
- Original stocks.csv had insufficient data for VAR model (singular matrix error)

---

## [1.0.0] - 2026-03-17
### Added
- Initial release with Python implementation
- TimescaleDB integration for time-series storage
- VAR model for multivariate forecasting
- ADF stationarity testing
- Matplotlib visualization
- Shell scripts for setup/start/stop
- R reference implementation (multivariate_forecasting.R)
