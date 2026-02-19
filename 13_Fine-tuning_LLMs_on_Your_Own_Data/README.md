# Fine-tuning LLMs on Your Own Data

> PEFT/LoRA fine-tuning workflow for sentiment classification with offline-safe fallbacks.

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: Hugging Face Transformers
- **Fine-tuning**: PEFT (Parameter-Efficient Fine-Tuning) with LoRA
- **Dataset**: IMDb Movie Reviews (Hugging Face Datasets)
- **Model**: DistilBERT-base-uncased
- **Libraries**: PyTorch, Accelerate, scikit-learn

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Optional: CUDA-capable GPU (script runs on CPU fallback)
- 8GB+ RAM
- 5GB+ disk space for model cache

## Installation

### Step 1: Navigate to Project Directory

```bash
cd 13_Fine-tuning_LLMs_on_Your_Own_Data
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: First run will download ~500MB of model weights and datasets from Hugging Face.

## Usage

### Quick Start

Run the fine-tuning script:

```bash
./.venv/bin/python fine_tuning.py
```

Or with activated virtual environment:

```bash
source .venv/bin/activate
python fine_tuning.py
```

### What Happens

1. **Dataset Loading**: Downloads IMDb dataset (25K train, 25K test reviews)
2. **Tokenization**: Converts text to token IDs using DistilBERT tokenizer
3. **Model Loading**: Loads pretrained DistilBERT with classification head
4. **LoRA Configuration**: Applies Low-Rank Adaptation (only ~1.09% trainable parameters)
5. **Training**: Fine-tunes for 1 epoch on 200 samples (configurable)
6. **Evaluation**: Tests on 50 samples, reports accuracy/precision/recall/F1
7. **Inference**: Demonstrates predictions on sample reviews

### Expected Output

```
============================================================
Fine-tuning LLMs with PEFT/LoRA
============================================================
Model: distilbert-base-uncased
Dataset: imdb
Device: CUDA
Train samples: 200 | Test samples: 50 | Epochs: 1
============================================================

[1/6] Loading IMDb dataset...
  Source: IMDb (Hugging Face)
  Training samples: 200
  Test samples: 50

...

trainable params: 739,586 || all params: 67,694,596 || trainable%: 1.0925

...

Evaluation Results:
  eval_loss: 0.6425
  eval_accuracy: 0.5800
  eval_precision: 1.0000
  eval_recall: 0.0455
  eval_f1: 0.0870

Testing inference on sample reviews...

Review: This movie was absolutely fantastic! The acting was superb.
Prediction: POSITIVE (confidence: 51.85%)

Review: Terrible waste of time. The plot made no sense at all.
Prediction: NEGATIVE (confidence: 56.38%)
```

## Project Structure

```
13_Fine-tuning_LLMs_on_Your_Own_Data/
├── fine_tuning.py             # Main PEFT/LoRA training script
├── requirements.txt           # Python dependencies
├── guide.txt                  # Original lab brief
├── RULES.md                   # Agent operating rules
├── KIRO_PROMPT.txt            # Build instructions
├── training_output.log        # Execution log (generated)
├── README.md                  # This file
├── BUILD_LOG.md               # Build verification notes
├── docs/                      # Documentation
│   ├── agent_log.md           # Agent session log
│   ├── CHANGELOG.md           # Version history
│   ├── tasks.md               # Task backlog
│   ├── sdlc.md                # SDLC tracking
│   ├── architecture.md        # System architecture
│   └── tech_stack.md          # Technology decisions
├── lora-imdb-model/           # Saved fine-tuned model (generated)
├── results/                   # Training checkpoints (generated)
├── logs/                      # Training logs (generated)
├── .cache/                    # Hugging Face cache (generated)
└── .venv/                     # Virtual environment (not committed)
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Input: IMDb Reviews                      │
│              (Text: "This movie was great!")               │
└──────────────────────┬────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Tokenizer (DistilBERT)                         │
│         Converts text → token IDs (input_ids)              │
└──────────────────────┬────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Pretrained Model (DistilBERT)                  │
│              + Classification Head (2 classes)            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  LoRA Adapters (trainable: q_lin, v_lin layers)    │  │
│  │  - Rank: 8                                         │  │
│  │  - Alpha: 16                                       │  │
│  │  - Only 1.09% of parameters trainable               │  │
│  └─────────────────────────────────────────────────────┘  │
└──────────────────────┬────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Output: Sentiment Prediction                   │
│              Class: POSITIVE / NEGATIVE                   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Input**: Raw text reviews from IMDb dataset
2. **Preprocessing**: Tokenization with max_length=256, truncation
3. **Model**: DistilBERT encoder + LoRA adapters + classification head
4. **Training**: Cross-entropy loss, AdamW optimizer, linear scheduler
5. **Output**: Binary sentiment classification (0=NEGATIVE, 1=POSITIVE)

## Environment Variables

| Name | Required | Description | Default |
|------|----------|-------------|---------|
| `HF_HOME` | No | Hugging Face cache root | `./.cache/huggingface` (set by script) |
| `HF_DATASETS_CACHE` | No | Dataset cache path | inside `HF_HOME` |
| `HUGGINGFACE_HUB_CACHE` | No | Hub cache path | inside `HF_HOME` |
| `TRANSFORMERS_CACHE` | No | Transformers cache path | inside `HF_HOME` |
| `CUDA_VISIBLE_DEVICES` | No | GPU device selection | `0` |

## Configuration

Edit these constants in `fine_tuning.py` to customize training:

