#!/bin/bash
# Complete build script for Synthetic Medical Records GAN project

echo "=== Building Synthetic Medical Records using GANs ==="
echo "Date: $(date)"
echo

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    if [ $? -eq 0 ]; then
        echo "✓ Dependencies installed successfully"
        DEPS_AVAILABLE=true
    else
        echo "⚠ Dependency installation failed"
        DEPS_AVAILABLE=false
    fi
else
    echo "⚠ requirements.txt not found"
    DEPS_AVAILABLE=false
fi

# Check for dependencies
echo "Checking dependencies..."
if python3 -c "import torch, sklearn, pandas" 2>/dev/null && [ "$DEPS_AVAILABLE" = true ]; then
    echo "✓ All dependencies available - running full PyTorch version"
    python3 medical_gan.py
else
    echo "⚠ Dependencies missing - running simplified demo version"
    python3 simple_gan_demo.py
fi

echo
echo "Build completed. Check log.txt for detailed information."
echo "Generated synthetic medical records are displayed above."
echo
echo "To run again: ./build.sh"
echo "To clean: rm -rf venv"
