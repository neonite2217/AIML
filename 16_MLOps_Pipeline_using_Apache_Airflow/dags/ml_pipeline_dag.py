"""
MLOps Pipeline DAG for Screentime Analysis

This DAG implements a complete ML pipeline with:
- Data preprocessing and feature engineering
- Model training with Random Forest Regressor
- Model evaluation with MAE metrics
- Comprehensive logging for observability

Author: MLOps Team
Version: 1.0.0
Date: 2026-03-25
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import os
import logging
import json
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
RAW_DATA_PATH = DATA_DIR / "screentime_analysis.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed_data.csv"
METRICS_PATH = ARTIFACTS_DIR / "metrics.json"
MODEL_PATH = ARTIFACTS_DIR / "model.pkl"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
ARTIFACTS_DIR.mkdir(exist_ok=True)


def create_dataset():
    """
    Create sample screentime analysis dataset.
    
    Generates synthetic data simulating app usage patterns:
    - days_since_install: Days since app installation (1-100)
    - app_usage_hours: Cumulative hours of app usage
    - user_rating: User rating (5.0 to 1.0, decreasing with usage)
    
    Returns:
        dict: Metadata about the created dataset
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Starting dataset creation task")
    
    if not RAW_DATA_PATH.exists():
        logger.info(f"Creating dataset at {RAW_DATA_PATH}")
        
        # Generate synthetic data
        n_samples = 100
        data = {
            'days_since_install': range(1, n_samples + 1),
            'app_usage_hours': [h * 1.5 for h in range(n_samples)],
            'user_rating': [5.0 - (x / (n_samples / 4)) for x in range(n_samples)]
        }
        
        df = pd.DataFrame(data)
        df.to_csv(RAW_DATA_PATH, index=False)
        
        dataset_info = {
            'path': str(RAW_DATA_PATH),
            'shape': df.shape,
            'columns': list(df.columns),
            'size_bytes': RAW_DATA_PATH.stat().st_size
        }
        
        logger.info(f"Dataset created: {dataset_info}")
        
        return dataset_info
    else:
        logger.info(f"Dataset already exists at {RAW_DATA_PATH}")
        df = pd.read_csv(RAW_DATA_PATH)
        
        dataset_info = {
            'path': str(RAW_DATA_PATH),
            'shape': df.shape,
            'columns': list(df.columns),
            'size_bytes': RAW_DATA_PATH.stat().st_size
        }
        
        return dataset_info


