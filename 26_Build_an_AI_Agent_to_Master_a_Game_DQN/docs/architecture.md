# Architecture — DQN Game Agent

## System Overview

This project implements a Deep Q-Network (DQN) agent that learns to play a simple 1D grid world game through reinforcement learning. The agent uses a neural network to approximate the Q-function, which estimates the expected future reward for each action in a given state.

## Component Diagram

```
+-----------------------+        +-----------------------+
|                       |        |                       |
|   Game Environment    |<------>|     DQN Agent         |
|   (game.h)            | Action |   (dqn.cpp)           |
|                       |        |                       |
|  - State: position    |        |  - QNetwork           |
|  - Actions: L/R       |        |  - ReplayBuffer       |
|  - Rewards: +1/-1     |        |  - select_action()    |
|                       |        |                       |
+-----------+-----------+        +-----------+-----------+
            |                                |
            | State, Reward, Done            | Experience
            v                                v
+---------------------------------------------+
|                                             |
|           Training Loop (main)              |
|                                             |
|  1. Select action (epsilon-greedy)        |
|  2. Execute action in environment           |
|  3. Store experience in replay buffer       |
|  4. Sample batch and train network          |
|  5. Update epsilon (decay)                    |
|                                             |
+---------------------------------------------+
```

## Data Flow

1. **Initialization**: Game environment resets to starting state (position 0)
2. **Action Selection**: Agent uses epsilon-greedy policy to choose action (explore vs exploit)
3. **Environment Step**: Game executes action, returns new state, reward, and done flag
4. **Experience Storage**: Tuple (s, a, r, s', done) is stored in replay buffer
5. **Training**: When buffer has enough samples, a batch is used to update the Q-network
6. **Loss Calculation**: MSE loss between predicted Q-values and target Q-values (Bellman equation)
7. **Optimization**: Adam optimizer updates network weights
8. **Iteration**: Process repeats for 500 episodes, with epsilon decaying over time

## Key Design Decisions

### 1. Epsilon-Greedy Exploration
- **Decision**: Use epsilon-greedy with decay (1.0 → 0.01)
- **Rationale**: Balances exploration (trying new actions) with exploitation (using learned policy)
- **Trade-off**: Simple but may be inefficient in large state spaces

### 2. Experience Replay Buffer
- **Decision**: Fixed-size buffer (10,000 experiences) with random sampling
- **Rationale**: Breaks correlations in training data, improves stability
- **Trade-off**: Requires memory but significantly improves learning

### 3. Neural Network Architecture
- **Decision**: 3-layer MLP (1 → 128 → 128 → 2)
- **Rationale**: Sufficient for simple 1D state space, ReLU activations for non-linearity
- **Trade-off**: Simple but may need expansion for complex environments

### 4. C++ with LibTorch
- **Decision**: Implement in C++ using PyTorch C++ frontend
- **Rationale**: High performance for RL training loops, fine-grained control
- **Trade-off**: Steeper learning curve than Python but better performance

## External Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| LibTorch | Deep learning framework | Latest stable |
| CMake | Build system | 3.10+ |
| C++ Standard | Language features | C++17 |

## File Structure

```
project-root/
├── CMakeLists.txt          # Build configuration
├── dqn.cpp                 # Main DQN implementation
├── game.h                  # Game environment
├── guide.txt               # Project handbook
├── RULES.md                # Agent operating rules
├── ENGINEERING_DECISIONS.md # Decision log
├── docs/
│   ├── agent_log.md        # Session logs
│   ├── CHANGELOG.md        # Version history
│   ├── tasks.md            # Task tracking
│   ├── architecture.md     # This file
│   ├── tech_stack.md       # Technology choices
│   └── sdlc.md             # Development lifecycle
├── scripts/
│   └── setup.sh            # Build automation
└── backups/                # File backups (git-ignored)
```
