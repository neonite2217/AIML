# Claude Ops MCP Server

A powerful Model Context Protocol (MCP) server that transforms Claude into your personal system administrator. This tool provides secure, controlled access to system operations, file management, and task automation across multiple operating systems.

## Overview

Claude Ops MCP Server bridges the gap between AI assistance and system administration by giving Claude the ability to:
- Execute system commands safely within a containerized environment
- Manage files and directories throughout your user home directory
- Automate common development and maintenance tasks
- Monitor system resources and performance
- Handle multi-OS package management (apt, yum, dnf, brew, pacman, etc.)

All operations are secured through command whitelisting, path restrictions, and dangerous operation confirmations.

## Key Features

### 🛡️ Security First
- **Containerized Execution**: All commands run in isolated Docker environment
- **Path Whitelisting**: File access limited to user home directory and workspace
- **Command Whitelisting**: Only pre-approved command patterns can be executed
- **Dangerous Command Confirmation**: Operations like `sudo rm` require explicit user confirmation
- **Comprehensive Logging**: Full audit trail of all operations for security review

### 🔧 System Administration
- **Multi-OS Support**: Works across Linux, macOS, and Windows environments
- **Package Management**: Supports apt, yum, dnf, brew, pacman, zypper, emerge
- **Process Management**: Monitor and manage system processes safely
- **Resource Monitoring**: CPU, memory, disk usage tracking
- **Service Management**: systemctl and service command support

### 📁 File Management
- **Full Home Directory Access**: Complete file operations throughout user space
- **Smart File Detection**: Automatic encoding detection and file type recognition
- **Directory Operations**: Create, list, navigate, and organize directories
- **File Operations**: Read, write, modify, and delete files with safety checks
- **Archive Support**: Create and extract tar.gz, zip, and other archive formats

### 🚀 Task Automation
- **Predefined Workflows**: Common development and system tasks ready to use
- **Custom Task Creation**: Define your own automation workflows
- **Live Configuration**: Edit tasks and commands without server restart
- **Multi-Step Operations**: Chain commands together for complex workflows

### 🔄 Live Configuration Management
- **Hot Reloading**: Configuration changes take effect immediately
- **Web-Based Editing**: Modify allowed commands and tasks through Claude
- **Backup System**: Automatic configuration backups before changes
- **Version Control**: Track configuration changes over time

## Installation

### Prerequisites
- Docker Desktop (latest version)
- Claude Desktop application
- Git (for repository management)

### One-Step Installation

The installer automatically:
1. Downloads and builds the Docker image
2. Creates necessary configuration files
3. Updates Claude Desktop configuration
4. Sets up workspace directories
5. Configures security settings

**Linux/macOS:**
```bash
curl -sSL https://raw.githubusercontent.com/yourusername/claude-ops-mcp/main/install.sh | bash
```

**Windows (PowerShell as Administrator):**
```powershell
iwr -useb https://raw.githubusercontent.com/yourusername/claude-ops-mcp/main/install.ps1 | iex
```

### Manual Installation

If you prefer manual setup:

1. **Clone Repository:**
   ```bash
   git clone https://github.com/yourusername/claude-ops-mcp-server.git
   cd claude-ops-mcp-server
   ```

2. **Build Docker Image:**
   ```bash
   docker build -t claude-ops-mcp-server .
   ```

3. **Configure Claude Desktop:**
   
   **macOS:**
   ```bash
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```
   
   **Linux:**
   ```bash
   nano ~/.config/Claude/claude_desktop_config.json
   ```
   
   **Windows:**
   ```powershell
   notepad "$env:APPDATA\Claude\claude_desktop_config.json"
   ```

4. **Add Configuration:**
   ```json
   {
     "mcpServers": {
       "claude-ops": {
         "command": "docker",
         "args": [
           "run", "-i", "--rm",
           "-v", "$HOME:$HOME",
           "-v", "/tmp:/tmp",
           "-w", "$HOME",
           "-e", "USER_HOME=$HOME",
           "-e", "WORKSPACE_DIR=$HOME/workspace",
           "claude-ops-mcp-server"
         ]
       }
     }
   }
   ```

## Usage Guide

### Getting Started

After installation, restart Claude Desktop and start a new conversation. Claude will automatically have access to the new system administration tools.

