# Hybrid Machine Learning Models
> Forecast stock values with a hybrid ensemble combining PyTorch LSTM and linear regression lag modeling.

## Tech Stack
- Python 3.10+
- pandas, numpy
- scikit-learn (MinMaxScaler, LinearRegression)
- PyTorch (LSTM model)

## Prerequisites
- Python 3
- `pip`
- CPU is sufficient (GPU optional)

## Installation
```bash
cd 15_Hybrid_Machine_Learning_Models
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage
```bash
python hybrid_model.py
```

## Project Structure
```text
15_Hybrid_Machine_Learning_Models/
├── hybrid_model.py            # Main hybrid forecasting script
├── apple_stock_data.csv       # Input time-series data
├── hybrid_predictions.csv     # Output predictions (generated)
├── BUILD_FROM_SCRATCH.md      # Setup and run guide
├── BUILD_LOG.md               # Verification notes
├── guide.txt                  # Lab/project brief
├── requirements.txt           # Dependencies
└── docs/
    └── sdlc.md                # SDLC plan/status
```

## Architecture Overview
1. Load and sort stock data by date.
2. Scale close prices for LSTM training.
3. Train a PyTorch LSTM regressor on sliding windows.
4. Train linear regression on lag features (`lag_1`, `lag_2`, `lag_3`).
5. Align predictions and combine via simple average ensemble.
6. Save merged predictions to `hybrid_predictions.csv`.

## Environment Variables
| Name | Required | Description | Default |
|---|---|---|---|
| `PYTHONHASHSEED` | No | Optional deterministic hashing | unset |

## Running Tests
Smoke test:
```bash
python hybrid_model.py
```

Expected:
- prints first 5 predictions for LSTM/linear/hybrid
- creates `hybrid_predictions.csv`

## SDLC Status
- Current phase: **Implementation and verification complete**
- Details: [`docs/sdlc.md`](./docs/sdlc.md)

## Contributing
1. Keep data alignment logic explicit when combining models.
2. Re-run smoke test after changing sequence/lag logic.
3. Update `BUILD_LOG.md` when model behavior changes.

## License
Project-level license is not explicitly defined. Follow repository owner guidance.
