# SDLC — AI Research Automation Agent

This document tracks the Software Development Lifecycle for the AI Research Agent project.

## Project Information

- **Project Name**: AI Research Automation Agent
- **Current Version**: 0.2.0
- **Phase**: Development (v0.2 Mistral LLM Integration)
- **Last Updated**: 2026-03-25

---

## 1. Requirements

### 1.1 Functional Requirements

- [x] **FR-001**: Accept user research query as input
- [x] **FR-002**: Search web for relevant source URLs
- [x] **FR-003**: Scrape and clean HTML content from URLs
- [x] **FR-004**: Chunk text into manageable segments
- [x] **FR-005**: Generate semantic embeddings for chunks
- [x] **FR-006**: Rank chunks by relevance to query using cosine similarity
- [x] **FR-007**: Return top-K most relevant passages
- [x] **FR-008**: Generate abstractive summary using local Mistral 7B LLM
- [x] **FR-009**: Graceful fallback to concatenation when LLM model unavailable
- [x] **FR-010**: Configurable pipeline parameters via environment variables

### 1.2 Non-Functional Requirements

- [x] **NFR-001**: Response time < 5 minutes for typical queries (including LLM inference)
- [x] **NFR-002**: Memory usage < 8GB for standard operation with LLM
- [x] **NFR-003**: No API keys required for core functionality
- [x] **NFR-004**: Graceful error handling for failed requests
- [x] **NFR-005**: Python 3.8+ compatibility
- [x] **NFR-006**: LLM context window management to prevent token overflow

### 1.3 User Personas

**Primary User: ML Developer**
- Background: Software engineer learning ML
- Goal: Quickly research technical topics with LLM-generated summaries
- Pain Point: Manual web searching is time-consuming
- Success Criteria: Get relevant, synthesized information in < 5 minutes

**Secondary User: Research Assistant**
- Background: Academic or professional researcher
- Goal: Automate initial research phase with abstractive summaries
- Pain Point: Sifting through multiple sources and synthesizing findings
- Success Criteria: High-quality passage retrieval and coherent summaries

---

## 2. Design

### 2.1 Architecture Design
- [x] Architecture diagram created
- [x] Component specifications defined
- [x] Data flow documented
- [x] Interface contracts established
- [x] LLM summarization sub-pipeline designed

**Location**: [docs/architecture.md](architecture.md)

### 2.2 Technology Selection
- [x] Tech stack finalized
- [x] Dependencies identified
- [x] Alternatives evaluated
- [x] Rationale documented
- [x] ctransformers selected over llama-cpp-python (no C++ compiler needed)

**Location**: [docs/tech_stack.md](tech_stack.md)

### 2.3 System Design

**Pipeline Architecture:**
```
Search → Scrape → Chunk → Embed → Rank → Summarize (Mistral LLM)
```

**Key Decisions:**
1. Linear pipeline for v0.2 (easier to debug)
2. Semantic search over keyword matching
3. Mock search for consistent testing
4. ctransformers for GGUF inference (pre-built binaries)
5. Mistral 7B Instruct for abstractive summarization
6. Context-window-aware prompt truncation

### 2.4 API Contracts

Not applicable for standalone script. Future versions may include:
- REST API wrapper
- CLI interface
- Python module interface

---

## 3. Development

### 3.1 Coding Standards
- [x] PEP 8 style guide followed
- [x] Docstrings for all functions
- [x] Error handling implemented
- [x] No hardcoded secrets or API keys
- [x] Structured logging via Python logging module
- [x] Environment variable configuration for all parameters

**Standards Applied:**
- Function names: snake_case
- Constants: UPPER_SNAKE_CASE
- Max line length: 120 characters
- Comments explain "why", not "what"

### 3.2 Version Control
- [x] Backups created before modifications
- [x] Timestamped backup in backups/ directory
- [x] No sensitive data committed

### 3.3 Code Organization

**File Structure:**
```
/
├── research_agent.py       # Main implementation (v0.2)
├── requirements.txt        # Dependencies
├── guide.txt               # Implementation guide
├── ENGINEERING_DECISIONS.md
├── RULES.md                # Agent operating rules
├── README.md               # Setup and usage
├── docs/                   # Documentation
│   ├── architecture.md
│   ├── tech_stack.md
│   ├── sdlc.md
│   ├── agent_log.md
│   ├── CHANGELOG.md
│   └── tasks.md
└── backups/                # Timestamped backups
```

### 3.4 Development Phases

**Phase v0.1 - Core Pipeline** ✅ COMPLETE
- [x] Search module (mock)
- [x] Scrape module (requests + BeautifulSoup)
- [x] Chunking logic (sliding window)
- [x] Embedding (SentenceTransformers)
- [x] Ranking (cosine similarity)
- [x] Summarization placeholder

**Phase v0.2 - Mistral LLM Integration** ✅ COMPLETE
- [x] Local Mistral 7B Instruct model integration
- [x] ctransformers runtime for GGUF inference
- [x] Abstractive summarization via instruct prompt
- [x] Context-window-aware prompt truncation
- [x] Graceful fallback when model unavailable
- [x] Environment variable configuration

**Phase v0.3 - Robust Retriever** 🔄 PLANNED
- [ ] Playwright integration for JS rendering
- [ ] Enhanced error handling
- [ ] Rate limiting
- [ ] Caching layer

