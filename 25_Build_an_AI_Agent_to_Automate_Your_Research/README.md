# AI Research Automation Agent

> An autonomous AI agent that automates online research by searching the web, scraping content, and synthesizing findings into concise, abstractive summaries using semantic search and a local Mistral 7B LLM.

## Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.x | Core programming language |
| **Web Scraping** | BeautifulSoup4, requests | HTML parsing and HTTP requests |
| **Search** | DuckDuckGo Search | Free web search API |
| **ML/NLP** | Sentence Transformers | Semantic embeddings (all-MiniLM-L6-v2) |
| **Deep Learning** | PyTorch | Tensor operations for similarity search |
| **LLM Runtime** | ctransformers | Local inference of Mistral GGUF model |
| **LLM Model** | Mistral 7B Instruct (Q4_K_M) | Abstractive summarization |
| **Environment** | Python venv | Virtual environment management |

## Prerequisites

- Python 3.8+ installed on your system
- Internet connection (for downloading models and web scraping)
- At least 6GB free disk space (for the Mistral GGUF model + sentence transformer)
- 8GB+ RAM recommended (4GB minimum without LLM)

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /var/home/ansh/Projects/super_30/25_Build_an_AI_Agent_to_Automate_Your_Research
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
pip install -r requirements.txt
```

**Note:** First run will download the sentence transformer model (~80MB) which may take 2-3 minutes.

### Step 5: Obtain the Mistral GGUF Model

Place the quantized Mistral model at the project root (one level above this directory):

```
super_30/
├── mistral-7b-instruct-v0.1.Q4_K_M.gguf   ← 4.1 GB
└── 25_Build_an_AI_Agent_to_Automate_Your_Research/
    └── research_agent.py
```

Or set the `MISTRAL_MODEL_PATH` environment variable to the full path of the `.gguf` file.

## Usage

### Run the Research Agent

```bash
python research_agent.py
```

The agent will:
1. Perform a web search for the query (mocked for reproducibility)
2. Scrape and clean content from each result URL
3. Chunk the text (1000-char sliding window, 200-char overlap)
4. Embed all chunks and the query using `all-MiniLM-L6-v2`
5. Rank passages by cosine similarity and select the top 3
6. Generate an **abstractive summary** using the local Mistral 7B Instruct model

### Customize Your Research Query

Edit the `query` variable at the bottom of `research_agent.py`:

```python
if __name__ == "__main__":
    query = "Your research question here"
    run_research_agent(query)
```

### Environment Variables

| Name | Default | Description |
|------|---------|-------------|
| `MISTRAL_MODEL_PATH` | `../mistral-7b-instruct-v0.1.Q4_K_M.gguf` | Path to the Mistral GGUF model file |
| `CHUNK_SIZE` | `1000` | Characters per text chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between consecutive chunks |
| `TOP_K` | `3` | Number of top passages to retrieve |
| `LLM_MAX_TOKENS` | `256` | Maximum tokens the LLM will generate |
| `LLM_TEMPERATURE` | `0.3` | LLM sampling temperature (lower = more deterministic) |
| `LLM_CONTEXT_WINDOW` | `2048` | Context window size for the LLM |
| `MAX_PASSAGE_CHARS` | `500` | Max characters per passage sent to the LLM |

### Use Live DuckDuckGo Search (Optional)

Replace the mock `search_web()` function with:

```python
from duckduckgo_search import DDGS

