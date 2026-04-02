# Engineering Decisions Log

This document records the key decisions made during the development of the Multi-Agent System project.

---

### Decision 1: Choice of Framework (LangGraph)

*   **Problem:** We need a way to orchestrate multiple AI agents in a structured workflow. How do we manage the state and the flow of control between them?
*   **Options Considered:**
    1.  **Custom Python Script:** Write a manual `while` loop or a series of `if/else` statements to control which agent runs next. We would have to manage the state in a simple dictionary ourselves. This is very flexible but can quickly become "spaghetti code" and is hard to debug or visualize.
    2.  **Standard LangChain Agents:** Use a pre-built agent type from LangChain, like ReAct. These are powerful for single-agent workflows with tools but are not explicitly designed for multi-agent collaboration.
    3.  **LangGraph:** A library specifically built to create agentic systems as graphs. It provides a formal structure for defining states, nodes (agents), and edges (transitions), making the workflow explicit and debuggable.
*   **Final Choice:** **LangGraph**.
*   **Trade-offs:**
    *   **Pros:** Enforces a clean, state-machine-based architecture. Makes the flow of control explicit and easy to visualize. Handles state management automatically. It's designed for loops and cycles, which are common in agentic workflows.
    *   **Cons:** Introduces a new layer of abstraction to learn. For a very simple linear workflow, it might be slight overkill compared to a basic script.

---

### Decision 2: State Management (TypedDict)

*   **Problem:** How should we define the data structure that is shared between all the agents in our graph?
*   **Options Considered:**
    1.  **Standard Python `dict`:** A regular dictionary is easy to use and completely flexible. However, there are no checks to ensure the keys are spelled correctly or that the data types are right. This often leads to runtime `KeyError` exceptions.
    2.  **Pydantic `BaseModel`:** Pydantic models provide robust, runtime data validation. This is a very strong choice for production systems but adds a heavier dependency for a simple project.
    3.  **`typing.TypedDict`:** A built-in Python feature that provides static type checking for dictionary schemas. It allows type checkers like MyPy to catch errors before the code is even run, but it doesn't perform runtime validation.
*   **Final Choice:** **`typing.TypedDict`**.
*   **Trade-offs:**
    *   **Pros:** Provides excellent developer experience with static analysis and autocompletion. It's lightweight as it's part of the standard library. It clearly documents the expected shape of the state object.
    *   **Cons:** It does not prevent runtime errors if a node returns a dictionary with the wrong shape. A Pydantic model would be safer but more complex to set up.

---

### Decision 3: Choice of LLM (Local with Ollama)

*   **Problem:** Our agents need access to a Large Language Model. Should we use a cloud-based API or run one locally?
*   **Options Considered:**
    1.  **Cloud API (e.g., OpenAI, Anthropic):** These services provide access to powerful, state-of-the-art models. They are easy to use but require an internet connection, an API key, and can incur costs.
    2.  **Local LLM with Ollama:** Ollama makes it incredibly easy to download and run powerful open-source models (like Llama, Mistral, etc.) directly on a developer's machine. This is free, private, and works offline.
*   **Final Choice:** **Local LLM with Ollama**.
*   **Trade-offs:**
    *   **Pros:** Free to use, completely private (no data leaves the machine), and works offline. It's perfect for rapid, cost-effective development and experimentation.
    *   **Cons:** Requires a reasonably powerful local machine (especially RAM and a good CPU/GPU). The open-source models available, while excellent, may not match the absolute peak performance of the very largest proprietary models.
