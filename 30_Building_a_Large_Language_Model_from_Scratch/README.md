# Building a Large Language Model from Scratch

> Implementation of a transformer-based language model from scratch using PyTorch

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.14 |
| Deep Learning Framework | PyTorch |
| Model Architecture | Transformer (GPT-style) |
| Tokenization | Character-level |

---

## Prerequisites

- Python 3.8 or higher
- pip package manager
- At least 4GB RAM (8GB recommended for training)
- Internet connection (for downloading PyTorch)

---

## Installation

### Step 1: Navigate to Project Directory
```bash
cd 30_Building_a_Large_Language_Model_from_Scratch
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install --upgrade pip
pip install torch
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

---

## Usage

### Running the Training and Inference
```bash
source venv/bin/activate
python llm_from_scratch.py
```

### Expected Output
```
step 100: train loss 0.5698
step 200: train loss 0.0967
step 300: train loss 0.0771
step 400: train loss 0.0680
step 500: train loss 0.0547
step 600: train loss 0.0810
step 700: train loss 0.0820
step 800: train loss 0.0680
step 900: train loss 0.0445
step 999: train loss 0.0649

Generated Text:
This is a simple text for training a language model.
We will use this text to learn the basics og la
```

---

## Understanding the Model Architecture

The implementation includes all core components of a modern LLM:

### 1. Tokenization (Character-Level)
- Maps each character to a unique integer ID
- Simple but effective for small datasets

### 2. Embedding Layers
- **Token Embeddings**: Maps token IDs to dense vectors (dimension: 64)
- **Position Embeddings**: Injects positional information about token order

### 3. Self-Attention Mechanism
- Implements Query, Key, Value (QKV) computation
- Scaled dot-product attention with mask
- Multi-head attention (4 heads)

### 4. Transformer Blocks
- Multi-head self-attention layer
- Feed-forward network (64 → 256 → 64)
- Layer normalization (pre-norm and post-norm)
- Residual connections

### 5. Language Model Head
- Linear projection from embedding space to vocabulary
- Cross-entropy loss for next-token prediction

---

## Hyperparameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `batch_size` | 16 | Number of sequences per batch |
| `block_size` | 32 | Maximum sequence length |
| `max_iters` | 1000 | Training iterations |
| `learning_rate` | 1e-3 | AdamW optimizer learning rate |
| `n_embd` | 64 | Embedding dimension |
| `n_head` | 4 | Number of attention heads |
| `n_layer` | 4 | Number of transformer blocks |
| `dropout` | 0.0 | Dropout rate (disabled) |

---

## Project Structure

```
30_Building_a_Large_Language_Model_from_Scratch/
├── llm_from_scratch.py       # Main implementation
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── BUILD_LOG.md             # Build process documentation
├── guide.txt                 # University project handbook
├── RULES.md                  # Agent operating rules
├── CHECKLIST.md              # Project checklist
├── agent_PROMPT.txt          # Project prompt
├── venv/                     # Virtual environment (created)
└── docs/                     # Documentation folder (created)
    ├── sdlc.md              # SDLC documentation
    ├── architecture.md      # System architecture
    └── tech_stack.md        # Technology decisions
```

---

## Architecture Overview

```
Input Text
    |
    v
[Character Tokenizer] --> Token IDs
    |
    v
[Token Embedding Layer] + [Position Embedding]
    |
    v
[Transformer Block 1] --> Multi-Head Self-Attention + Feed-Forward
    |
    v
[Transformer Block 2] --> Multi-Head Self-Attention + Feed-Forward
    |
    v
[Transformer Block 3] --> Multi-Head Self-Attention + Feed-Forward
    |
    v
[Transformer Block 4] --> Multi-Head Self-Attention + Feed-Forward
    |
    v
[Layer Norm] --> [Linear Layer] --> Logits
    |
    v
[Cross-Entropy Loss] --> Next Token Prediction
    |
    v
Output (Training) / Generated Text (Inference)
```

---

## SDLC Status

Current Phase: **Deployment** ✅

- ✅ Requirements: Defined in guide.txt
- ✅ Design: Architecture documented
- ✅ Development: Script implemented
- ✅ Testing: Smoke test passed (training + inference verified)
- ✅ Deployment: Ready for use
- 🔄 Maintenance: Ongoing

See [docs/sdlc.md](docs/sdlc.md) for full SDLC documentation.

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'torch'"

**Solution:** Ensure virtual environment is activated and install dependencies:
```bash
source venv/bin/activate
pip install torch
```

### Issue: Training is slow on CPU

**Solution:** This is expected. The model runs on CPU by default. For faster training:
- Reduce `max_iters` for quick testing
- Use smaller `n_embd`, `n_layer`, `n_head` values

### Issue: "RuntimeError: CUDA out of memory"

**Solution:** The script automatically uses CUDA if available. If you encounter memory issues, the model will fall back to CPU automatically.

### Issue: Loss doesn't decrease

**Solution:** 
- Increase `max_iters` for more training
- Check that learning rate is appropriate (1e-3 is default)
- Verify data is properly formatted

### Issue: Generated text is gibberish

**Solution:** 
- The model needs sufficient training iterations
- Try increasing `max_iters` to 2000+
- The small dataset limits quality of output

---

## Customization Guide

### Scaling the Model
Edit hyperparameters in `llm_from_scratch.py`:
```python
n_embd = 128      # Increase embedding size
n_head = 8       # More attention heads
n_layer = 6      # More transformer blocks
max_iters = 5000 # More training iterations
```

### Using a Different Dataset
Replace the `text` variable with your own dataset:
```python
text = """
Your custom text data here.
Add as much text as possible for better training.
"""
```

### Changing Tokenization
Currently uses character-level. For word-level:
```python
words = text.split()
chars = sorted(list(set(words)))  # Change from characters to words
```

---

## Common Commands

```bash
# Activate environment
source venv/bin/activate

# Run training and inference
python llm_from_scratch.py

# Deactivate environment
deactivate

# Update dependencies
pip install --upgrade torch

# Check installed packages
pip list
```

---

## Learning Outcomes

After completing this project, you will understand:

1. **Tokenization**: How text is converted to numerical representations
2. **Embeddings**: How tokens are mapped to dense vectors
3. **Positional Encoding**: How sequence order is preserved
4. **Self-Attention**: How the model weighs relationships between tokens
5. **Transformer Blocks**: How attention and feed-forward layers combine
6. **Language Modeling**: How next-token prediction works
7. **Training Loop**: How gradient descent optimizes model weights

---

## Contributing

This project follows the Super 30 AI curriculum guidelines. See `RULES.md` for development standards.

---

## License

This project is for educational purposes as part of the Super 30 AI curriculum.

---

## Additional Resources

- [PyTorch Documentation](https://pytorch.org/docs/)
- [Attention Is All You Need Paper](https://arxiv.org/abs/1706.03762)
- [GPT-2 Paper](https://arxiv.org/abs/1909.05855)
- [Andrej Karpathy's NanoGPT](https://github.com/karpathy/nanoGPT)

---

*Project #30 - Super 30 AI Curriculum*  
*Last Updated: 2026-03-25*