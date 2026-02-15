# Build From Scratch - Project 12

## 1. Clean Setup
```bash
cd 12_Document_Analysis_using_LLMs
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Smoke Verification (CLI)
```bash
python cli_test.py info
python cli_test.py process --pdf sample_document.pdf
python cli_test.py query --pdf sample_document.pdf --question "What is the agreement about?" --results 2
```

## 3. Run Web App
```bash
streamlit run app.py
```

## 4. Expected Behavior
- `info` prints device/chunk strategy.
- `process` reports extracted/chunked content and sample chunks.
- `query` prints retrieved context block for the question.

## 5. Notes
- First run may take longer due model load.
- GPU warnings can appear in CPU-only environments; pipeline continues on CPU.
