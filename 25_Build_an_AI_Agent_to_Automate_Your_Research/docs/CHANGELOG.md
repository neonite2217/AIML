# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Playwright integration for JavaScript rendering
- Redis caching layer for embeddings
- DuckDuckGo live search option
- Unit and integration tests
- Docker containerization

---

## [0.2.0] - 2026-03-25

### Added
- Local Mistral 7B Instruct model integration via `ctransformers` for abstractive summarization
- `load_llm()` function to load GGUF model with configurable context window
- `summarize_with_llm()` for LLM-powered abstractive summarization
- `summarize_fallback()` for graceful degradation when model is absent
- `run_research_agent()` orchestrator for the full pipeline
- Environment variable configuration for all pipeline parameters:
  - `MISTRAL_MODEL_PATH`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K`
  - `LLM_MAX_TOKENS`, `LLM_TEMPERATURE`, `LLM_CONTEXT_WINDOW`, `MAX_PASSAGE_CHARS`
- Token-level prompt truncation to fit within LLM context window
- Passage truncation (MAX_PASSAGE_CHARS) before LLM input
- Structured logging throughout (replaced raw print statements)
- Mistral instruct prompt template `[INST]...[/INST]`
- Cosine similarity scores displayed alongside top passages
- ctransformers dependency to requirements.txt

### Changed
- `research_agent.py` rewritten from v0.1 to v0.2 with full LLM integration
- `fetch_and_clean()` now also strips nav, footer, header elements
- Documentation updated across all files (README, architecture, tech_stack, sdlc, tasks)

### Fixed
- Summarization no longer produces placeholder text — generates real abstractive summaries
- Graceful fallback when Mistral GGUF model file is missing

---

## [0.1.0] - 2026-03-23

### Added
- Initial release of AI Research Automation Agent
- Core pipeline: Search → Scrape → Chunk → Embed → Rank → Summarize
- Mock web search with Wikipedia and HuggingFace URLs
- Web scraping using requests + BeautifulSoup4
- Text chunking with sliding window approach (1000 chars, 200 overlap)
- Semantic embedding using all-MiniLM-L6-v2 model (384 dimensions)
- Cosine similarity ranking for passage relevance
- Placeholder summarization (joins top 3 passages)
- Virtual environment setup (venv)
- Complete dependency management (requirements.txt)
- Comprehensive documentation:
  - README.md with setup, usage, and troubleshooting
  - docs/architecture.md with system design
  - docs/tech_stack.md with technology choices
  - docs/sdlc.md with full SDLC documentation
  - docs/agent_log.md for session tracking
  - docs/tasks.md with MoSCoW prioritization
  - This CHANGELOG.md

### Technical Details
- Python 3.8+ compatibility
- Sentence Transformers 5.3.0
- PyTorch 2.10.0
- BeautifulSoup4 4.14.3
- DuckDuckGo Search 8.1.1 (prepared for v0.2)
- requests 2.32.5 (added to requirements)

### Known Issues (v0.1)
- Web scraper fails on JavaScript-heavy sites (403 Forbidden)
- No rate limiting between requests
- Placeholder summarization (not true LLM summarization)
- Memory usage scales linearly with content size
- No caching mechanism for repeated queries

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 0.1.0 | 2026-03-23 | Initial release — Core Pipeline |
| 0.2.0 | 2026-03-25 | Mistral LLM Integration — Abstractive Summarization |
| 0.3.0 | TBD | Robust Retriever — Playwright, caching |
| 1.0.0 | TBD | Autonomous Agent — ReAct, multi-step research |

---

**Note**: This project is for educational purposes. See guide.txt for detailed implementation instructions.

**Last Updated**: 2026-03-25
