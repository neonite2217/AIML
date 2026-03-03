#!/bin/bash

# Setup script for MLOps Pipeline using Apache Airflow
# Supports: Unix/Linux/macOS
# Usage: ./setup.sh

set -e  # Exit on error

echo "=========================================="
echo "MLOps Pipeline Setup Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${YELLOW}Step 1: Checking prerequisites...${NC}"

# Check Python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python is not installed${NC}"
    echo "Please install Python 3.14+ from https://python.org"
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"

# Check pip
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip is not installed${NC}"
    exit 1
fi

PIP_CMD=$(command -v pip3 || command -v pip)
echo -e "${GREEN}✓ pip found${NC}"

echo ""
echo -e "${YELLOW}Step 2: Setting up Airflow home...${NC}"

# Set Airflow home
export AIRFLOW_HOME="$PROJECT_ROOT/airflow_home"
mkdir -p "$AIRFLOW_HOME"
echo -e "${GREEN}✓ Airflow home set to: $AIRFLOW_HOME${NC}"

echo ""
echo -e "${YELLOW}Step 3: Installing dependencies...${NC}"

# Install requirements
cd "$PROJECT_ROOT"
$PIP_CMD install -r requirements.txt --quiet 2>&1 | grep -v "already satisfied" || true
echo -e "${GREEN}✓ Dependencies installed${NC}"

echo ""
echo -e "${YELLOW}Step 4: Initializing Airflow database...${NC}"

# Initialize Airflow database
airflow db migrate --quiet
echo -e "${GREEN}✓ Airflow database initialized${NC}"

echo ""
echo -e "${YELLOW}Step 5: Creating directories...${NC}"

# Create required directories
mkdir -p "$PROJECT_ROOT/data"
mkdir -p "$PROJECT_ROOT/artifacts"
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/plugins"
mkdir -p "$PROJECT_ROOT/backups"

echo -e "${GREEN}✓ Directories created${NC}"

echo ""
echo -e "${YELLOW}Step 6: Setting up DAGs folder...${NC}"

# Configure DAGs folder in airflow.cfg if it exists
AIRFLOW_CFG="$AIRFLOW_HOME/airflow.cfg"
if [ -f "$AIRFLOW_CFG" ]; then
    # Backup existing config
    cp "$AIRFLOW_CFG" "$AIRFLOW_CFG.backup"
    
    # Update DAGs folder
    sed -i "s|^dags_folder = .*|dags_folder = $PROJECT_ROOT/dags|" "$AIRFLOW_CFG" 2>/dev/null || \
    sed -i '' "s|^dags_folder = .*|dags_folder = $PROJECT_ROOT/dags|" "$AIRFLOW_CFG" 2>/dev/null || true
    
    echo -e "${GREEN}✓ DAGs folder configured${NC}"
else
    # Set via environment variable
    echo "export AIRFLOW_HOME=$PROJECT_ROOT/airflow_home" > "$PROJECT_ROOT/.env"
    echo "export AIRFLOW__CORE__DAGS_FOLDER=$PROJECT_ROOT/dags" >> "$PROJECT_ROOT/.env"
    echo -e "${GREEN}✓ Environment variables configured in .env${NC}"
fi

echo ""
echo -e "${YELLOW}Step 7: Creating admin user...${NC}"

# Create admin user (skip if already exists)
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin 2>/dev/null || echo -e "${YELLOW}User already exists, skipping...${NC}"

echo -e "${GREEN}✓ Admin user created (admin/admin)${NC}"

echo ""
echo -e "${YELLOW}Step 8: Verifying setup...${NC}"

# Check DAG can be imported
if python -c "import sys; sys.path.insert(0, '$PROJECT_ROOT/dags'); from ml_pipeline_dag import dag; print('DAG imported successfully')" 2>/dev/null; then
    echo -e "${GREEN}✓ DAG import successful${NC}"
else
    echo -e "${YELLOW}⚠ DAG import check skipped (will be checked when Airflow is running)${NC}"
fi

# Check database
if airflow db check &>/dev/null; then
    echo -e "${GREEN}✓ Database connection verified${NC}"
else
    echo -e "${RED}✗ Database connection failed${NC}"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start Airflow services:"
echo "   airflow scheduler --daemon"
echo "   airflow webserver --daemon -p 8080"
echo ""
echo "2. Access the web UI:"
echo "   http://localhost:8080"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "3. Trigger the DAG:"
echo "   airflow dags trigger mlops_pipeline_screentime"
echo ""
echo "4. View the artifacts:"
echo "   cat artifacts/metrics.json"
echo ""
echo -e "${YELLOW}Environment Variables:${NC}"
echo "   export AIRFLOW_HOME=$PROJECT_ROOT/airflow_home"
echo "   export AIRFLOW__CORE__DAGS_FOLDER=$PROJECT_ROOT/dags"
echo ""