def search_web(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        return [r['href'] for r in results]
```

## Project Structure

```
25_Build_an_AI_Agent_to_Automate_Your_Research/
├── README.md                  # This file — setup, usage, and architecture
├── research_agent.py          # Main agent implementation (v0.2 with Mistral LLM)
├── requirements.txt           # Python dependencies
├── guide.txt                  # Detailed implementation guide
├── ENGINEERING_DECISIONS.md   # Design decisions and trade-offs
├── KIRO_PROMPT.txt            # Original build prompt
├── PROJECTCHECKLIST.md        # Build verification checklist
├── RULES.md                   # Agent operating rules
├── docs/                      # Documentation directory
│   ├── architecture.md        # System architecture and data flow
│   ├── tech_stack.md          # Technology choices and rationale
│   ├── sdlc.md                # SDLC tracking
│   ├── agent_log.md           # Agent session logs
│   ├── CHANGELOG.md           # Version history
│   └── tasks.md               # Task backlog (MoSCoW)
├── backups/                   # Timestamped backups
└── venv/                      # Virtual environment (git-ignored)
```

## Architecture Overview

The AI Research Agent implements a **linear pipeline architecture** with 6 stages:

```
[User Query]
     │
     ▼
[1. Search] → Returns list of URLs (mocked or DuckDuckGo)
     │
     ▼
[2. Scrape & Clean] → Extracts clean text from each URL
     │
     ▼
[3. Chunk & Embed] → Creates semantic vector embeddings
     │
     ▼
[4. Rank] → Cosine similarity matching (query vs chunks)
     │
     ▼
[5. Summarize] → Mistral 7B generates abstractive summary
     │
     ▼
[Final Answer]
```

### Key Components

- **Semantic Search**: Uses `all-MiniLM-L6-v2` for embedding text into 384-dimensional vectors
- **Cosine Similarity**: Measures semantic relevance between query and content chunks
- **Sliding Window Chunking**: Splits text into 1000-character chunks with 200-character overlap
- **Abstractive Summarization**: Local Mistral 7B Instruct model generates concise, coherent summaries from the top-ranked passages

### Summarization Pipeline Detail

```
Top-K Passages (each truncated to 500 chars)
        │
        ▼
  Prompt Template (Mistral instruct format)
        │
        ▼
  Token-level truncation (fit within context window)
        │
        ▼
  Mistral 7B Instruct (Q4_K_M) generation
        │
        ▼
  Abstractive Summary Output
```

## Running Tests

Run the smoke test to validate the full pipeline:

```bash
python research_agent.py
```

**Expected output includes:**
1. Mocking web search confirmation
2. Scraped content stats (character counts)
3. Top 3 relevant passages with cosine similarity scores
4. Abstractive summary generated by the Mistral model

### Manual Test Cases

| Test Case | Input | Expected Result |
|-----------|-------|-----------------|
| Standard ML Query | "What is a Transformer model in machine learning?" | Passages about Transformer architecture, attention mechanisms |
| Custom Query | "Python web scraping best practices" | Passages about requests, BeautifulSoup, rate limiting |
| Edge Case (No Model) | Any query without GGUF file | Graceful fallback to concatenation-based summary |

## SDLC Status

See [docs/sdlc.md](docs/sdlc.md) for complete Software Development Lifecycle documentation.

**Current Phase**: v0.2 (Mistral LLM Integration) — COMPLETE

- Requirements defined
- Architecture designed
- Core pipeline implemented
- Mistral LLM integration verified
- End-to-end smoke test passed
- Documentation complete

**Next Phase**: v0.3 (Live Search + Robust Scraping) — Planned
- DuckDuckGo live search integration
- Headless browser integration (Playwright)
- Caching layer
- Unit and integration tests

## Common Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'ctransformers'`

**Solution:** Install the dependency:
```bash
pip install ctransformers
```

### Issue: `FileNotFoundError` for the Mistral GGUF model

**Cause:** The model file is not at the expected path.

**Solution:** Either:
1. Place the `.gguf` file at `../mistral-7b-instruct-v0.1.Q4_K_M.gguf` relative to the project directory, or
2. Set `MISTRAL_MODEL_PATH` to the absolute path of the file:
   ```bash
   export MISTRAL_MODEL_PATH="/path/to/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
   ```

The agent will gracefully fall back to a concatenation-based summary if the model file is not found.

### Issue: `Failed to fetch [URL]` with 403 Forbidden

**Cause:** Website blocks automated requests.

**Solutions:**
1. Check the website's `/robots.txt` policy
2. Implement rate limiting between requests
3. Use a headless browser (Selenium/Playwright) for v0.3
4. Try different URLs that are more scraper-friendly (Wikipedia, documentation sites)

### Issue: OutOfMemoryError during embedding or LLM loading

**Cause:** Insufficient RAM for the 4.1 GB Mistral model + embeddings.

**Solutions:**
1. Reduce the number of URLs processed (change `TOP_K`)
2. Reduce `MAX_PASSAGE_CHARS` to send less context to the LLM
3. Use GPU if available (set `gpu_layers` > 0 in `load_llm`)
4. Close other memory-intensive applications

### Issue: LLM summary is short or low quality

**Cause:** Passages may be truncated too aggressively or temperature is too low.

**Solutions:**
1. Increase `MAX_PASSAGE_CHARS` (e.g., `export MAX_PASSAGE_CHARS=800`)
2. Increase `LLM_MAX_TOKENS` (e.g., `export LLM_MAX_TOKENS=512`)
3. Slightly increase `LLM_TEMPERATURE` (e.g., `export LLM_TEMPERATURE=0.5`)

### Issue: Model download is slow/fails

**Cause:** HuggingFace model download issues.

**Solutions:**
1. Check internet connection
2. Wait and retry (temporary network issue)
3. Use offline mode if model is cached: set `local_files_only=True`
4. Manually download model from HuggingFace hub

## Development Roadmap

### v0.1 — Core Pipeline (Complete)
- Linear pipeline: Search → Scrape → Chunk → Embed → Rank → Placeholder Summarize
- Mock search with web scraping
- Semantic ranking with sentence transformers

### v0.2 — Mistral LLM Integration (Current)
- Local Mistral 7B Instruct model for abstractive summarization
- ctransformers runtime for GGUF inference
- Context-window-aware prompt truncation
- Graceful fallback when model file is absent

### v0.3 (Planned) — Robust Retriever
- Replace `requests` with Playwright/Selenium
- JavaScript rendering support
- Retry logic and rate limiting
- Caching layer for embeddings

### v1.0 (Future) — Autonomous ReAct Agent
- Plan-and-solve architecture
- Multi-step research with feedback loops
- Knowledge graph generation

## Contributing

This is an educational project following the RULES.md guidelines. When contributing:

1. Read RULES.md before making changes
2. Follow Phase 0-7 workflow
3. Update docs/agent_log.md with session entries
4. Maintain changelog in docs/CHANGELOG.md
5. Run smoke tests before submitting

## License

This project is for educational purposes. See guide.txt for attribution requirements.

---

**Built**: March 2026
**Last Updated**: 2026-03-25
**Version**: 0.2.0
