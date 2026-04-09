# Lab Project: Building a Diffusion Model From Scratch

import math
import os
import random
import warnings

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
from torchvision.utils import save_image


# Hyperparameters
seed = 42
epochs = 1
train_steps_per_epoch = 200
batch_size = 128
num_samples = 16
T = 200
artifact_dir = "artifacts"
os.makedirs(artifact_dir, exist_ok=True)


def safe_cuda_available():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="CUDA initialization")
        try:
            return torch.cuda.is_available()
        except Exception:
            return False


device = "cuda" if safe_cuda_available() else "cpu"

random.seed(seed)
torch.manual_seed(seed)
if device == "cuda":
    torch.cuda.manual_seed_all(seed)
torch.set_num_threads(min(4, os.cpu_count() or 1))


# Load MNIST
transform = transforms.Compose(
    [
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),
    ]
)
dataset = MNIST(".", train=True, download=True, transform=transform)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
print(f"Device: {device}")


# 1. Define beta schedule
betas = torch.linspace(1e-4, 0.02, T, device=device)
alphas = 1.0 - betas
alphas_cumprod = torch.cumprod(alphas, axis=0)


# 2. Implement forward noising (q_sample)
def q_sample(x_0, t, noise=None):
    if noise is None:
        noise = torch.randn_like(x_0)
    sqrt_alphas_cumprod_t = torch.sqrt(alphas_cumprod[t.cpu()]).to(device)[:, None, None, None]
    sqrt_one_minus_alphas_cumprod_t = torch.sqrt(1.0 - alphas_cumprod[t.cpu()]).to(device)[
        :, None, None, None
    ]
    return sqrt_alphas_cumprod_t * x_0 + sqrt_one_minus_alphas_cumprod_t * noise


