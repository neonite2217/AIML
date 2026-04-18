# BUILD LOG — Agentic RAG Pipeline

## What Was Built

An agentic RAG (Retrieval-Augmented Generation) pipeline that routes queries intelligently:

- **Router**: keyword-based classifier decides whether a query needs document retrieval or can be answered directly by the LLM
- **RAG path**: retrieves top-2 relevant chunks from a Chroma vector store, builds a context-augmented prompt, and generates an answer
- **Direct path**: passes the query straight to the LLM without retrieval
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` via `langchain-community`
- **LLM**: `google/flan-t5-base` loaded directly via HuggingFace `transformers` (no paid APIs)
- **Vector store**: ChromaDB (persisted to `./chroma_db`)
- **Documents**: a dummy PDF (`agentic_rag_doc.pdf`) with facts about France/Paris

## How to Run

```bash
# From the project directory
source venv/bin/activate
python agentic_rag.py
```

## Sample Output

```
Indexed 1 chunks into Chroma.
Loading google/flan-t5-base...
LLM ready.

============================================================
AGENTIC RAG PIPELINE — QUERY ROUTING DEMO
============================================================

Query  : What is 2 + 2?
Route  : DIRECT
Answer : a doubling of 2

Query  : What is the capital of France?
Route  : RAG
Answer : Paris

Query  : Tell me about the Eiffel Tower.
Route  : RAG
Answer : The Eiffel Tower is a tall building in Paris.

Query  : What color is the sky?
Route  : DIRECT
Answer : blue

Query  : When did the French Revolution begin?
Route  : RAG
Answer : (iii).
============================================================
```

## Issues & Notes

- **Venv was broken**: the original venv pointed to a non-existent Python path (`/home/ansh/Downloads/p3/...`). Recreated with `/usr/bin/python3` (3.14.3).
- **`langchain.text_splitter` removed**: in langchain 1.x, moved to `langchain_text_splitters`. Fixed import.
- **`langchain.chains.RetrievalQA` removed**: dropped in langchain 1.x. Replaced with a manual RAG chain (similarity search + prompt construction).
- **`text2text-generation` pipeline removed**: dropped in newer `transformers`. Used `T5ForConditionalGeneration` + `T5Tokenizer` directly instead.
- **Router accuracy**: the keyword-based router works well for the demo queries. The "French Revolution" answer from flan-t5-base is weak (`(iii).`) — the model is small (250M params) and the PDF chunk only has one sentence about it. A larger model or more document content would improve this.
- **Deprecation warning**: `SentenceTransformerEmbeddings` is deprecated in favor of `langchain-huggingface`. Functional for now; migrate to `langchain-huggingface` for future-proofing.
