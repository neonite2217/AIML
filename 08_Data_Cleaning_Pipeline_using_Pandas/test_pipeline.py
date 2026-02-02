#!/usr/bin/env python3
"""
Test script to demonstrate the data cleaning pipeline with synthetic messy data
"""

import pandas as pd
import numpy as np
from data_cleaning_pipeline import DataCleaningPipeline

def create_messy_test_data():
    """Create test data with various data quality issues"""
    np.random.seed(42)
    
    data = {
        'Loan_ID': [f'LP{str(i).zfill(3)}' for i in range(1, 21)],
        'Gender': ['Male', 'Female', None, 'male ', ' FEMALE', 'Male', None, 'female', 'Male', 'Female',
                  'MALE', 'female ', None, 'Male', 'Female', 'male', 'FEMALE', 'Male', None, 'Female'],
        'Married': ['Yes', 'No', None, 'yes', 'NO ', 'Yes', 'No', None, 'YES', 'no',
                   'Yes', 'No', 'yes ', None, 'NO', 'Yes', 'No', 'YES', 'no', None],
        'Dependents': ['0', '1', '2', '3+', None, '0', '1', '2', None, '3+',
                      '0', None, '1', '2', '3+', '0', '1', None, '2', '3+'],
        'Education': ['Graduate', 'Not Graduate'] * 10,
        'Self_Employed': ['No', 'Yes', None, 'no', 'YES', 'No', None, 'yes', 'NO', 'Yes',
                         'no ', None, 'YES', 'No', 'yes', 'NO', 'Yes', None, 'no', 'YES'],
        'ApplicantIncome': [5849, 4583, 3000, 2583, 6000, 5417, 2333, 3036, 4006, 12841,
                           3200, None, 4500, 2800, 150000, 3600, 2900, 4200, None, 5100],  # Outliers and missing
        'CoapplicantIncome': [0, 1508, 0, 2358, 0, 4196, 1516, 2504, 1526, 10968,
                             1200, 0, None, 1800, 0, 2200, None, 1600, 1400, 0],
        'LoanAmount': [128, 128, 66, 120, 141, 267, 95, 158, 168, 349,
                      180, None, 200, 150, 800, 175, None, 190, 160, 220],  # Outliers and missing
        'Loan_Amount_Term': [360, 360, 360, 360, 360, 360, 360, 360, 360, 360,
                            None, 240, 360, None, 120, 360, 240, 360, None, 360],
        'Credit_History': [1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                          None, 1, 0, 1, None, 1, 1, 0, 1, None],
        'Property_Area': ['Urban', 'Rural', 'Urban', 'Urban', 'Urban', 'Urban', 'Urban', 'Semiurban', 'Urban', 'Semiurban',
                         'rural ', 'URBAN', 'semiurban', 'Urban', 'Rural', 'urban', 'RURAL', 'Semiurban', 'URBAN', 'rural'],
        'Loan_Status': ['Y', 'N', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'Y', 'N',
                       'y', 'N', 'Y', 'n', 'Y', 'y', 'N', 'Y', 'n', 'Y']
    }
    
    return pd.DataFrame(data)

def main():
    print("="*60)
    print("DATA CLEANING PIPELINE TEST")
    print("="*60)
    
    # Create messy test data
    df_messy = create_messy_test_data()
    
    print(f"\nOriginal messy data shape: {df_messy.shape}")
    print(f"Missing values: {df_messy.isnull().sum().sum()}")
    print(f"Memory usage: {df_messy.memory_usage(deep=True).sum()} bytes")
    
    print("\nSample of messy data:")
    print(df_messy.head(10))
    
    print("\nMissing values by column:")
    print(df_messy.isnull().sum())
    
    # Initialize and run pipeline
    pipeline = DataCleaningPipeline()
    df_clean = pipeline.clean_data(df_messy)
    
    print("\n" + "="*60)
    print("DETAILED CLEANING REPORT")
    print("="*60)
    
    for log_entry in pipeline.get_cleaning_report():
        print(f"• {log_entry}")
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    
    print(f"Cleaned data shape: {df_clean.shape}")
    print(f"Missing values after cleaning: {df_clean.isnull().sum().sum()}")
    print(f"Memory usage after cleaning: {df_clean.memory_usage(deep=True).sum()} bytes")
    
    print("\nSample of cleaned data:")
    print(df_clean.head(10))
    
    print("\nData types after cleaning:")
    print(df_clean.dtypes)
    
    # Save test results
    df_clean.to_csv("test_cleaned_data.csv", index=False)
    print("\n✓ Test results saved to 'test_cleaned_data.csv'")

if __name__ == '__main__':
    main()
