#!/bin/bash

# Setup script for the project
echo "=== Multivariate Time Series Forecasting Setup ==="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Start database: ./start_db.sh"
echo "  2. Run forecast:   python forecast.py"
echo "  3. Stop database:  ./stop_db.sh"
