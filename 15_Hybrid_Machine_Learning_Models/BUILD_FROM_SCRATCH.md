# Build From Scratch - Project 15

## 1. Setup
```bash
cd 15_Hybrid_Machine_Learning_Models
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Run
```bash
python hybrid_model.py
```

## 3. Expected Outputs
- Console prints:
  - first 5 LSTM predictions
  - first 5 linear regression predictions
  - first 5 hybrid predictions
- File output:
  - `hybrid_predictions.csv`

## 4. Notes
- Script auto-adjusts LSTM sequence window for small datasets.
- If `apple_stock_data.csv` is missing, script creates a dummy dataset.
