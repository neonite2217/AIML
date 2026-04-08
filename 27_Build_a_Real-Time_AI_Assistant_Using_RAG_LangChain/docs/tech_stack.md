# Tech Stack — Real-Time AI Assistant

This document details the technology choices made for the Real-Time AI Assistant project.

---

## Core Technologies

### 1. Programming Language: Python 3.10+

**Version:** 3.14 (current system)  
**Rationale:**
- Rich ecosystem for AI/ML development
- Excellent LangChain support
- Easy to read and maintain
- Strong community support

**Alternatives Considered:**
- **Node.js:** Less mature AI/ML ecosystem
- **Go:** Limited LangChain support
- **Rust:** Steeper learning curve, less AI library support

---

### 2. LLM Runtime: Ollama

**Version:** Latest (as of 2026-03-25)  
**Website:** https://ollama.ai/

**Purpose:** Local LLM inference engine

**Rationale:**
- Simple installation and setup
- No API costs
- Full data privacy
- Supports multiple model families
- Active development and community

**Alternatives Considered:**
- **Hugging Face Transformers:** More complex setup, requires GPU for good performance
- **vLLM:** Optimized for production, overkill for this project
- **Cloud APIs (OpenAI, Anthropic):** Cost, privacy concerns, rate limits

---

### 3. Language Model: Qwen3.5

**Version:** Latest (qwen3.5:latest)  
**Size:** 6.6 GB  
**Developer:** Alibaba Cloud

**Rationale:**
- Already available in local Ollama installation
- Strong performance on general knowledge tasks
- Good balance of speed and quality
- No additional download required

**Alternatives Considered:**
- **Llama2:** Original choice, but Qwen3.5 available and more recent
- **Mistral:** Good performance, but not available locally
- **Phi-3:** Smaller footprint, but less capable for general queries

---

### 4. RAG Framework: LangChain

**Version:** 1.2.13  
**Components:**
- `langchain-core`: 1.2.20
- `langchain-community`: 0.4.1
- `langchain-ollama`: 1.0.1
- `langchain-text-splitters`: 1.1.1

**Website:** https://python.langchain.com/

**Rationale:**
- Industry-standard RAG framework
- LCEL provides clean, composable pipelines
- Extensive documentation and examples
- Active community and ecosystem
- Built-in streaming support

**Alternatives Considered:**
- **LlamaIndex:** More focused on document indexing, less flexible for web search
- **Haystack:** Good alternative, but less popular
- **Custom implementation:** More control, but reinventing the wheel

---

### 5. Search Tool: DuckDuckGo Search

**Package:** `langchain-community` + `ddgs`  
**Version:** ddgs 9.11.4

**Purpose:** Real-time web search for RAG retrieval

**Rationale:**
- No API key required
- Free to use
- Good enough quality for demonstration
- Multiple search engine fallbacks
- Easy integration with LangChain

**Alternatives Considered:**
- **Google Custom Search API:** Higher quality, but requires API key and has costs
- **Bing Search API:** Similar to Google, requires Azure account
- **Serper API:** Good quality, but paid service
- **Vector Database:** Not suitable for real-time web data

---

## Supporting Libraries

### 6. Logging: Python `logging` Module

**Version:** Built-in (Python 3.14)

**Configuration:**
- Dual output: Console + File
- Format: `%(asctime)s - %(levelname)s - %(message)s`
- Level: INFO (configurable)

**Rationale:**
- Standard library (no dependencies)
- Flexible and powerful
- Production-ready

---

### 7. HTTP Client: Primp

**Version:** 1.1.3 (via ddgs dependency)

**Purpose:** HTTP requests for search engines

**Rationale:**
- Modern HTTP client
- Better performance than requests
- Automatic dependency via ddgs

---

## Development Tools

### 8. Version Control: Git

**Purpose:** Source code management

**Best Practices:**
- Feature branches for new functionality
- Conventional commits for clear history
- No direct commits to main

---

### 9. Package Management: pip

**Purpose:** Python dependency management

**File:** `requirements.txt`

**Best Practices:**
- Minimum version pins (`>=`)
- No exact version pins unless required
- Regular updates for security patches

---

## Infrastructure

### 10. Operating System: Linux

**Distribution:** Not specified (cross-compatible)

**Requirements:**
- Python 3.10+
- Ollama runtime
- Internet connection for search

**Compatibility:**
- ✅ Linux (tested)
- ✅ macOS (compatible)
- ✅ Windows (via WSL or native Python)

---

## Technology Matrix

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Language** | Python | 3.14 | Core implementation |
| **LLM Runtime** | Ollama | Latest | Local model serving |
| **Model** | Qwen3.5 | Latest | Answer generation |
| **Framework** | LangChain | 1.2.13 | RAG orchestration |
| **Search** | DuckDuckGo | N/A | Real-time retrieval |
| **Logging** | logging | Built-in | Debugging & monitoring |

---

## Dependency Graph

```
real_time_assistant.py
├── langchain_ollama
│   └── ChatOllama
├── langchain_core
│   ├── PromptTemplate
│   ├── RunnablePassthrough
│   └── StrOutputParser
├── langchain_community
│   └── DuckDuckGoSearchRun
│       └── ddgs
│           └── primp (HTTP client)
└── logging (built-in)
```

---

## Version Compatibility

| Python Version | Status | Notes |
|----------------|--------|-------|
| 3.10 | ✅ Supported | Minimum version |
| 3.11 | ✅ Supported | Recommended |
| 3.12 | ✅ Supported | Tested |
| 3.13 | ✅ Supported | Compatible |
| 3.14 | ⚠️ Warning | Pydantic v1 compatibility warnings (non-critical) |

---

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **Model Load Time** | ~5-10s | First invocation |
| **Search Time** | 1-3s | Per query |
| **Generation Time** | 20-60s | Depends on response length |
| **Total Response Time** | 30-120s | End-to-end |
| **Memory Usage** | ~7-8 GB | Model + Python overhead |

---

## Security Considerations

- **No hardcoded secrets:** All configuration via defaults or environment
- **Local execution:** Minimal external API calls (only search queries)
- **Dependency verification:** All packages from PyPI
- **No telemetry:** No analytics or tracking implemented

---

## Future Technology Considerations

### Potential Upgrades
- **LangChain 2.0:** When stable, for improved performance
- **Qwen3.5-Max:** For better reasoning capabilities
- **Ollama 0.6+:** For improved model management
- **FastAPI:** For web interface in future versions

### Deprecation Risks
- **DuckDuckGo API changes:** Monitor for breaking changes
- **LangChain API evolution:** Track migration guides
- **Ollama model availability:** Ensure qwen3.5 remains available

---

*Last Updated: 2026-03-25*
