# Architecture — Multivariate Time Series Forecasting

## System Overview
This project implements a multivariate time series forecasting pipeline using Vector Autoregression (VAR). It stores stock price data in TimescaleDB, performs stationarity testing via ADF test, fits a VAR model, and generates forecasts with visualization.

---

## Component Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   stocks.csv    │────▶│    forecast.py   │────▶│ forecast_plot.png
│  (Input Data)   │     │  (Main Pipeline) │     │  (Visualization)│
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
              ┌─────▼─────┐            ┌─────▼─────┐
              │    db.py  │            │ statsmodels
              │ (TimescaleDB)           │   (VAR)   │
              └───────────┘            └───────────┘
```

---

## Data Flow

1. **Data Loading**: `stocks.csv` loaded via pandas, pivoted to wide format (Date × Ticker)
2. **Database Storage**: Data stored in TimescaleDB hypertable via `db.py`
3. **Stationarity Check**: ADF test performed on each ticker series
4. **Differencing**: First-order differencing applied to achieve stationarity
5. **VAR Model Fitting**: statsmodels VAR model fit on differenced data
6. **Forecasting**: Predict next N steps (default: 3 days)
7. **Reverse Differencing**: Cumsum + last actual value to restore original scale
8. **Visualization**: Matplotlib plots actual vs forecast, saved as PNG

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| TimescaleDB over plain PostgreSQL | Optimized for time-series queries, hypertable partitioning |
| VAR model | Captures interdependencies between multiple stock prices |
| First-order differencing | Simple yet effective method to achieve stationarity |
| Matplotlib for visualization | Standard Python plotting, outputs PNG for easy sharing |

---

## External Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| TimescaleDB | latest-pg14 | Time-series database |
| pandas | >=2.0.0 | Data manipulation |
| numpy | >=1.24.0 | Numerical operations |
| statsmodels | >=0.14.0 | VAR model, ADF test |
| matplotlib | >=3.7.0 | Visualization |
| psycopg2-binary | >=2.9.0 | PostgreSQL connection |
| python-dotenv | >=1.0.0 | Environment variables |

---

## Database Schema

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE stock_prices (
    time TIMESTAMPTZ NOT NULL,
    ticker TEXT NOT NULL,
    close DOUBLE PRECISION NOT NULL
);

SELECT create_hypertable('stock_prices', 'time', if_not_exists => TRUE);
```

---

## File Structure

```
.
├── forecast.py           # Main forecasting pipeline (with DB)
├── forecast_standalone.py # Standalone version (no DB required)
├── db.py                 # TimescaleDB operations
├── stocks.csv            # Sample stock data (AAPL, GOOG)
├── forecast_plot.png     # Generated visualization
├── requirements.txt     # Python dependencies
├── setup.sh             # One-time setup script
├── start_db.sh          # Start TimescaleDB container
├── stop_db.sh           # Stop TimescaleDB container
├── .env.example         # Database configuration template
├── .env                 # Actual configuration (git-ignored)
├── docs/
│   ├── sdlc.md          # SDLC tracking
│   ├── agent_log.md     # Session logs
│   ├── CHANGELOG.md     # Version history
│   ├── tasks.md         # Task backlog
│   ├── architecture.md  # This file
│   └── tech_stack.md    # Technology decisions
├── multivariate_forecasting.R  # R implementation reference
└── README.md            # Main documentation
```
