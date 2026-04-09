# Changelog

All notable changes to this project are documented here.

## [Unreleased]

### Changed
- Improved `diffusion_from_scratch.py` for reliable smoke testing and artifact generation.
- Added safer CUDA detection with CPU fallback to avoid noisy CUDA-init warnings in CPU-only environments.

### Added
- Forward noising artifact export.
- Reverse denoising trajectory export.
- Generated sample grid and best-sample exports.
- Lightweight nearest-neighbor recognizability sanity check.
- Standard documentation set: `README.md`, `docs/ARCHITECTURE.md`, and `docs/TESTING.md`.
