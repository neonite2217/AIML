# Engineering Decisions Log

This document records the key decisions made during the development of the Real-Time AI Assistant project.

---

### Decision 1: Choice of Architecture (RAG)

*   **Problem:** We need our AI assistant to answer questions about recent events, but standard LLMs have a knowledge cutoff.
*   **Options Considered:**
    1.  **Fine-tuning:** We could constantly fine-tune an LLM on a stream of new articles. This is extremely expensive, slow, and would require a massive engineering effort.
    2.  **Standard "Agent" with Search:** We could give an LLM a search tool and just ask it to "answer the question." This can work, but it gives the LLM a lot of autonomy and can be less reliable. The LLM might ignore the search results or use them incorrectly.
    3.  **Retrieval-Augmented Generation (RAG):** This is a specific, structured pipeline where we first retrieve information and then explicitly pass it to the LLM as context to inform its answer.
*   **Final Choice:** **Retrieval-Augmented Generation (RAG)**.
*   **Trade-offs:**
    *   **Pros:** RAG is a much more reliable and controllable pattern than giving an agent free-form access to a tool. It's cost-effective and ensures the LLM's answer is grounded in the retrieved context, reducing the likelihood of hallucinations.
    *   **Cons:** A simple RAG pipeline is less flexible than a true agent. It can only follow the "retrieve then answer" pattern and can't, for example, decide to use a different tool or ask a clarifying question.

---

### Decision 2: Choice of Pipeline Framework (LangChain Expression Language)

*   **Problem:** We need to connect our components (retriever, prompt, LLM) into a pipeline. How should we write the code for this?
*   **Options Considered:**
    1.  **Manual Python Code:** We could write a simple Python function that calls the retriever, then formats the prompt string manually, and finally calls the LLM. This is simple for a linear chain but becomes very messy if we want to add more complex logic, like parallel steps or conditional branches.
    2.  **Legacy LangChain `LLMChain`:** Older versions of LangChain used a more object-oriented, class-based approach. This has been largely superseded.
    3.  **LangChain Expression Language (LCEL):** A declarative, functional approach where components are "piped" together using the `|` operator. It's designed to be composable, streamable, and easy to modify.
*   **Final Choice:** **LangChain Expression Language (LCEL)**.
*   **Trade-offs:**
    *   **Pros:** LCEL makes it incredibly easy to build and visualize complex data flows. It provides benefits like streaming and parallel execution "for free." It's the modern, idiomatic way to build with LangChain.
    *   **Cons:** The "pipe" syntax can be a little unusual for developers who are not familiar with functional programming concepts. It can feel like "magic" at first.

---

### Decision 3: Choice of Retriever (DuckDuckGo Search)

*   **Problem:** We need a source of real-time information for the "Retrieval" step.
*   **Options Considered:**
    1.  **Vector Database:** We could populate a vector database (like FAISS or Chroma) with our own private documents. This is the right choice for building a Q&A bot for a specific knowledge base (e.g., your company's internal wiki). For our goal of answering questions about *public, recent events*, this is not suitable.
    2.  **Google/Bing Search APIs:** These are powerful, high-quality search APIs. However, they often require signing up for a developer account and getting an API key, which adds friction for a beginner project.
    3.  **LangChain's `DuckDuckGoSearchRun` Tool:** A simple, free-to-use tool that requires no API key. It's a convenient wrapper around the DuckDuckGo search engine.
*   **Final Choice:** **DuckDuckGoSearchRun**.
*   **Trade-offs:**
    *   **Pros:** Extremely easy to set up and use (no API key needed). It's free and provides good enough results for a demonstration project.
    *   **Cons:** The quality and depth of the search results may not be as high as a paid, commercial search API like Google's. It's not suitable for high-volume production use.
