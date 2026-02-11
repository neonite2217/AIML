# AI Image Studio — Diffusion-Based Image Generator

A modern **web application** for generating images from text prompts using Stable Diffusion.  
Features a Flask REST API backend and a dark-themed, glassmorphism UI.
---

## Quick Start

### 1. Activate the virtual environment

```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
# GPU (recommended) — install PyTorch with CUDA first
pip install torch torchvision \
  --extra-index-url https://download.pytorch.org/whl/cu128

# Then install everything else
pip install -r requirements.txt
```

### 3. Run the web server

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## Features

| Feature | Description |
|---|---|
| **Web UI** | Dark-themed, responsive interface with glassmorphism design |
| **REST API** | JSON endpoints for generation, models, device info, gallery |
| **Multiple Models** | SD v1.5, v1.4, v2.1, and SDXL support |
| **GPU Auto-detect** | Automatically uses CUDA if available; CPU fallback |
| **Generated** | Browse all previously generated images |
| **CLI Mode** | Still works as a command-line tool |

---

## CLI Usage (still works)

```bash
python diffusion_image_gen.py "a cat wearing a wizard hat"
python diffusion_image_gen.py "sunset" --negative "blurry" --steps 75 --guidance 8.5
```

By default, CLI outputs are saved into `generated/` inside the project root.
If you pass `--output`, relative paths are still resolved inside the project root.

---

## Storage Behavior (Project-Local)

To keep behavior consistent for anyone cloning from GitHub, runtime artifacts are
forced into this repository instead of system temp folders like `/tmp`.

- Generated images: `generated/`
- Temp files: `.project_data/tmp/`
- Hugging Face cache: `.project_data/cache/huggingface/`
- Transformers cache: `.project_data/cache/huggingface/transformers/`
- Torch cache: `.project_data/cache/torch/`

---

## API Endpoints

| Route | Method | Description |
|---|---|---|
| `/` | GET | Serve web UI |
| `/api/generate` | POST | Generate image from JSON body |
| `/api/models` | GET | List available models |
| `/api/device` | GET | GPU/CPU info |
| `/api/generated` | GET | Recent generated images |
| `/generated/<file>` | GET | Serve image file |

### Example: Generate via API

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cat in space", "steps": 50, "guidance_scale": 7.5}'
```

---

## Project Structure

```
├── app.py                  # Flask web server
├── engine.py               # Shared diffusion engine (model loading, generation)
├── diffusion_image_gen.py  # CLI interface (imports from engine.py)
├── requirements.txt        # Python dependencies
├── static/
│   ├── index.html          # Web UI
│   ├── style.css           # Dark theme + glassmorphism styles
│   └── app.js              # Frontend logic
├── .project_data/          # Project-local temp/cache/model artifacts
├── generated/              # Output images (auto-created)
├── v1_backup/              # Original CLI-only project files
└── venv/                   # Python 3.12 virtual environment
```

---

## Requirements

- **Python 3.12** (via pyenv)
- **NVIDIA GPU** with 4GB+ VRAM (recommended) — CPU fallback supported
- ~4GB disk space per model

---

**Version**: 2.0 | **Python**: 3.12 | **CUDA**: 12.8 | **Status**: Development Ready