**Test the installation:**
```
Ask Claude: "What system tools do you have available?"
```

Claude should respond with a list of available MCP tools including file management, command execution, and system monitoring capabilities.

### Basic Operations

#### File Management
```
"List all files in my Documents directory"
"Read my .bashrc file and show me the current PATH"
"Create a new Python script called hello.py in my workspace"
"Delete the temporary files in my Downloads folder"
```

#### System Information
```
"Show me current system status including CPU and memory usage"
"What version of Python, Node, and Docker do I have installed?"
"List all running processes and their resource usage"
"Check disk space across all mounted drives"
```

#### Package Management
```
"Update my system packages and show what's available"
"Install Flask and requests using pip"
"Install Node.js packages for my project"
"Check what development tools I have installed"
```

#### Task Automation
```
"Run the system health check task"
"Execute the Python development environment setup"
"Start my development server and show the output"
"Run the backup task for my configuration files"
```

### Advanced Workflows

#### Development Environment Setup
```
"Check if I have Python 3.11+, Node 18+, and Docker installed"
"Create a new Flask project structure in my workspace"
"Install all dependencies and start the development server"
"Set up git repository and make initial commit"
```

#### System Maintenance
```
"Run full system maintenance: update packages, check disk space, clean temporary files"
"Monitor system performance and identify resource-heavy processes"
"Back up my configuration files and important documents"
"Check system logs for any errors or warnings"
```

#### Project Management
```
"Analyze my current project structure and dependencies"
"Run tests, check code quality, and generate coverage report"
"Build and deploy my application to staging environment"
"Create release notes and tag the current version"
```

## Configuration

### Command Whitelisting

Commands are organized by category in `allowed_commands.json`:

```json
{
  "system_info": [
    "ps aux", "top -b -n1", "uptime", "whoami"
  ],
  "package_management": [
    "pip install", "npm install", "brew install", "sudo apt install"
  ],
  "version_control": [
    "git status", "git log", "git pull", "git push"
  ],
  "development": [
    "python --version", "node --version", "docker --version"
  ]
}
```

### Task Definitions

Predefined workflows in `tasks.json`:

```json
{
  "system_health": "uptime && df -h && free -h && ps aux | head -10",
  "dev_setup": "python --version && pip list && node --version && npm list -g",
  "git_overview": "git status && git log --oneline -10 && git remote -v",
  "update_all": "sudo apt update && sudo apt list --upgradable || brew update && brew outdated"
}
```

### Live Configuration Editing

You can modify configurations through Claude:

```
"Show me the current allowed commands configuration"
"Add MySQL and PostgreSQL commands to the database category"
"Create a new deployment task that builds and pushes to production"
"Backup my current configurations before making changes"
```

## Security Model

### Container Isolation
- All operations execute within a secure Docker container
- Container runs as non-root user with selective sudo access
- Home directory mounted read-write for necessary file operations
- System directories mounted read-only or not mounted at all

### Permission System
- **File Operations**: Limited to user home directory and workspace
- **Command Execution**: Only whitelisted command patterns allowed
- **Dangerous Operations**: Require explicit user confirmation
- **Resource Limits**: CPU and memory usage bounded by container limits

### Audit Trail
- All commands logged with timestamp and user context
- File operations tracked with full path information
- Failed operations and permission denials recorded
- Configuration changes logged with before/after states

### Dangerous Command Handling

Commands containing potentially harmful patterns require confirmation:
- `sudo rm`, `rm -rf` - File deletion with elevated privileges
- `shutdown`, `reboot` - System state changes
- `mkfs`, `fdisk` - Disk formatting operations
- `iptables`, `ufw` - Firewall modifications

Example:
```
User: "Clean up old log files with sudo rm -rf /var/log/old/*"
Claude: "This is a dangerous command that will permanently delete files. 
        To proceed, confirm by saying 'execute with confirmation' or use 
        the confirm_dangerous parameter."
```

## Troubleshooting

### Common Issues

#### Tools Not Appearing in Claude
1. Verify Docker image built successfully: `docker images | grep claude-ops`
2. Check Claude Desktop configuration file syntax
3. Restart Claude Desktop completely
4. Verify Docker is running: `docker ps`