def preprocess_data():
    """
    Preprocess raw data for model training.
    
    Performs:
    1. Feature engineering: usage_per_day calculation
    2. Missing value imputation
    3. Feature scaling using StandardScaler
    4. Data validation
    
    Returns:
        dict: Preprocessing statistics and metadata
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Starting data preprocessing task")
    
    # Read raw data
    logger.info(f"Reading raw data from {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH)
    
    original_shape = df.shape
    logger.info(f"Original data shape: {original_shape}")
    
    # Feature engineering
    logger.info("Creating usage_per_day feature")
    df['usage_per_day'] = df['app_usage_hours'] / df['days_since_install']
    
    # Handle missing values
    missing_before = df.isnull().sum().sum()
    df.fillna(0, inplace=True)
    missing_after = df.isnull().sum().sum()
    
    logger.info(f"Missing values filled: {missing_before} -> {missing_after}")
    
    # Feature scaling
    logger.info("Applying feature scaling")
    scaler = StandardScaler()
    feature_cols = ['days_since_install', 'app_usage_hours', 'usage_per_day']
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    
    # Save processed data
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    
    preprocessing_stats = {
        'original_shape': original_shape,
        'processed_shape': df.shape,
        'features': list(df.columns),
        'missing_values_filled': missing_before,
        'processed_path': str(PROCESSED_DATA_PATH)
    }
    
    logger.info(f"Preprocessing complete: {preprocessing_stats}")
    
    return preprocessing_stats


def train_and_evaluate():
    """
    Train Random Forest Regressor and evaluate performance.
    
    Workflow:
    1. Load preprocessed data
    2. Split into train/test sets (80/20)
    3. Train Random Forest model
    4. Generate predictions
    5. Calculate metrics (MAE, MSE, R2)
    6. Save metrics and model artifacts
    
    Returns:
        dict: Model evaluation metrics
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Starting model training task")
    
    # Load processed data
    logger.info(f"Loading processed data from {PROCESSED_DATA_PATH}")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    # Prepare features and target
    feature_cols = ['days_since_install', 'usage_per_day']
    X = df[feature_cols]
    y = df['user_rating']
    
    logger.info(f"Feature matrix shape: {X.shape}, Target shape: {y.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    logger.info(f"Train set: {X_train.shape[0]} samples, Test set: {X_test.shape[0]} samples")
    
    # Train model
    logger.info("Training Random Forest Regressor (n_estimators=100)")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Generate predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'mean_absolute_error': round(mae, 4),
        'mean_squared_error': round(mse, 4),
        'root_mean_squared_error': round(rmse, 4),
        'r2_score': round(r2, 4),
        'n_estimators': 100,
        'test_samples': len(y_test),
        'training_samples': len(y_train)
    }
    
    logger.info("=" * 50)
    logger.info("MODEL EVALUATION METRICS")
    logger.info("=" * 50)
    logger.info(f"Mean Absolute Error (MAE): {mae:.4f}")
    logger.info(f"Mean Squared Error (MSE): {mse:.4f}")
    logger.info(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    logger.info(f"R2 Score: {r2:.4f}")
    logger.info("=" * 50)
    
    # Save metrics to JSON
    logger.info(f"Saving metrics to {METRICS_PATH}")
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Save model
    try:
        import joblib
        logger.info(f"Saving model to {MODEL_PATH}")
        joblib.dump(model, MODEL_PATH)
        metrics['model_saved'] = True
    except ImportError:
        logger.warning("joblib not available, model not saved")
        metrics['model_saved'] = False
    
    return metrics


# DAG Configuration
default_args = {
    'owner': 'mlops-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2026, 3, 25),
}

with DAG(
    'mlops_pipeline_screentime',
    default_args=default_args,
    description='Production-grade MLOps pipeline for screentime analysis with MAE evaluation',
    schedule=timedelta(days=1),
    catchup=False,
    tags=['mlops', 'machine-learning', 'screentime', 'production'],
    doc_md="""
    # MLOps Pipeline - Screentime Analysis
    
    This DAG implements a complete machine learning pipeline:
    
    ## Pipeline Stages
    
    1. **Data Creation** (`create_dataset`)
       - Generates synthetic screentime usage data
       - Creates CSV with days_since_install, app_usage_hours, user_rating
    
    2. **Preprocessing** (`preprocess_data`)
       - Feature engineering (usage_per_day)
       - Missing value imputation
       - Feature scaling with StandardScaler
    
    3. **Training & Evaluation** (`train_and_evaluate`)
       - Train Random Forest Regressor
       - Calculate MAE, MSE, RMSE, R2 metrics
       - Save metrics to artifacts/metrics.json
    
    ## Output Artifacts
    
    - `data/screentime_analysis.csv` - Raw dataset
    - `data/processed_data.csv` - Preprocessed dataset
    - `artifacts/metrics.json` - Evaluation metrics including MAE
    - `artifacts/model.pkl` - Trained model (if joblib available)
    
    ## Usage
    
    ```bash
    # Trigger DAG manually
    airflow dags trigger mlops_pipeline_screentime
    
    # Check task status
    airflow tasks list mlops_pipeline_screentime
    ```
    """
) as dag:
    
    # Task 1: Create Dataset
    create_data_task = PythonOperator(
        task_id='create_dataset',
        python_callable=create_dataset,
    )
    
    # Task 2: Preprocess Data
    preprocess_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
    )
    
    # Task 3: Train and Evaluate Model
    train_eval_task = PythonOperator(
        task_id='train_and_evaluate',
        python_callable=train_and_evaluate,
    )
    
    # Define task dependencies
    create_data_task >> preprocess_task >> train_eval_task
