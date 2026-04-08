# Setup Script for Real-Time AI Assistant
# Platform: Windows PowerShell
# Description: Automated setup for RAG-based AI assistant

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Real-Time AI Assistant - Setup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python installation
Write-Host "[INFO] Step 1: Checking Python installation..." -ForegroundColor Green
try {
    $pythonVersion = python --version
    Write-Host "[INFO] Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}

# Step 2: Check Ollama installation
Write-Host "[INFO] Step 2: Checking Ollama installation..." -ForegroundColor Green
try {
    $ollamaVersion = ollama --version
    Write-Host "[INFO] Found Ollama: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Ollama not found. Please install Ollama from https://ollama.ai/" -ForegroundColor Red
    exit 1
}

# Step 3: Check if Ollama is running
Write-Host "[INFO] Step 3: Checking if Ollama is running..." -ForegroundColor Green
try {
    ollama list | Out-Null
    Write-Host "[INFO] Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "[WARN] Ollama is not running. Please start Ollama manually." -ForegroundColor Yellow
    Write-Host "  Run: ollama serve" -ForegroundColor Yellow
}

# Step 4: Check for required model
Write-Host "[INFO] Step 4: Checking for Qwen3.5 model..." -ForegroundColor Green
$ollamaList = ollama list
if ($ollamaList -match "qwen3.5") {
    Write-Host "[INFO] Qwen3.5 model found" -ForegroundColor Green
} else {
    Write-Host "[WARN] Qwen3.5 model not found. Downloading..." -ForegroundColor Yellow
    ollama pull qwen3.5
    Write-Host "[INFO] Qwen3.5 model downloaded successfully" -ForegroundColor Green
}

# Step 5: Create virtual environment
Write-Host "[INFO] Step 5: Setting up virtual environment..." -ForegroundColor Green
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "[INFO] Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "[INFO] Virtual environment already exists" -ForegroundColor Green
}

# Step 6: Activate virtual environment
Write-Host "[INFO] Step 6: Activating virtual environment..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

# Step 7: Install dependencies
Write-Host "[INFO] Step 7: Installing Python dependencies..." -ForegroundColor Green
python -m pip install --upgrade pip
pip install -r requirements.txt

# Step 8: Verify installation
Write-Host "[INFO] Step 8: Verifying installation..." -ForegroundColor Green
python -c "from langchain_ollama import ChatOllama; print('✓ LangChain Ollama integration OK')"
python -c "from langchain_community.tools import DuckDuckGoSearchRun; print('✓ DuckDuckGo search OK')"

# Step 9: Run smoke test
Write-Host "[INFO] Step 9: Running smoke test..." -ForegroundColor Green
python real_time_assistant.py

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the assistant manually:" -ForegroundColor White
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python real_time_assistant.py" -ForegroundColor White
Write-Host ""
Write-Host "For interactive mode, edit real_time_assistant.py and uncomment line 119" -ForegroundColor White
Write-Host ""
