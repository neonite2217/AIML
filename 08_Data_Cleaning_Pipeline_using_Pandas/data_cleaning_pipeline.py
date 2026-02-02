import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataCleaningPipeline:
    def __init__(self):
        self.cleaning_log = []
        
    def log_operation(self, operation: str, details: str):
        """Log cleaning operations for transparency"""
        log_entry = f"{operation}: {details}"
        self.cleaning_log.append(log_entry)
        logging.info(log_entry)
    
    def inspect_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Inspect schema and missing values"""
        inspection = {
            'shape': df.shape,
            'missing_values': df.isnull().sum().to_dict(),
            'dtypes': df.dtypes.to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum()
        }
        self.log_operation("Data Inspection", f"Shape: {inspection['shape']}, Missing values: {sum(inspection['missing_values'].values())}")
        return inspection
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute missing values: categorical with mode, numeric with median"""
        df = df.copy()
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'string']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                missing_count = df[col].isnull().sum()
                df[col] = df[col].fillna(mode_val)
                self.log_operation("Missing Value Imputation", f"{col}: {missing_count} values filled with mode '{mode_val}'")
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                median_val = df[col].median()
                missing_count = df[col].isnull().sum()
                df[col] = df[col].fillna(median_val)
                self.log_operation("Missing Value Imputation", f"{col}: {missing_count} values filled with median {median_val}")
        
        return df
    
    def fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fix and optimize column data types"""
        df = df.copy()
        
        # Convert Credit_History to int if it exists
        if 'Credit_History' in df.columns:
            df['Credit_History'] = pd.to_numeric(df['Credit_History'], errors='coerce').fillna(1).astype(int)
            self.log_operation("Data Type Fix", "Credit_History converted to int")
        
        # Convert Loan_Amount_Term to int if it exists
        if 'Loan_Amount_Term' in df.columns:
            df['Loan_Amount_Term'] = pd.to_numeric(df['Loan_Amount_Term'], errors='coerce').fillna(360).astype(int)
            self.log_operation("Data Type Fix", "Loan_Amount_Term converted to int")
        
        # Optimize numeric types for memory efficiency
        for col in df.select_dtypes(include=[np.number]).columns:
            if df[col].dtype == 'int64':
                if df[col].min() >= 0 and df[col].max() <= 65535:
                    df[col] = df[col].astype('uint16')
                elif df[col].min() >= -32768 and df[col].max() <= 32767:
                    df[col] = df[col].astype('int16')
                elif df[col].min() >= -2147483648 and df[col].max() <= 2147483647:
                    df[col] = df[col].astype('int32')
            elif df[col].dtype == 'float64':
                df[col] = pd.to_numeric(df[col], downcast='float')
        
        self.log_operation("Memory Optimization", "Numeric types optimized")
        return df
    
    def standardize_strings(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize string data: trim whitespace and convert to consistent case"""
        df = df.copy()
        
        string_cols = df.select_dtypes(include=['object', 'string']).columns
        for col in string_cols:
            if col != 'Loan_ID':  # Keep ID columns as-is
                original_unique = df[col].nunique()
                df[col] = df[col].astype(str).str.strip().str.title()
                new_unique = df[col].nunique()
                self.log_operation("String Standardization", f"{col}: {original_unique} -> {new_unique} unique values")
        
        return df
    
    def handle_outliers(self, df: pd.DataFrame, percentile: float = 0.99) -> pd.DataFrame:
        """Cap outliers using percentile-based approach"""
        df = df.copy()
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        outlier_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']
        
        for col in outlier_cols:
            if col in numeric_cols:
                q_low = df[col].quantile(1 - percentile)
                q_high = df[col].quantile(percentile)
                
                outliers_low = (df[col] < q_low).sum()
                outliers_high = (df[col] > q_high).sum()
                
                df[col] = df[col].clip(lower=q_low, upper=q_high)
                
                if outliers_low + outliers_high > 0:
                    self.log_operation("Outlier Handling", f"{col}: {outliers_low + outliers_high} outliers capped")
        
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Main cleaning pipeline function"""
        self.cleaning_log = []
        self.log_operation("Pipeline Start", f"Processing dataset with shape {df.shape}")
        
        # Step 1: Inspect data
        initial_inspection = self.inspect_data(df)
        
        # Step 2: Handle missing values
        df_cleaned = self.handle_missing_values(df)
        
        # Step 3: Fix data types
        df_cleaned = self.fix_data_types(df_cleaned)
        
        # Step 4: Standardize strings
        df_cleaned = self.standardize_strings(df_cleaned)
        
        # Step 5: Handle outliers
        df_cleaned = self.handle_outliers(df_cleaned)
        
        # Final inspection
        final_inspection = self.inspect_data(df_cleaned)
        memory_saved = initial_inspection['memory_usage'] - final_inspection['memory_usage']
        self.log_operation("Pipeline Complete", f"Memory saved: {memory_saved} bytes")
        
        return df_cleaned
    
    def get_cleaning_report(self) -> List[str]:
        """Return detailed cleaning report"""
        return self.cleaning_log

def main():
    # Load data
    try:
        df = pd.read_csv("loan_prediction.csv")
        print("✓ Dataset loaded successfully")
    except FileNotFoundError:
        print("✗ loan_prediction.csv not found")
        return
    
    # Initialize pipeline
    pipeline = DataCleaningPipeline()
    
    # Clean data
    print("\n" + "="*50)
    print("STARTING DATA CLEANING PIPELINE")
    print("="*50)
    
    cleaned_df = pipeline.clean_data(df)
    
    # Display results
    print("\n" + "="*50)
    print("CLEANING SUMMARY")
    print("="*50)
    
    print(f"Original shape: {df.shape}")
    print(f"Cleaned shape: {cleaned_df.shape}")
    print(f"Missing values before: {df.isnull().sum().sum()}")
    print(f"Missing values after: {cleaned_df.isnull().sum().sum()}")
    
    # Save cleaned data
    cleaned_df.to_csv("loan_prediction_cleaned.csv", index=False)
    print("\n✓ Cleaned data saved to 'loan_prediction_cleaned.csv'")
    
    # Display sample
    print("\nCleaned data sample:")
    print(cleaned_df.head())

if __name__ == '__main__':
    main()
