#!/bin/sh
# Build and run DQN Game Agent in Alpine container

set -e

echo "=========================================="
echo "Building DQN Game Agent"
echo "=========================================="

# Install dependencies and build
cd /workspace

# Download LibTorch if not already present
if [ ! -d "/workspace/libtorch" ]; then
    echo "Downloading LibTorch..."
    curl -L -o libtorch.zip "https://download.pytorch.org/libtorch/cpu/libtorch-shared-with-deps-2.6.0%2Bcpu.zip"
    echo "Extracting LibTorch..."
    unzip -q libtorch.zip
    rm libtorch.zip
fi

echo "Configuring with CMake..."
rm -rf build
mkdir build
cd build

cmake -DCMAKE_PREFIX_PATH="/workspace/libtorch" ..

echo "Building project..."
cmake --build . --parallel $(nproc)

echo ""
echo "=========================================="
echo "Running DQN Agent"
echo "=========================================="
echo ""

# Run the agent
./dqn
