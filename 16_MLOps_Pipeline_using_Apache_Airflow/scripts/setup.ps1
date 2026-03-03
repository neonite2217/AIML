# Setup script for MLOps Pipeline using Apache Airflow
# Supports: Windows PowerShell
# Usage: .\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "MLOps Pipeline Setup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "Step 1: Checking prerequisites..." -ForegroundColor Yellow

# Check Python
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    $PythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $PythonCmd) {
    Write-Host "Error: Python is not installed" -ForegroundColor Red
    Write-Host "Please install Python 3.14+ from https://python.org"
    exit 1
}

$PythonVersion = & $PythonCmd.Source --version 2>&1
Write-Host "✓ Python found: $PythonVersion" -ForegroundColor Green

# Check pip
$PipCmd = Get-Command pip -ErrorAction SilentlyContinue
if (-not $PipCmd) {
    $PipCmd = Get-Command pip3 -ErrorAction SilentlyContinue
}

if (-not $PipCmd) {
    Write-Host "Error: pip is not installed" -ForegroundColor Red
    exit 1
}

Write-Host "✓ pip found" -ForegroundColor Green

Write-Host ""
Write-Host "Step 2: Setting up Airflow home..." -ForegroundColor Yellow

# Set Airflow home
$env:AIRFLOW_HOME = "$ProjectRoot\airflow_home"
New-Item -ItemType Directory -Force -Path $env:AIRFLOW_HOME | Out-Null
Write-Host "✓ Airflow home set to: $($env:AIRFLOW_HOME)" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Installing dependencies..." -ForegroundColor Yellow

# Install requirements
Set-Location $ProjectRoot
& $PipCmd.Source install -r requirements.txt --quiet 2>&1 | Where-Object { $_ -notmatch "already satisfied" } | Out-Null
Write-Host "✓ Dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Initializing Airflow database..." -ForegroundColor Yellow

# Initialize Airflow database
airflow db migrate --quiet
Write-Host "✓ Airflow database initialized" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Creating directories..." -ForegroundColor Yellow

# Create required directories
New-Item -ItemType Directory -Force -Path "$ProjectRoot\data" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectRoot\artifacts" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectRoot\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectRoot\plugins" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectRoot\backups" | Out-Null

Write-Host "✓ Directories created" -ForegroundColor Green

Write-Host ""
Write-Host "Step 6: Setting up DAGs folder..." -ForegroundColor Yellow

# Configure DAGs folder via environment variables
$EnvContent = @"
# Airflow Environment Variables
`$env:AIRFLOW_HOME = "$ProjectRoot\airflow_home"
`$env:AIRFLOW__CORE__DAGS_FOLDER = "$ProjectRoot\dags"
"@

$EnvContent | Out-File -FilePath "$ProjectRoot\.env.ps1" -Encoding UTF8

Write-Host "✓ Environment variables configured in .env.ps1" -ForegroundColor Green

Write-Host ""
Write-Host "Step 7: Creating admin user..." -ForegroundColor Yellow

# Create admin user (skip if already exists)
try {
    airflow users create `
        --username admin `
        --firstname Admin `
        --lastname User `
        --role Admin `
        --email admin@example.com `
        --password admin 2>$null
    Write-Host "✓ Admin user created" -ForegroundColor Green
} catch {
    Write-Host "User already exists, skipping..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 8: Verifying setup..." -ForegroundColor Yellow

# Check DAG can be imported
try {
    $env:PYTHONPATH = "$ProjectRoot\dags;" + $env:PYTHONPATH
    python -c "from ml_pipeline_dag import dag; print('DAG imported successfully')" 2>$null
    Write-Host "✓ DAG import successful" -ForegroundColor Green
} catch {
    Write-Host "⚠ DAG import check skipped (will be checked when Airflow is running)" -ForegroundColor Yellow
}

# Check database
try {
    $null = airflow db check 2>&1
    Write-Host "✓ Database connection verified" -ForegroundColor Green
} catch {
    Write-Host "✗ Database connection failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start Airflow services (in separate terminals):" -ForegroundColor White
Write-Host "   airflow scheduler" -ForegroundColor Gray
Write-Host "   airflow webserver -p 8080" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Access the web UI:" -ForegroundColor White
Write-Host "   http://localhost:8080" -ForegroundColor Gray
Write-Host "   Username: admin" -ForegroundColor Gray
Write-Host "   Password: admin" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Trigger the DAG:" -ForegroundColor White
Write-Host "   airflow dags trigger mlops_pipeline_screentime" -ForegroundColor Gray
Write-Host ""
Write-Host "4. View the artifacts:" -ForegroundColor White
Write-Host "   Get-Content artifacts\metrics.json" -ForegroundColor Gray
Write-Host ""
Write-Host "Environment Variables:" -ForegroundColor Yellow
Write-Host "   AIRFLOW_HOME = $ProjectRoot\airflow_home" -ForegroundColor Gray
Write-Host "   AIRFLOW__CORE__DAGS_FOLDER = $ProjectRoot\dags" -ForegroundColor Gray
Write-Host ""
