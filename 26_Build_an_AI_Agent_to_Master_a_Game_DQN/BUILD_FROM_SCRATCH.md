# Build From Scratch - Project 26

## 1. Prerequisites
- CMake 3.10+
- C++ compiler (`g++` or `clang++`)
- LibTorch installation (or Python torch with CMake prefix path)

## 2. Validate Structure
```bash
cd 26_Build_an_AI_Agent_to_Master_a_Game_DQN
./scripts/validate.sh
```

## 3. Build via Script
```bash
./scripts/setup.sh
```

## 4. Manual Build (Alternative)
```bash
mkdir -p build
cd build
cmake -DCMAKE_PREFIX_PATH="/path/to/libtorch" ..
cmake --build .
cd ..
```

## 5. Run
```bash
./build/dqn
```

Expected:
- Episode progress logs every 20 episodes
- `dqn_model.pt` saved at the end

## 6. Known Environment Blocker (Current Session)
- Build currently fails when no C++ compiler is installed:
  - `No CMAKE_CXX_COMPILER could be found`
