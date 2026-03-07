import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.var_model import VAR
import matplotlib.pyplot as plt
from db import init_db, load_data, fetch_data

def check_stationarity(series, name):
    result = adfuller(series.dropna())
    print(f"{name}: ADF Statistic = {result[0]:.4f}, p-value = {result[1]:.4f}")
    return result[1] < 0.05

def main():
    # Initialize DB and load data
    print("Initializing database...")
    init_db()
    
    print("Loading data into TimescaleDB...")
    load_data('stocks.csv')
    
    print("Fetching data from database...")
    df = fetch_data()
    
    # Pivot to wide format
    df_wide = df.pivot(index='time', columns='ticker', values='close')
    print(f"\nData shape: {df_wide.shape}")
    print(f"Tickers: {df_wide.columns.tolist()}")
    
    # Check stationarity
    print("\nChecking stationarity (original):")
    for col in df_wide.columns:
        check_stationarity(df_wide[col], col)
    
    # Difference the series
    df_diff = df_wide.diff().dropna()
    
    print("\nChecking stationarity (differenced):")
    for col in df_diff.columns:
        check_stationarity(df_diff[col], col)
    
    # Fit VAR model
    model = VAR(df_diff)
    results = model.fit(maxlags=2)
    print(f"\nVAR Model Summary:")
    print(results.summary())
    
    # Forecast
    n_forecast = 3
    forecast_diff = results.forecast(df_diff.values[-results.k_ar:], steps=n_forecast)
    
    # Reverse differencing
    last_values = df_wide.iloc[-1].values
    forecast_original = np.cumsum(np.vstack([last_values, forecast_diff]), axis=0)[1:]
    
    # Create forecast dataframe
    forecast_dates = pd.date_range(start=df_wide.index[-1], periods=n_forecast+1, freq='D')[1:]
    forecast_df = pd.DataFrame(forecast_original, index=forecast_dates, columns=df_wide.columns)
    
    print(f"\nForecast:")
    print(forecast_df)
    
    # Plot
    plt.figure(figsize=(12, 6))
    for col in df_wide.columns:
        plt.plot(df_wide.index, df_wide[col], label=f'{col} (Actual)', marker='o')
        plt.plot(forecast_df.index, forecast_df[col], label=f'{col} (Forecast)', marker='x', linestyle='--')
    
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Multivariate Time Series Forecasting with VAR')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('forecast_plot.png')
    print("\nPlot saved as 'forecast_plot.png'")

if __name__ == '__main__':
    main()
