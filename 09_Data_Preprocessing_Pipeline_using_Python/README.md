# Data Preprocessing Pipeline

A production-ready, configuration-driven data preprocessing pipeline for machine learning workflows. Built with Python and scikit-learn best practices.

## Overview

This project implements a robust data preprocessing pipeline that handles common data cleaning tasks including missing value imputation, outlier detection and handling, and feature scaling. The pipeline uses scikit-learn's Pipeline and ColumnTransformer for a modular, reusable, and deployable architecture.

## Features

- **Modular Pipeline Architecture**: Uses scikit-learn Pipeline and ColumnTransformer
- **Configuration-Driven**: All preprocessing steps configurable via JSON
- **Mixed-Type Support**: Handles both numeric and categorical data
- **Outlier Detection**: IQR-based outlier detection with configurable replacement strategies
- **Data Quality Reporting**: Automated before/after comparison reports
- **CLI Interface**: Professional command-line interface for easy integration
- **Production Ready**: Follows sklearn best practices for reproducibility and deployment

## Approach & Logic

### Architecture

The pipeline follows a modular, scikit-learn compatible architecture:

1. **ColumnTransformer**: Separates processing for numeric and categorical columns
2. **Pipeline**: Chains preprocessing steps for each column type
3. **Custom Transformers**: Implements custom OutlierHandler class that integrates with sklearn
4. **Configuration System**: JSON-based configuration for flexibility without code changes

### Preprocessing Steps

#### Numeric Columns:
1. **Imputation**: Fill missing values using configurable strategy (mean, median, constant)
2. **Outlier Handling**: Detect outliers using IQR bounds and replace with mean or bounds
3. **Scaling**: Standardize features using StandardScaler (zero mean, unit variance)

#### Categorical Columns:
1. **Imputation**: Fill missing values using mode (most_frequent) strategy

### Outlier Detection Algorithm

Uses the Interquartile Range (IQR) method:
- Calculate Q1 (25th percentile) and Q3 (75th percentile)
- IQR = Q3 - Q1
- Lower bound = Q1 - multiplier × IQR
- Upper bound = Q3 + multiplier × IQR
- Values outside bounds are considered outliers

## Frameworks & Libraries

### Core Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning toolkit providing:
  - `Pipeline`: Chain preprocessing steps
  - `ColumnTransformer`: Apply different transformations to different columns
  - `SimpleImputer`: Missing value imputation
  - `StandardScaler`: Feature standardization
  - `BaseEstimator`, `TransformerMixin`: Base classes for custom transformers

### Development Dependencies
- Python 3.8+
- Virtual environment (venv recommended)

## Project Structure

```
.
├── data_preprocessing_pipeline.py    # Main pipeline implementation
├── config.json                        # Configuration file
├── data.csv                          # Sample input data
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
├── guide.txt                         # Original project guide
└── DEV_LOG.txt                       # Development changelog
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd data-preprocessing-pipeline
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Process the default data.csv file:
```bash
python data_preprocessing_pipeline.py
```

### With Options

```bash
python data_preprocessing_pipeline.py \
    -i input.csv \
    -o cleaned.csv \
    -c config.json \
    -r report.txt \
    -v
```

### CLI Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| --input | -i | Input CSV file path | data.csv |
| --output | -o | Output CSV file path | cleaned_data.csv |
| --config | -c | Configuration JSON file | config.json |
| --report | -r | Quality report output path | quality_report.txt |
| --no-report | | Skip generating quality report | False |
| --verbose | -v | Enable verbose output | False |
| --help | -h | Show help message | - |

## Configuration

The `config.json` file controls all preprocessing behavior:

```json
{
  "imputation": {
    "numeric_strategy": "mean",
    "categorical_strategy": "most_frequent"
  },
  "outlier_detection": {
    "method": "iqr",
    "iqr_multiplier": 1.5,
    "replacement": "mean"
  },
  "scaling": {
    "method": "standard",
    "apply_to": "numeric"
  },
  "columns": {
    "exclude": []
  }
}
```

### Configuration Options

#### Imputation
- `numeric_strategy`: "mean", "median", "most_frequent", "constant"
- `categorical_strategy`: "most_frequent", "constant"

#### Outlier Detection
- `method`: Currently only "iqr" supported
- `iqr_multiplier`: Sensitivity of outlier detection (default: 1.5)
  - Lower values = more aggressive outlier detection
  - Higher values = more conservative
- `replacement`: "mean" (replace with column mean) or "bounds" (clip to bounds)

#### Column Handling
- `exclude`: List of column names to exclude from preprocessing

## Data Quality Report

The pipeline generates a detailed quality report showing:

- Dataset shape (rows, columns)
- Missing value counts (before and after)
- Missing values by column
- Numeric column statistics (count, mean, std, min, max, quartiles)
- Summary of changes applied

Example report:
```
============================================================
DATA QUALITY REPORT
============================================================

