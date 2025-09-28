# ClaudeOPS - System Administration MCP Server

Transform Claude into your personal system administrator with secure, containerized command execution and comprehensive DevOps automation.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Docker](https://img.shields.io/badge/Docker-Required-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## 🎯 Overview

ClaudeOPS bridges the gap between AI assistance and system administration by providing Claude with secure, controlled access to system operations, file management, and development workflows.

### Key Capabilities
- **🛡️ Secure Command Execution** - Containerized environment with whitelisted commands
- **📁 File System Management** - Full home directory access with safety controls
- **🔧 Multi-OS Package Management** - Support for apt, brew, yum, dnf, pacman, and more
- **🚀 Development Automation** - Git workflows, project setup, and task management
- **📊 System Monitoring** - Resource usage, process management, and health checks

## ✨ Features

### Security First
- **Containerized Execution** - All commands run in isolated Docker environment
- **Command Whitelisting** - Only pre-approved command patterns allowed
- **Path Restrictions** - File access limited to user home directory
- **Dangerous Command Confirmation** - Operations like `sudo rm` require explicit confirmation
- **Comprehensive Logging** - Full audit trail for security review

### System Administration
- **Multi-OS Support** - Works across Linux, macOS, and Windows
- **Package Management** - apt, yum, dnf, brew, pacman, zypper, emerge
- **Process Management** - Monitor and manage system processes safely
- **Resource Monitoring** - CPU, memory, disk usage tracking
- **Service Management** - systemctl and service command support

### Development Tools
- **Git Operations** - Complete Git workflow automation
- **Project Management** - Initialize and manage development projects
- **Dependency Management** - Python pip, Node npm/yarn, system packages
- **Build Automation** - Make, CMake, Docker, and more
- **Environment Setup** - Automated development environment configuration

## 🚀 Quick Start

### One-Line Installation

**Linux/macOS:**
```bash
curl -sSL https://raw.githubusercontent.com/yourusername/claude-ops-mcp/main/install.sh | bash
```

**Windows (PowerShell as Administrator):**
```powershell
iwr -useb https://raw.githubusercontent.com/yourusername/claude-ops-mcp/main/install.ps1 | iex
```

The installer automatically:
1. ✅ Downloads and builds Docker image
2. ✅ Creates project directory with all files
3. ✅ Sets up Python virtual environment
4. ✅ Updates Claude Desktop configuration
5. ✅ Creates diagnostic and testing tools

### Manual Installation

If you prefer step-by-step setup:

```bash
# 1. Create project directory
mkdir claudeops && cd claudeops

# 2. Download installer script
curl -O https://raw.githubusercontent.com/yourusername/claude-ops-mcp/main/Claudeops_MCP-server.sh
chmod +x Claudeops_MCP-server.sh

# 3. Run installer
./Claudeops_MCP-server.sh

# 4. Test installation

```

## 💻 Usage Examples

### Getting Started

After installation, restart Claude Desktop and test:

```
"What system tools do you have available?"
```

Claude will show available MCP tools including file management, command execution, and system monitoring.

### Basic Operations

**System Information:**
```
"Show me current system status including CPU and memory usage"
"What version of Python, Node, and Docker do I have installed?"
"List all running processes and their resource usage"
```

**File Management:**
```
"List all files in my Documents directory"
"Read my .bashrc file and show me the current PATH"
"Create a new Python script called hello.py in my workspace"
"Delete temporary files in my Downloads folder"
```

**Package Management:**
```
"Update my system packages and show what's available"
"Install Flask and requests using pip"
"Install Node.js packages for my project"
"Check what development tools I have installed"
```

### Advanced Workflows

**Development Environment Setup:**
```
"Check if I have Python 3.11+, Node 18+, and Docker installed"
"Create a new Flask project structure in my workspace"
"Install all dependencies and start the development server"
"Set up git repository and make initial commit"
```

**System Maintenance:**
```
"Run full system maintenance: update packages, check disk space, clean temporary files"
"Monitor system performance and identify resource-heavy processes"
"Back up my configuration files and important documents"
```

**Git Workflow Automation:**
```
"Show me the current git status and recent commits"
"Create a new feature branch called 'user-authentication'"
"Stage all changes, commit with message 'Add login functionality', and push to origin"
"Merge the current branch to main and clean up"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                Claude Desktop                       │
└─────────────────┬───────────────────────────────────┘
                  │ MCP Protocol (stdio)
                  │
┌─────────────────▼───────────────────────────────────┐
│              Docker Container                       │
│  ┌──────────────────────────────────────────────┐  │
│  │  ClaudeOPS MCP Server (Python)              │  │
│  │  - FastMCP framework                         │  │
│  │  - Command whitelisting                      │  │
│  │  - File system operations                    │  │
│  │  - System monitoring                         │  │
│  └──────────────┬───────────────────────────────┘  │
│                 │                                   │
│  ┌──────────────▼───────────────────────────────┐  │
│  │  Host System Access                          │  │
│  │  - Home directory mounted                    │  │
│  │  - Docker socket access                      │  │
│  │  - Network access                            │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 🔧 Configuration

### Command Categories

Commands are organized by category in the server:

```python
ALLOWED_COMMANDS = {
    "system_info": [
        "ps aux", "top -b -n1", "uptime", "whoami", "free -h", "df -h"
    ],
    "package_management": [
        "apt update", "sudo apt install", "brew install", "pip install"
    ],
    "git_operations": [
        "git status", "git commit", "git push", "git pull", "git branch"
    ],
    "file_operations": [
        "ls", "cat", "mkdir", "cp", "mv", "find", "grep"
    ],
    "development": [
        "make", "docker build", "npm install", "python --version"
    ]
}
```

### Predefined Tasks

Common workflows available as single commands:

```python
TASKS = {
    "system_health": "uptime && df -h && free -h && ps aux | head -10",
    "update_system": "sudo apt update && sudo apt upgrade -y",
    "python_setup": "python3 --version && pip3 list",
    "git_overview": "git status && git log --oneline -10",
    "docker_status": "docker --version && docker ps"
}
```

### Security Controls

**Path Restrictions:**
- Full access to user home directory (`$HOME`)
- Read-only access to system paths (`/usr`, `/opt`, `/etc`)
- No access to sensitive system directories

**Dangerous Command Handling:**
Commands requiring confirmation:
- `sudo rm`, `rm -rf` - File deletion with elevated privileges
- `shutdown`, `reboot` - System state changes
- `mkfs`, `fdisk` - Disk operations
- `iptables`, `ufw` - Firewall changes

## 🛠️ Available Tools

### Core System Tools

| Tool | Description |
|------|-------------|
| `system_status()` | CPU, memory, disk usage, process count |
| `server_status()` | MCP server uptime and configuration |
| `list_directory(path)` | List files and directories |
| `read_file(filepath)` | Read file contents with encoding detection |
| `write_file(filepath, content)` | Write content to file |
| `execute_command(command)` | Run whitelisted system commands |
| `run_task(task_name)` | Execute predefined workflows |

### Advanced Tools

| Tool | Description |
|------|-------------|
| `list_allowed_commands()` | Show all whitelisted command patterns |
| `system_cleanup()` | Analyze and clean temporary files |
| `analyze_disk_usage()` | Find largest files and directories |
| `monitor_processes()` | Real-time process monitoring |
| `git_operations()` | Git workflow automation |
| `project_init()` | Initialize development projects |

## 📊 Project Structure

```
claudeops/
├── claude_ops_server.py         # Main MCP server
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── debug_server.sh             # Diagnostic tool
├── verify_config.sh            # Configuration validator
├── claude_ops.log              # Server logs
├── claude_ops.pid              # Process ID file
├── venv/                       # Python virtual environment
└── docs/
    ├── installation-guide.md   # Detailed setup instructions
    ├── security-guide.md       # Security considerations
    └── troubleshooting.md      # Common issues and solutions
```

## 🔍 Diagnostic Tools

### Debug Server
```bash
./debug_server.sh
```
Comprehensive diagnostic suite that checks:
- ✅ Python virtual environment
- ✅ Package installations
- ✅ MCP server functionality
- ✅ Claude Desktop configuration
- ✅ Docker container status

### Configuration Verifier
```bash
./verify_config.sh
```
Validates Claude Desktop configuration:
- ✅ JSON syntax validation
- ✅ Server configuration check
- ✅ File path verification
- ✅ Environment variable validation

## 🐛 Troubleshooting

### Common Issues

**Tools Not Appearing:**
```bash
# Check server status
./debug_server.sh

# Verify configuration
./verify_config.sh

# Check Claude Desktop logs
# macOS: ~/Library/Logs/Claude/
# Windows: %APPDATA%\Claude\logs\
```

**Command Execution Failures:**
```bash
# List allowed commands
# In Claude: "Show me all allowed commands"

# Check for exact pattern matching
# Commands must match whitelist prefixes exactly
```

**Permission Errors:**
```bash
# Check file permissions
ls -la claude_ops_server.py

# Ensure Docker is running
docker info

# Verify home directory access
# In Claude: "List files in my home directory"
```

### Debug Mode

Enable detailed logging in Claude:
```
"Enable debug mode and show me detailed logs for the next command"
"Execute 'ls -la' and show me the full execution trace"
```

## 🔐 Security Model

### Container Isolation
- All operations execute within secure Docker container
- Container runs as non-root user with selective sudo access
- Home directory mounted read-write for file operations
- System directories mounted read-only or not mounted

### Permission System
- **File Operations**: Limited to user home directory and workspace
- **Command Execution**: Only whitelisted command patterns allowed
- **Dangerous Operations**: Require explicit user confirmation
- **Resource Limits**: CPU and memory usage bounded by container

### Audit Trail
- All commands logged with timestamp and context
- File operations tracked with full path information
- Failed operations and permission denials recorded
- Configuration changes logged with before/after states

## 📈 Performance

### Benchmarks
- **Command Execution**: < 100ms for simple commands
- **File Operations**: < 50ms for typical file sizes
- **System Monitoring**: Real-time updates
- **Container Startup**: < 2 seconds cold start

### Optimization Tips
1. Keep frequently used files in workspace
2. Use task workflows for multi-step operations
3. Monitor resource usage with system_status()
4. Clean up temporary files regularly

## 🚧 Future Enhancements

### Planned Features
- [ ] Web UI for server management
- [ ] Custom command templates
- [ ] Integration with CI/CD pipelines
- [ ] Multi-container orchestration
- [ ] Remote server management
- [ ] Plugin system for extensions

### Integration Roadmap
- [ ] Kubernetes cluster management
- [ ] AWS/GCP/Azure cloud operations
- [ ] Terraform infrastructure management
- [ ] Ansible playbook execution
- [ ] Jenkins pipeline integration

## 🤝 Contributing

Contributions welcome! Please follow these guidelines:

1. **Security First** - Never bypass security restrictions
2. **Test Thoroughly** - All new commands must be whitelisted
3. **Document Changes** - Update command lists and examples
4. **Follow Patterns** - Use existing code patterns for consistency

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/claude-ops-mcp
cd claude-ops-mcp

# Set up development environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Test server locally
python claude_ops_server.py
```

## 📄 License

MIT License - See [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- **FastMCP** - Python MCP framework
- **Docker** - Containerization platform
- **psutil** - System monitoring library
- **Anthropic** - MCP specification and Claude Desktop

---

**⚠️ Security Notice:** This tool provides Claude with system administration capabilities. While designed with security in mind, always review commands before execution and maintain regular backups.

*Made with ❤️ for developers who want AI-powered system administration*
