# Real-Time AI Assistant (RAG + LangChain)

> An intelligent AI assistant that performs real-time web searches using Retrieval-Augmented Generation (RAG) to provide accurate, up-to-date answers to user queries.

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM** | Qwen3.5 (via Ollama) | Local language model for answer generation |
| **Framework** | LangChain 1.2+ | RAG pipeline orchestration |
| **Search Tool** | DuckDuckGo Search | Real-time web search |
| **Language** | Python 3.10+ | Core implementation |
| **Integration** | Ollama | Local LLM runtime |

## Prerequisites

Before installing, ensure you have:

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **Ollama** - [Install Ollama](https://ollama.ai/)
- **Internet connection** - Required for web searches

### Verify Prerequisites

```bash
# Check Python version
python --version  # Should be 3.10+

# Check Ollama installation
ollama --version

# Verify Ollama is running
ollama list
```

## Installation

### Quick Start (Automated)

```bash
# Run the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Manual Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd 27_Build_a_Real-Time_AI_Assistant_Using_RAG_LangChain
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Pull the Qwen3.5 model (if not already available):**
   ```bash
   ollama pull qwen3.5
   ```

5. **Verify installation:**
   ```bash
   python real_time_assistant.py
   ```

## Usage

### Running the Assistant

The assistant runs in non-interactive demonstration mode by default:

```bash
python real_time_assistant.py
```

This will execute three demonstration queries:
1. Latest news about OpenAI
2. Recent developments in quantum computing
3. Main announcements at the last Apple event

### Interactive Mode

To enable interactive mode, edit `real_time_assistant.py` and uncomment line 119:

```python
# Change this line:
# run_assistant()

# To:
run_assistant()
```

Then run:
```bash
python real_time_assistant.py
```

### Example Interaction

```
Starting the Real-Time AI Assistant...
Try asking: 'What were the main announcements at the last Apple event?'

Enter your question (or 'exit' to quit): What is the weather like today?

Thinking...
[Response streams in real-time]
```

## Project Structure

```
27_Build_a_Real-Time_AI_Assistant_Using_RAG_LangChain/
├── docs/                          # Documentation directory
│   ├── agent_log.md              # Agent session logs
│   ├── architecture.md           # System architecture
│   ├── CHANGELOG.md              # Version history
│   ├── sdlc.md                   # SDLC tracking
│   ├── tasks.md                  # Task backlog
│   └── tech_stack.md             # Technology decisions
├── scripts/                       # Utility scripts
│   ├── setup.sh                  # Linux/macOS setup
│   └── setup.ps1                 # Windows setup
├── backups/                       # File backups (git-ignored)
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── ENGINEERING_DECISIONS.md       # Engineering decision log
├── rag_output.log                 # Execution logs (generated)
├── real_time_assistant.py         # Main application
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── RULES.md                       # Development rules
```

## Architecture Overview

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DuckDuckGo     │
│  Search Tool    │
└────────┬────────┘
         │
         │ Search Results
         ▼
┌─────────────────┐
│  Prompt         │
│  Template       │
│  (Context +     │
│   Question)     │
└────────┬────────┘
         │
         │ Formatted Prompt
         ▼
┌─────────────────┐
│  Qwen3.5 LLM    │
│  (via Ollama)   │
└────────┬────────┘
         │
         │ Generated Answer
         ▼
┌─────────────────┐
│   User          │
│   Response      │
└─────────────────┘
```

### Data Flow

1. **Query Input**: User submits a natural language question
2. **Retrieval**: DuckDuckGo search retrieves real-time web results
3. **Context Building**: Search results are formatted into a prompt template
4. **Generation**: Qwen3.5 LLM generates an answer based on the context
5. **Output**: Answer is streamed back to the user in real-time

## Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `OLLAMA_HOST` | No | Ollama server host | `127.0.0.1` |
| `OLLAMA_PORT` | No | Ollama server port | `11434` |
| `LOG_LEVEL` | No | Logging verbosity | `INFO` |

Create a `.env` file from the template:
```bash
cp .env.example .env
```

## Running Tests

### Smoke Test

```bash
python real_time_assistant.py
```

Expected output:
- Ollama connection successful
- Three demonstration queries executed
- Responses generated for each query
- Logs saved to `rag_output.log`

### Manual Testing

```bash
# Test Ollama connection
ollama run qwen3.5 "Hello, how are you?"

# Test search tool independently
python -c "from langchain_community.tools import DuckDuckGoSearchRun; search = DuckDuckGoSearchRun(); print(search.run('Python programming'))"
```

## SDLC Status

Current Phase: **✅ Deployment Complete**

See [docs/sdlc.md](docs/sdlc.md) for full SDLC tracking.

## Contributing

1. Read [RULES.md](RULES.md) completely before making changes
2. Create a feature branch
3. Follow the coding standards in RULES.md
4. Update documentation
5. Run smoke tests
6. Submit a pull request

## Known Issues

| Issue | Status | Workaround |
|-------|--------|------------|
| Grokipedia engine errors in search | Minor | Non-blocking; other search engines compensate |
| Python 3.14 Pydantic v1 warnings | Minor | Non-critical; functionality unaffected |

## Troubleshooting

### Common Issues

#### 1. Ollama Connection Failed

**Error:** `Failed to connect to Ollama`

**Solution:**
```bash
# Start Ollama service
ollama serve

# In a separate terminal, verify it's running
ollama list

# Pull the model if missing
ollama pull qwen3.5
```

#### 2. Module Not Found: ddgs

**Error:** `ModuleNotFoundError: No module named 'ddgs'`

**Solution:**
```bash
pip install ddgs
```

#### 3. Slow Response Times

**Cause:** Large search results or model loading

**Solution:**
- Ensure Ollama has the model loaded: `ollama run qwen3.5 "test"`
- Check internet connection for search
- Consider using a smaller model if needed

#### 4. Search Returns Empty Results

**Cause:** Network issues or search engine limitations

**Solution:**
- Verify internet connectivity
- Try a different query
- Check `rag_output.log` for detailed error messages

## License

This project is for educational purposes as part of the SUPER_30 learning series.

## Contact

Project Owner: Ansh

---

*Last Updated: 2026-03-25*
