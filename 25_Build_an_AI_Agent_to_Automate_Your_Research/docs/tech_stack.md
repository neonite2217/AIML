# Technology Stack

## Overview

This document details the technology choices made for the AI Research Agent project, including rationale for each decision and alternatives considered.

## Core Stack

### Programming Language
**Python 3.8+**

**Why Python?**
- Dominant language in ML/AI ecosystem
- Rich library support for NLP and web scraping
- Excellent HuggingFace integration
- Easy prototyping and debugging

**Version Requirements:**
- Python 3.8+ (type hints support)
- Python 3.11+ recommended (performance improvements)

### Virtual Environment
**Python venv**

**Why venv?**
- Built-in Python module (no external dependency)
- Cross-platform compatible
- Isolated dependency management
- Standard for Python projects

**Activation:**
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## Web Scraping

### Primary: requests + BeautifulSoup4

**requests**
- **Purpose**: HTTP library for fetching web pages
- **Version**: 2.32.5+
- **Why**: Simple, reliable, industry standard

**beautifulsoup4**
- **Purpose**: HTML/XML parsing and navigation
- **Version**: 4.14.3+
- **Why**: Flexible parsing, handles malformed HTML, CSS selector support

**Usage Pattern:**
```python
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 ...'}
response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')
```

**Trade-offs:**
- Simple and fast
- Low memory footprint
- Cannot execute JavaScript
- Limited to static HTML

### Alternative: Playwright (Planned for v0.3)
- Headless browser automation
- JavaScript rendering support
- Harder to detect as bot
- Higher resource usage

## Search API

### DuckDuckGo Search
**Library**: `duckduckgo-search` v8.1.1+

**Why DuckDuckGo?**
- Free, no API key required
- No rate limiting for moderate use
- Privacy-focused
- Python library available

**Current Implementation:**
Currently using mocked search for consistency:
```python
def search_web(query):
    print(f"Mocking web search for: '{query}'")
    return [
        "https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)",
        "https://huggingface.co/docs/transformers/index"
    ]
```

**Live Implementation:**
```python
from duckduckgo_search import DDGS

def search_web(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        return [r['href'] for r in results]
```

## Machine Learning / NLP

### Sentence Transformers
**Library**: `sentence-transformers` v5.3.0+

**Purpose**: Generate semantic embeddings from text

**Model Used**: `all-MiniLM-L6-v2`
- Size: ~80MB
- Dimensions: 384
- Training data: 1B+ sentence pairs
- Performance: Strong on semantic similarity tasks

**Why Sentence Transformers?**
- Easy-to-use API
- Pre-trained models available
- Optimized for sentence-level embeddings
- Supports GPU acceleration

**Alternative Models:**
| Model | Size | Dimensions | Speed | Accuracy |
|-------|------|------------|-------|----------|
| all-MiniLM-L6-v2 | 22M | 384 | Fast | Good |
| all-MiniLM-L12-v2 | 33M | 384 | Medium | Better |
| all-mpnet-base-v2 | 109M | 768 | Slow | Best |
| paraphrase-MiniLM | 22M | 384 | Fast | Good |

### PyTorch
**Library**: `torch` v2.10.0+

**Purpose**: Deep learning framework for tensor operations

**Why PyTorch?**
- Native tensor operations
- Required by sentence-transformers
- Supports CPU and GPU execution
- Dynamic computation graphs

## LLM Runtime (v0.2)

### ctransformers
**Library**: `ctransformers` v0.2.27+

**Purpose**: Local inference of GGUF-quantized language models

**Why ctransformers?**
- Ships pre-built Python wheels (no C++ compiler required)
- Uses the same llama.cpp engine as llama-cpp-python
- Supports all GGUF model formats (Q4_K_M, Q5_K_M, etc.)
- Simple Python API for loading and inference
- CPU and GPU support

**Model Used**: Mistral 7B Instruct v0.1 (Q4_K_M)
- Size: ~4.1 GB (4-bit quantized)
- Parameters: 7 billion
- Format: GGUF
- Context window: Configurable (default 2048)
- Inference: CPU-only by default (gpu_layers=0)

**Usage Pattern:**
```python
from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained(
    model_path,
    model_type="mistral",
    gpu_layers=0,
    context_length=2048,
)
output = llm(prompt, max_new_tokens=256, temperature=0.3)
```

**Alternatives Considered:**
| Library | Pros | Cons |
|---------|------|------|
| ctransformers | Pre-built wheel, simple API | Fewer config options |
| llama-cpp-python | More features, better docs | Requires C++ compiler to build |
| transformers (HF) | Full HF ecosystem | Does not natively support GGUF |
| Ollama | Easy setup | Separate server process |

**Decision**: ctransformers — pre-built binary, zero build dependencies, same llama.cpp core.

### Prompt Engineering

**Mistral Instruct Format:**
```
[INST] You are a research assistant. Based ONLY on the context below,
write a concise, well-structured summary that answers the user's question.

Question: {query}

Context:
{context}

Summary: [/INST]
```

**Why this format?**
- Matches Mistral's training format for instruction following
- Constrains LLM output to context-based answers
- Clear role definition improves output quality
- "Based ONLY on the context" prevents hallucination

## Supporting Libraries

### NumPy
- **Version**: 2.4.3+
- **Purpose**: Numerical computing
- **Dependency of**: torch, scikit-learn, sentence-transformers

### scikit-learn
- **Version**: 1.8.0+
- **Purpose**: Machine learning utilities
- **Dependency of**: sentence-transformers

### Transformers
- **Version**: 5.3.0+
- **Purpose**: HuggingFace model library
- **Dependency of**: sentence-transformers

### HuggingFace Hub
- **Version**: 1.7.2+
- **Purpose**: Model downloading and caching
- **Dependency of**: sentence-transformers, transformers

## Environment Management

### pip
- Python package installer
- Standard with Python

### requirements.txt
```
duckduckgo-search
beautifulsoup4
sentence-transformers
torch
requests
ctransformers
```

## Hardware Requirements

### Minimum (without LLM)
- CPU: 2 cores
- RAM: 4GB
- Storage: 2GB free
- OS: Linux, macOS, Windows with WSL

### Recommended (with LLM)
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 6GB free (4.1GB model + 80MB embedding model + code)
- GPU: Optional (CUDA-compatible for LLM acceleration)

### Production
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 10GB+
- GPU: NVIDIA with 8GB+ VRAM (for batch processing)

## Deployment Options

### Local Development
- Virtual environment
- Direct Python execution

### Cloud Deployment
- **AWS**: EC2, Lambda (with container)
- **Google Cloud**: Compute Engine, Cloud Functions
- **Azure**: Virtual Machines, Functions
- **HuggingFace**: Spaces (for demos)

### Containerization
- Docker (future consideration)
- Kubernetes (for multi-instance scaling)

## Future Technology Roadmap

### v0.3 - Robust Retriever
- **Playwright**: Headless browser for JS rendering
- **Redis**: Caching layer for embeddings
- **FastAPI**: API wrapper for HTTP interface

### v1.0 - Autonomous Agent
- **LangChain**: Agent framework for ReAct pattern
- **ChromaDB**: Vector database for persistence
- **Docker**: Containerization for deployment

---

**Last Updated**: 2026-03-25  
**Version**: 0.2.0