--- Before Preprocessing ---
Shape: (6, 4)
Missing values: 2

Missing by column:
  numeric_1: 1
  categorical_1: 1

--- After Preprocessing ---
Shape: (6, 4)
Missing values: 0

--- Changes Summary ---
Rows processed: 6
Columns processed: 4
```

## Example

### Input Data (data.csv)
```csv
numeric_1,numeric_2,categorical_1,categorical_2
1,1.1,A,X
2,2.2,B,Y
,3.3,A,X
4,4.4,C,Z
5,5.5,,Y
100,-20.0,B,Z
```

### Processing Steps

1. **Missing Values**:
   - numeric_1: 1 missing → filled with mean (22.4)
   - categorical_1: 1 missing → filled with mode ("A")

2. **Outliers** (using IQR with 1.5 multiplier):
   - numeric_1: 100 is outlier → replaced with mean
   - numeric_2: -20 is outlier → replaced with mean

3. **Scaling**:
   - All numeric columns standardized (mean=0, std=1)

### Output Data
```csv
numeric_1,numeric_2,categorical_1,categorical_2
-0.9167106762896033,-0.7658216891566691,A,X
-0.8084377617672092,-0.2233075766235009,B,Y
1.40032969448963,0.3192065359096671,A,X
-0.591891932722421,0.8617206484428355,C,Z
-0.48361901820002695,1.4042347609760035,A,Y
1.4003296944896304,-1.5960326795483357,B,Z
```

## Implementation Details

### Custom OutlierHandler Class

A scikit-learn compatible transformer that:
- Extends BaseEstimator and TransformerMixin
- Calculates IQR bounds during fit()
- Replaces outliers during transform()
- Supports mean or bounds replacement strategies
- Integrates seamlessly with sklearn Pipeline

### Pipeline Architecture

```
ColumnTransformer
├── Numeric Pipeline
│   ├── SimpleImputer (mean)
│   ├── OutlierHandler (IQR, mean replacement)
│   └── StandardScaler
└── Categorical Pipeline
    └── SimpleImputer (most_frequent)
```

### Benefits of This Approach

1. **Reproducibility**: Same preprocessing applied consistently
2. **Deployment Ready**: Can be saved/loaded as part of ML workflow
3. **Extensibility**: Easy to add new preprocessing steps
4. **Maintainability**: Configuration-driven, no code changes needed
5. **Testing**: Each component can be tested independently
6. **Integration**: Works with sklearn model training pipelines

## Future Enhancements

Potential improvements for production use:

1. **Advanced Imputation**: KNN imputation, MICE for numeric data
2. **Feature Engineering**: One-hot encoding, label encoding for categoricals
3. **Missing Category**: Create explicit "missing" category for categoricals
4. **Pipeline Persistence**: Save/load pipeline with joblib/pickle
5. **Validation**: Add data validation and schema checking
6. **Visualization**: Generate distribution plots before/after
7. **Logging**: Add structured logging for production monitoring

## Testing

The pipeline has been tested with:
- Mixed-type datasets (numeric + categorical)
- Various missing value patterns
- Different outlier scenarios
- CLI argument combinations
- Edge cases (empty data, all missing columns)

Run basic test:
```bash
python data_preprocessing_pipeline.py -v
```

## License

This project is part of educational coursework for Advanced Topics in AI and Data Science.

## Contributing

This project follows scikit-learn best practices and Python style guidelines. When contributing:

1. Follow PEP 8 style guide
2. Add docstrings to all functions/classes
3. Update tests for new features
4. Update README.md with changes
5. Ensure backward compatibility

## Acknowledgments

- Scikit-learn team for the excellent ML toolkit
- Pandas team for data manipulation capabilities
- Original project guide from University of Gemini
