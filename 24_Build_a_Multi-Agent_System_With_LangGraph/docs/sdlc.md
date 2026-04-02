# SDLC — Multi-Agent System with LangGraph

## 1. Requirements
- [x] Functional requirements listed
- [x] Non-functional requirements listed (performance, security, scalability)
- [x] User personas / target audience defined

### Functional Requirements
1. Multi-agent workflow with at least two agents (Researcher and Writer)
2. State management using TypedDict for type safety
3. Graph-based workflow orchestration using LangGraph
4. LLM integration via Ollama for local inference
5. Blog post generation from research notes

### Non-Functional Requirements
- **Performance:** Response time depends on local LLM model; should complete within reasonable time
- **Security:** Local LLM ensures data privacy; no external API calls
- **Scalability:** Architecture supports adding more nodes and conditional logic
- **Maintainability:** Clean separation of concerns with typed state and modular nodes

### User Personas
- Developers interested in AI agents and LangGraph
- Engineers learning multi-agent orchestration patterns
- Researchers exploring collaborative AI workflows

---

## 2. Design
- [x] Architecture diagram created
- [x] Tech stack finalised
- [x] API contracts defined
- [x] Database schema documented
- [ ] UI/UX wireframes (not applicable)

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Multi-Agent System                       │
│                      (LangGraph Workflow)                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  START   │───▶│ Researcher│───▶│  Writer  │───▶│  END   │
│  └──────────┘    │   Node    │    │   Node   │    └──────────┘
│                  └──────────┘    └──────────┘              │
│                       │               │                     │
│                       ▼               ▼                     │
│                  ┌─────────────────────────────────┐        │
│                  │      AgentState (TypedDict)     │        │
│                  │  - topic: str                   │        │
│                  │  - research_notes: str         │        │
│                  │  - final_output: str           │        │
│                  └─────────────────────────────────┘        │
│                              │                               │
│                              ▼                               │
│                  ┌─────────────────────────────────┐        │
│                  │        Ollama LLM               │        │
│                  │    (qwen3.5:latest)             │        │
│                  └─────────────────────────────────┘        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack
| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.14 |
| Multi-agent Framework | LangGraph | 1.1.3 |
| LLM Integration | langchain-ollama | 1.0.1 |
| LLM Backend | Ollama | latest |
| State Management | TypedDict | built-in |
| Package Manager | pip | 25.1+ |

### API Contracts
The system uses a programmatic API through the compiled LangGraph app:

```python
# Input
initial_state = {"topic": "The latest advancements in AI"}

# Output
final_state = {
    "topic": "...",
    "research_notes": "...",
    "final_output": "..."
}
```

---

## 3. Development
- [x] Coding standards followed (see RULES.md Phase 4)
- [ ] Feature branches used (not applicable for single developer)
- [ ] Code reviewed before merge (not applicable)

### Development Status
- Core workflow implemented and tested
- Two agents (Researcher, Writer) working in sequence
- State passing between nodes verified

---

## 4. Testing
- [ ] Unit tests written (>70% coverage)
- [x] Integration tests written
- [x] Smoke test passes
- [x] Edge cases tested

### Test Results
| Test Case | Input | Expected | Result |
|-----------|-------|----------|--------|
| Standard Case | "The latest advancements in AI" | Blog post generated | PASS |
| Edge Case | "a cat" | Simple blog post | PASS |

### Smoke Test Verification
```
$ python langgraph_system.py
Ollama connection successful.
Invoking the multi-agent system...
--- Researcher Node ---
--- Writer Node ---
--- Final Output ---
[Blog post content]
```

---

## 5. Deployment
- [x] Environment variables documented
- [ ] Deployment guide written
- [ ] Rollback plan documented
- [ ] CI/CD pipeline configured

### Environment Variables
| Name | Required | Description | Default |
|------|----------|-------------|---------|
| OLLAMA_HOST | No | Ollama server URL | http://localhost:11434 |
| LLM_MODEL | No | Model to use | qwen3.5:latest |

### Notes
- This is a local development project
- No production deployment required
- Runs locally with Ollama

---

## 6. Maintenance
- [x] Changelog kept up to date
- [x] Known issues tracked
- [x] Agent log maintained

---

## Phase History

| Phase | Status | Date | Notes |
|-------|--------|------|-------|
| Requirements | COMPLETE | 2026-01-30 | Defined in guide.txt |
| Design | COMPLETE | 2026-01-30 | TypedDict state, LangGraph |
| Development | COMPLETE | 2026-03-23 | Verified with Ollama |
| Testing | COMPLETE | 2026-03-23 | Smoke test passes |
| Deployment | N/A | - | Local project |
| Maintenance | ONGOING | 2026-03-23 | Documentation updated |

---

*Last updated: 2026-03-23*