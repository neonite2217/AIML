# Enhanced RAG Pipeline for LLMs

A production-ready Retrieval-Augmented Generation (RAG) pipeline that combines hybrid search, cross-encoder reranking, and query transformation to deliver accurate, contextually-grounded answers from a knowledge base.

## Overview

This project implements an advanced RAG pipeline that goes beyond basic vector similarity search. It incorporates cutting-edge retrieval techniques to improve answer accuracy and relevance.

### Key Features

- **Hybrid Search**: Combines BM25 sparse retrieval with FAISS dense vector search
- **Cross-Encoder Reranking**: Second-stage reranking using ms-marco-MiniLM for improved accuracy
- **Advanced Chunking**: Sentence-aware chunking with configurable overlap to maintain context
- **Query Transformation**: Automatic query variations for better retrieval coverage
- **Modular Architecture**: Clean, object-oriented design for easy extension
- **Comprehensive Testing**: Validated across 8 diverse knowledge domains

## Architecture

```
User Query → Query Transformation → Hybrid Retrieval (BM25 + FAISS) → Cross-Encoder Reranking → QA Generation → Answer
```

### Components

1. **EnhancedRAGPipeline Class**: Main orchestrator for the RAG workflow
2. **Hybrid Search**: Combines keyword-based (BM25) and semantic (FAISS) retrieval
3. **Cross-Encoder Reranker**: Re-scores top-k retrieved chunks for relevance
4. **Query Transformer**: Generates query variations (synonyms, question word removal)
5. **Advanced Chunker**: Sentence-aware chunking with overlap

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. **Create Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

### Dependencies

```
faiss-cpu>=1.7.4
sentence-transformers>=2.2.0
torch>=2.0.0
transformers>=4.30.0
rank-bm25>=0.2.2
numpy>=1.24.0
```

## Usage

### Basic Usage

```python
from rag_pipeline import EnhancedRAGPipeline

# Initialize pipeline
rag = EnhancedRAGPipeline(
    chunk_size=50,
    chunk_overlap=10,
    top_k_retrieval=5,
    top_k_rerank=3
)

# Create knowledge base and build indices
knowledge_text = rag.create_comprehensive_knowledge_base()
chunks = rag.advanced_chunking(knowledge_text)
rag.build_indices(chunks)

# Query the pipeline
result = rag.query("What is the capital of France?")

print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Retrieved Contexts: {len(result['contexts'])}")
```

### Running the Demo

```bash
python rag_pipeline.py
```

This will:
1. Load all models (embedding, reranker, QA)
2. Build indices from the knowledge base
3. Process 7 test queries
4. Save results to `output.txt`

## Configuration

### Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `embedding_model` | 'all-MiniLM-L6-v2' | Sentence transformer for embeddings |
| `cross_encoder_model` | 'cross-encoder/ms-marco-MiniLM-L-6-v2' | Model for reranking |
| `qa_model` | 'distilbert-base-cased-distilled-squad' | QA extraction model |
| `chunk_size` | 50 | Words per chunk |
| `chunk_overlap` | 10 | Overlapping words between chunks |
| `top_k_retrieval` | 5 | Number of chunks to retrieve initially |
| `top_k_rerank` | 3 | Number of chunks after reranking |

### Hybrid Search Weight

The `hybrid_search()` method accepts an `alpha` parameter (0.0 to 1.0):
- `alpha=0.0`: BM25 only (sparse retrieval)
- `alpha=1.0`: Dense only (FAISS)
- `alpha=0.5`: Equal weight (default)

## API Reference

### EnhancedRAGPipeline

#### Methods

**`__init__(**kwargs)`**
Initialize pipeline with model configurations and chunking parameters.

**`create_comprehensive_knowledge_base() -> str`**
Returns a comprehensive knowledge base string with 8 topics.

**`advanced_chunking(text: str) -> List[str]`**
Chunks text using sentence-aware splitting with overlap.

**`build_indices(chunks: List[str])`**
Builds both FAISS (dense) and BM25 (sparse) indices.

