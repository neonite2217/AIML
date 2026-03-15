# Build From Scratch - Project 19

## 1. Setup
```bash
cd 19_Synthetic_Data_Generation_with_Generative_AI
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Run
```bash
python gan.py
```

## 3. Expected Outputs
- GAN progress logs (`epoch`, `D loss`, `D accuracy`, `G loss`)
- Printed generated rows preview
- Printed real vs synthetic means
- Output file: `synthetic_screentime_data.csv`

## 4. Notes
- If source CSV is missing, script auto-generates dummy input data.
- Script uses PyTorch GAN implementation and runs on CPU.

## 5. Common Troubleshooting
1. `ModuleNotFoundError`:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```
2. CUDA warning messages:
- Non-blocking in CPU environments; can be ignored.
3. No output CSV generated:
- Re-run `python gan.py` and confirm completion message:
  - `Training and generation complete.`
