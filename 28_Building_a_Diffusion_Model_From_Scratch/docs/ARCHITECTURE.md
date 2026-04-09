# Architecture

## Pipeline

1. Load MNIST images and normalize to `[-1, 1]`.
2. Define linear beta schedule across `T` timesteps.
3. Forward process (`q_sample`): add timestep-dependent Gaussian noise.
4. Train U-Net to predict added noise from noisy image + timestep.
5. Reverse process (`p_sample`): iteratively denoise from pure noise to sample.
6. Save process snapshots and final generated samples.
7. Run nearest-neighbor MNIST distance check for quick quality sanity check.

## Core Components

- `q_sample(x_0, t, noise)`: forward diffusion/noising.
- `UNet`: compact encoder-decoder for noise prediction.
- `p_sample(model, x, t, t_index)`: one reverse denoising step.
- `nearest_mnist_distance(samples)`: compares generated images with MNIST reference set.

## Inputs

- Dataset: MNIST (downloaded via `torchvision.datasets.MNIST`).

## Outputs

- Artifacts for forward/reverse dynamics and generated digits.
- Console metrics for generated-vs-random nearest-neighbor distance.
