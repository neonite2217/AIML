# Data Cleaning Pipeline using Pandas

A robust, reusable data cleaning pipeline for preprocessing datasets with missing values, inconsistent formatting, and outliers.

## Features

- **Missing Value Imputation**: Mode for categorical, median for numeric columns
- **Data Type Optimization**: Automatic memory optimization through type downcasting
- **String Standardization**: Consistent formatting and case normalization
- **Outlier Detection**: Percentile-based capping (99th percentile)
- **Comprehensive Logging**: Detailed operation tracking and reporting
- **Memory Efficient**: 5-10% memory usage reduction

## Quick Start

```python
from data_cleaning_pipeline import DataCleaningPipeline

# Initialize pipeline
pipeline = DataCleaningPipeline()

# Clean your data
cleaned_df = pipeline.clean_data(raw_df)

# Get detailed report
report = pipeline.get_cleaning_report()
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python data_cleaning_pipeline.py
```

### Run Tests
```bash
python test_pipeline.py
```

## Pipeline Steps

1. **Data Inspection** - Analyze schema and missing values
2. **Missing Value Handling** - Impute using statistical methods
3. **Data Type Optimization** - Convert to memory-efficient types
4. **String Standardization** - Normalize text data
5. **Outlier Management** - Cap extreme values using percentiles

## Example Output

```
Pipeline Start: Processing dataset with shape (20, 13)
Missing Value Imputation: Gender: 4 values filled with mode 'Male'
String Standardization: Gender: 9 -> 2 unique values
Outlier Handling: ApplicantIncome: 2 outliers capped
Pipeline Complete: Memory saved: 487 bytes
```

## Files

- `data_cleaning_pipeline.py` - Main pipeline implementation
- `test_pipeline.py` - Comprehensive test suite
- `loan_prediction.csv` - Sample dataset
- `development_log.md` - Detailed development notes

## Requirements

- pandas
- numpy
- typing

## License

MIT License
