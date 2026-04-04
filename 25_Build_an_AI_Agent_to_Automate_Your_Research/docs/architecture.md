# System Architecture

## Overview

The AI Research Agent is a linear pipeline system that automates online research through six distinct stages. Each stage transforms data and passes it to the next, creating an end-to-end RAG (Retrieval-Augmented Generation) workflow with local LLM-powered abstractive summarization.

## Component Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                       AI Research Agent (v0.2)                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                       │
│  │  Search  │───▶│ Scrape   │───▶│  Chunk   │                       │
│  │  Module  │    │ & Clean  │    │ & Embed  │                       │
│  └──────────┘    └──────────┘    └────┬─────┘                       │
│         │            │                  │                            │
│         │            │                  ▼                            │
│         │            │           ┌──────────────┐                   │
│         │            │           │  Sentence     │                   │
│         │            │           │  Transformers │                   │
│         │            │           │ (all-MiniLM)  │                   │
│         │            │           └──────┬───────┘                   │
│         │            │                  │                            │
│         ▼            ▼                  ▼                            │
│  ┌───────────────────────────────────────────────┐                  │
│  │          In-Memory Chunk Embeddings            │                  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐         │                  │
│  │  │Chunk 1  │ │Chunk 2  │ │Chunk N  │         │                  │
│  │  │[384-dim]│ │[384-dim]│ │[384-dim]│         │                  │
│  │  └─────────┘ └─────────┘ └─────────┘         │                  │
│  └────────────────────┬──────────────────────────┘                  │
│                       │                                              │
│                       ▼                                              │
│  ┌──────────┐    ┌──────────┐    ┌───────────────┐                  │
│  │  Query   │───▶│  Rank    │───▶│  Summarize    │                  │
│  │ Embedding│    │(Cosine   │    │ (Mistral 7B   │                  │
│  │          │    │Similarity)│    │  Instruct)    │                  │
│  └──────────┘    └──────────┘    └───────────────┘                  │
│                                                 │                    │
│                                                 ▼                    │
│                                        ┌──────────────┐             │
│                                        │ Abstractive   │             │
│                                        │   Summary     │             │
│                                        └──────────────┘             │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Stage 1: Search (Input → URLs)
**Input**: User query string  
**Output**: List of URLs  
**Process**:
- Mock function returns predefined URLs (Wikipedia, HuggingFace docs)
- Can be replaced with DuckDuckGo API for live search
- Returns 2-5 relevant source URLs

### Stage 2: Scrape & Clean (URLs → Raw Text)
**Input**: List of URLs  
**Output**: Clean text strings  
**Process**:
1. HTTP GET request with User-Agent header
2. BeautifulSoup HTML parsing
3. Remove script, style, navigation, footer, header elements
4. Extract main body text
5. Error handling for 403/404/timeout

### Stage 3: Chunk & Embed (Text → Vectors)
**Input**: Raw text from all sources  
**Output**: Collection of (chunk, embedding) pairs  
**Process**:
1. Sliding window chunking (1000 chars, 200 overlap)
2. Load SentenceTransformer model (all-MiniLM-L6-v2)
3. Encode each chunk to 384-dimensional vector
4. Store in PyTorch tensor

### Stage 4: Rank (Query + Chunks → Top-K)
**Input**: Query string, chunk embeddings  
**Output**: Top-K most relevant chunks  
**Process**:
1. Embed query using same model
2. Calculate cosine similarity: `cos_sim(query, chunk)`
3. Sort by similarity score descending
4. Select top 3 passages

### Stage 5: Summarize (Passages → Abstractive Summary)
**Input**: Top-K passages  
**Output**: LLM-generated abstractive summary  
**Process**:
1. Truncate each passage to MAX_PASSAGE_CHARS (default 500)
2. Assemble into Mistral instruct prompt template
3. Tokenize and truncate prompt to fit context window
4. Generate with Mistral 7B Instruct (Q4_K_M quantized)
5. Fallback to concatenation if model file is absent

### Summarization Sub-Pipeline

```
Top-3 Passages (similarity-scored)
        │
        ▼
  Truncate each to 500 chars
        │
        ▼
  Build [INST]...[/INST] prompt
        │
        ▼
  Tokenize → truncate to (context_window - max_new_tokens)
        │
        ▼
  Mistral 7B Instruct inference (CPU, ~2-3 min)
        │
        ▼
  Clean abstractive summary
```

