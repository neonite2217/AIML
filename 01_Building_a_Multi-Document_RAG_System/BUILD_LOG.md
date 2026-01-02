# BUILD_LOG.md — Multi-Document RAG System

## What Was Built

A fully local Multi-Document RAG (Retrieval-Augmented Generation) pipeline that:
1. Loads multiple PDF documents from a folder
2. Chunks text with overlap to preserve context across boundaries
3. Embeds chunks using TF-IDF and stores them in an in-memory vector store
4. Retrieves the most relevant chunks via cosine similarity for any query
5. Formats a strict "answer only from context" prompt and passes it to an LLM

**Why TF-IDF instead of ChromaDB/sentence-transformers:**  
Python 3.14 breaks ChromaDB's native bindings and Pydantic v1 compatibility. TF-IDF via `scikit-learn` is a zero-dependency, fully compatible alternative that still demonstrates the core RAG concept correctly.

**Why FakeListLLM:**  
No paid API keys are used. `FakeListLLM` simulates LLM responses for demo purposes. To use a real local LLM, swap it with an Ollama-backed `langchain_community.llms.Ollama` instance (see below).

---

## How to Run

```bash
# Activate the existing venv
source venv/bin/activate

# Run the main script
python multi_doc_rag.py
```

No additional setup needed — the venv is already created and all dependencies are installed.

---

## Sample Output

```
Loaded 2 documents
Created 2 text chunks
Vector store created and persisted in memory.

--- Query: 'What is the currency of Japan?' ---
Answer: The currency of Japan is the Yen.

--- Query: 'What is the capital of France?' ---
Answer: The capital of France is Paris.

✓ Multi-Document RAG System demo completed successfully!
```

---

## Dependencies

Listed in `requirements.txt`:
- `langchain`, `langchain-core`, `langchain-community`, `langchain-text-splitters` — RAG pipeline
- `pypdf` — PDF loading
- `scikit-learn`, `numpy` — TF-IDF embeddings and cosine similarity
- `reportlab` — generates `doc1.pdf` / `doc2.pdf` if they don't exist

---

## Architecture

```
PDF files (doc1.pdf, doc2.pdf)
        │
        ▼
  PyPDFLoader  →  all_docs (LangChain Documents)
        │
        ▼
  RecursiveCharacterTextSplitter (chunk_size=500, overlap=50)
        │
        ▼
  TfidfEmbeddings (scikit-learn TfidfVectorizer)
        │
        ▼
  InMemoryVectorStore (cosine similarity search)
        │
   query ──▶  similarity_search(k=4)  ──▶  top-k chunks
                                                │
                                    PromptTemplate (context + question)
                                                │
                                            LLM.invoke()
                                                │
                                            Answer
```

---

## Known Issues / Notes

- **Pydantic v1 warning**: Python 3.14 triggers a `UserWarning` from `langchain_core` about Pydantic v1 compatibility. This is cosmetic — all functionality works correctly.
- **FakeListLLM**: Responses are hardcoded in order. For real Q&A, replace with Ollama:
  ```python
  from langchain_community.llms import Ollama
  llm = Ollama(model="llama3")
  ```
- **In-memory store**: The vector store is rebuilt on each run (no persistence). For persistence, use ChromaDB once Python 3.14 support stabilises.

---

## Date

Built: 2026-03-14
