# Architecture — Multi-Agent System with LangGraph

## System Overview

This project demonstrates a collaborative AI workflow using LangGraph. A "Researcher" agent gathers information on a topic and passes its findings to a "Writer" agent, which composes a blog post. The system is designed as a stateful graph where agents communicate through a shared state object.

## Component Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                     LangGraph Workflow                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐                                                │
│   │  START   │                                                │
│   └────┬─────┘                                                │
│        │                                                      │
│        ▼                                                      │
│   ┌─────────────────────────────────────────────────────┐     │
│   │              AgentState (TypedDict)                  │     │
│   │  - topic: str          (input)                      │     │
│   │  - research_notes: str (intermediate)                │     │
│   │  - final_output: str   (output)                      │     │
│   └─────────────────────────────────────────────────────┘     │
│        │                                                      │
│        ▼                                                      │
│   ┌──────────────┐    ┌──────────────┐    ┌─────────────┐    │
│   │  Researcher  │───▶│    Writer    │───▶│     END     │    │
│   │    Node      │    │    Node      │    │             │    │
│   └──────────────┘    └──────────────┘    └─────────────┘    │
│        │                    │                                  │
│        ▼                    ▼                                  │
│   ┌─────────────────────────────────────────────────────┐    │
│   │              LLM (Ollama - qwen3.5:latest)           │    │
│   └─────────────────────────────────────────────────────┘    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Initialization:** Initial state created with `topic` field
2. **Researcher Node:** 
   - Receives state with `topic`
   - Invokes LLM to generate research notes
   - Returns updated state with `research_notes`
3. **Writer Node:**
   - Receives state with `research_notes`
   - Invokes LLM to generate blog post
   - Returns updated state with `final_output`
4. **Termination:** Graph reaches END, final state returned

## Key Design Decisions

### 1. Framework Choice: LangGraph
**Rationale:** LangGraph provides a formal structure for defining states, nodes (agents), and edges (transitions). This makes the workflow explicit, debuggable, and designed for cycles which are common in agentic workflows.

### 2. State Management: TypedDict
**Rationale:** TypedDict provides static type checking and excellent developer experience with autocompletion. It's lightweight (part of standard library) and clearly documents the expected state shape.

### 3. LLM Backend: Local with Ollama
**Rationale:** Ollama provides free, private, and offline LLM access. It works locally without API costs, perfect for development and experimentation.

### 4. Sequential Agent Pattern
**Rationale:** Simple linear workflow (Researcher → Writer) demonstrates core multi-agent patterns without complexity of parallel execution or conditional logic.

## External Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| langgraph | Multi-agent orchestration | 1.1.3 |
| langchain | LLM integration framework | 1.2.13 |
| langchain-ollama | Ollama LLM integration | 1.0.1 |
| ollama | Local LLM server | 0.6.1 |
| duckduckgo-search | Web search capability | 8.1.1 |

## Extension Points

The architecture supports these extensions:

1. **Tool Integration:** Add web search to Researcher node
2. **Conditional Edges:** Add gatekeeper for quality control
3. **Parallel Nodes:** Multiple researchers for different aspects
4. **Human-in-the-Loop:** Add approval nodes
5. **State Persistence:** Checkpointing with SQLite

---

*Architecture follows clean separation of concerns.*
*Last updated: 2026-03-23*