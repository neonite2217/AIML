# Multi-Agent System with LangGraph

> A collaborative AI workflow demonstrating multi-agent orchestration using LangGraph. The system features a "Researcher" agent that gathers information and passes it to a "Writer" agent to generate blog posts.

## Tech Stack
| Component | Technology |
|-----------|------------|
| Language | Python 3.14 |
| Multi-agent Framework | LangGraph 1.1.3 |
| LLM Integration | langchain-ollama 1.0.1 |
| LLM Backend | Ollama (local) |
| State Management | TypedDict |

## Prerequisites
- Python 3.10+
- Ollama installed and running
- At least one LLM model pulled (e.g., qwen3.5, llama2, mistral)

## Installation

### Step 1: Clone/Navigate to Project
```bash
cd 24_Build_a_Multi-Agent_System_With_LangGraph
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt

# Install updated Ollama integration (if needed)
pip install langchain-ollama
```

### Step 5: Verify Ollama is Running
```bash
# Check if Ollama is running
ollama list

# If no models, pull one:
ollama pull qwen3.5
```

## Usage

### Running the System
```bash
source venv/bin/activate
python langgraph_system.py
```

### Expected Output
```
Ollama connection successful.
Invoking the multi-agent system...
--- Researcher Node ---
Research Notes: [AI-generated research content]
--- Writer Node ---
Blog post generated.
--- Final Output ---
[Generated blog post content]
```

### Customizing the Topic
Edit `langgraph_system.py` line 59:
```python
initial_state = {"topic": "Your custom topic here"}
```

### Changing the LLM Model
Edit `langgraph_system.py` line 13:
```python
llm = OllamaLLM(model="your-model-name")
```

Then run `ollama pull your-model-name` to download it.

## Project Structure
```
24_Build_a_Multi-Agent_System_With_LangGraph/
├── langgraph_system.py    # Main implementation
├── requirements.txt       # Python dependencies
├── guide.txt             # Detailed development guide
├── ENGINEERING_DECISIONS.md  # Architectural decisions
├── docs/
│   └── sdlc.md           # SDLC documentation
├── BUILD_ANALYSIS_LOG.md # Build analysis log
├── DEVELOPMENT_LOG.md    # Development log
└── venv/                 # Virtual environment
```

## Architecture Overview

The system uses LangGraph to orchestrate a two-agent workflow:

1. **State (AgentState):** A TypedDict containing `topic`, `research_notes`, and `final_output`
2. **Researcher Node:** Takes the topic, generates research notes via LLM
3. **Writer Node:** Takes research notes, generates a blog post via LLM
4. **Graph:** Connects nodes in sequence: START → Researcher → Writer → END

## Common Troubleshooting

### Issue: "Failed to connect to Ollama"
**Cause:** Ollama server not running or model not installed

**Solutions:**
1. Start Ollama server:
   ```bash
   ollama serve
   ```
2. Check available models:
   ```bash
   ollama list
   ```
3. Pull a model:
   ```bash
   ollama pull qwen3.5
   ```

### Issue: "ModuleNotFoundError: No module named 'langchain_ollama'"
**Cause:** langchain-ollama not installed

**Solution:**
```bash
pip install langchain-ollama
```

### Issue: "ModuleNotFoundError: No module named 'langgraph'"
**Cause:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "model 'llama2' not found (status code: 404)"
**Cause:** Model specified in code not installed

**Solution:** Change model in `langgraph_system.py` to one you have:
```python
llm = OllamaLLM(model="qwen3.5:latest")
```

### Issue: "Core Pydantic V1 functionality isn't compatible with Python 3.14"
**Cause:** Python 3.14 compatibility warning (non-critical)

**Solution:** This is a warning only. The system will still run correctly.

## Running Tests

### Smoke Test
```bash
source venv/bin/activate
python langgraph_system.py
```

Expected: Script runs without errors and generates a blog post

### Manual Test Cases

| Test | Input | Expected Behavior |
|------|-------|-------------------|
| Standard | "The latest advancements in AI" | Full workflow executes |
| Edge Case | "a cat" | Simple blog post generated |

## SDLC Status

See [docs/sdlc.md](docs/sdlc.md) for complete SDLC documentation.

## Contributing

This is an educational project. To extend:

1. **Add Tools:** Give the Researcher a web search tool
2. **Conditional Logic:** Add a gatekeeper node for quality control
3. **Human-in-the-Loop:** Add a node for human approval
4. **State Persistence:** Add checkpointing for long-running workflows

## License

This project is for educational purposes.

---

*Last updated: 2026-03-23*