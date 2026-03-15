# Lab Project: Synthetic Data Generation with Generative AI
# PyTorch implementation of a simple tabular GAN for app usage data.

import os
import random

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

SEED = 42
DATA_FILE = "Screentime-App-Details.csv"
OUTPUT_FILE = "synthetic_screentime_data.csv"

FEATURES = ["Usage", "Notifications", "Times opened"]
NOISE_DIM = 10
BATCH_SIZE = 32
EPOCHS = 400
LR = 2e-4


def set_seed(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def create_dummy_data(path=DATA_FILE):
    if os.path.exists(path):
        return

    n = 100
    df = pd.DataFrame(
        {
            "Usage": np.random.randint(1, 1000, n),
            "Notifications": np.random.randint(0, 50, n),
            "Times opened": np.random.randint(1, 100, n),
            "Date": pd.date_range(start="2023-01-01", periods=n, freq="D"),
            "App": np.random.choice(["App1", "App2", "App3"], n),
        }
    )
    df.to_csv(path, index=False)


class Generator(nn.Module):
    def __init__(self, noise_dim, out_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(noise_dim, 128),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(128),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(128),
            nn.Linear(128, out_dim),
            nn.Sigmoid(),
        )

    def forward(self, z):
        return self.net(z)


class Discriminator(nn.Module):
    def __init__(self, in_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)


def sample_real_batch(data_tensor, batch_size):
    idx = torch.randint(0, data_tensor.shape[0], (batch_size,))
    return data_tensor[idx]


def main():
    set_seed()
    create_dummy_data()

    print("=" * 60)
    print("Synthetic Data Generation with GAN (PyTorch)")
    print("=" * 60)

    # 1. Load dataset and select numeric features
    df = pd.read_csv(DATA_FILE)
    data_to_generate = df[FEATURES]

    # 2. Normalize features to [0, 1]
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data_to_generate.values)
    data_tensor = torch.tensor(data_scaled, dtype=torch.float32)

    data_dim = len(FEATURES)

    # 3-4. Build generator and discriminator
    generator = Generator(NOISE_DIM, data_dim)
    discriminator = Discriminator(data_dim)

    criterion = nn.BCELoss()
    opt_d = torch.optim.Adam(discriminator.parameters(), lr=LR, betas=(0.5, 0.999))
    opt_g = torch.optim.Adam(generator.parameters(), lr=LR, betas=(0.5, 0.999))

    # 5. Train GAN
    for epoch in range(EPOCHS):
        # Train Discriminator
        real_data = sample_real_batch(data_tensor, BATCH_SIZE)
        real_labels = torch.ones((BATCH_SIZE, 1), dtype=torch.float32)
        fake_labels = torch.zeros((BATCH_SIZE, 1), dtype=torch.float32)

        z = torch.randn((BATCH_SIZE, NOISE_DIM), dtype=torch.float32)
        fake_data = generator(z).detach()

        opt_d.zero_grad()
        d_real = discriminator(real_data)
        d_fake = discriminator(fake_data)
        d_loss_real = criterion(d_real, real_labels)
        d_loss_fake = criterion(d_fake, fake_labels)
        d_loss = 0.5 * (d_loss_real + d_loss_fake)
        d_loss.backward()
        opt_d.step()

        # Train Generator
        z = torch.randn((BATCH_SIZE, NOISE_DIM), dtype=torch.float32)
        opt_g.zero_grad()
        generated = generator(z)
        g_loss = criterion(discriminator(generated), real_labels)
        g_loss.backward()
        opt_g.step()

        if epoch % 100 == 0:
            d_acc = ((d_real >= 0.5).float().mean() + (d_fake < 0.5).float().mean()) * 50.0
            print(
                f"{epoch:04d} [D loss: {d_loss.item():.4f} | D accuracy: {d_acc.item():.2f}%] "
                f"[G loss: {g_loss.item():.4f}]"
            )

    # 6. Generate synthetic samples and inverse transform
    with torch.no_grad():
        z = torch.randn((20, NOISE_DIM), dtype=torch.float32)
        gen_scaled = generator(z).numpy()

    gen_unscaled = scaler.inverse_transform(gen_scaled)
    synthetic_df = pd.DataFrame(gen_unscaled, columns=FEATURES)

    # Keep values in reasonable numeric ranges and cast to int-like values.
    synthetic_df["Usage"] = synthetic_df["Usage"].clip(lower=0).round().astype(int)
    synthetic_df["Notifications"] = synthetic_df["Notifications"].clip(lower=0).round().astype(int)
    synthetic_df["Times opened"] = synthetic_df["Times opened"].clip(lower=0).round().astype(int)

    synthetic_df.to_csv(OUTPUT_FILE, index=False)

    print("\nGenerated Data (first 10 rows):")
    print(synthetic_df.head(10).to_string(index=False))

    print("\nReal vs Synthetic Means:")
    summary = pd.DataFrame(
        {
            "real_mean": data_to_generate.mean(),
            "synthetic_mean": synthetic_df.mean(),
        }
    )
    print(summary)

    print(f"\nSaved synthetic data to: {OUTPUT_FILE}")
    print("Training and generation complete.")


if __name__ == "__main__":
    main()