# Save forward noising artifact before training.
vis_image = dataset[0][0].unsqueeze(0).to(device)
vis_steps = torch.tensor([0, T // 4, T // 2, (3 * T) // 4, T - 1], device=device).long()
vis_noised = q_sample(vis_image.repeat(vis_steps.shape[0], 1, 1, 1), vis_steps)
save_image(
    torch.cat([vis_image, vis_noised], dim=0),
    os.path.join(artifact_dir, "forward_noising_steps.png"),
    nrow=6,
    normalize=True,
)
print(f"Saved forward noising artifact: {artifact_dir}/forward_noising_steps.png")


# 3. Implement U-Net (simplified)
class UNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.enc1 = nn.Sequential(nn.Conv2d(1, 32, 3, padding=1), nn.ReLU())
        self.enc2 = nn.Sequential(nn.Conv2d(32, 64, 3, padding=1), nn.ReLU())
        self.pool = nn.MaxPool2d(2, 2)
        self.bottleneck = nn.Sequential(nn.Conv2d(64, 64, 3, padding=1), nn.ReLU())
        self.up1 = nn.ConvTranspose2d(64, 64, 2, stride=2)
        self.dec1 = nn.Sequential(nn.Conv2d(64 + 64, 64, 3, padding=1), nn.ReLU())
        self.up2 = nn.ConvTranspose2d(64, 32, 2, stride=2)
        self.dec2 = nn.Sequential(nn.Conv2d(32 + 32, 32, 3, padding=1), nn.ReLU())
        self.out = nn.Conv2d(32, 1, 1)

    def forward(self, x, t):
        # Timestep conditioning is omitted for simplicity.
        del t
        s1 = self.enc1(x)
        x = self.pool(s1)
        s2 = self.enc2(x)
        x = self.pool(s2)
        x = self.bottleneck(x)
        x = self.up1(x)
        x = self.dec1(torch.cat([x, s2], dim=1))
        x = self.up2(x)
        x = self.dec2(torch.cat([x, s1], dim=1))
        return self.out(x)


model = UNet().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=5e-4)
loss_fn = nn.MSELoss()


# 5. Train
for epoch in range(epochs):
    for step, (images, _) in enumerate(dataloader):
        if step >= train_steps_per_epoch:
            break
        optimizer.zero_grad()
        images = images.to(device)
        t = torch.randint(0, T, (images.shape[0],), device=device).long()
        noise = torch.randn_like(images)
        x_t = q_sample(images, t, noise)
        predicted_noise = model(x_t, t)
        loss = loss_fn(noise, predicted_noise)
        loss.backward()
        optimizer.step()
        if step % 50 == 0:
            print(f"Epoch {epoch}, Step {step}, Loss: {loss.item():.6f}")


# 6. Generate digits (reverse denoising)
@torch.no_grad()
def p_sample(model, x, t, t_index):
    betas_t = betas[t_index]
    sqrt_one_minus_alphas_cumprod_t = torch.sqrt(1.0 - alphas_cumprod[t_index])
    sqrt_recip_alphas_t = torch.sqrt(1.0 / alphas[t_index])
    model_mean = sqrt_recip_alphas_t * (x - betas_t * model(x, t) / sqrt_one_minus_alphas_cumprod_t)
    if t_index == 0:
        return model_mean
    posterior_variance_t = betas_t
    noise = torch.randn_like(x)
    return model_mean + torch.sqrt(posterior_variance_t) * noise


img = torch.randn(num_samples, 1, 32, 32, device=device)
trace_indices = sorted({T - 1, int(0.75 * (T - 1)), int(0.5 * (T - 1)), int(0.25 * (T - 1)), 0}, reverse=True)
trace_frames = []
for i in reversed(range(T)):
    t_batch = torch.full((num_samples,), i, device=device, dtype=torch.long)
    img = p_sample(model, img, t_batch, i)
    if i in trace_indices:
        trace_frames.append(img[:1].detach().cpu())

trace_tensor = torch.cat(trace_frames, dim=0)
save_image(
    trace_tensor,
    os.path.join(artifact_dir, "reverse_denoising_steps.png"),
    nrow=trace_tensor.shape[0],
    normalize=True,
)
save_image(
    img.detach().cpu(),
    os.path.join(artifact_dir, "generated_digits_grid.png"),
    nrow=int(math.sqrt(num_samples)),
    normalize=True,
)
save_image(img[:1].detach().cpu(), "generated_digit.png", normalize=True)
save_image(img[:1].detach().cpu(), os.path.join(artifact_dir, "generated_digit.png"), normalize=True)


# 7. Lightweight recognizability check with nearest-neighbor distance.
@torch.no_grad()
def nearest_mnist_distance(samples, ref_count=1000):
    ref_images = torch.stack([dataset[i][0] for i in range(ref_count)], dim=0)
    ref_images = F.interpolate(ref_images, size=(28, 28), mode="bilinear", align_corners=False)
    ref_images = ((ref_images.clamp(-1, 1) + 1.0) / 2.0).view(ref_count, -1).cpu()
    ref_labels = torch.tensor([dataset[i][1] for i in range(ref_count)], dtype=torch.long)

    samples_28 = F.interpolate(samples, size=(28, 28), mode="bilinear", align_corners=False)
    samples_flat = ((samples_28.clamp(-1, 1) + 1.0) / 2.0).view(samples_28.shape[0], -1).cpu()

    dists = torch.cdist(samples_flat, ref_images, p=2)
    nn_dist, nn_idx = torch.min(dists, dim=1)
    return nn_dist, ref_labels[nn_idx]


nn_dist, nn_labels = nearest_mnist_distance(img.detach().cpu())
rand_dist, _ = nearest_mnist_distance(torch.randn_like(img).cpu())
label_hist = torch.bincount(nn_labels, minlength=10)
best_idx = torch.argsort(nn_dist)[:9]
save_image(
    img[best_idx].detach().cpu(),
    os.path.join(artifact_dir, "generated_digits_best9.png"),
    nrow=3,
    normalize=True,
)

print(f"Saved reverse denoising artifact: {artifact_dir}/reverse_denoising_steps.png")
print(f"Saved generated grid artifact: {artifact_dir}/generated_digits_grid.png")
print(f"Saved best-samples artifact: {artifact_dir}/generated_digits_best9.png")
print("Generated digit saved to generated_digit.png")
print(f"Avg NN distance (generated): {nn_dist.mean().item():.4f}")
print(f"Avg NN distance (random): {rand_dist.mean().item():.4f}")
print(f"Nearest-neighbor label histogram: {label_hist.tolist()}")
