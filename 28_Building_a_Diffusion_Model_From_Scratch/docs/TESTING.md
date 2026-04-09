# Testing and Debugging Guide

## Smoke Test Command

Run from project root:

```bash
python -u diffusion_from_scratch.py
```

## Pass Criteria

- Process exits with code `0`.
- Training logs appear (`Epoch 0, Step ... Loss: ...`).
- Reverse sampling completes.
- Files are written:
  - `generated_digit.png`
  - `artifacts/forward_noising_steps.png`
  - `artifacts/reverse_denoising_steps.png`
  - `artifacts/generated_digits_grid.png`
  - `artifacts/generated_digits_best9.png`
  - `artifacts/generated_digit.png`
- Metric check prints:
  - `Avg NN distance (generated): ...`
  - `Avg NN distance (random): ...`
  - Generated distance should be lower than random.

## Common Failures

### 1) Dataset download error

Symptom:
- `RuntimeError: Error downloading train-images-idx3-ubyte.gz`

Fix:
- Ensure internet access for first run.
- Re-run; MNIST is cached under `MNIST/raw/`.

### 2) CUDA initialization warning in CPU-only env

Symptom:
- `CUDA initialization ... operation not supported ...`

Fix:
- Script now safely falls back to CPU and suppresses this warning.

### 3) Slow runtime on CPU

Symptom:
- Long training/sampling time.

Fix:
- Reduce `train_steps_per_epoch` or `T` in `diffusion_from_scratch.py` for faster iteration.
