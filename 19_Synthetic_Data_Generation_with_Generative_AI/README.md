# Synthetic Data Generation with Generative AI
> Train a tabular GAN to generate synthetic app usage records from real screentime patterns.

## Tech Stack
- Python 3.10+
- PyTorch
- pandas, numpy
- scikit-learn (`MinMaxScaler`)

## Prerequisites
- Python 3
- `pip`
- CPU runtime is sufficient

## Installation
```bash
cd 19_Synthetic_Data_Generation_with_Generative_AI
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Getting Started
1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Run `python gan.py`.
4. Review generated rows in the console.
5. Open `synthetic_screentime_data.csv` for the final synthetic dataset.

## Usage
```bash
python gan.py
```

## Build Process
The full build/run process for this project is:
1. Environment setup:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
2. Training and generation:
```bash
python gan.py
```
3. Validation checks:
- GAN logs appear every 100 epochs
- synthetic sample rows are printed
- `synthetic_screentime_data.csv` is created/updated

## Project Structure
```text
19_Synthetic_Data_Generation_with_Generative_AI/
├── gan.py                             # Main GAN training + generation script
├── Screentime-App-Details.csv         # Input real data
├── synthetic_screentime_data.csv      # Generated synthetic rows
├── BUILD_FROM_SCRATCH.md              # Setup/run guide
├── BUILD_LOG.md                       # Verification notes
├── guide.txt                          # Lab brief
├── requirements.txt                   # Dependencies
└── docs/
    └── sdlc.md                        # SDLC status and lifecycle plan
```

## Architecture Overview
1. Load tabular screentime dataset.
2. Normalize numeric features to [0, 1].
3. Train discriminator to classify real/fake samples.
4. Train generator to fool discriminator.
5. Sample synthetic rows from trained generator.
6. Inverse-transform and save synthetic outputs.

## Environment Variables
| Name | Required | Description | Default |
|---|---|---|---|
| `PYTHONHASHSEED` | No | Optional deterministic hashing | unset |

## Running Tests
Smoke test:
```bash
python gan.py
```

Expected:
- GAN training logs every 100 epochs
- prints generated sample rows
- saves `synthetic_screentime_data.csv`

## SDLC Status
- Current phase: **Implementation and verification complete**
- Details: [`docs/sdlc.md`](./docs/sdlc.md)

## Troubleshooting
1. `ModuleNotFoundError` for `torch`/`pandas`/`sklearn`:
- Activate `.venv` and rerun `pip install -r requirements.txt`.
2. CUDA warnings on CPU-only machine:
- Safe to ignore; training runs on CPU.
3. Missing input CSV:
- Script auto-creates `Screentime-App-Details.csv`.
4. Output CSV not found:
- Ensure `gan.py` completed without interruption and check project root for `synthetic_screentime_data.csv`.

## Contributing
1. Keep generated feature ranges realistic with post-processing constraints.
2. Re-run smoke test after architecture/training changes.
3. Update `BUILD_LOG.md` when behavior changes.

## License
Project-level license is not explicitly defined. Follow repository owner guidance.
