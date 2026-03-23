# Text Summarization Model using LLMs

> Abstractive text summarization using Hugging Face Transformers and T5 model

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.14 |
| Deep Learning Framework | PyTorch |
| NLP Library | Hugging Face Transformers |
| Model | T5 (Text-to-Text Transfer Transformer) |
| Model Variant | t5-small |

---

## Prerequisites

- Python 3.8 or higher
- pip package manager
- At least 2GB free disk space (for model download)
- Internet connection (for downloading pre-trained model)

---

## Installation

### Step 1: Clone or Navigate to Project
```bash
cd 21_Text_Summarization_Model_using_LLMs
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
pip install transformers torch
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

---

## Usage

### Basic Usage
```bash
source venv/bin/activate
python text_summarization.py
```

### Expected Output
```
Original Text:
The James Webb Space Telescope (JWST) is a space telescope designed primarily to conduct infrared astronomy...

Generated Summary:
the James Webb Space Telescope (JWST) is a space telescope designed primarily to conduct infrared astronomy...
```

### Customizing the Model

Edit `text_summarization.py` to change the model:

```python
# Available T5 models:
MODEL_NAME = "t5-small"    # Fast, ~60M parameters
MODEL_NAME = "t5-base"     # Better quality, ~220M parameters  
MODEL_NAME = "t5-large"    # Best quality, ~770M parameters
```

### Customizing Generation Parameters

```python
summary_ids = model.generate(
    input_ids,
    num_beams=4,              # Number of beams for beam search
    length_penalty=2.0,       # Length penalty (higher = longer summaries)
    max_length=150,           # Maximum summary length
    min_length=40,            # Minimum summary length
    no_repeat_ngram_size=2    # Prevent repetition
)
```

---

## Project Structure

```
21_Text_Summarization_Model_using_LLMs/
├── text_summarization.py      # Main script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── BUILD_LOG.md               # Build process documentation
├── guide.txt                  # University project handbook
├── RULES.md                   # Agent operating rules
├── CHECKLIST.md               # Super 30 project checklist
├── KIRO_PROMPT.txt            # Project prompt
├── venv/                      # Virtual environment (created)
└── docs/                      # Documentation folder (created)
    ├── sdlc.md               # SDLC documentation
    ├── architecture.md       # System architecture
    ├── tech_stack.md         # Technology decisions
    ├── CHANGELOG.md          # Version history
    └── agent_log.md          # Agent session log
```

---

## Architecture Overview

```
Input Text
    |
    v
[Prefix: "summarize: "]
    |
    v
[T5 Tokenizer] --> Token IDs
    |
    v
[T5 Model (t5-small)] --> Generate Summary Tokens
    |
    v
[Tokenizer Decoder] --> Human-Readable Summary
    |
    v
Output Summary
```

**Data Flow:**
1. User provides input text
2. Text is prefixed with "summarize: " to instruct the model
3. Tokenizer converts text to token IDs
4. T5 model generates summary token IDs using beam search
5. Tokenizer decodes token IDs back to text
6. Summary is displayed/output

---

## Environment Variables

This project does not require environment variables. Model is downloaded automatically on first run.

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| None | N/A | N/A | N/A |

---

## Running Tests

### Smoke Test
Verify the model works correctly:
```bash
source venv/bin/activate
python text_summarization.py
```

Expected: Summary generation completes without errors.

---

## SDLC Status

Current Phase: **Deployment** ✅

- ✅ Requirements: Defined in guide.txt
- ✅ Design: Architecture documented
- ✅ Development: Script implemented
- ✅ Testing: Smoke test passed
- ✅ Deployment: Ready for use
- 🔄 Maintenance: Ongoing

See [docs/sdlc.md](docs/sdlc.md) for full SDLC documentation.

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'transformers'"

**Solution:** Ensure virtual environment is activated and install dependencies:
```bash
source venv/bin/activate
pip install transformers torch
```

### Issue: "HTTPError: 403 Forbidden" when downloading model

**Solution:** Check internet connection. If behind a proxy:
```bash
export HTTPS_PROXY=http://proxy:port
python text_summarization.py
```

### Issue: "RuntimeError: CUDA out of memory"

**Solution:** The script runs on CPU by default. If you modified it for GPU, reduce batch size or use smaller model (t5-small).

### Issue: "Summary is too short/long"

**Solution:** Adjust `max_length` and `min_length` parameters in the script.

### Issue: Model download is slow

**Solution:** First download caches the model. Subsequent runs will be much faster.

---

## Common Commands

```bash
# Activate environment
source venv/bin/activate

# Run summarization
python text_summarization.py

# Deactivate environment
deactivate

# Update dependencies
pip install --upgrade transformers torch

# Check installed packages
pip list
```

---

## Contributing

This project follows the Super 30 AI curriculum guidelines. See `RULES.md` for development standards.

---

## License

This project is for educational purposes as part of the Super 30 AI curriculum.

---

## Additional Resources

- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers)
- [T5 Paper: Exploring the Limits of Transfer Learning](https://arxiv.org/abs/1910.10683)
- [Text Summarization Guide](https://huggingface.co/tasks/summarization)

---

*Project #21 - Super 30 AI Curriculum*  
*Last Updated: 2026-03-23*
