# Building a Diffusion Model From Scratch

Minimal DDPM-style training and sampling pipeline on MNIST using PyTorch.

## Overview

This project trains a lightweight U-Net to predict noise at random diffusion timesteps, then runs reverse denoising to generate handwritten digit samples.

The script also saves visual artifacts for:
- forward noising progression (`q_sample`)
- reverse denoising progression (`p_sample`)
- final generated digit samples

## Requirements

- Python 3.10+
- `torch`
- `torchvision`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run from this directory:

```bash
python diffusion_from_scratch.py
```

## Expected Outputs

After a successful run, these files are created:

- `generated_digit.png`
- `artifacts/forward_noising_steps.png`
- `artifacts/reverse_denoising_steps.png`
- `artifacts/generated_digits_grid.png`
- `artifacts/generated_digits_best9.png`
- `artifacts/generated_digit.png`

The script also prints a lightweight recognizability check comparing generated images against random-noise baseline:
- `Avg NN distance (generated)`
- `Avg NN distance (random)`

Lower distance is better; generated should be lower than random.

## Testing and Debugging

Primary smoke test:

```bash
python -u diffusion_from_scratch.py
```

A successful run must:
- exit with code `0`
- print loss logs for training steps
- print reverse-sampling save confirmations
- write all artifacts listed above

See [docs/TESTING.md](docs/TESTING.md) for test checklist and failure triage.

## Project Structure

```text
28_Building_a_Diffusion_Model_From_Scratch/
├── diffusion_from_scratch.py
├── requirements.txt
├── generated_digit.png
├── artifacts/
│   ├── forward_noising_steps.png
│   ├── reverse_denoising_steps.png
│   ├── generated_digits_grid.png
│   ├── generated_digits_best9.png
│   └── generated_digit.png
└── docs/
    ├── ARCHITECTURE.md
    ├── TESTING.md
    └── CHANGELOG.md
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Testing](docs/TESTING.md)
- [Changelog](docs/CHANGELOG.md)
