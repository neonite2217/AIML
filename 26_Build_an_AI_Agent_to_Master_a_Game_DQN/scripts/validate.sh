#!/bin/bash

# Validation script for DQN Game Agent
# This script validates the project structure without requiring compilation

set -e

echo "=========================================="
echo "DQN Game Agent - Project Validation"
echo "=========================================="
echo ""

ERRORS=0
WARNINGS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✓ Found: $1"
        return 0
    else
        echo "✗ Missing: $1"
        ((ERRORS++))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✓ Found directory: $1"
        return 0
    else
        echo "✗ Missing directory: $1"
        ((ERRORS++))
        return 1
    fi
}

echo "Checking project structure..."
echo ""

# Check root files
echo "Root files:"
check_file "CMakeLists.txt"
check_file "dqn.cpp"
check_file "game.h"
check_file "README.md"
check_file ".gitignore"
check_file "guide.txt"
check_file "RULES.md"
check_file "ENGINEERING_DECISIONS.md"

echo ""
echo "Documentation:"
check_dir "docs"
check_file "docs/agent_log.md"
check_file "docs/CHANGELOG.md"
check_file "docs/tasks.md"
check_file "docs/architecture.md"
check_file "docs/tech_stack.md"
check_file "docs/sdlc.md"

echo ""
echo "Scripts:"
check_dir "scripts"
check_file "scripts/setup.sh"

echo ""
echo "Checking C++ code syntax..."

# Check for basic C++ syntax patterns in dqn.cpp
if grep -q "#include <torch/torch.h>" dqn.cpp; then
    echo "✓ dqn.cpp: LibTorch include found"
else
    echo "✗ dqn.cpp: Missing LibTorch include"
    ((ERRORS++))
fi

if grep -q "struct QNetwork" dqn.cpp; then
    echo "✓ dqn.cpp: QNetwork struct found"
else
    echo "✗ dqn.cpp: QNetwork struct not found"
    ((ERRORS++))
fi

if grep -q "int main()" dqn.cpp; then
    echo "✓ dqn.cpp: main function found"
else
    echo "✗ dqn.cpp: main function not found"
    ((ERRORS++))
fi

# Check game.h
if grep -q "class Game" game.h; then
    echo "✓ game.h: Game class found"
else
    echo "✗ game.h: Game class not found"
    ((ERRORS++))
fi

if grep -q "std::tuple" game.h; then
    echo "✓ game.h: step() return type uses tuple"
else
    echo "✗ game.h: step() return type issue"
    ((ERRORS++))
fi

# Check CMakeLists.txt
if grep -q "find_package(Torch REQUIRED)" CMakeLists.txt; then
    echo "✓ CMakeLists.txt: LibTorch package configured"
else
    echo "✗ CMakeLists.txt: LibTorch not configured"
    ((ERRORS++))
fi

if grep -q "add_executable(dqn" CMakeLists.txt; then
    echo "✓ CMakeLists.txt: Executable target defined"
else
    echo "✗ CMakeLists.txt: Executable target not defined"
    ((ERRORS++))
fi

echo ""
echo "Checking documentation completeness..."

# Check README sections
if grep -q "## Tech Stack" README.md; then
    echo "✓ README.md: Tech Stack section present"
else
    echo "✗ README.md: Missing Tech Stack section"
    ((ERRORS++))
fi

if grep -q "## Installation" README.md; then
    echo "✓ README.md: Installation section present"
else
    echo "✗ README.md: Missing Installation section"
    ((ERRORS++))
fi

if grep -q "## Usage" README.md; then
    echo "✓ README.md: Usage section present"
else
    echo "✗ README.md: Missing Usage section"
    ((ERRORS++))
fi

echo ""
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo "✓ All checks passed!"
    echo "=========================================="
    echo ""
    echo "Project structure is complete and ready for build."
    echo ""
    echo "To build the project:"
    echo "  1. Install a C++ compiler (g++ or clang++)"
    echo "  2. Install CMake 3.10+"
    echo "  3. Install LibTorch (PyTorch C++ distribution)"
    echo "  4. Run: ./scripts/setup.sh"
    echo ""
    exit 0
else
    echo "✗ Validation failed with $ERRORS error(s)"
    echo "=========================================="
    exit 1
fi
