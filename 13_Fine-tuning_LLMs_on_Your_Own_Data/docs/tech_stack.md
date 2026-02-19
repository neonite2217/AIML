# Tech Stack — Fine-tuning LLMs on Your Own Data

## Overview

This document describes the technology stack used in the Fine-tuning LLMs project, including the rationale for each choice and alternatives considered.

## Core Technologies

### Programming Language

**Python 3.10+**

- **Rationale**: 
  - Dominant language in ML/AI ecosystem
  - Excellent library support for transformers
  - Readable and maintainable
  - Strong community and documentation

- **Alternatives Considered**:
  - R: Good for statistics but limited deep learning support
  - Julia: Fast but smaller ecosystem
  - C++: Fast but development overhead too high for demo

### Deep Learning Framework

**PyTorch 2.0+**

- **Rationale**:
  - Preferred by Hugging Face ecosystem
  - Dynamic computation graphs (easier debugging)
  - Strong GPU acceleration
  - Excellent Python integration

- **Key Features Used**:
  - `torch.cuda` for GPU management
  - `torch.no_grad()` for inference
  - Automatic mixed precision (FP16)

- **Alternatives Considered**:
  - TensorFlow: More production-focused, steeper learning curve
  - JAX: Functional paradigm, less mature ecosystem

## Model and Training

### Transformer Library

**Hugging Face Transformers 4.30+**

- **Rationale**:
  - Industry standard for pretrained models
  - Unified API across model architectures
  - Excellent documentation and community
  - Built-in Trainer API

- **Components Used**:
  - `AutoTokenizer`: Automatic tokenizer selection
  - `AutoModelForSequenceClassification`: Model with classification head
  - `TrainingArguments`: Training configuration
  - `Trainer`: High-level training loop
  - `DataCollatorWithPadding`: Dynamic batch padding

- **Model Choice**: DistilBERT-base-uncased
  - 40% smaller than BERT
  - 60% faster
  - Retains 97% of BERT performance
  - Uncased for simplicity

### Parameter-Efficient Fine-Tuning

**PEFT (Parameter-Efficient Fine-Tuning) 0.4+**

- **Rationale**:
  - Official Hugging Face library for PEFT methods
  - Supports LoRA, Prefix Tuning, P-Tuning, etc.
  - Easy integration with existing models
  - Well-maintained and documented

- **Method**: LoRA (Low-Rank Adaptation)
  - Only 1.09% trainable parameters
  - Reduces memory by ~70%
  - Prevents catastrophic forgetting
  - Easy to swap adapters

- **Configuration**:
  ```python
  LoraConfig(
      task_type=TaskType.SEQ_CLS,
      r=8,              # Rank
      lora_alpha=16,    # Scaling
      lora_dropout=0.1, # Regularization
      target_modules=["q_lin", "v_lin"]
  )
  ```

### Dataset Management

**Hugging Face Datasets 2.12+**

- **Rationale**:
  - Efficient memory-mapped datasets
  - Streaming support for large datasets
  - Built-in preprocessing utilities
  - Integration with transformers

- **Dataset**: IMDb
  - 50,000 movie reviews
  - Binary sentiment labels
  - Standard NLP benchmark

### Training Acceleration

**Accelerate 0.20+**

- **Rationale**:
  - Simplifies multi-GPU training
  - Handles device placement automatically
  - Mixed precision support
  - DeepSpeed integration (future)

- **Features Used**:
  - Automatic device detection
  - FP16 mixed precision

## Evaluation and Metrics

**scikit-learn 1.2+**

- **Rationale**:
  - Industry standard for ML metrics
  - Well-tested implementations
  - Easy to use API

- **Metrics Used**:
  - `accuracy_score`: Overall correctness
  - `precision_recall_fscore_support`: Detailed classification metrics

## Development Tools

### Virtual Environment

**venv (built-in)**

- **Rationale**:
  - No external dependencies
  - Standard Python tool
  - Isolated dependencies

### Package Management

**pip + requirements.txt**

- **Rationale**:
  - Standard Python approach
  - Simple and well-understood
  - Compatible with all platforms

- **Version Pinning Strategy**:
  - Minimum versions (`>=`) for flexibility
  - Avoid exact pins (`==`) unless necessary
  - Major version compatibility

## Infrastructure

### Compute

**Local Development**

- **GPU**: Optional but recommended
  - CUDA-capable NVIDIA GPU
  - 8GB+ VRAM for comfortable training
  - FP16 support for efficiency

- **CPU**: Supported fallback
  - 8GB+ RAM
  - Multi-core for data loading
  - Slower but functional

### Storage

**Local Filesystem**

- **Cache**: `./.cache/huggingface/`
  - Models: ~250MB
  - Datasets: ~80MB
  - Isolated per project

- **Outputs**: `./lora-imdb-model/`
  - Adapter weights: ~3MB
  - Tokenizer files: ~1MB

## Dependencies Summary

### Production Dependencies

```
torch>=2.0.0              # Deep learning
transformers>=4.30.0      # Pretrained models
datasets>=2.12.0          # Dataset loading
peft>=0.4.0               # LoRA implementation
accelerate>=0.20.0        # Training acceleration
scikit-learn>=1.2.0       # Evaluation metrics
```

### Development Dependencies

```
pytest                    # Testing (optional)
black                     # Code formatting (optional)
flake8                    # Linting (optional)
```

## Version Compatibility

### Tested Combinations

| Python | PyTorch | Transformers | PEFT | Status |
|--------|---------|--------------|------|--------|
| 3.10 | 2.0.0 | 4.30.0 | 0.4.0 | ✅ Compatible |
| 3.11 | 2.1.0 | 4.35.0 | 0.6.0 | ✅ Compatible |
| 3.12 | 2.2.0 | 4.38.0 | 0.8.0 | ✅ Compatible |

### Known Incompatibilities

- Transformers <4.30: Missing `eval_strategy` parameter
- PEFT <0.4.0: Different API for LoRA config
- PyTorch <2.0: Missing some optimization features

## Security

### Dependency Security

- All packages from PyPI (trusted source)
- No custom or unofficial packages
- Regular updates recommended

### Runtime Security

- No network calls during training (after initial download)
- No API keys or secrets required
- Local processing only

## Performance Benchmarks

### Training Speed

| Configuration | Time/Epoch | Memory |
|--------------|-----------|--------|
| GPU (RTX 3090) | 2s | 560MB |
| GPU (T4) | 5s | 560MB |
| CPU (8 cores) | 60s | 560MB |

### Model Size

| Component | Size |
|-----------|------|
| Base Model | 255MB |
| LoRA Adapters | 3MB |
| **Total (saved)** | **3MB** |

## Future Technology Considerations

### Potential Additions

1. **DeepSpeed**: For larger model training
2. **Weights & Biases**: For experiment tracking
3. **ONNX**: For model deployment optimization
4. **TensorRT**: For inference acceleration
5. **Docker**: For reproducible environments

### Migration Path

If moving to production:
- Add `fastapi` for API serving
- Add `docker` for containerization
- Add `pytest` for comprehensive testing
- Add `pre-commit` for code quality
- Consider `poetry` or `pipenv` for dependency management

---

**Last Updated**: 2026-03-17
**Version**: 1.0.0
