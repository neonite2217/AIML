import pandas as pd
import numpy as np
import json
import argparse
import os
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin


class OutlierHandler(BaseEstimator, TransformerMixin):
    """Custom transformer to handle outliers using IQR method."""
    
    def __init__(self, iqr_multiplier=1.5, replacement='mean'):
        self.iqr_multiplier = iqr_multiplier
        self.replacement = replacement
        self.bounds_ = {}
        self.means_ = {}
    
    def fit(self, X, y=None):
        X = pd.DataFrame(X)
        for col in X.columns:
            q1 = X[col].quantile(0.25)
            q3 = X[col].quantile(0.75)
            iqr = q3 - q1
            self.bounds_[col] = {
                'lower': q1 - self.iqr_multiplier * iqr,
                'upper': q3 + self.iqr_multiplier * iqr
            }
            self.means_[col] = X[col].mean()
        return self
    
    def transform(self, X):
        X = pd.DataFrame(X)
        X_copy = X.copy()
        for col in X.columns:
            lower_bound = self.bounds_[col]['lower']
            upper_bound = self.bounds_[col]['upper']
            mask = (X_copy[col] < lower_bound) | (X_copy[col] > upper_bound)
            if self.replacement == 'mean':
                X_copy.loc[mask, col] = self.means_[col]
            elif self.replacement == 'bounds':
                X_copy.loc[X_copy[col] < lower_bound, col] = lower_bound
                X_copy.loc[X_copy[col] > upper_bound, col] = upper_bound
        return X_copy.values


def create_dummy_data():
    """Create sample data if it doesn't exist."""
    if not os.path.exists("data.csv"):
        data = {
            'numeric_1': [1, 2, np.nan, 4, 5, 100],
            'numeric_2': [1.1, 2.2, 3.3, 4.4, 5.5, -20],
            'categorical_1': ['A', 'B', 'A', 'C', np.nan, 'B'],
            'categorical_2': ['X', 'Y', 'X', 'Z', 'Y', 'Z']
        }
        df = pd.DataFrame(data)
        df.to_csv("data.csv", index=False)
        print("Created sample data.csv")


def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {
        "imputation": {"numeric_strategy": "mean", "categorical_strategy": "most_frequent"},
        "outlier_detection": {"method": "iqr", "iqr_multiplier": 1.5, "replacement": "mean"},
        "scaling": {"method": "standard", "apply_to": "numeric"},
        "columns": {"exclude": []}
    }


def generate_quality_report(df_before, df_after, output_path=None):
    """Generate a data quality report comparing before and after preprocessing."""
    report = []
    report.append("=" * 60)
    report.append("DATA QUALITY REPORT")
    report.append("=" * 60)
    
    report.append("\n--- Before Preprocessing ---")
    report.append(f"Shape: {df_before.shape}")
    report.append(f"Missing values: {df_before.isnull().sum().sum()}")
    report.append("\nMissing by column:")
    for col in df_before.columns:
        missing = df_before[col].isnull().sum()
        if missing > 0:
            report.append(f"  {col}: {missing}")
    
    numeric_cols = df_before.select_dtypes(include=np.number).columns
    if len(numeric_cols) > 0:
        report.append("\nNumeric columns statistics:")
        report.append(df_before[numeric_cols].describe().to_string())
    
    report.append("\n--- After Preprocessing ---")
    report.append(f"Shape: {df_after.shape}")
    report.append(f"Missing values: {df_after.isnull().sum().sum()}")
    
    if len(numeric_cols) > 0:
        report.append("\nNumeric columns statistics:")
        report.append(df_after[numeric_cols].describe().to_string())
    
    report.append("\n--- Changes Summary ---")
    report.append(f"Rows processed: {len(df_before)}")
    report.append(f"Columns processed: {len(df_before.columns)}")
    
    report_text = "\n".join(report)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(report_text)
        print(f"\nQuality report saved to: {output_path}")
    
    return report_text


def build_pipeline(config):
    """Build sklearn Pipeline based on configuration."""
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy=config['imputation']['numeric_strategy'])),
        ('outlier', OutlierHandler(
            iqr_multiplier=config['outlier_detection']['iqr_multiplier'],
            replacement=config['outlier_detection']['replacement']
        )),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy=config['imputation']['categorical_strategy']))
    ])
    
    return numeric_transformer, categorical_transformer


def preprocess_data(df, config=None, verbose=True):
    """
    A preprocessing pipeline for a mixed-type dataset.
    Uses sklearn Pipeline and ColumnTransformer for robust, reusable workflow.
    """
    if config is None:
        config = load_config()
    
    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Include both object and string dtypes for pandas 3.0+ compatibility
    categorical_cols = df.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
    
    # Remove excluded columns
    exclude_cols = config.get('columns', {}).get('exclude', [])
    numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
    categorical_cols = [col for col in categorical_cols if col not in exclude_cols]
    
    if verbose:
        print(f"Numeric columns: {numeric_cols}")
        print(f"Categorical columns: {categorical_cols}")
    
    # Build transformers
    numeric_transformer, categorical_transformer = build_pipeline(config)
    
    # Create column transformer
    transformers = []
    if numeric_cols:
        transformers.append(('num', numeric_transformer, numeric_cols))
    if categorical_cols:
        transformers.append(('cat', categorical_transformer, categorical_cols))
    
    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder='drop'
    )
    
    # Fit and transform
    processed_array = preprocessor.fit_transform(df)
    
    # Reconstruct DataFrame
    all_cols = numeric_cols + categorical_cols
    cleaned_df = pd.DataFrame(processed_array, columns=all_cols)
    
    # Restore original index
    cleaned_df.index = df.index
    
    return cleaned_df, preprocessor


def main():
    parser = argparse.ArgumentParser(
        description='Data Preprocessing Pipeline - Clean and standardize your dataset'
    )
    parser.add_argument(
        '-i', '--input',
        default='data.csv',
        help='Input CSV file path (default: data.csv)'
    )
    parser.add_argument(
        '-o', '--output',
        default='cleaned_data.csv',
        help='Output CSV file path (default: cleaned_data.csv)'
    )
    parser.add_argument(
        '-c', '--config',
        default='config.json',
        help='Configuration JSON file path (default: config.json)'
    )
    parser.add_argument(
        '-r', '--report',
        default='quality_report.txt',
        help='Quality report output path (default: quality_report.txt)'
    )
    parser.add_argument(
        '--no-report',
        action='store_true',
        help='Skip generating quality report'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Create dummy data if needed
    if not os.path.exists(args.input):
        create_dummy_data()
    
    # Load data
    print(f"Loading data from: {args.input}")
    df = pd.read_csv(args.input)
    
    if args.verbose:
        print("\nOriginal DataFrame:")
        print(df)
        print(f"\nShape: {df.shape}")
    
    # Load config
    config = load_config(args.config)
    
    # Preprocess
    print("\nPreprocessing data...")
    cleaned_df, pipeline = preprocess_data(df, config, verbose=args.verbose)
    
    if args.verbose:
        print("\nCleaned DataFrame:")
        print(cleaned_df)
    
    # Save output
    cleaned_df.to_csv(args.output, index=False)
    print(f"\nCleaned data saved to: {args.output}")
    
    # Generate report
    if not args.no_report:
        report = generate_quality_report(df, cleaned_df, args.report)
        if args.verbose:
            print("\n" + report)
    
    print("\nPreprocessing complete!")


if __name__ == '__main__':
    main()
