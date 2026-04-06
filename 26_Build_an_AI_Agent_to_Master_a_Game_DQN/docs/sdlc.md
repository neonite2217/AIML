# SDLC — DQN Game Agent

## 1. Requirements

### Functional Requirements
- [x] Implement 1D grid world game environment
- [x] Create DQN agent with neural network
- [x] Implement epsilon-greedy exploration
- [x] Build experience replay buffer
- [x] Create training loop with 500 episodes
- [x] Save trained model to file
- [x] Display training progress (episode, reward, epsilon)

### Non-Functional Requirements
- [x] Training completes in reasonable time (< 5 minutes on CPU)
- [x] Code compiles with C++17 toolchain
- [x] Agent shows learning progress (increasing rewards)
- [x] Model file is successfully saved and loadable

### Target Audience
- C++ developers learning Reinforcement Learning
- Students studying DQN algorithms
- Engineers exploring high-performance RL implementations

## 2. Design

### Architecture
- [x] Architecture diagram created (docs/architecture.md)
- [x] Component interactions documented
- [x] Data flow defined

### Tech Stack
- [x] Language: C++17
- [x] Deep Learning: LibTorch
- [x] Build System: CMake 3.10+

### API Contracts
- Game Environment API:
  - `reset() -> vector<float>`: Reset to initial state
  - `step(action) -> tuple<state, reward, done>`: Execute action
- DQN Agent API:
  - `forward(state) -> Q-values`: Predict action values
  - `select_action(state, epsilon) -> action`: Choose action

### State Space
- Single float: position on 1D grid (-5 to +5)
- Actions: 0 (left), 1 (right)
- Rewards: +1 (goal), -1 (fall), -0.1 (step penalty)

## 3. Development

### Coding Standards
- [x] C++17 standard compliance
- [x] Consistent naming conventions
- [x] Comments explaining "why" not "what"
- [x] No magic numbers (use named constants)

### Version Control
- [x] Git repository initialized
- [x] .gitignore configured
- [x] Feature branches used (if applicable)

### Code Review
- [x] Self-review completed
- [x] Documentation reviewed

## 4. Testing

### Unit Tests
- [ ] Test Game environment reset
- [ ] Test Game step function
- [ ] Test QNetwork forward pass
- [ ] Test ReplayBuffer push and sample

### Integration Tests
- [x] Full training loop executes
- [x] Model saves successfully
- [x] Console output is correct

### Smoke Test
```bash
# Build and run
./scripts/setup.sh
./build/dqn

# Expected output:
# Training on CPU.
# Episode 0, Total Reward: X, Epsilon: 1.0
# ...
# Episode 480, Total Reward: Y, Epsilon: Z
# Training finished and model saved.
```

### Performance Tests
- [x] Training completes in < 5 minutes
- [x] Memory usage remains stable
- [x] No memory leaks detected

## 5. Deployment

### Environment Variables
- `CMAKE_PREFIX_PATH`: Path to LibTorch installation

### Deployment Guide
1. Install dependencies (CMake, C++ compiler)
2. Download LibTorch
3. Set CMAKE_PREFIX_PATH
4. Run `scripts/setup.sh`
5. Execute `./build/dqn`

### Rollback Plan
- Keep previous model checkpoints
- Document working LibTorch versions
- Maintain build instructions

### CI/CD
- [ ] GitHub Actions workflow for automated builds
- [ ] Automated testing on push
- [ ] Release tagging

## 6. Maintenance

### Changelog
- [x] CHANGELOG.md created
- [x] Version 1.0.0 documented

### Known Issues
- No active build blocker in the validated environment (2026-03-25 run succeeded).

### Agent Log
- [x] Initial session logged
- [x] Build process documented

### Future Enhancements
- Target network for stability
- Visualization of gameplay
- TensorBoard integration
- More complex environments

## Current Status

**Phase:** Development Complete  
**Version:** 1.0.0  
**Status:** Build and runtime verification passed in environment using local `libtorch` and C++17  
**Next Milestone:** v0.2 (Target Network)
