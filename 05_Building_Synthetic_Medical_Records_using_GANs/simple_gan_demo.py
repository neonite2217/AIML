#!/usr/bin/env python3
"""
Simplified Medical Records GAN - Demo Version
Demonstrates GAN concepts without external dependencies
"""

import random
import math
import csv
import os

class SimpleGAN:
    def __init__(self, data_dim=5, noise_dim=10):
        self.data_dim = data_dim
        self.noise_dim = noise_dim
        self.generator_weights = [[random.uniform(-1, 1) for _ in range(noise_dim)] for _ in range(data_dim)]
        self.discriminator_weights = [[random.uniform(-1, 1) for _ in range(data_dim)] for _ in range(1)]

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-max(-500, min(500, x))))

    def tanh(self, x):
        return math.tanh(max(-500, min(500, x)))

    def generate_fake_data(self, noise):
        """Simple generator: linear transformation + tanh"""
        output = []
        for i in range(self.data_dim):
            val = sum(noise[j] * self.generator_weights[i][j] for j in range(self.noise_dim))
            output.append(self.tanh(val))
        return output

    def discriminate(self, data):
        """Simple discriminator: linear transformation + sigmoid"""
        val = sum(data[i] * self.discriminator_weights[0][i] for i in range(self.data_dim))
        return self.sigmoid(val)

    def train_step(self, real_data_batch):
        """Simplified training step"""
        # Train discriminator
        for real_data in real_data_batch:
            # Real data should get score close to 1
            d_real = self.discriminate(real_data)
            d_error_real = 1 - d_real

            # Fake data should get score close to 0
            noise = [random.gauss(0, 1) for _ in range(self.noise_dim)]
            fake_data = self.generate_fake_data(noise)
            d_fake = self.discriminate(fake_data)
            d_error_fake = d_fake

            # Simple weight update (gradient descent approximation)
            lr = 0.01
            for i in range(self.data_dim):
                self.discriminator_weights[0][i] += lr * (d_error_real * real_data[i] - d_error_fake * fake_data[i])

        # Train generator
        noise = [random.gauss(0, 1) for _ in range(self.noise_dim)]
        fake_data = self.generate_fake_data(noise)
        d_fake = self.discriminate(fake_data)
        g_error = 1 - d_fake  # Generator wants discriminator to output 1

        # Update generator weights
        for i in range(self.data_dim):
            for j in range(self.noise_dim):
                self.generator_weights[i][j] += lr * g_error * noise[j]

def create_sample_data():
    """Create sample medical records"""
    if not os.path.exists("Follow-up_Records.csv"):
        with open("Follow-up_Records.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Age', 'Gender', 'BMI', 'Glucose', 'BloodPressure'])

            for _ in range(100):
                age = random.randint(20, 80)
                gender = random.choice([0, 1])  # 0=Female, 1=Male
                bmi = random.uniform(18.5, 40.0)
                glucose = random.randint(70, 200)
                bp = random.randint(80, 180)
                writer.writerow([age, gender, bmi, glucose, bp])

def normalize_data(data):
    """Simple min-max normalization to [-1, 1]"""
    # Find min/max for each feature
    mins = [min(row[i] for row in data) for i in range(len(data[0]))]
    maxs = [max(row[i] for row in data) for i in range(len(data[0]))]

    normalized = []
    for row in data:
        norm_row = []
        for i, val in enumerate(row):
            # Scale to [-1, 1]
            norm_val = 2 * (val - mins[i]) / (maxs[i] - mins[i]) - 1
            norm_row.append(norm_val)
        normalized.append(norm_row)

    return normalized, mins, maxs

def denormalize_data(data, mins, maxs):
    """Convert back from [-1, 1] to original scale"""
    denormalized = []
    for row in data:
        denorm_row = []
        for i, val in enumerate(row):
            # Scale back from [-1, 1]
            orig_val = (val + 1) / 2 * (maxs[i] - mins[i]) + mins[i]
            denorm_row.append(orig_val)
        denormalized.append(denorm_row)
    return denormalized

def main():
    print("Building Synthetic Medical Records using GANs")
    print("=" * 50)

    # Create sample data
    create_sample_data()

    # Load data
    data = []
    with open("Follow-up_Records.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gender_code = 1.0 if row['Gender'] == 'Male' else 0.0
            data.append([
                float(row['Age']),
                gender_code,
                float(row['BMI']),
                float(row['Glucose']),
                float(row['BloodPressure'])
            ])

    print(f"Loaded {len(data)} real medical records")

    # Normalize data
    normalized_data, mins, maxs = normalize_data(data)

    # Initialize GAN
    gan = SimpleGAN()

    # Training
    print("\nTraining GAN...")
    epochs = 50
    batch_size = 10

    for epoch in range(epochs):
        # Shuffle data
        random.shuffle(normalized_data)

        # Train in batches
        for i in range(0, len(normalized_data), batch_size):
            batch = normalized_data[i:i+batch_size]
            gan.train_step(batch)

        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{epochs} completed")

    # Generate synthetic records
    print("\nGenerating synthetic medical records...")
    synthetic_records = []

    for _ in range(10):
        noise = [random.gauss(0, 1) for _ in range(gan.noise_dim)]
        fake_record = gan.generate_fake_data(noise)
        synthetic_records.append(fake_record)

    # Denormalize
    synthetic_denorm = denormalize_data(synthetic_records, mins, maxs)

    # Display results
    print("\nSynthetic Medical Records Generated:")
    print("-" * 60)
    print(f"{'Age':<5} {'Gender':<8} {'BMI':<6} {'Glucose':<8} {'BloodPressure'}")
    print("-" * 60)

    for record in synthetic_denorm:
        age = int(max(20, min(80, record[0])))
        gender = "Male" if record[1] > 0 else "Female"
        bmi = max(18.5, min(40.0, record[2]))
        glucose = int(max(70, min(200, record[3])))
        bp = int(max(80, min(180, record[4])))

        print(f"{age:<5} {gender:<8} {bmi:<6.1f} {glucose:<8} {bp}")

    print(f"\nSynthetic data generation completed!")
    print("Check log.txt for detailed build information.")

if __name__ == "__main__":
    main()
