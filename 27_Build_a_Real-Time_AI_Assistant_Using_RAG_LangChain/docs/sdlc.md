# SDLC — Real-Time AI Assistant (RAG + LangChain)

## 1. Requirements

### Functional Requirements
- [x] Accept natural language questions from users
- [x] Perform real-time web searches using DuckDuckGo
- [x] Generate answers using a local LLM (Qwen3.5 via Ollama)
- [x] Stream responses in real-time for better UX
- [x] Log all interactions to a file for debugging
- [x] Support both interactive and demonstration modes

### Non-Functional Requirements
- [x] **Performance**: Response generation within 60 seconds for typical queries
- [x] **Security**: No API keys or secrets hardcoded
- [x] **Scalability**: Single-user local deployment (not designed for high concurrency)
- [x] **Maintainability**: Clear code structure with comprehensive documentation
- [x] **Reliability**: Graceful error handling with informative messages

### User Personas
- **Primary**: Students and developers learning RAG patterns
- **Secondary**: Researchers needing quick access to recent information
- **Technical Level**: Intermediate Python developers

---

## 2. Design

### Architecture
- [x] Architecture diagram created (see [docs/architecture.md](architecture.md))
- [x] Tech stack finalised (see [docs/tech_stack.md](tech_stack.md))
- [x] Component interactions defined
- [x] Data flow documented

### Design Documents
- [x] System components identified
- [x] RAG pipeline design documented
- [x] Error handling strategy defined
- [x] Logging approach specified

---

## 3. Development

### Coding Standards
- [x] PEP 8 style guide followed
- [x] Max line length: 120 characters
- [x] Docstrings for all functions
- [x] No magic numbers
- [x] No commented-out code
- [x] Logging instead of print statements

### Version Control
- [x] Feature-based development
- [x] Incremental commits with descriptive messages
- [x] No direct commits to main without testing

---

## 4. Testing

### Test Coverage
- [x] Smoke test implemented
- [x] Integration test (Ollama + Search + LLM)
- [x] Manual test cases documented
- [x] Edge cases considered (empty queries, network failures)

### Test Results
- [x] Smoke test: **PASS**
- [x] Ollama connection: **PASS**
- [x] Search functionality: **PASS**
- [x] Response generation: **PASS**
- [x] Logging: **PASS**

---

## 5. Deployment

### Environment Setup
- [x] Environment variables documented (`.env.example`)
- [x] Setup script created (`scripts/setup.sh`)
- [x] Windows setup script created (`scripts/setup.ps1`)
- [x] Dependencies pinned in `requirements.txt`

### Deployment Guide
- [x] Installation steps documented
- [x] Prerequisites clearly stated
- [x] Verification steps included

### Rollback Plan
- [x] Backup directory structure created
- [x] Version control enables easy rollback
- [x] Dependencies can be reinstalled from requirements.txt

### CI/CD
- [ ] CI/CD pipeline configured (Not applicable for local-only project)

---

## 6. Maintenance

### Documentation
- [x] Changelog maintained ([docs/CHANGELOG.md](CHANGELOG.md))
- [x] Known issues tracked in README
- [x] Agent log maintained ([docs/agent_log.md](agent_log.md))
- [x] Tasks tracked ([docs/tasks.md](tasks.md))

### Monitoring
- [x] Execution logs saved to `rag_output.log`
- [x] Error logging implemented
- [x] Search engine errors captured

---

## SDLC Phase Status

| Phase | Status | Completion Date |
|-------|--------|-----------------|
| Requirements | ✅ Complete | 2026-01-30 |
| Design | ✅ Complete | 2026-01-30 |
| Development | ✅ Complete | 2026-03-25 |
| Testing | ✅ Complete | 2026-03-25 |
| Deployment | ✅ Complete | 2026-03-25 |
| Maintenance | 🔄 Active | Ongoing |

---

## Sign-Off

**Project Owner:** Ansh  
**Final Review Date:** 2026-03-25  
**Version:** 1.0.0

---

*Last Updated: 2026-03-25*
