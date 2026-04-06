# DQN Game Agent

> A Deep Q-Network (DQN) agent implemented in C++ using LibTorch that learns to play a 1D grid world game through reinforcement learning.

## Tech Stack

- **Language:** C++17
- **Deep Learning:** LibTorch (PyTorch C++ Frontend)
- **Build System:** CMake 3.10+
- **Math:** C++ Standard Library

## Prerequisites

- C++17 compatible compiler (GCC, Clang, MSVC)
- CMake 3.10 or higher
- LibTorch (PyTorch C++ distribution)
- Python 3.x (optional, for CMAKE_PREFIX_PATH detection)

## Installation

### 1. Install Build Tools

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install cmake build-essential
```

**macOS:**
```bash
brew install cmake
```

**Windows:**
Download and install CMake from https://cmake.org/download/

### 2. Download LibTorch

Visit https://pytorch.org/get-started/locally/ and download the LibTorch C++ library for your platform.

Extract it to a known location, e.g., `/path/to/libtorch`.

Note: this project already includes a `libtorch/` folder, and `scripts/setup.sh` now auto-detects it.

### 3. Build the Project

Using the automated setup script:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Or manually:
```bash
mkdir build
cd build

# Configure with LibTorch path
cmake -DCMAKE_PREFIX_PATH="/path/to/libtorch" ..

# Build
cmake --build .

# Return to project root
cd ..
```

## Usage

Run the trained agent:
```bash
./build/dqn
```

The agent will:
1. Train for 500 episodes
2. Display progress every 20 episodes
3. Save the trained model to `dqn_model.pt`

### Expected Output
```
Training on CPU.
Episode 0, Total Reward: -2.1, Epsilon: 1.0
Episode 20, Total Reward: -0.5, Epsilon: 0.9
Episode 40, Total Reward: 0.3, Epsilon: 0.81
...
Episode 480, Total Reward: 0.9, Epsilon: 0.01
Training finished and model saved.
```

## Project Structure

```
Build_an_AI_Agent_to_Master_a_Game_DQN/
├── CMakeLists.txt              # Build configuration
├── dqn.cpp                     # DQN agent implementation
├── game.h                      # Game environment
├── guide.txt                   # Detailed project guide
├── RULES.md                    # Development rules
├── ENGINEERING_DECISIONS.md    # Design decisions
├── README.md                   # This file
├── docs/
│   ├── agent_log.md            # Development session logs
│   ├── CHANGELOG.md            # Version history
│   ├── tasks.md                # Task tracking
│   ├── architecture.md         # System architecture
│   ├── tech_stack.md           # Technology choices
│   └── sdlc.md                 # Development lifecycle
├── scripts/
│   └── setup.sh                # Automated build script
└── backups/                    # File backups (git-ignored)
```

## Architecture Overview

The DQN agent consists of four main components:

1. **Game Environment** (`game.h`): A 1D grid world where the agent moves left/right to reach a goal
2. **Q-Network** (`dqn.cpp`): A neural network that estimates Q-values for each action
3. **Replay Buffer** (`dqn.cpp`): Stores experiences for stable training
4. **Training Loop** (`dqn.cpp`): Orchestrates learning through interaction

See `docs/architecture.md` for detailed diagrams and data flow.

## Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `CMAKE_PREFIX_PATH` | No | Path to LibTorch installation (auto-detected if omitted) | project-local `./libtorch` |

## Running Tests

### Smoke Test
```bash
# Build and run
./scripts/setup.sh
./build/dqn

# Verify:
# - Training completes without errors
# - Rewards increase over time
# - Model file dqn_model.pt is created
```

### Manual Test Cases

| Test | Procedure | Expected Result |
|------|-----------|-----------------|
| Learning Progress | Run training | Total Reward increases from ~-2 to ~+1 |
| Model Save | Check after training | `dqn_model.pt` exists and is > 0 bytes |
| Epsilon Decay | Observe output | Epsilon decreases from 1.0 to 0.01 |

## SDLC Status

**Current Phase:** Development Complete  
**Version:** 1.0.0  
**Status:** Ready for use

See `docs/sdlc.md` for full lifecycle documentation.

## Contributing

1. Follow the coding standards in `RULES.md`
2. Update `docs/CHANGELOG.md` with changes
3. Log sessions in `docs/agent_log.md`
4. Ensure smoke test passes before submitting

## License

This project is for educational purposes.

## Resources

- [PyTorch C++ Documentation](https://pytorch.org/cppdocs/)
- [DQN Paper (Mnih et al., 2015)](https://www.nature.com/articles/nature14236)
- [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/RLbook2020.pdf)
