#!/bin/bash
# Setup Script for Real-Time AI Assistant
# Platform: Linux/macOS
# Description: Automated setup for RAG-based AI assistant

set -e  # Exit on error

echo "=========================================="
echo "Real-Time AI Assistant - Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Check Python installation
print_info "Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_info "Found $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    print_info "Found $PYTHON_VERSION"
else
    print_error "Python not found. Please install Python 3.10 or higher."
    exit 1
fi

# Step 2: Check Ollama installation
print_info "Step 2: Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    OLLAMA_VERSION=$(ollama --version)
    print_info "Found Ollama: $OLLAMA_VERSION"
else
    print_error "Ollama not found. Please install Ollama from https://ollama.ai/"
    exit 1
fi

# Step 3: Check if Ollama is running
print_info "Step 3: Checking if Ollama is running..."
if ollama list &> /dev/null; then
    print_info "Ollama is running"
else
    print_warn "Ollama is not running. Starting Ollama service..."
    ollama serve &
    sleep 3
fi

# Step 4: Check for required model
print_info "Step 4: Checking for Qwen3.5 model..."
if ollama list | grep -q "qwen3.5"; then
    print_info "Qwen3.5 model found"
else
    print_warn "Qwen3.5 model not found. Downloading..."
    ollama pull qwen3.5
    print_info "Qwen3.5 model downloaded successfully"
fi

# Step 5: Create virtual environment (optional but recommended)
print_info "Step 5: Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_info "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Step 6: Activate virtual environment
print_info "Step 6: Activating virtual environment..."
source venv/bin/activate

# Step 7: Install dependencies
print_info "Step 7: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 8: Verify installation
print_info "Step 8: Verifying installation..."
python -c "from langchain_ollama import ChatOllama; print('✓ LangChain Ollama integration OK')"
python -c "from langchain_community.tools import DuckDuckGoSearchRun; print('✓ DuckDuckGo search OK')"

# Step 9: Run smoke test
print_info "Step 9: Running smoke test..."
python real_time_assistant.py

print_info "=========================================="
print_info "Setup Complete!"
print_info "=========================================="
echo ""
print_info "To run the assistant manually:"
echo "  source venv/bin/activate"
echo "  python real_time_assistant.py"
echo ""
print_info "For interactive mode, edit real_time_assistant.py and uncomment line 119"
echo ""
