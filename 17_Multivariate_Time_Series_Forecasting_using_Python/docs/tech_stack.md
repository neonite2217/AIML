# Tech Stack — Multivariate Time Series Forecasting

## Language
- **Python 3.8+** — Primary implementation language
- **R** — Reference implementation (multivariate_forecasting.R)

---

## Core Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| pandas | >=2.0.0 | Data loading, pivoting, manipulation |
| numpy | >=1.24.0 | Numerical computations, cumsum |
| statsmodels | >=0.14.0 | VAR model, ADF test |
| matplotlib | >=3.7.0 | Visualization |
| psycopg2-binary | >=2.9.0 | PostgreSQL/TimescaleDB connection |
| python-dotenv | >=1.0.0 | Environment variable loading |

---

## Database

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Time-series DB | TimescaleDB (PostgreSQL extension) | Optimized for time-series data, hypertables |
| Docker container | timescale/timescaledb:latest-pg14 | Easy setup, reproducible environment |

---

## Development Tools

| Tool | Purpose |
|------|---------|
| Docker | Containerize TimescaleDB |
| pip | Package management |
| bash | Automation scripts (setup.sh, start_db.sh, stop_db.sh) |

---

## Architecture Pattern
- **Modular design**: Separate `db.py` for database operations
- **CLI-based**: No web UI, runs via `python forecast.py`
- **Standalone option**: `forecast_standalone.py` runs without Docker/DB

---

## Why This Stack?

1. **TimescaleDB**: Purpose-built for time-series workloads with automatic partitioning
2. **statsmodels VAR**: Well-established statistical library for vector autoregression
3. **pandas/numpy**: Industry standards for data manipulation in Python
4. **matplotlib**: Simple, reliable plotting for static outputs
5. **Docker**: Reproducible database setup without manual installation