#### Command Execution Failures
1. Use `list_allowed_commands` to check exact patterns
2. Commands must match whitelist prefixes exactly
3. For dangerous commands, use confirmation parameter
4. Check Docker container logs: `docker logs <container_id>`

#### File Access Denied
1. Verify path is within user home directory
2. Check file permissions: `ls -la <filepath>`
3. Ensure parent directories exist
4. Use absolute paths when relative paths fail

#### Performance Issues
1. Monitor system resources: Ask Claude for system status
2. Check for long-running processes
3. Adjust Docker resource limits if needed
4. Review command timeout settings

### Debug Mode

Enable detailed logging:
```
"Enable debug mode and show me detailed logs for the next command"
"Execute 'ls -la' and show me the full execution trace"
```

### Configuration Validation

Check configuration integrity:
```
"Validate my current allowed commands configuration"
"Test all predefined tasks and show any errors"
"Show me the current security settings and restrictions"
```

## Best Practices

### For Users
- Start with simple commands to verify functionality
- Use descriptive names for custom tasks and configurations
- Regular backups of important configurations
- Monitor system resources during heavy operations
- Review audit logs periodically for security

### For Developers
- Keep command patterns specific but flexible
- Test new commands in isolation before adding to production
- Use meaningful task names that clearly describe their purpose
- Document custom workflows for team members
- Version control configuration files

### For System Administrators
- Regular security audits of allowed commands
- Monitor Docker resource usage and set appropriate limits
- Keep base Docker image updated for security patches
- Review user access patterns and adjust permissions as needed
- Implement log rotation and archival policies

## API Reference

### Core Tools

#### `list_directory(path: str = "") -> str`
List files and directories in the specified path.

**Parameters:**
- `path`: Directory path to list (defaults to workspace)

**Returns:** Formatted directory listing with file sizes and timestamps

#### `read_file(filepath: str) -> str`
Read the contents of a text file.

**Parameters:**
- `filepath`: Path to file to read

**Returns:** File contents as string

#### `write_file(filepath: str, content: str) -> str`
Write content to a file, creating directories as needed.

**Parameters:**
- `filepath`: Destination file path
- `content`: Content to write

**Returns:** Confirmation message with character count

#### `execute_command(command: str, confirm_dangerous: str = "false") -> str`
Execute a whitelisted system command safely.

**Parameters:**
- `command`: Command to execute
- `confirm_dangerous`: Set to "true" for dangerous commands

**Returns:** Command output, error messages, and exit code

#### `run_task(task_name: str, confirm_dangerous: str = "false") -> str`
Execute a predefined task workflow.

**Parameters:**
- `task_name`: Name of task to execute
- `confirm_dangerous`: Set to "true" for dangerous tasks

**Returns:** Task output and execution results

#### `system_status() -> str`
Get current system status including resource usage.

**Returns:** CPU, memory, disk usage, and system information

#### `list_allowed_commands() -> str`
Display all whitelisted command patterns by category.

**Returns:** Organized list of allowed commands with danger warnings

### Advanced Tools

#### Configuration Management
- `edit_config()` - Modify allowed commands and tasks
- `backup_configs()` - Create configuration backups
- `validate_config()` - Check configuration integrity

#### System Operations
- `system_cleanup()` - Clean temporary files and caches
- `analyze_disk_usage()` - Find largest files and directories
- `monitor_processes()` - Real-time process monitoring

#### Development Tools
- `project_init()` - Initialize new development projects
- `dependency_check()` - Verify and update project dependencies
- `test_runner()` - Execute test suites and report results

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make changes with appropriate tests
4. Submit pull request with detailed description

### Code Standards
- Follow Python PEP 8 style guidelines
- Add comprehensive error handling
- Include security considerations in all features
- Document all public functions and methods
- Add tests for new functionality

### Security Considerations
- Never bypass security restrictions
- All new commands must be whitelisted
- Dangerous operations require confirmation
- File access must respect path restrictions
- Log all security-relevant operations

## License

MIT License - See LICENSE file for details.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/yourusername/claude-ops-mcp/issues
- Documentation: https://github.com/yourusername/claude-ops-mcp/wiki
- Security Issues: security@yourdomain.com

---

**⚠️ Security Notice:** This tool provides Claude with system administration capabilities. While designed with security in mind, always review commands before execution and maintain regular backups of important data.