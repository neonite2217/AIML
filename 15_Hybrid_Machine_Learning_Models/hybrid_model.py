# Lab Project: Hybrid Machine Learning Models
# Hybrid forecasting using PyTorch LSTM + Linear Regression ensemble.

import os
import random

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

SEED = 42
DATA_FILE = "apple_stock_data.csv"
OUTPUT_FILE = "hybrid_predictions.csv"
TIME_STEP = 30
EPOCHS = 40
LEARNING_RATE = 1e-2


class LSTMRegressor(nn.Module):
    def __init__(self, input_size=1, hidden_size=32, num_layers=1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])


def set_seed(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def create_dummy_data(path=DATA_FILE):
    if os.path.exists(path):
        return
    dates = pd.date_range(start="2020-01-01", periods=200, freq="D")
    close = 100 + np.cumsum(np.random.randn(len(dates)))
    pd.DataFrame({"Date": dates, "Close": close}).to_csv(path, index=False)


def create_sequences(array_2d, time_step):
    x_data = []
    y_data = []
    for i in range(len(array_2d) - time_step - 1):
        x_data.append(array_2d[i : i + time_step, 0])
        y_data.append(array_2d[i + time_step, 0])
    return np.array(x_data), np.array(y_data)


def train_lstm_model(scaled_close, time_step):
    x_np, y_np = create_sequences(scaled_close, time_step)
    if x_np.size == 0:
        return np.array([])

    x_tensor = torch.tensor(x_np, dtype=torch.float32).unsqueeze(-1)
    y_tensor = torch.tensor(y_np, dtype=torch.float32).unsqueeze(-1)

    model = LSTMRegressor()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    model.train()
    for _ in range(EPOCHS):
        optimizer.zero_grad()
        preds = model(x_tensor)
        loss = criterion(preds, y_tensor)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        pred_scaled = model(x_tensor).numpy().flatten()
    return pred_scaled


def main():
    set_seed()
    create_dummy_data()

    # 1. Prepare data
    df = pd.read_csv(DATA_FILE, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_close = scaler.fit_transform(df[["Close"]].values)

    # 2-3. Train LSTM model
    # Use a dynamic window for small datasets.
    effective_time_step = min(TIME_STEP, max(3, len(df) // 2))

    lstm_pred_scaled = train_lstm_model(scaled_close, effective_time_step)
    if len(lstm_pred_scaled) > 0:
        lstm_preds = scaler.inverse_transform(lstm_pred_scaled.reshape(-1, 1)).flatten()
    else:
        lstm_preds = np.array([])

    # 4-5. Train linear regression on lag features
    df_lr = df.copy()
    df_lr["lag_1"] = df_lr["Close"].shift(1)
    df_lr["lag_2"] = df_lr["Close"].shift(2)
    df_lr["lag_3"] = df_lr["Close"].shift(3)
    df_lr = df_lr.dropna().reset_index(drop=True)

    x_lr = df_lr[["lag_1", "lag_2", "lag_3"]]
    y_lr = df_lr["Close"]

    lr_model = LinearRegression()
    lr_model.fit(x_lr, y_lr)
    lr_preds = lr_model.predict(x_lr)

    # 6. Combine predictions (simple average ensemble)
    if len(lstm_preds) == 0:
        print("Not enough data for LSTM sequences; showing linear predictions only.")
        print("Linear Regression Predictions (first 5):", lr_preds[:5])
        return

    min_len = min(len(lstm_preds), len(lr_preds))
    lstm_use = lstm_preds[-min_len:]
    lr_use = lr_preds[-min_len:]
    hybrid_preds = (lstm_use + lr_use) / 2.0

    dates = (
        df["Date"]
        .iloc[effective_time_step + 1 : effective_time_step + 1 + len(lstm_preds)]
        .iloc[-min_len:]
        .reset_index(drop=True)
    )

    output_df = pd.DataFrame(
        {
            "Date": dates,
            "lstm_prediction": lstm_use,
            "linear_prediction": lr_use,
            "hybrid_prediction": hybrid_preds,
        }
    )
    output_df.to_csv(OUTPUT_FILE, index=False)

    print("LSTM Predictions (first 5):", np.round(lstm_use[:5], 4))
    print("Linear Regression Predictions (first 5):", np.round(lr_use[:5], 4))
    print("Hybrid Predictions (first 5):", np.round(hybrid_preds[:5], 4))
    print(f"Saved predictions to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
