# Lab Project: Building Synthetic Medical Records using GANs

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
import os

def create_dummy_data():
    if not os.path.exists("Follow-up_Records.csv"):
        data = {
            'Age': np.random.randint(20, 80, 100),
            'Gender': np.random.choice(['Male', 'Female'], 100),
            'BMI': np.random.uniform(18.5, 40.0, 100),
            'Glucose': np.random.randint(70, 200, 100),
            'BloodPressure': np.random.randint(80, 180, 100),
        }
        df = pd.DataFrame(data)
        df.to_csv("Follow-up_Records.csv", index=False)

# 1. Preprocess data
create_dummy_data()
df = pd.read_csv("Follow-up_Records.csv")
df['Gender'] = df['Gender'].astype('category').cat.codes # Simple encoding
scaler = MinMaxScaler(feature_range=(-1, 1))
data_scaled = scaler.fit_transform(df)

# GAN parameters
data_dim = data_scaled.shape[1]
noise_dim = 10
batch_size = 32
epochs = 100 # Reduced for demonstration
lr = 0.0002
device = 'cuda' if torch.cuda.is_available() else 'cpu'


# DataLoader
dataloader = DataLoader(TensorDataset(torch.FloatTensor(data_scaled).to(device)), batch_size=batch_size, shuffle=True)

# 2. Build generator
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.Linear(noise_dim, 128), nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(128, 256), nn.BatchNorm1d(256), nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, data_dim), nn.Tanh()
        )
    def forward(self, input):
        return self.main(input)

# 3. Build discriminator
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.main = nn.Sequential(
            nn.Linear(data_dim, 256), nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 128), nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(128, 1), nn.Sigmoid()
        )
    def forward(self, input):
        return self.main(input)

generator = Generator().to(device)
discriminator = Discriminator().to(device)
adversarial_loss = nn.BCELoss()
optimizer_G = torch.optim.Adam(generator.parameters(), lr=lr)
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=lr)

# 4. Train
for epoch in range(epochs):
    for i, (real_data,) in enumerate(dataloader):
        # Train Discriminator
        optimizer_D.zero_grad()
        real_labels = torch.ones(real_data.size(0), 1).to(device)
        fake_labels = torch.zeros(real_data.size(0), 1).to(device)

        # loss with real data
        outputs = discriminator(real_data.to(device))
        d_loss_real = adversarial_loss(outputs, real_labels)

        # loss with fake data
        noise = torch.randn(real_data.size(0), noise_dim).to(device)
        fake_data = generator(noise)
        outputs = discriminator(fake_data.detach())
        d_loss_fake = adversarial_loss(outputs, fake_labels)

        d_loss = d_loss_real + d_loss_fake
        d_loss.backward()
        optimizer_D.step()

        # Train Generator
        optimizer_G.zero_grad()
        outputs = discriminator(fake_data)
        g_loss = adversarial_loss(outputs, real_labels)
        g_loss.backward()
        optimizer_G.step()
    if epoch % 10 == 0:
      print(f"Epoch [{epoch}/{epochs}], d_loss: {d_loss.item():.4f}, g_loss: {g_loss.item():.4f}")


# 5. Generate synthetic records
noise = torch.randn(10, noise_dim).to(device)
gen_data = generator(noise)
gen_data_unscaled = scaler.inverse_transform(gen_data.cpu().detach().numpy())

# Convert back to DataFrame
gen_df = pd.DataFrame(gen_data_unscaled, columns=df.columns)
gen_df['Gender'] = gen_df['Gender'].round().astype(int).map({0: 'Female', 1: 'Male'}) # Post-processing

print("\nGenerated Synthetic Medical Records:")
print(gen_df)
