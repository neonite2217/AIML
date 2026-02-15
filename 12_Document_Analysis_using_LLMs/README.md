# Document Analysis using LLMs
> Extract, chunk, retrieve, and query PDF content with a hardware-aware local pipeline.

## Tech Stack
- Python 3.12+
- PyMuPDF (`fitz`) for PDF extraction
- ChromaDB for vector retrieval
- FLAN-T5 (`google/flan-t5-large`) for answer generation
- Streamlit for UI

## Prerequisites
- Python 3.12+
- `pip`
- Optional CUDA-capable GPU (falls back to CPU automatically)

## Installation
```bash
cd 12_Document_Analysis_using_LLMs
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage
### CLI mode
```bash
python cli_test.py info
python cli_test.py process --pdf sample_document.pdf
python cli_test.py query --pdf sample_document.pdf --question "What is the agreement about?" --results 2
```

### Streamlit app
```bash
streamlit run app.py
```

## Project Structure
```text
12_Document_Analysis_using_LLMs/
├── document_analysis.py        # Core extraction, chunking, retrieval, and generation pipeline
├── cli_test.py                 # CLI test harness
├── app.py                      # Streamlit UI
├── sample_document.pdf         # Sample input document
├── chroma_db/                  # Persistent Chroma vector storage
├── BUILD_FROM_SCRATCH.md       # Clean setup and run guide
├── BUILD_LOG.md                # Verified run notes
├── requirements.txt            # Dependencies
└── docs/
    └── sdlc.md                 # SDLC status and lifecycle plan
```

## Architecture Overview
1. Detect hardware (CPU/GPU) and choose chunking strategy.
2. Extract document text (PyMuPDF).
3. Chunk text (standard recursive or parent-child strategy).
4. Index chunks in ChromaDB.
5. Retrieve top relevant chunks for user query.
6. Generate answer with FLAN-T5 constrained by retrieved context.

## Environment Variables
| Name | Required | Description | Default |
|---|---|---|---|
| `CHROMA_TELEMETRY` | No | Informational toggle only; telemetry is programmatically disabled in code | disabled |
| `CUDA_VISIBLE_DEVICES` | No | Restrict visible GPU devices | system default |

## Running Tests
CLI smoke tests:
```bash
python cli_test.py info
python cli_test.py process --pdf sample_document.pdf
python cli_test.py query --pdf sample_document.pdf --question "What is the agreement about?" --results 2
```

Expected:
- system info loads successfully
- document processing reports chunk creation
- query returns retrieved context block

## SDLC Status
- Current phase: **Verified implementation and docs complete**
- Details: [`docs/sdlc.md`](./docs/sdlc.md)

## Contributing
1. Keep retrieval and generation behavior transparent via logs.
2. Document any model/config changes in `BUILD_LOG.md`.
3. Re-run CLI smoke commands after core pipeline changes.

## License
Project-level license is not explicitly defined. Follow repository owner guidance.
