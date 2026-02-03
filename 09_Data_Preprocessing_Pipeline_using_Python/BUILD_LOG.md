# BUILD LOG

## What Was Built

A production-ready, configuration-driven data preprocessing pipeline for ML workflows using scikit-learn's `Pipeline` and `ColumnTransformer`.

**Key components:**
- `OutlierHandler` — custom sklearn-compatible transformer using IQR-based outlier detection
- `ColumnTransformer` — applies separate pipelines to numeric vs categorical columns
- Numeric pipeline: mean imputation → outlier replacement → StandardScaler
- Categorical pipeline: mode imputation
- JSON-driven config (`config.json`) — no code changes needed to adjust behavior
- Data quality report (before/after comparison)
- CLI via `argparse`

## How to Run

```bash
# Setup (one-time)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with defaults (reads data.csv, writes cleaned_data.csv + quality_report.txt)
python data_preprocessing_pipeline.py

# Run with verbose output
python data_preprocessing_pipeline.py -v

# Full options
python data_preprocessing_pipeline.py -i data.csv -o cleaned_data.csv -c config.json -r report.txt -v
```

## Sample Output

**Input (`data.csv`):**
```
numeric_1,numeric_2,categorical_1,categorical_2
1,1.1,A,X
2,2.2,B,Y
,3.3,A,X        ← missing numeric
4,4.4,C,Z
5,5.5,,Y         ← missing categorical
100,-20.0,B,Z   ← outliers
```

**Output (`cleaned_data.csv`):**
```
numeric_1,numeric_2,categorical_1,categorical_2
-0.916711,-0.765822,A,X
-0.808438,-0.223308,B,Y
1.40033,0.319207,A,X
-0.591892,0.861721,C,Z
-0.483619,1.404235,A,Y
1.40033,-1.596033,B,Z
```

**Transformations applied:**
- `numeric_1`: NaN filled with mean (22.4), outlier `100` replaced with mean, then scaled
- `numeric_2`: outlier `-20.0` replaced with mean, then scaled
- `categorical_1`: NaN filled with mode (`A`)

## Issues

None. Script ran cleanly on first attempt with Python 3.14.3.

> Note: venv had to be created with `python3` explicitly (not `python`) since only `python3` is in PATH on this system.
