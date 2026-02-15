# SDLC - Document Analysis using LLMs

## 1. Requirements
### Functional
- Extract text from input documents (PDF/TXT/MD).
- Chunk content for semantic retrieval.
- Index chunks in vector store.
- Retrieve relevant context for user questions.
- Generate answers grounded in retrieved context.

### Non-Functional
- Run on both CPU and GPU environments.
- Provide both CLI and UI interfaces.
- Maintain deterministic and debuggable behavior.

## 2. Design
- Modular components:
  - `HardwareDetector`
  - `DocumentExtractor`
  - `Chunker` (standard and parent-child)
  - `VectorStore`
  - `Generator`
- Main orchestrator: `DocumentAnalysisV2`.

## 3. Implementation
- ChromaDB persistent vector store integrated.
- FLAN-T5 answer generator integrated.
- CLI utility (`cli_test.py`) implemented for operational checks.
- Telemetry disabled in vector store client to improve behavior in offline/restricted runs.

## 4. Verification
Verified on 2026-03-17:
- `./venv/bin/python cli_test.py info` -> PASS
- `./venv/bin/python cli_test.py process --pdf sample_document.pdf` -> PASS
- `./venv/bin/python cli_test.py query --pdf sample_document.pdf --question "What is the agreement about?" --results 2` -> PASS

## 5. Deployment / Runtime
- Local runtime via CLI or Streamlit.
- ChromaDB persisted under `./chroma_db`.

## 6. Maintenance
- Re-run CLI smoke checks when changing chunking, vector store, or model behavior.
- Track updates in `BUILD_LOG.md`.

## 7. Risks and Mitigation
- Risk: Large model load time on CPU.
  - Mitigation: keep CLI smoke tests targeted and bounded.
- Risk: Network noise from telemetry in restricted environments.
  - Mitigation: telemetry disabled in `VectorStore` initialization.

## 8. Current SDLC Phase (2026-03-17)
- Requirements: Complete
- Design: Complete
- Implementation: Complete
- Verification: Complete
- Documentation: Complete
- Status: Ready / Completed
