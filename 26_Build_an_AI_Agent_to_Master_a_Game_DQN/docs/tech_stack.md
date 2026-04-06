# Tech Stack — DQN Game Agent

## Core Technologies

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Language | C++ | C++17 | High-performance implementation |
| Deep Learning | LibTorch | Latest | Neural network training |
| Build System | CMake | 3.10+ | Cross-platform compilation |
| Math | Standard Library | C++17 | Random number generation |

## Why This Stack?

### C++ (C++17)
**Pros:**
- Maximum performance for tight training loops
- Fine-grained memory control
- Industry standard for game engines and simulations
- Direct hardware access when needed

**Cons:**
- Steeper learning curve than Python
- Manual memory management
- Longer compilation times

**Decision Rationale:** Reinforcement Learning requires many environment interactions. C++ provides the performance needed for efficient training.

### LibTorch (PyTorch C++ Frontend)
**Pros:**
- Same API as Python PyTorch
- Automatic differentiation
- GPU acceleration support
- Active development and community

**Cons:**
- Large binary size
- Complex setup requirements
- Less documentation than Python version

**Decision Rationale:** LibTorch provides powerful deep learning capabilities while maintaining C++ performance benefits.

### CMake
**Pros:**
- Cross-platform build generation
- Industry standard for C++ projects
- Easy dependency management
- Integration with IDEs

**Cons:**
- Complex syntax
- Steep learning curve

**Decision Rationale:** CMake is the standard for C++ projects and handles LibTorch integration well.

## Dependencies

### Required
- **LibTorch**: PyTorch C++ distribution
  - Download from: https://pytorch.org/get-started/locally/
  - Requires: C++17 compatible compiler

### Build Tools
- **CMake** (>= 3.10)
- **Make** or **Ninja** (build tool)
- **GCC** or **Clang** (C++17 compatible)

### Optional
- **CUDA** (for GPU acceleration)
- **Python** (for CMAKE_PREFIX_PATH detection)

## Installation Commands

```bash
# Ubuntu/Debian
sudo apt-get install cmake build-essential

# macOS
brew install cmake

# LibTorch (download manually from PyTorch website)
# Extract to /path/to/libtorch
```

## Build Commands

```bash
# Create build directory
mkdir build && cd build

# Configure with LibTorch path
cmake -DCMAKE_PREFIX_PATH="/path/to/libtorch" ..

# Build
cmake --build .

# Run
./dqn
```

## Performance Characteristics

- **Training Speed**: ~500 episodes in minutes (CPU)
- **Memory Usage**: ~50MB (model + replay buffer)
- **CPU Usage**: Single-threaded training
- **GPU Support**: Available if CUDA-enabled LibTorch used

## Future Considerations

### Potential Additions
- **SFML/SDL**: For game visualization
- **TensorBoard**: For training metrics logging
- **OpenCV**: For image-based environments
- **MPI**: For distributed training

### Migration Path
If moving to more complex environments:
- Consider Python with PyTorch for rapid prototyping
- Use C++ only for performance-critical components
- Implement Python bindings for hybrid approach
