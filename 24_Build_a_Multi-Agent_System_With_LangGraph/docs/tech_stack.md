# Tech Stack — Multi-Agent System with LangGraph

## Languages & Runtimes

| Component | Technology | Version | Rationale |
|-----------|------------|---------|-----------|
| Primary Language | Python | 3.14 | Required for LangGraph and LangChain |
| LLM Runtime | Ollama | latest | Local, private, free LLM inference |

## Frameworks & Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| langgraph | 1.1.3 | Multi-agent orchestration framework |
| langchain | 1.2.13 | LLM integration framework |
| langchain-community | 0.4.1 | Community tools and integrations |
| langchain-ollama | 1.0.1 | Ollama LLM integration (replaces deprecated) |
| langchain-core | 1.2.20 | Core LangChain functionality |

## Development Tools

| Tool | Purpose |
|------|---------|
| pip | Package management |
| venv | Virtual environment isolation |
| Python 3.14 | Runtime environment |

## Runtime Environment

| Component | Configuration |
|-----------|--------------|
| Python | 3.14 |
| Ollama URL | http://localhost:11434 |
| Default Model | qwen3.5:latest |
| Virtual Environment | venv/ |

## Dependencies Summary

```
langgraph==1.1.3
langchain==1.2.13
langchain-community==0.4.1
langchain-ollama==1.0.1
ollama==0.6.1
duckduckgo-search==8.1.1
```

## External Services

| Service | Purpose | Connection |
|---------|---------|------------|
| Ollama | Local LLM inference | localhost:11434 |
| (none) | No external API calls | - |

---

*Tech stack optimized for local development and learning.*
*Last updated: 2026-03-23*