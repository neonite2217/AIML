# **LocalOps Assistant**

**AI-Powered System Operations Assistant with MCP Integration**

LocalOps Assistant leverages conversational AI to transform natural language into precise Linux commands. With integrated safety controls and seamless Model Context Protocol (MCP) support, it enhances system operations workflows through intuitive AI assistance.

## 🚀 **Quick Start**

```bash
# Build the application
./build.sh

# Install and set up the application
./localops install

# Test conversational features
./localops "hello"
./localops "show system info"

# Start the MCP server for AI integration
./build.sh mcp
```

## ✨ **Key Features**

### 🧠 **Enhanced Intelligence**

* **Conversational AI**: Understands natural interactions like greetings and system queries.
* **Instant Command Execution**: Supports 100+ common system commands for immediate execution.
* **AI Fallback**: Complex commands are handled intelligently using Ollama.
* **Smart Pattern Recognition**: Prioritizes and recognizes commands efficiently.
* **Natural Language Processing**: Seamlessly processes commands like "show me system info."

### 🔌 **MCP Integration (NEW!)**

* **Protocol Support**: Full compliance with Model Context Protocol (MCP) 
* **Three MCP Tools**: Includes system commands, system info, and file operations.
* **AI System Integration**: Works with Claude Desktop and other MCP clients.
* **Security**: All safety mechanisms apply to MCP tool calls.

### 🖥️ **Rich System Information**

* **Formatted Output**: Provides visually appealing, structured system overviews with emojis.
* **Comprehensive Data**: Displays CPU, memory, disk, and hardware info in clear sections.
* **Performance Monitoring**: Monitors CPU usage, load averages, and top processes.
* **Smart Categorization**: Organizes data by type for easier navigation.

### 📦 **Smart Package Management**

* **Auto-sudo**: Automatically applies `sudo` for package management operations.
* **Smart Chaining**: Updates packages before installing or upgrading.
* **Full APT Support**: Includes `update`, `upgrade`, `install`, `clean`, and `autoremove`.
* **Version Checking**: Instantly checks the versions of over 15 commonly used packages.

### 📁 **Enhanced File Operations**

* **Directory-Specific Operations**: Smart handling for system directories like home, root, and /etc.
* **Priority Matching**: Checks specific patterns before generic ones.
* **Colorful Listings**: Displays file listings with enhanced formatting.
* **Smart Navigation**: Contextual directory navigation with commands like "what’s here."

### 🛡️ **Smart Authorization System**

* **Auto-approved**: Safe, read-only operations such as system queries and file readings.
* **Confirmation Required**: Potentially dangerous commands require explicit confirmation.
* **Permanently Blocked**: System-destructive commands are blocked.
* **Learning System**: Remembers your preferences for safer, faster interactions.

## 📋 **Installation & Setup**

### 🎯 **Quick Install (Recommended)**

```bash
# 1. Build the application
./build.sh

# 2. Run the installer (automates setup)
./localops install

# 3. Test it immediately
./localops "show system info"
```

### 🛠️ **Manual Installation**

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull the AI model
ollama pull llama3.2:3b

# 3. Build LocalOps
./build.sh

# 4. Test functionality
./localops "hello"
```

## 💡 **Usage Examples**

### 🗣️ **Conversational Intelligence**

```bash
./localops "hello"
./localops "what can you do"
./localops "thank you"
```

### 🖥️ **Enhanced System Information**

```bash
./localops "show system info"
```

### 📦 **Smart Package Management**

```bash
./localops "apt update"
./localops "install htop"
```

### 📁 **Enhanced File Operations**

```bash
./localops "list files in home directory"
```

## 🔌 **MCP Integration**

### 🚀 **Start MCP Server**

```bash
# Method 1: Using build script
./build.sh mcp

# Method 2: Direct command
./localops mcp
```

### 🛠️ **Available MCP Tools**

1. **`execute_system_command`**: Execute system commands via natural language.
2. **`get_system_info`**: Retrieve detailed system information.
3. **`list_files`**: List files and directories with optional path filtering.

## 🎮 **Interactive Mode**

```bash
./localops
```

## 🛡️ **Security Features**

* **Auto-Approved (Safe)**: System info queries, file reading, version checks.
* **Requires Confirmation**: Package operations, service control, file deletion.
* **Permanently Blocked**: Destructive commands, system formatting, force operations.

## 📁 **Project Structure**

```
main.go                    # Go source code with enhanced intelligence
go.mod                     # Go module file
build.sh                   # Build & management script
README.md                 # Documentation
localops                  # Compiled binary
~/.localops/              # Configuration directory
├── approved-commands.conf # Auto-approved commands
├── blocked-commands.conf  # Blocked commands
└── usage.log             # Command history
```

## ⚙️ **Configuration**

### Environment Variables

```bash
export OLLAMA_MODEL="llama3.2:3b"  # Default model (recommended)
export OLLAMA_MODEL="llama3.2:1b"  # Faster, less capable model
export OLLAMA_MODEL="llama3.2:7b"  # Slower, more capable model
export OLLAMA_URL="http://localhost:11434"  # Ollama server URL
```

### Model Recommendations

* **llama3.2:1b**: Fast, suitable for simple commands.
* **llama3.2:3b**: Balanced performance (recommended).
* **llama3.2:7b**: Best accuracy but slower.

⚠️ **Caution**: The performance and accuracy of the results may vary depending on the model selected. Smaller models (e.g., llama3.2:1b) provide faster responses but may have lower accuracy for complex tasks, while larger models (e.g., llama3.2:7b) offer better results at the cost of increased processing time.

## 🎯 **Advanced Features**

* **Conversational Responses**: Natural language interactions without AI overhead.
* **Smart Command Chaining**: Handles dependencies automatically.
* **Error Recovery**: Gracefully handles command errors.

## 🔍 **Troubleshooting**

### Common Issues

```bash
# Check available build options
./build.sh help
```

## 📊 **Performance**

### System Requirements

* **Minimum**: 4GB RAM, 2GB storage
* **Recommended**: 8GB RAM, 4GB storage
* **Optimal**: 16GB RAM, 8GB storage

---

## 📑 **Credits and Acknowledgements**

* **LocalOps Assistant** was developed and maintained by **neonite._**.
* **Ollama**: Used for AI-powered natural language processing.
* **MCP Protocol**: The integration of Model Context Protocol is inspired by the work of the [mark3labs MCP-Go](https://github.com/mark3labs/mcp-go), whose implementation of a Go-based MCP server provided a strong foundation.
* **Thanks to contributors and open-source libraries**: LocalOps Assistant uses various open-source libraries and contributions that help bring this project to life.
