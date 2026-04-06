# Engineering Decisions Log

This document records the key decisions made during the development of the DQN Game Agent project.

---

### Decision 1: Choice of Programming Language (C++)

*   **Problem:** We need to implement a Reinforcement Learning agent and a game environment. What language offers the necessary performance and control?
*   **Options Considered:**
    1.  **Python:** Excellent for rapid prototyping, rich ML ecosystem (PyTorch, TensorFlow). However, it might be too slow for the game environment and the tight training loops required by RL.
    2.  **Java/Kotlin:** Good performance, mature ecosystems. Less commonly used for core RL implementations compared to C++ or Python.
    3.  **C++:** Offers maximum performance, fine-grained memory control, and is often used for high-performance simulations and game engines.
*   **Final Choice:** **C++**.
*   **Trade-offs:**
    *   **Pros:** High performance is crucial for RL, allowing more interactions with the environment and faster training times. Provides a deep understanding of low-level mechanics.
    *   **Cons:** Steeper learning curve, especially with memory management and build systems. Longer compilation times compared to interpreted languages.

---

### Decision 2: Choice of Deep Learning Framework (LibTorch)

*   **Problem:** We need a deep learning framework in C++ to build and train our Q-network.
*   **Options Considered:**
    1.  **Implement Neural Network from Scratch:** This would provide full control but is a massive undertaking for a beginner project, requiring re-implementing backpropagation, optimizers, etc.
    2.  **TensorFlow C++ API:** A powerful option, but can sometimes be more complex to set up and integrate into C++ projects.
    3.  **LibTorch (PyTorch C++ Frontend):** Provides a C++ API for PyTorch. It allows us to leverage PyTorch's powerful tensor operations and automatic differentiation within a C++ environment.
*   **Final Choice:** **LibTorch**.
*   **Trade-offs:**
    *   **Pros:** Excellent performance. Benefits from PyTorch's active development and research. Relatively straightforward integration into C++ projects compared to some alternatives, especially with CMake.
    *   **Cons:** Adds a significant dependency (large download size for the library). Can still have a learning curve if not familiar with PyTorch's computational graph model.

---

### Decision 3: Epsilon-Greedy Exploration Strategy

*   **Problem:** How should our agent choose actions during training to balance finding new, potentially better strategies (exploration) with using what it already knows (exploitation)?
*   **Options Considered:**
    1.  **Pure Exploitation:** Always choose the action with the highest Q-value. The agent would never learn anything new after its initial random actions.
    2.  **Pure Exploration:** Always choose random actions. The agent would never converge on an optimal strategy.
    3.  **Epsilon-Greedy:** With a small probability (`epsilon`), choose a random action (explore). Otherwise, choose the action with the highest Q-value (exploit). `epsilon` is usually decayed over time.
*   **Final Choice:** **Epsilon-Greedy Exploration**.
*   **Trade-offs:**
    *   **Pros:** Simple to implement and a very effective baseline strategy. It guarantees that the agent will continue to explore new actions early in training, leading to a better understanding of the environment. As `epsilon` decays, the agent focuses on optimizing its learned policy.
    *   **Cons:** Can sometimes be inefficient. For very large state spaces, uniform random exploration might miss important parts of the environment. More advanced exploration strategies exist (e.g., UCB, Boltzmann exploration).
