# Changelog

All notable changes to the Real-Time AI Assistant project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Add support for multiple LLM backends
- Implement conversation history
- Add vector database support for document-based RAG

---

## [1.0.0] - 2026-03-25

### Added
- Initial release of Real-Time AI Assistant
- RAG pipeline with DuckDuckGo search integration
- Qwen3.5 LLM integration via Ollama
- Comprehensive logging system (console + file output)
- Interactive and demonstration modes
- Full documentation suite (README, SDLC, Architecture, etc.)
- Automated setup scripts for Linux/macOS and Windows
- Project completion checklist

### Changed
- Updated LLM from llama2 to qwen3.5:latest (optimized for local deployment)
- Enhanced logging from basic print statements to structured logging
- Improved error handling with detailed messages

### Fixed
- Missing `ddgs` dependency issue
- Grokipedia search engine errors (now logged as non-blocking)
- Python 3.14 Pydantic v1 compatibility warnings (non-critical)

### Technical Details
- **LangChain Version:** 1.2.13
- **Ollama Integration:** langchain-ollama 1.0.1
- **Search Tool:** DuckDuckGoSearchRun with ddgs 9.11.4
- **Model:** qwen3.5:latest (6.6 GB)

---

## [0.1.0] - 2026-01-30

### Added
- Initial project structure
- Basic RAG pipeline implementation
- Engineering decisions documentation
- Development rules (RULES.md)

---

*Last Updated: 2026-03-25*