```python
# Dataset Configuration
TRAIN_SIZE = 200          # Number of training samples
TEST_SIZE = 50            # Number of test samples

# Training Configuration
EPOCHS = 1                # Training epochs
BATCH_SIZE = 4            # Batch size per device
LEARNING_RATE = 2e-4      # Learning rate
WEIGHT_DECAY = 0.01       # L2 regularization

# LoRA Configuration
LORA_R = 8                # LoRA rank (higher = more capacity)
LORA_ALPHA = 16           # LoRA alpha scaling
LORA_DROPOUT = 0.1        # Dropout rate for LoRA layers

# Other
SEED = 42                 # Random seed for reproducibility
MAX_LENGTH = 256          # Maximum sequence length
```

## Running Tests

### Smoke Test

Verify installation:

```bash
python -c "import torch; import transformers; import peft; print('All imports successful')"
```

### Full Training Run

```bash
python fine_tuning.py
```

**Success indicators:**
- ✅ Training + evaluation complete without errors
- ✅ Model adapter files saved in `lora-imdb-model/`
- ✅ Sample inference predictions printed
- ✅ Training metrics displayed (loss, accuracy, etc.)

**Expected runtime:**
- GPU: ~2-5 minutes
- CPU: ~10-20 minutes

## SDLC Status

See [docs/sdlc.md](docs/sdlc.md) for full SDLC tracking.

**Current Phase**: Completed ✅

- ✅ **Requirements**: Defined (sentiment classification on IMDb)
- ✅ **Design**: Architecture documented with LoRA integration
- ✅ **Implementation**: PEFT/LoRA fine-tuning script complete
- ✅ **Testing**: Smoke test passed, training completed successfully
- ✅ **Documentation**: README, SDLC, architecture docs complete

## Troubleshooting

### Issue: "CUDA out of memory"

**Symptoms**: RuntimeError during training

**Solutions**:
1. Reduce batch size in `fine_tuning.py`:
   ```python
   per_device_train_batch_size=2,  # Instead of 4
   per_device_eval_batch_size=2,
   ```
2. Reduce sequence length:
   ```python
   max_length=128  # Instead of 256
   ```
3. Use CPU instead of GPU:
   ```bash
   export CUDA_VISIBLE_DEVICES=""
   python fine_tuning.py
   ```

### Issue: "ModuleNotFoundError: No module named 'peft'"

**Symptoms**: Import error when running script

**Solution**: Install PEFT:
```bash
pip install peft>=0.4.0
```

Or reinstall all requirements:
```bash
pip install -r requirements.txt
```

### Issue: "Dataset download fails"

**Symptoms**: Connection error or timeout when loading IMDb

**Solution**: The script automatically falls back to a synthetic dataset. To force offline mode:
```bash
export HF_DATASETS_OFFLINE=1
python fine_tuning.py
```

### Issue: "Model download fails"

**Symptoms**: Cannot load pretrained weights

**Solution**: The script automatically falls back to randomly initialized weights. For better results:
1. Ensure internet connectivity for first run
2. Pre-download model:
   ```python
   from transformers import AutoModel
   model = AutoModel.from_pretrained("distilbert-base-uncased")
   ```

### Issue: "Training is very slow"

**Symptoms**: Taking longer than expected

**Solutions**:
1. Verify GPU is available:
   ```bash
   python -c "import torch; print(torch.cuda.is_available())"
   ```
2. If no GPU, reduce dataset size:
   ```python
   TRAIN_SIZE = 100  # Instead of 200
   TEST_SIZE = 25    # Instead of 50
   ```
3. Reduce epochs:
   ```python
   EPOCHS = 1  # Keep minimal for demo
   ```

### Issue: "ImportError: cannot import name 'TrainingArguments'"

**Symptoms**: Import error from transformers

**Solution**: Update transformers:
```bash
pip install --upgrade transformers>=4.30.0
```

### Issue: "Permission denied when saving model"

**Symptoms**: Cannot write to output directory

**Solution**: Check directory permissions:
```bash
mkdir -p lora-imdb-model results logs
chmod 755 lora-imdb-model results logs
```

### Issue: "Trainer.__init__() got an unexpected keyword argument"

**Symptoms**: API compatibility error

**Solution**: Update all dependencies:
```bash
pip install --upgrade transformers accelerate peft
```

## Build Process

### Complete Build Steps

1. **Environment Setup**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   ```

2. **Dependency Installation**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python -c "import torch; import transformers; import peft; print('OK')"
   ```

4. **Run Training**
   ```bash
   python fine_tuning.py
   ```

5. **Verify Output**
   - Check `lora-imdb-model/` directory exists
   - Check `training_output.log` for success messages
   - Review evaluation metrics

### Build Artifacts

After successful build:
- `lora-imdb-model/adapter_config.json` - LoRA configuration
- `lora-imdb-model/adapter_model.safetensors` - Trained LoRA weights
- `training_output.log` - Complete training log
- `results/checkpoint-*/` - Training checkpoints
- `logs/` - TensorBoard logs (if enabled)

## Contributing

1. Preserve offline-safe behavior for dataset/model loading
2. Keep training defaults lightweight for reproducible CPU runs
3. Update `BUILD_LOG.md` after changing training flow
4. Follow PEP 8 style guidelines
5. Add tests for new features

## License

Project-level license is not explicitly defined. Follow repository owner guidance.

## Acknowledgments

- Hugging Face for Transformers, Datasets, and PEFT libraries
- Microsoft Research for LoRA (Low-Rank Adaptation) paper
- IMDb dataset by Stanford AI Lab
- DistilBERT by Hugging Face (Sanh et al., 2019)

---

**Last Updated**: 2026-03-17
**Version**: 1.0.0
**Status**: ✅ Completed
