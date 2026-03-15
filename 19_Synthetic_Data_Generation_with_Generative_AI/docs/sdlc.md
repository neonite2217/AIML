# SDLC - Synthetic Data Generation with Generative AI

## 1. Requirements
### Functional
- Load real tabular app-usage data.
- Train GAN to generate synthetic numeric feature rows.
- Produce inverse-scaled synthetic outputs for analysis.

### Non-Functional
- CPU-friendly execution.
- Stable training signal for small sample datasets.
- Reproducible generation behavior.

## 2. Design
- Two-network adversarial setup:
  - Generator: noise -> synthetic tabular row
  - Discriminator: row -> real/fake score
- Feature scaling via `MinMaxScaler` for stable adversarial training.
- Output constraints applied after inverse transform.

## 3. Implementation
- Replaced TensorFlow dependency path with PyTorch GAN implementation for environment compatibility.
- Added deterministic seeding.
- Added synthetic CSV export and summary statistics printout.

## 4. Verification
Verified on 2026-03-17:
- `python gan.py` -> PASS
- Generated `synthetic_screentime_data.csv`
- Printed training checkpoints and real-vs-synthetic mean comparison

## 5. Deployment / Runtime
- Local CLI batch generation flow.
- Generated synthetic CSV can be consumed by downstream experiments.

## 6. Maintenance
- Keep scaling and inverse-scaling logic synchronized with selected features.
- Revalidate synthetic quality metrics when architecture changes.

## 7. Risks and Mitigation
- Risk: unstable GAN dynamics on tiny datasets.
  - Mitigation: bounded training epochs, value clipping, and data sanity checks.
- Risk: unrealistic synthetic rows.
  - Mitigation: post-process with rounding and non-negative clipping.

## 8. Current SDLC Phase (2026-03-17)
- Requirements: Complete
- Design: Complete
- Implementation: Complete
- Verification: Complete
- Documentation: Complete
- Status: Ready / Completed
