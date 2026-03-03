from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import os

def create_dummy_data():
    if not os.path.exists('/tmp/screentime_analysis.csv'):
        data = {
            'days_since_install': range(1, 101),
            'app_usage_hours': [h * 1.5 for h in range(100)],
            'user_rating': [5 - (x/25) for x in range(100)]
        }
        df = pd.DataFrame(data)
        df.to_csv("/tmp/screentime_analysis.csv", index=False)


def preprocess_data_fn():
    create_dummy_data()
    df = pd.read_csv('/tmp/screentime_analysis.csv')
    df['usage_per_day'] = df['app_usage_hours'] / df['days_since_install']
    df.fillna(0, inplace=True)
    df.to_csv('/tmp/processed_data.csv', index=False)
    print("Preprocessing complete.")

def train_model_fn():
    df = pd.read_csv('/tmp/processed_data.csv')
    X = df[['days_since_install', 'usage_per_day']]
    y = df['user_rating']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Model MAE: {mae}")

    # In a real scenario, you would save the model
    # import joblib
    # joblib.dump(model, '/tmp/model.pkl')
    print("Model training complete.")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 1, 1),
}

with DAG(
    'ml_pipeline_dag',
    default_args=default_args,
    description='A simple MLOps pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    preprocess_data = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data_fn,
    )

    train_model = PythonOperator(
        task_id='train_model',
        python_callable=train_model_fn,
    )

    preprocess_data >> train_model
