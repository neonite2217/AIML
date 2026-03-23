# Architecture - Text Summarization Model

> System architecture and design decisions

---

## System Overview

This project implements an abstractive text summarization system using the T5 (Text-to-Text Transfer Transformer) model from Hugging Face. It takes long-form text as input and generates a concise summary that captures the main ideas while using natural language generation.

---

## Component Diagram

```
±--------------------------------------------------------µ
|                    USER INTERFACE                      |
|  - Input: Raw text to summarize                       |
|  - Output: Generated summary                          |
±------------------------|-------------------------------µ
                         |
                         v
±--------------------------------------------------------µ
|                 PREPROCESSING LAYER                   |µ
|  - Text cleaning                                      |µ
|  - Prefix addition: "summarize: "                     |µ
|  - Tokenization (T5Tokenizer)                         |µ
|  - Truncation to max_length=512                       |µ
±------------------------|-------------------------------µ
                         |
                         v
±--------------------------------------------------------µ
|                   MODEL LAYER                         |µ
|  - T5ForConditionalGeneration (t5-small)              |µ
|  - ~60M parameters                                    |µn|  - Encoder-Decoder architecture                       |µ
|  - Beam search generation (num_beams=4)               |µ
±------------------------|-------------------------------µ
                         |
                         v
±--------------------------------------------------------µ
|                POSTPROCESSING LAYER                   |µ
|  - Token ID to text decoding                          |µ
|  - Special token removal                              |µ
|  - Summary output                                     |µ
±--------------------------------------------------------µ
```

---

## Data Flow

```
Raw Input Text
      |
      v
[Add Prefix: "summarize: "]
      |
      v
[Tokenize: T5Tokenizer]
      |
      v
Token IDs [batch_size, seq_len]
      |
      v
[T5 Model.generate()]
      |
      v
Summary Token IDs
      |
      v
[Decode: T5Tokenizer.decode()]
      |
      v
Generated Summary Text
```

---

## Key Design Decisions

### 1. Model Selection: T5-small

**Rationale:**
- Fast inference time suitable for CPU
- Smaller memory footprint (~60M params)
- Good quality for educational purposes
- Easy to upgrade to t5-base or t5-large

**Alternatives Considered:**
- BART: Good for summarization but larger
- PEGASUS: Specialized for summarization but requires more compute
- GPT-based: Not ideal for summarization tasks

### 2. Task Prefix Pattern

**Implementation:**
```python
prefixed_text = "summarize: " + text
```

**Rationale:**
- T5 is trained on text-to-text tasks with prefixes
- "summarize:" instructs the model on the task
- Improves summarization quality

### 3. Beam Search Generation

**Configuration:**
- num_beams=4
- length_penalty=2.0
- no_repeat_ngram_size=2

**Rationale:**
- Beam search produces higher quality than greedy decoding
- Length penalty encourages comprehensive summaries
- No-repeat prevents redundant phrases

### 4. Input Truncation

**Implementation:**
```python
max_length=512, truncation=True
```

**Rationale:**
- T5 has maximum context window
- Prevents runtime errors with long inputs
- 512 tokens sufficient for most use cases

---

## External Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| transformers | Hugging Face library | 5.3.0 |
| torch | Deep learning framework | 2.10.0 |
| tokenizers | Fast tokenization | 0.22.2 |
| huggingface-hub | Model downloading | 1.7.2 |

---

## Model Specifications

### T5-small Details

```
Architecture:     Transformer (Encoder-Decoder)
Parameters:       ~60 million
Vocab Size:       32,100 tokens
Hidden Size:      512
Num Layers:         6 (encoder) + 6 (decoder)
Num Heads:          8
FFN Dim:        2,048
Max Length:       512 tokens
```

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| First Load Time | ~30 seconds (download) |
| Subsequent Loads | ~2 seconds (cached) |
| Inference Time | ~2-5 seconds (CPU) |
| Memory Usage | ~250 MB RAM |
| Max Input Length | 512 tokens |
| Output Length | 40-150 tokens |

---

## Scalability Considerations

### Current Limitations
- Single-threaded execution
- No batch processing
- Limited to 512 tokens input

### Potential Improvements
1. **Batch Processing:** Process multiple texts simultaneously
2. **GPU Acceleration:** Enable CUDA for faster inference
3. **Model Serving:** Use TorchServe or FastAPI for API
4. **Chunking Strategy:** Split long documents for summarization

---

## Security Considerations

- No user input validation (single-user script)
- No network exposure (local execution)
- No secrets or API keys required
- Model downloaded from trusted source (Hugging Face)

---

## Monitoring & Logging

Current state:
- Console output for summary
- Progress bar during model download
- No persistent logging (intentional for simplicity)

Future enhancements:
- Structured logging
- Performance metrics
- Error tracking

---

*Last Updated: 2026-03-23*