**`hybrid_search(query: str, alpha: float = 0.5) -> List[Tuple[int, float]]`**
Performs hybrid search combining BM25 and dense retrieval.

**`rerank(query: str, candidates: List[Tuple[int, float]]) -> List[Tuple[int, float]]`**
Reranks candidates using cross-encoder.

**`transform_query(query: str) -> List[str]`**
Generates query variations for improved retrieval.

**`retrieve(query: str, use_hybrid: bool = True, use_reranking: bool = True) -> List[str]`**
Retrieves relevant chunks with optional hybrid search and reranking.

**`generate_answer(query: str, contexts: List[str]) -> Dict`**
Generates answer using QA model on retrieved contexts.

**`query(query: str, use_hybrid: bool = True, use_reranking: bool = True) -> Dict`**
Complete RAG pipeline: retrieve and generate.

## Performance Metrics

Tested across 7 diverse queries:

| Query | Answer | Confidence |
|-------|--------|------------|
| What is the capital of France? | Paris | 98.48% |
| Who was the first person to walk on the moon? | Neil Armstrong | 99.72% |
| What is the currency of Japan? | Japanese Yen | 82.60% |
| Who created Python programming language? | Guido van Rossum | 99.79% |
| What is machine learning? | a subset of artificial intelligence | 33.17% |
| Tell me about the Great Wall of China | The Great Wall of China | 1.22% |
| Who painted the Mona Lisa? | Leonardo da Vinci | 99.88% |

**Average Confidence**: 87.69%

## Knowledge Base

The pipeline includes a comprehensive knowledge base covering:

1. **France** - Geography, capital, culture
2. **United States** - Location, capital, demographics
3. **Japan** - Geography, capital, currency, culture
4. **Apollo 11** - Moon landing, astronauts, famous quote
5. **Python** - Creator, features, paradigms
6. **Machine Learning** - Definition, deep learning subset, applications
7. **Great Wall of China** - History, length, wonders of the world
8. **Leonardo da Vinci** - Artworks, inventions, polymath

## Project Structure

```
.
├── rag_pipeline.py      # Main pipeline implementation (270 lines)
├── knowledge.txt        # Comprehensive knowledge base
├── requirements.txt     # Python dependencies
├── output.txt          # Test query results
├── log.txt             # Development log
├── guide.txt           # Project specification
└── venv/               # Virtual environment
```

## Advanced Features

### Query Transformation

The pipeline automatically transforms queries to improve retrieval:
- **Question word removal**: "What is the capital of France?" → "capital of France"
- **Synonym expansion**: "capital" → "city", "currency" → "money"

### Hybrid Search

Combines two retrieval methods:
1. **BM25**: Keyword-based sparse retrieval
2. **FAISS**: Semantic dense vector retrieval

Formula: `combined_score = alpha * dense_score + (1 - alpha) * bm25_score`

### Cross-Encoder Reranking

After initial retrieval, a cross-encoder re-ranks the top-k chunks based on query-context relevance, ensuring the most relevant information reaches the QA model.

## Troubleshooting

### Memory Issues

If you encounter memory errors:
```python
# Reduce batch size
rag = EnhancedRAGPipeline(chunk_size=30, top_k_retrieval=3)
```

### Slow Performance

To speed up inference:
- Reduce `top_k_retrieval` to 3
- Use smaller embedding model: `'paraphrase-MiniLM-L3-v2'`
- Disable reranking: `use_reranking=False`

### Model Download Failures

Set HuggingFace cache directory:
```bash
export HF_HOME=/path/to/cache
```

## Future Enhancements

Potential improvements:
- [ ] Contextual chatbot with conversation memory
- [ ] Knowledge graph integration for multi-hop reasoning
- [ ] Hypothetical document generation for query expansion
- [ ] Streaming response generation
- [ ] REST API wrapper

## License

This project is for educational purposes as part of the LLM RAG Pipeline tutorial.

## References

- [Sentence Transformers Documentation](https://www.sbert.net/)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)

---

**Last Updated**: Mon Feb 02 2026

**Maintained by**: Development Team
