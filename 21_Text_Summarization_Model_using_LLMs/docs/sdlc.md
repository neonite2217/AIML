# SDLC - Text Summarization Model using LLMs

> Software Development Lifecycle Documentation

---

## 1. Requirements

### Functional Requirements
- [x] Load pre-trained T5 model from Hugging Face
- [x] Accept text input for summarization
- [x] Generate abstractive summary using beam search
- [x] Display original text and generated summary
- [x] Support customizable generation parameters

### Non-Functional Requirements
- [x] Fast model loading (cached after first run)
- [x] Reasonable inference time (< 10 seconds)
- [x] Handle texts up to 512 tokens
- [x] No GPU required (CPU compatible)
- [x] Clear error messages for debugging

### User Personas
- Students learning NLP and transformers
- Developers exploring text summarization
- Researchers testing summarization techniques

---

## 2. Design

### Architecture Diagram

```
±------------------µ     ±------------------µ     ±------------------µ
|   Input Layer    |     |  Processing      |     |   Output Layer   |
|                  |     |                  |     |                  |
| - Raw Text       |>---->| - Tokenization   |>---->| - Summary Text   |
| - Prefix Add     |     | - Model Generate |     | - Display        |
±------------------µ     ±------------------µ     ±------------------µ
                                    |
                            ±------------------µ
                            |   T5 Model       |
                            |   (t5-small)     |
                            ±------------------µ
```

### Tech Stack Finalized
- Python 3.14
- Hugging Face Transformers (T5)
- PyTorch (backend)
- Virtual environment for isolation

### Data Flow
1. User provides input text
2. Text prefixed with "summarize: "
3. Tokenizer converts to token IDs
4. T5 model generates summary tokens
5. Tokenizer decodes tokens to text
6. Summary displayed to user

---

## 3. Development

### Coding Standards
- [x] PEP 8 compliant Python code
- [x] Clear variable names
- [x] Comments explaining key steps
- [x] Modular structure

### Version Control
- [x] All code tracked
- [x] Meaningful commit messages
- [x] No secrets in code

---

## 4. Testing

### Unit Tests
- [x] Model loading test
- [x] Tokenization test
- [x] Generation test
- [x] Decoding test

### Integration Tests
- [x] End-to-end summarization pipeline

### Smoke Test
**Command:** `python text_summarization.py`
**Result:** PASS - Summary generated successfully

### Edge Cases Tested
- [x] Empty input handling
- [x] Very long input (truncated)
- [x] Special characters in input

---

## 5. Deployment

### Environment Setup
- [x] Virtual environment created
- [x] Dependencies documented in requirements.txt
- [x] README.md with setup instructions

### Deployment Guide
See README.md for installation and usage instructions.

### Rollback Plan
- Delete venv folder
- Recreate with requirements.txt

---

## 6. Maintenance

### Changelog
See docs/CHANGELOG.md

### Known Issues
- Model size limitation for very long documents
- CPU-only execution (no GPU optimization)

### Agent Log
See docs/agent_log.md

---

## SDLC Status Summary

| Phase | Status |
|-------|--------|
| Requirements | ✅ Complete |
| Design | ✅ Complete |
| Development | ✅ Complete |
| Testing | ✅ Complete |
| Deployment | ✅ Complete |
| Maintenance | 🔄 Ongoing |

**Overall Status:** ✅ COMPLETED

---

*Last Updated: 2026-03-23*
