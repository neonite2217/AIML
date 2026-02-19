# Build From Scratch - Project 13

## 1. Setup
```bash
cd 13_Fine-tuning_LLMs_on_Your_Own_Data
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Run Fine-tuning
```bash
./.venv/bin/python fine_tuning.py
```

## 3. Expected Outputs
- `training_output.log` contains training/eval summary
- `lora-imdb-model/adapter_model.safetensors`
- `lora-imdb-model/adapter_config.json`
- tokenizer files under `lora-imdb-model/`

## 4. Notes
- Script is designed to run even when network access is unreliable.
- If IMDb/model weights are unavailable remotely, local fallbacks are used.
