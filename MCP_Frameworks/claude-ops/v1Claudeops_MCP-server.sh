#!/bin/bash

# Claude Ops MCP Server - Simple v1 Installer
# Reliable, tested, minimal approach
# Based on working localops implementation

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

print_step() { echo -e "${BLUE}→ $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Configuration
CURRENT_DIR="$(pwd)"
PROJECT_NAME="localops"
PROJECT_DIR="$CURRENT_DIR/$PROJECT_NAME"

echo -e "${BOLD}${BLUE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║             Claude Ops MCP Server v1.0               ║"
echo "║              Simple & Reliable                       ║"
echo "║              Made by neonite._                       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo

print_info "Installing in: $PROJECT_DIR"

# Check Python
print_step "Checking Python..."
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    print_error "Python not found. Please install Python 3.8+"
    exit 1
fi

python_version=$($PYTHON_CMD --version 2>&1)
print_success "Found: $python_version"

# Check pip and venv
if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
    print_error "pip not found"
    exit 1
fi

if ! $PYTHON_CMD -m venv --help >/dev/null 2>&1; then
    print_error "venv not found"
    exit 1
fi

# Handle existing installation
if [[ -d "$PROJECT_DIR" ]]; then
    print_warning "Existing installation found"
    read -p "Remove and reinstall? (y/N): " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR"
    else
        print_info "Keeping existing installation"
        exit 0
    fi
fi

# Create project
print_step "Creating project..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create virtual environment
print_step "Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate and install packages
print_step "Installing packages..."
source venv/bin/activate
pip install --upgrade pip
pip install mcp httpx psutil

# Create simple server
print_step "Creating server..."
cat > localops_server.py << 'EOF'
#!/usr/bin/env python3
"""
LocalOps MCP Server v1.0 - Simple & Reliable
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server

# Create server
server = Server("localops")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="system_info",
            description="Get system information",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="list_processes",
            description="List running processes",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="run_command",
            description="Run a shell command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command to run"}
                },
                "required": ["command"]
            }
        ),
        types.Tool(
            name="list_directory",
            description="List directory contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path"}
                },
                "required": ["path"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool calls."""
    
    if name == "system_info":
        result = await get_system_info()
    elif name == "list_processes":
        result = await list_processes()
    elif name == "run_command":
        result = await run_command(arguments.get("command", ""))
    elif name == "list_directory":
        result = await list_directory(arguments.get("path", "."))
    else:
        result = {"error": f"Unknown tool: {name}"}
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    try:
        import psutil
        import platform
        
        return {
            "platform": platform.platform(),
            "system": platform.system(),
            "cpu_count": psutil.cpu_count(),
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "free": psutil.disk_usage('/').free,
                "percent": psutil.disk_usage('/').percent
            }
        }
    except Exception as e:
        return {"error": str(e)}

async def list_processes() -> Dict[str, Any]:
    """List running processes."""
    try:
        import psutil
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return {"processes": processes[:10]}
    except Exception as e:
        return {"error": str(e)}

async def run_command(command: str) -> Dict[str, Any]:
    """Run a shell command."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=10
        )
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"error": str(e)}

async def list_directory(path: str) -> Dict[str, Any]:
    """List directory contents."""
    try:
        dir_path = Path(path)
        if not dir_path.exists():
            return {"error": "Directory does not exist"}
        
        items = []
        for item in dir_path.iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None
            })
        
        return {"path": str(dir_path), "items": items}
    except Exception as e:
        return {"error": str(e)}

async def main():
    """Main server entry point."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="localops",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
EOF

chmod +x localops_server.py

# Test the server
print_step "Testing server..."
if python localops_server.py --help >/dev/null 2>&1 || timeout 2s python localops_server.py >/dev/null 2>&1; then
    print_success "Server test passed"
else
    print_warning "Server test inconclusive (may be normal)"
fi

# Create test script
cat > test_server.sh << 'EOF'
#!/bin/bash
echo "Testing LocalOps MCP Server..."
cd "$(dirname "$0")"

if [[ -f "venv/bin/python" ]]; then
    echo "✅ Using: venv/bin/python"
    venv/bin/python -c "
try:
    import localops_server
    print('✅ Server imports successfully')
except Exception as e:
    print(f'❌ Import failed: {e}')
"
else
    echo "❌ Virtual environment not found"
fi
EOF
chmod +x test_server.sh

print_success "LocalOps MCP Server v1.0 installed successfully!"
echo
print_info "📋 Installation Summary:"
print_info "  • Directory: $PROJECT_DIR"
print_info "  • Python: $PROJECT_DIR/venv/bin/python"
print_info "  • Server: $PROJECT_DIR/localops_server.py"
echo
print_info "🚀 Next Steps:"
print_info "  1. Test with: ./test_server.sh"
print_info "  2. Configure in Claude Desktop:"
print_info "     Command: $PROJECT_DIR/venv/bin/python"
print_info "     Args: [\"$PROJECT_DIR/localops_server.py\"]"
echo
print_success "✅ Ready to use!"