# Single-File Multi-Document RAG Server

This project now uses one robust RAG implementation: `rag_server.py`.

## What It Does

- Runs a minimal black-and-white web interface
- Lets users upload PDF documents (max 10 total)
- Stores uploaded PDFs in `runtime/user_uploads/`
- Clears the runtime upload folder every time the server restarts
- Supports interactive Q&A over uploaded documents
- Returns answers with source filenames and confidence score

## Run

```bash
./venv/bin/python rag_server.py
```

Then open:

- `http://127.0.0.1:8000`

## API Endpoints

- `GET /` - Web UI
- `GET /health` - Current document/chunk status
- `POST /upload` - Upload files as base64 JSON
- `POST /ask` - Ask a question
- `POST /reset` - Clear all uploaded docs

## Notes

- Only PDFs are accepted.
- Upload limit is enforced at 10 documents.
- The app is local and does not require API keys.
