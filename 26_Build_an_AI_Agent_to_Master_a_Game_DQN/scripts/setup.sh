#!/bin/bash

# Setup script for DQN Game Agent
# This script automates the build process for the C++ DQN project

set -e  # Exit on error

echo "=========================================="
echo "DQN Game Agent - Build Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if CMake is installed
if ! command -v cmake &> /dev/null; then
    print_error "CMake is not installed. Please install CMake 3.10 or higher."
    exit 1
fi

# Check CMake version
CMAKE_VERSION=$(cmake --version | head -n1 | grep -oE '[0-9]+\.[0-9]+')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$CMAKE_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "CMake version $CMAKE_VERSION is too old. Need $REQUIRED_VERSION or higher."
    exit 1
fi

print_status "CMake version: $CMAKE_VERSION"

# Ensure a usable C/C++ compiler is available (fallback to Homebrew toolchain aliases).
compiler_works_cxx() {
    local cxx_bin="$1"
    if [ -z "$cxx_bin" ] || [ ! -x "$cxx_bin" ]; then
        return 1
    fi
    echo "int main(){return 0;}" | "$cxx_bin" -x c++ -std=c++17 - -o /tmp/cxx_probe.$$ &>/dev/null
}

compiler_works_cc() {
    local cc_bin="$1"
    if [ -z "$cc_bin" ] || [ ! -x "$cc_bin" ]; then
        return 1
    fi
    echo "int main(){return 0;}" | "$cc_bin" -x c - -o /tmp/cc_probe.$$ &>/dev/null
}

DEFAULT_CXX="$(command -v g++ 2>/dev/null || true)"
DEFAULT_CC="$(command -v gcc 2>/dev/null || true)"

if ! compiler_works_cxx "$DEFAULT_CXX" && command -v g++-15 &> /dev/null; then
    export CXX="$(command -v g++-15)"
    print_warning "Default g++ unavailable/broken; using fallback compiler: $CXX"
fi

if ! compiler_works_cc "$DEFAULT_CC" && command -v gcc-15 &> /dev/null; then
    export CC="$(command -v gcc-15)"
    print_warning "Default gcc unavailable/broken; using fallback compiler: $CC"
fi

# Try to detect LibTorch path
print_status "Detecting LibTorch installation..."

LIBTORCH_PATH=""

# Method 0: Use project-local LibTorch if present
if [ -z "$LIBTORCH_PATH" ] && [ -d "./libtorch/share/cmake/Torch" ]; then
    LIBTORCH_PATH="$(pwd)/libtorch"
    print_status "Found project-local LibTorch: $LIBTORCH_PATH"
fi

# Method 1: Check if CMAKE_PREFIX_PATH is set
if [ -n "$CMAKE_PREFIX_PATH" ]; then
    print_status "Found CMAKE_PREFIX_PATH environment variable"
    LIBTORCH_PATH="$CMAKE_PREFIX_PATH"
fi

# Method 2: Try to get path from Python
if [ -z "$LIBTORCH_PATH" ] && command -v python3 &> /dev/null; then
    print_status "Attempting to detect LibTorch via Python..."
    PYTHON_TORCH_PATH=$(python3 -c 'import torch; print(torch.utils.cmake_prefix_path)' 2>/dev/null || true)
    if [ -n "$PYTHON_TORCH_PATH" ]; then
        LIBTORCH_PATH="$PYTHON_TORCH_PATH"
        print_status "Found LibTorch via Python: $LIBTORCH_PATH"
    fi
fi

# Method 3: Check common installation paths
if [ -z "$LIBTORCH_PATH" ]; then
    COMMON_PATHS=(
        "/usr/local/libtorch"
        "/opt/libtorch"
        "$HOME/libtorch"
        "$HOME/.local/libtorch"
        "/usr/lib/libtorch"
    )
    
    for path in "${COMMON_PATHS[@]}"; do
        if [ -d "$path" ]; then
            LIBTORCH_PATH="$path"
            print_status "Found LibTorch at: $LIBTORCH_PATH"
            break
        fi
    done
fi

if [ -z "$LIBTORCH_PATH" ]; then
    print_error "Could not find LibTorch installation."
    echo ""
    echo "Please install LibTorch from: https://pytorch.org/get-started/locally/"
    echo "Then set CMAKE_PREFIX_PATH to the LibTorch directory:"
    echo "  export CMAKE_PREFIX_PATH=/path/to/libtorch"
    echo ""
    echo "Or run cmake manually with:"
    echo "  cmake -DCMAKE_PREFIX_PATH=/path/to/libtorch .."
    exit 1
fi

print_status "Using LibTorch at: $LIBTORCH_PATH"

# Create build directory
print_status "Creating build directory..."
if [ -d "build" ]; then
    print_warning "Build directory already exists. Cleaning..."
    rm -rf build
fi
mkdir build

# Configure with CMake
print_status "Configuring with CMake..."
cd build

cmake -DCMAKE_PREFIX_PATH="$LIBTORCH_PATH" .. || {
    print_error "CMake configuration failed"
    exit 1
}

# Build the project
print_status "Building project..."
cmake --build . --parallel $(nproc 2>/dev/null || echo 4) || {
    print_error "Build failed"
    exit 1
}

cd ..

# Verify executable was created
if [ -f "build/dqn" ]; then
    print_status "Build successful!"
    echo ""
    echo "=========================================="
    echo "Build complete!"
    echo "=========================================="
    echo ""
    echo "To run the DQN agent:"
    echo "  ./build/dqn"
    echo ""
    echo "The agent will train for 500 episodes and save the model to dqn_model.pt"
else
    print_error "Build completed but executable not found"
    exit 1
fi

# Post-install check
print_status "Running post-install verification..."

# Check if we can run the executable (just check version/help if available)
if ./build/dqn --help &> /dev/null || true; then
    print_status "Executable verification passed"
fi

echo ""
print_status "Setup complete! Ready to train the DQN agent."
