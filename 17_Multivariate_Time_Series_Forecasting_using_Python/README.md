# Multivariate Time Series Forecasting with TimescaleDB

> Forecasts multiple stock prices using Vector Autoregression (VAR) model with TimescaleDB for time series storage.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8+ |
| Database | TimescaleDB (PostgreSQL extension) |
| Time Series Model | VAR (Vector Autoregression) |
| Data Processing | pandas, numpy |
| Statistical Tests | statsmodels (ADF test) |
| Visualization | matplotlib |
| Container | Docker |

## Prerequisites

- **Docker** (for TimescaleDB)
- **Python 3.8+**
- **pip** (Python package manager)

## Installation

### 1. Clone/Setup the Project

```bash
cd 17_Multivariate_Time_Series_Forecasting_using_Python
```

### 2. Run Setup Script (One-time)

```bash
chmod +x setup.sh start_db.sh stop_db.sh
./setup.sh
```

This script will:
- Create `.env` file from `.env.example`
- Install Python dependencies from `requirements.txt`

### 3. Start TimescaleDB

```bash
./start_db.sh
```

Wait a few seconds for the database to initialize. The database runs on `localhost:5432`.

## Usage

### Option A: Full Pipeline (with TimescaleDB)

```bash
python forecast.py
```

This will:
1. Initialize TimescaleDB and create hypertable
2. Load stock data from `stocks.csv` into database
3. Fetch data back from database
4. Perform ADF stationarity test
5. Apply differencing
6. Fit VAR model
7. Generate 3-day forecast
8. Save visualization to `forecast_plot.png`

### Option B: Standalone (No Docker Required)

```bash
python forecast_standalone.py
```

Runs the forecasting pipeline directly from CSV without TimescaleDB. Useful for testing or when Docker is unavailable.

### Stop Database (When Done)

```bash
./stop_db.sh
```

## Project Structure

```
.
├── forecast.py              # Main pipeline (with DB)
├── forecast_standalone.py   # Standalone version (no DB)
├── db.py                    # TimescaleDB operations
├── stocks.csv               # Sample data (AAPL, GOOG)
├── forecast_plot.png        # Generated output
├── requirements.txt         # Python dependencies
├── setup.sh                 # Setup script
├── start_db.sh              # Start database
├── stop_db.sh               # Stop database
├── .env.example             # Environment template
├── .env                     # Actual config (git-ignored)
├── multivariate_forecasting.R  # R reference implementation
├── docs/                    # Documentation
│   ├── sdlc.md             # SDLC tracking
│   ├── architecture.md     # System architecture
│   ├── tech_stack.md       # Technology decisions
│   ├── agent_log.md        # Session logs
│   ├── CHANGELOG.md        # Version history
│   └── tasks.md            # Task backlog
└── README.md                # This file
```

## Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| DB_HOST | Yes | Database host | localhost |
| DB_PORT | Yes | Database port | 5432 |
| DB_NAME | Yes | Database name | timeseries_db |
| DB_USER | Yes | Database user | postgres |
| DB_PASSWORD | Yes | Database password | postgres |

## Architecture Overview

```
stocks.csv → forecast.py → TimescaleDB → VAR Model → forecast_plot.png
                 ↓
              db.py
```

1. **Data Loading**: CSV loaded via pandas
2. **Database Storage**: TimescaleDB hypertable
3. **Stationarity**: ADF test via statsmodels
4. **Modeling**: VAR (Vector Autoregression)
5. **Forecasting**: 3-day predictions
6. **Visualization**: matplotlib PNG output

## Running Tests

### Verify Python Dependencies

```bash
python -c "import pandas, numpy, statsmodels, matplotlib; print('All imports OK')"
```

### Verify Standalone Forecast

```bash
python forecast_standalone.py
```

Expected output:
- ADF test results for each ticker
- VAR model summary
- 3-day forecast table
- `forecast_plot.png` created

### Verify Full Pipeline (with Docker)

```bash
# Start DB
./start_db.sh
sleep 5

# Run forecast
python forecast.py

# Check output
ls -la forecast_plot.png

# Stop DB
./stop_db.sh
```

## SDLC Status

See [docs/sdlc.md](docs/sdlc.md) for complete SDLC documentation.

## Troubleshooting

### Database Connection Error

**Error:** `could not connect to server: Connection refused`

**Solutions:**
1. Ensure Docker is running: `docker ps`
2. Check if port 5432 is available: `lsof -i :5432`
3. Wait 10 seconds after starting the database
4. Verify credentials in `.env` file

### Port Already in Use

**Error:** `Bind for 0.0.0.0:5432 failed: port is already allocated`

**Solutions:**
1. Stop existing container: `docker stop timescaledb && docker rm timescaledb`
2. Or use a different port: modify `start_db.sh` to use `-p 5433:5432`

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'xxx'`

**Solutions:**
```bash
pip install -r requirements.txt
```

Or use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker Permission Denied

**Error:** `permission denied while trying to connect to the docker API`

**Solutions:**
1. Add user to docker group: `sudo usermod -aG docker $USER`
2. Log out and log back in
3. Or run with sudo: `sudo ./start_db.sh`

### VAR Model Error (Singular Matrix)

**Error:** `numpy.linalg.LinAlgError: Singular matrix`

**Cause:** Insufficient data points for the number of lags in VAR model.

**Solutions:**
1. Ensure `stocks.csv` has at least 20+ data points per ticker
2. Reduce maxlags in forecast.py: change `maxlags=2` to `maxlags=1`
3. Use the updated `stocks.csv` included in this project (31 data points)

### ADF Test Shows Non-Stationary After Differencing

**Issue:** Some tickers may still show non-stationarity after first differencing.

**Solutions:**
1. Apply second-order differencing (modify forecast.py)
2. Use log differencing instead
3. Accept borderline stationarity for short time series

### matplotlib Display Error

**Error:** `RuntimeError: DISPLAY not set` (headless environments)

**Solution:**
```python
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

The `forecast_standalone.py` already includes this fix.

### Database Initialization Error

**Error:** `permission denied for extension timescaledb`

**Cause:** Database user lacks superuser privileges.

**Solution:**
```bash
docker run -d --name timescaledb -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  timescale/timescaledb:latest-pg14
```

Then reconnect with superuser account.

## Contributing

1. Create a feature branch
2. Make changes
3. Test with `python forecast_standalone.py`
4. Update documentation if needed
5. Submit for review

## License

This is an educational project for the University of Gemini - Department of Computer Science.