**Phase v1.0 - Autonomous Agent** 📋 FUTURE
- [ ] ReAct architecture
- [ ] Multi-step research
- [ ] Knowledge graph generation

---

## 4. Testing

### 4.1 Test Strategy

**Test Levels:**
1. Unit tests (individual functions)
2. Integration tests (pipeline stages)
3. System tests (end-to-end)
4. Manual validation

### 4.2 Test Coverage

- [x] **Manual Testing**: Script runs successfully
- [x] **Smoke Test**: Model loads, search executes, LLM generates summary
- [x] **End-to-End**: Full pipeline verified with Mistral LLM
- [ ] **Unit Tests**: Not implemented (future)
- [ ] **Integration Tests**: Not implemented (future)

**Current Test Status**: Manual validation + end-to-end smoke test

### 4.3 Test Cases Executed

| Test Case | Input | Expected Result | Status |
|-----------|-------|-----------------|--------|
| Standard ML Query | "What is a Transformer model?" | Relevant passages + LLM summary | ✅ PASS |
| Web Scraping | Wikipedia URL | Clean text extraction | ✅ PASS |
| Embedding | Text chunks | 384-dim vectors | ✅ PASS |
| Ranking | Query + chunks | Top 3 most relevant | ✅ PASS |
| LLM Summarization | Top passages | Abstractive summary | ✅ PASS |
| Error Handling | Invalid URL | Graceful failure | ✅ PASS |
| Fallback | Missing GGUF file | Concatenation summary | ✅ PASS |

### 4.4 Known Issues

- Scraping may fail on JavaScript-heavy sites (403 errors)
- No rate limiting between requests
- CPU-only LLM inference is slow (~2-3 min)
- Memory usage scales with content size

---

## 5. Deployment

### 5.1 Environment Setup

**Development Environment:**
- Python 3.8+
- Virtual environment
- Local execution

**Deployment Requirements:**
- [x] requirements.txt documented
- [x] README.md with setup instructions
- [x] Environment variables documented
- [x] Model path configuration via MISTRAL_MODEL_PATH

### 5.2 Deployment Steps

1. Clone repository
2. Create virtual environment: `python3 -m venv venv`
3. Activate environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Place Mistral GGUF model at `../mistral-7b-instruct-v0.1.Q4_K_M.gguf`
6. Run agent: `python research_agent.py`

### 5.3 Rollback Plan

- Virtual environment can be recreated
- No database to migrate
- Version control tracks all changes
- Backups stored in `backups/` directory
- Fallback summarization when LLM unavailable

### 5.4 CI/CD Pipeline

**Current**: None (local development)
**Future Considerations:**
- GitHub Actions for automated testing
- Pre-commit hooks for linting
- Automated documentation generation

---

## 6. Maintenance

### 6.1 Changelog

**Location**: [CHANGELOG.md](CHANGELOG.md)

**Versioning**: Semantic Versioning (SemVer)
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

### 6.2 Issue Tracking

**Location**: [tasks.md](tasks.md)

**Categories:**
- Must Have: Critical features
- Should Have: Important features
- Could Have: Nice to have
- Won't Have: Out of scope

### 6.3 Documentation Maintenance

- [x] README.md kept current (updated for v0.2)
- [x] Architecture diagrams updated (LLM stage added)
- [x] Agent log entries added (v0.2 session)
- [x] Changelog updated (v0.2 entry)
- [x] Tasks updated (LLM summarization moved to Done)
- [x] Tech stack updated (ctransformers, Mistral)

### 6.4 Monitoring

**Metrics to Track (Production):**
- Request latency (total and per-stage)
- Success rate of scraping
- Memory usage (especially during LLM loading)
- Model inference time
- Error rates by type

**Current**: Console logging (local development)

---

## 7. Compliance Checklist

### 7.1 Code Quality

- [x] No hardcoded secrets
- [x] No API keys in code
- [x] Error handling implemented
- [x] Input validation present
- [x] Structured logging

### 7.2 Documentation

- [x] README.md complete
- [x] Architecture documented
- [x] Tech stack documented
- [x] SDLC documented
- [x] Agent log maintained
- [x] Changelog maintained
- [x] Troubleshooting guide included

### 7.3 Legal/Ethical

- [x] Respects robots.txt (manual check recommended)
- [x] User-Agent header set
- [x] Timeout implemented (10s)
- [x] No malicious scraping

---

## 8. Appendix

### 8.1 Glossary

- **RAG**: Retrieval-Augmented Generation
- **Embedding**: Vector representation of text
- **Cosine Similarity**: Measure of vector similarity
- **Chunking**: Splitting text into smaller pieces
- **Semantic Search**: Search based on meaning, not keywords
- **GGUF**: GPT-Generated Unified Format (llama.cpp model format)
- **Q4_K_M**: 4-bit quantization with K-means and medium precision
- **Abstractive Summarization**: Generating new text that captures the essence of source material

### 8.2 References

- Sentence Transformers: https://www.sbert.net/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
- DuckDuckGo Search: https://github.com/deedy5/duckduckgo-search
- ctransformers: https://github.com/marella/ctransformers
- Mistral AI: https://mistral.ai/
- RULES.md: Project operating rules
- guide.txt: Detailed implementation guide

### 8.3 Contact

- Project Owner: Ansh
- Last Updated: 2026-03-25

---

**SDLC Status**: ACTIVE DEVELOPMENT
**Current Phase**: v0.2 Mistral LLM Integration ✅ COMPLETE
