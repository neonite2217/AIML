#!/bin/bash

# 🚀 LocalOps Assistant - Build & Management Script
# Builds the Go application and provides management functions

set -e

# Function to build the application
build_app() {
    echo "🔨 Building LocalOps Assistant..."
    echo "📦 Building for current platform..."
    go build -o localops main.go
    chmod +x localops
    echo "✅ Build complete!"
    echo ""
    echo "🚀 Usage:"
    echo "  ./localops install          # Install and setup"
    echo "  ./localops \"show system info\" # Direct command"
    echo "  ./localops                  # Interactive mode"
    echo "  ./localops mcp              # MCP server mode"
    echo "  ./build.sh mcp              # Start MCP server"
    echo ""
    echo "📁 Binary created: ./localops"
}

# Function to start MCP server
start_mcp_server() {
    echo "🚀 Starting LocalOps Assistant MCP Server..."
    
    # Check if binary exists
    if [ ! -f "./localops" ]; then
        echo "❌ LocalOps binary not found. Building..."
        build_app
    fi
    
    # Check if Ollama is running (optional for basic commands)
    if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "⚠️  Ollama not detected. Some AI features may be limited."
        echo "💡 To enable full AI capabilities, run: ollama serve"
    fi
    
    echo "✅ Starting MCP server mode..."
    echo "📡 Listening for MCP requests on stdin/stdout..."
    
    # Start the MCP server
    exec ./localops mcp
}

# Main script logic
case "${1:-build}" in
    "build"|"")
        build_app
        ;;
    "mcp"|"server")
        start_mcp_server
        ;;
    "help"|"-h"|"--help")
        echo "🚀 LocalOps Assistant Build & Management Script"
        echo ""
        echo "Usage:"
        echo "  ./build.sh [command]"
        echo ""
        echo "Commands:"
        echo "  build (default)  Build the LocalOps Assistant binary"
        echo "  mcp, server      Start MCP server (builds if needed)"
        echo "  help             Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./build.sh           # Build the application"
        echo "  ./build.sh mcp       # Start MCP server"
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "💡 Use './build.sh help' for available commands"
        exit 1
        ;;
esac