## Key Design Decisions

### 1. Linear Pipeline vs. ReAct Agent
**Decision**: Linear pipeline for v0.1/v0.2  
**Rationale**: 
- Easier to debug and validate each stage
- Clear data flow visualization
- Foundation for future autonomous agent

**Future**: ReAct (Reason + Act) loop for v1.0

### 2. Semantic Search vs. Keyword Search
**Decision**: Semantic embeddings with cosine similarity  
**Rationale**:
- Captures meaning beyond exact word matches
- Handles synonyms and paraphrasing
- Robust to query variations

**Trade-off**: Higher compute cost than TF-IDF

### 3. SentenceTransformer Model Choice
**Decision**: all-MiniLM-L6-v2  
**Rationale**:
- Balance of speed and accuracy
- Only 22M parameters (fast loading)
- 384-dimensional embeddings (reasonable memory)
- Strong performance on semantic similarity

### 4. ctransformers vs. llama-cpp-python
**Decision**: ctransformers for GGUF inference  
**Rationale**:
- Ships pre-built binaries (no C++ compiler required)
- Same underlying llama.cpp engine
- Identical GGUF loading and inference capabilities

**Trade-off**: Slightly fewer configuration options than llama-cpp-python

### 5. Mistral 7B Instruct for Summarization
**Decision**: Local Mistral 7B Instruct (Q4_K_M)  
**Rationale**:
- Free, no API key required
- Runs entirely on CPU
- Good quality for 7B parameter model
- Instruct format produces structured outputs
- Q4_K_M quantization keeps model at 4.1 GB

**Trade-off**: Slower on CPU (~2-3 min per summary) vs. cloud APIs

### 6. Context Window Management
**Decision**: 2048-token context window with passage truncation  
**Rationale**:
- Keeps inference time manageable on CPU
- 500 chars × 3 passages ≈ 375 tokens + prompt ≈ 500 tokens
- Leaves 1536 tokens for LLM output
- Configurable via environment variables

### 7. Static Scraping vs. Headless Browser
**Decision**: requests + BeautifulSoup for v0.1/v0.2  
**Rationale**:
- Simple and fast for static content
- Works well with Wikipedia, documentation
- Lower resource usage

**Trade-off**: Fails on JavaScript-heavy sites  
**Future**: Playwright/Selenium for v0.3

## External Dependencies

| Service | Purpose | Integration |
|---------|---------|-------------|
| HuggingFace Hub | Model hosting | sentence-transformers downloads |
| DuckDuckGo | Web search | duckduckgo-search library |
| Wikipedia | Knowledge base | Direct scraping |
| HuggingFace Docs | Technical docs | Direct scraping |
| Local GGUF file | LLM inference | ctransformers loads from disk |

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Embedding Model Size | ~80MB | all-MiniLM-L6-v2 |
| LLM Model Size | ~4.1 GB | Mistral 7B Q4_K_M |
| Embedding Dimension | 384 | Fixed |
| Chunk Size | 1000 chars | Configurable |
| Chunk Overlap | 200 chars | Configurable |
| Top-K Results | 3 | Configurable |
| Avg Scrape Time | 1-3s | Per URL |
| Embedding Time | ~100ms | Per 1000 chars |
| LLM Load Time | ~2s | From disk to RAM |
| LLM Inference | ~2-3 min | CPU-only, 256 tokens |
| Total Runtime | 3-5 min | Depends on content |

## Security Considerations

1. **Rate Limiting**: No built-in rate limiting (add for production)
2. **User-Agent**: Sets browser-like User-Agent header
3. **Timeout**: 10-second timeout on HTTP requests
4. **Robots.txt**: Not checked (implement for production)
5. **Content Filtering**: No malicious content filtering
6. **LLM Safety**: Instruct template constrains LLM output to context-based answers

## Scalability Notes

**Current Limitations**:
- Single-threaded execution
- In-memory vector storage
- Synchronous HTTP requests
- No caching
- CPU-only LLM inference

**Scaling Strategies**:
1. Async/await for concurrent requests
2. Vector database (Pinecone, Weaviate, Chroma)
3. Redis caching for embeddings
4. Task queue (Celery) for background processing
5. GPU acceleration for LLM inference (set gpu_layers > 0)

---

**Last Updated**: 2026-03-25  
**Version**: 0.2.0
