# Engineering Decisions Log

This document records the key decisions made during the development of the AI Research Agent project.

---

### Decision 1: Choice of Information Retrieval Strategy (Semantic Search)

*   **Problem:** After scraping the text from multiple web pages, how do we find the specific passages that are most relevant to the user's query?
*   **Options Considered:**
    1.  **Keyword Matching:** We could simply search the text for the exact words used in the query. This is fast and simple but very brittle. It would miss synonyms or conceptually related ideas (e.g., a search for "cars" would not match a passage about "automobiles").
    2.  **TF-IDF:** A more advanced keyword-based method that scores terms based on their frequency. It's better than simple keyword matching but still doesn't understand the *meaning* of the words.
    3.  **Semantic Search (Embeddings):** We can use a deep learning model to convert both the query and the text chunks into numerical vectors (embeddings). We can then use cosine similarity to find the chunks that are semantically closest to the query, even if they don't use the same keywords.
*   **Final Choice:** **Semantic Search using Sentence Transformers**.
*   **Trade-offs:**
    *   **Pros:** Provides much more relevant and conceptually accurate results than keyword-based methods. It's robust to variations in language and phrasing.
    *   **Cons:** Requires loading a machine learning model (`all-MiniLM-L6-v2`), which uses more memory and compute than simpler methods. The process of embedding all the text chunks can be slow for very large documents.

---

### Decision 2: Choice of Web Scraping Library (`requests` + `BeautifulSoup`)

*   **Problem:** We need to fetch the content of web pages from a list of URLs.
*   **Options Considered:**
    1.  **`requests` + `BeautifulSoup`:** A classic, lightweight combination. `requests` is a simple library for making HTTP requests, and `BeautifulSoup` is excellent for parsing and navigating the resulting HTML.
    2.  **Scrapy:** A much larger, more powerful framework for building web crawlers and scrapers. It includes features for handling rate limiting, proxies, and data pipelines. It would be overkill for our simple agent.
    3.  **Selenium / Playwright:** These are "headless browser" tools that can control a real web browser programmatically. They are essential for scraping modern websites that rely on JavaScript to render content.
*   **Final Choice:** **`requests` + `BeautifulSoup`**.
*   **Trade-offs:**
    *   **Pros:** Very easy to set up and use. They are lightweight libraries with minimal dependencies. For simple, static HTML websites (like our mocked Wikipedia example), they work perfectly.
    *   **Cons:** This approach will completely fail on websites that require JavaScript to load their main content. The scraper is not very robust.

---

### Decision 3: Summarization Strategy — v0.1 Placeholder → v0.2 Mistral LLM

*   **Problem:** Once we have the top-ranked passages, how do we synthesize them into a final answer?
*   **v0.1 Choice (Placeholder):** For the initial release, we simply joined the top passages together and presented them. This was intentionally simple to focus on building the retrieval pipeline.
*   **v0.2 Choice (Abstractive Summarization with Local Mistral LLM):**
    *   **What changed:** We replaced the placeholder with true abstractive summarization using a local Mistral 7B Instruct model loaded via `ctransformers`.
    *   **How it works:**
        1. Top-ranked passages are truncated to a configurable character limit (default 500 chars each)
        2. The passages are assembled into a Mistral instruct-format prompt: `[INST]...[/INST]`
        3. The prompt is tokenized and truncated to fit within the model's context window
        4. The Mistral model generates a coherent, abstractive summary
    *   **Why Mistral 7B Instruct Q4_K_M:**
        - Free, no API key or cloud service required
        - 4-bit quantization keeps the model at 4.1 GB (manageable on consumer hardware)
        - Instruct format produces structured, well-organized outputs
        - Runs entirely on CPU (no GPU required)
    *   **Why ctransformers over llama-cpp-python:**
        - ctransformers ships pre-built Python wheels (no C++ compiler needed)
        - Uses the same underlying llama.cpp engine
        - Simpler installation in environments without build tools
    *   **Graceful fallback:** If the GGUF model file is not found, the agent falls back to a concatenation-based summary instead of crashing.

---

### Decision 4: Context Window Management

*   **Problem:** The Mistral 7B model has a limited context window. Three passages of 500 characters each, combined with the prompt template, can exceed the model's token limit.
*   **Options Considered:**
    1.  **No truncation:** Pass the full passages and let the model handle it. Risk: the model ignores tokens past its context window, producing degraded or empty output.
    2.  **Character-based truncation only:** Truncate each passage to a fixed character count. Simple but imprecise — characters don't map 1:1 to tokens.
    3.  **Token-level truncation:** Tokenize the full prompt after assembly and truncate to fit within `(context_window - max_new_tokens)`. Most accurate.
*   **Final Choice:** **Token-level truncation** as a safety net, with character-based truncation as the primary method.
*   **Trade-offs:**
    *   **Pros:** Guarantees the prompt fits within the model's context window. Prevents the "tokens exceeded" warnings seen in early testing.
    *   **Cons:** Tokenization adds a small overhead. Character-based truncation may cut passages mid-sentence.

---

### Decision 5: Default Configuration Values

*   **Problem:** What should the default values be for the pipeline parameters?
*   **Choices Made:**
    | Parameter | Default | Rationale |
    |-----------|---------|-----------|
    | CHUNK_SIZE | 1000 chars | Large enough to contain meaningful context, small enough for efficient embedding |
    | CHUNK_OVERLAP | 200 chars | 20% overlap prevents information loss at chunk boundaries |
    | TOP_K | 3 passages | Balances context richness against LLM context window limits |
    | LLM_MAX_TOKENS | 256 tokens | Enough for a concise summary, keeps inference time reasonable on CPU |
    | LLM_TEMPERATURE | 0.3 | Low temperature for factual, deterministic summaries |
    | LLM_CONTEXT_WINDOW | 2048 tokens | Conservative default for CPU inference; configurable for larger models |
    | MAX_PASSAGE_CHARS | 500 chars | 3 passages × 500 chars ≈ 375 tokens, leaving room for prompt + output |
*   **All parameters are configurable via environment variables** for advanced users.

---

*Owner: Ansh | Last updated: 2026-03-25 | Do not modify without owner approval.*
