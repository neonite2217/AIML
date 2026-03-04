# MCP Server Multi-Client Integration Guide

This guide helps you integrate your local Model Context Protocol (MCP) server with various AI clients and development tools.

## Table of Contents

1. [Claude Desktop](#1-claude-desktop)
2. [Continue.dev](#2-continuedev)
3. [Cursor IDE](#3-cursor-ide)
4. [Visual Studio Code](#4-visual-studio-code)
5. [Goose](#5-goose)
6. [LM Studio](#6-lm-studio)
7. [Gemini CLI](#7-gemini-cli)
8. [Troubleshooting](#troubleshooting)

---

## 1. Claude Desktop

### Configuration Location
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

### Configuration Format

```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "node",
      "args": ["/path/to/your/server/index.js"],
      "env": {
        "API_KEY": "your-api-key-if-needed"
      }
    }
  }
}
```

### Example Configurations

**Python Server:**
```json
{
  "mcpServers": {
    "my-python-server": {
      "command": "python",
      "args": ["-m", "your_server_module"],
      "env": {
        "PYTHONPATH": "/path/to/your/server"
      }
    }
  }
}
```

**NPX Server:**
```json
{
  "mcpServers": {
    "my-npx-server": {
      "command": "npx",
      "args": ["-y", "your-package-name"]
    }
  }
}
```

### Steps
1. Open the configuration file in your text editor
2. Add your server configuration under `mcpServers`
3. Save the file
4. Restart Claude Desktop
5. Your server tools will be available in conversations

---

## 2. Continue.dev

### Configuration Location
Create a folder: `.continue/mcpServers/` in your workspace root

### Configuration Format
Create individual YAML files for each server (e.g., `your-server.yaml`)

```yaml
name: your-server-name
type: stdio  # or 'sse' or 'streamable-http'
command: node
args:
  - /path/to/your/server/index.js
env:
  API_KEY: your-api-key-if-needed
```

### Supported Types
- **stdio**: Local servers using standard I/O
- **sse**: Server-sent events (remote servers)
- **streamable-http**: HTTP streaming servers

### Example Configurations

**Local Node Server:**
```yaml
name: my-local-server
type: stdio
command: node
args:
  - /home/user/projects/my-server/index.js
env:
  NODE_ENV: production
```

**Python Server with UV:**
```yaml
name: my-python-server
type: stdio
command: uvx
args:
  - my-server-package
```

**Remote SSE Server:**
```yaml
name: my-remote-server
type: sse
url: https://your-server.com/mcp
```

### Steps
1. Create `.continue/mcpServers/` folder in workspace root
2. Create a YAML file for your server
3. Save the file
4. Continue.dev will auto-detect the server
5. Use `@MCP` in chat to access resources

---

## 3. Cursor IDE

### Configuration Location
**Global**: `~/.cursor/mcp.json`  
**Project**: `.cursor/mcp.json` in project root

### Configuration Format

```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "node",
      "args": ["/path/to/your/server/index.js"],
      "env": {
        "API_KEY": "your-api-key-if-needed"
      }
    }
  }
}
```

### Remote Server Support (SSE/HTTP)

```json
{
  "mcpServers": {
    "remote-server": {
      "url": "https://your-server.com/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

### Transport Types

| Transport | Execution | Deployment | Users | Input | Auth |
|-----------|-----------|------------|-------|-------|------|
| stdio | Local | Cursor manages | Single | Shell command | Manual |
| SSE | Local/Remote | Deploy as server | Multiple | URL to SSE endpoint | OAuth |
| Streamable HTTP | Local/Remote | Deploy as server | Multiple | URL to HTTP endpoint | OAuth |

### Steps
1. Open Cursor Settings
2. Navigate to Features → Model Context Protocol
3. Enable MCP servers
4. Edit `mcp.json` file (global or project-specific)
5. Add your server configuration
6. Save and restart Cursor
7. Tools appear in "Available Tools" when relevant

---

## 4. Visual Studio Code

### Prerequisites
- VS Code version 1.102 or later
- GitHub Copilot extension installed

### Configuration Location
**Global**: Run `MCP: Open User Configuration` command  
**Workspace**: `.vscode/mcp.json` in project root  
**Remote**: Run `MCP: Open Remote User Configuration` for remote development

### Configuration Format

```json
{
  "servers": {
    "your-server-name": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/your/server/index.js"],
      "env": {
        "API_KEY": "${input:api-key}"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "api-key",
      "description": "Enter your API key",
      "password": true
    }
  ]
}
```

### Server Types

**stdio (Local):**
```json
{
  "servers": {
    "local-server": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "your_server"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      }
    }
  }
}
```

**HTTP/SSE (Remote):**
```json
{
  "servers": {
    "remote-server": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${input:api-token}"
      }
    }
  }
}
```

### Dev Container Support
Add to `.devcontainer/devcontainer.json`:

```json
{
  "image": "mcr.microsoft.com/devcontainers/typescript-node:latest",
  "customizations": {
    "vscode": {
      "mcp": {
        "servers": {
          "your-server": {
            "command": "node",
            "args": ["server.js"]
          }
        }
      }
    }
  }
}
```

### Steps
1. Open Command Palette (Ctrl/Cmd+Shift+P)
2. Run `MCP: Add Server` command
3. Choose server type (stdio, http, sse)
4. Enter server configuration
5. Choose Global or Workspace settings
6. Enable MCP support: `chat.mcp.enabled` setting
7. Open Chat view (Ctrl/Cmd+Alt+I)
8. Select Agent mode
9. Click Tools button to see available MCP tools
10. Tools are invoked automatically or via `#toolname`

### Useful Commands
- `MCP: Browse Servers` - View curated MCP servers
- `MCP: List Servers` - View installed servers
- `MCP: Show Installed Servers` - Manage servers
- `MCP: Reset Cached Tools` - Clear tool cache
- `MCP: Browse Resources` - View MCP resources
- `MCP: Reset Trust` - Reset server trust settings

---

## 5. Goose

### Configuration Location
Goose config directory (typically `~/.config/goose/`)

### Configuration Format
Create `mcp-servers.json` or add to Goose configuration:

```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "node",
      "args": ["/path/to/your/server/index.js"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### Installation Methods

**Via CLI:**
```bash
goose extension add /path/to/your/server
```

**Via Extensions Directory:**
1. Place server configuration in `~/.config/goose/extensions/`
2. Restart Goose

**Via UI:**
1. Open Goose
2. Navigate to Extensions/Plugins
3. Add new MCP server
4. Enter configuration details

### Key Features
- MCP functionality exposed through tools
- Direct installation via extensions directory, CLI, or UI
- Built-in tools for development, web scraping, automation
- Support for multiple LLM providers

### Steps
1. Install Goose from https://github.com/block/goose
2. Configure your preferred LLM provider
3. Add your MCP server using one of the installation methods above
4. Restart Goose
5. Tools are available in Goose sessions

---

## 6. LM Studio

### Configuration Location
Access via: `Program tab → Install → Edit mcp.json`

### Configuration Format

**stdio (Local):**
```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "node",
      "args": ["/path/to/your/server/index.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

**Remote (HTTP/SSE):**
```json
{
  "mcpServers": {
    "remote-server": {
      "url": "https://your-server.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

### Installation via "Add to LM Studio" Button
Some MCP servers provide a deeplink button for automatic installation:
1. Click "Add to LM Studio" button on server's page
2. LM Studio opens automatically
3. Confirm the installation
4. Server is added to your configuration

### Important Notes
- **Security**: Only install MCP servers from trusted sources
- **Token Usage**: Some servers designed for Claude/ChatGPT may use excessive tokens
- **Manual Installation**: When adding manually, copy only the content inside `"mcpServers": { ... }`

### Steps
1. Open LM Studio (version 0.3.17+)
2. Navigate to Program tab in right sidebar
3. Click Install → Edit mcp.json
4. Add your server configuration
5. Save the file
6. Restart LM Studio if needed
7. MCP tools are available in chat

---

## 7. Gemini CLI

### Status
Gemini CLI is a newly released open-source AI agent for terminal use. MCP support is being actively developed.

### Expected Configuration
Once MCP support is fully implemented, configuration will likely follow similar patterns:

**Anticipated Format:**
```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "node",
      "args": ["/path/to/your/server/index.js"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### Installation
```bash
# Install Gemini CLI
npm install -g @google/gemini-cli

# Or via GitHub
git clone https://github.com/google-gemini/gemini-cli
cd gemini-cli
npm install
npm link
```

### Current Capabilities
- Direct Gemini access in terminal
- Reason and act (ReAct) framework
- Command execution capabilities
- File system operations

### Future MCP Integration
Monitor the official repository for MCP updates:
- GitHub: https://github.com/google-gemini/gemini-cli
- Documentation: https://cloud.google.com/gemini/docs/codeassist/gemini-cli

---

## Troubleshooting

### Common Issues

#### Server Not Starting
**Problem**: MCP server fails to start  
**Solutions**:
1. Check command path is correct
2. Verify all dependencies are installed
3. Check server logs for errors
4. Ensure environment variables are set correctly
5. Try running the command manually in terminal

#### Tools Not Appearing
**Problem**: MCP tools don't show up in client  
**Solutions**:
1. Restart the client application
2. Verify server configuration syntax
3. Check server is running (look for process)
4. Clear tool cache if available
5. Review client logs for connection errors

#### Permission Errors
**Problem**: Permission denied when starting server  
**Solutions**:
1. Check file permissions: `chmod +x /path/to/server`
2. Verify user has access to required directories
3. Run with appropriate permissions if needed

#### Environment Variables Not Working
**Problem**: Server can't access environment variables  
**Solutions**:
1. Use `envFile` to load from `.env` file
2. Check variable names match exactly
3. Verify file path is absolute or uses workspace variables
4. For VS Code, use input variables with `${input:var-name}`

#### Remote Server Connection Issues
**Problem**: Can't connect to remote MCP server  
**Solutions**:
1. Verify URL is correct and accessible
2. Check authentication headers
3. Ensure server supports SSE or HTTP transport
4. Check firewall/network settings
5. Verify SSL certificates if using HTTPS

### Debug Tips

#### Enable Verbose Logging
Most clients support verbose logging:
- **VS Code**: Check Output panel → MCP
- **Cursor**: Check server logs in settings
- **Continue.dev**: Check `.continue/logs/`
- **LM Studio**: Check console output

#### Test Server Manually
Run your server directly in terminal:
```bash
# Node.js server
node /path/to/server/index.js

# Python server
python -m your_server_module

# NPX package
npx -y your-package-name
```

#### Validate JSON Configuration
Use a JSON validator to ensure configuration files are properly formatted:
```bash
# Using jq
cat mcp.json | jq empty

# Using Python
python -m json.tool mcp.json
```

---

## Auto-Integration Script

To help users automatically configure your MCP server, you can provide a setup script:

### Example Setup Script (Node.js)

```javascript
#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const CLIENTS = {
  claude: {
    darwin: '~/Library/Application Support/Claude/claude_desktop_config.json',
    win32: '%APPDATA%\\Claude\\claude_desktop_config.json',
    linux: '~/.config/Claude/claude_desktop_config.json'
  },
  cursor: {
    global: '~/.cursor/mcp.json'
  },
  vscode: {
    command: 'MCP: Add Server'
  },
  lmstudio: {
    note: 'Open LM Studio → Program → Install → Edit mcp.json'
  }
};

function getConfigPath(client) {
  const platform = os.platform();
  const home = os.homedir();
  
  if (client === 'claude') {
    let configPath = CLIENTS.claude[platform];
    return configPath.replace('~', home).replace('%APPDATA%', process.env.APPDATA);
  }
  
  if (client === 'cursor') {
    return CLIENTS.cursor.global.replace('~', home);
  }
  
  return null;
}

function addServerConfig(client, serverConfig) {
  const configPath = getConfigPath(client);
  
  if (!configPath) {
    console.log(`Please manually configure ${client}`);
    return;
  }
  
  try {
    let config = {};
    if (fs.existsSync(configPath)) {
      config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
    
    config.mcpServers = config.mcpServers || {};
    config.mcpServers['your-server-name'] = serverConfig;
    
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(`✓ Configured ${client} at ${configPath}`);
  } catch (error) {
    console.error(`✗ Failed to configure ${client}:`, error.message);
  }
}

// Usage
const serverConfig = {
  command: 'node',
  args: ['/path/to/your/server/index.js']
};

console.log('🚀 Setting up MCP server integration...\n');

addServerConfig('claude', serverConfig);
addServerConfig('cursor', serverConfig);

console.log('\n📝 Manual setup required for:');
console.log('- VS Code: Run "MCP: Add Server" command');
console.log('- Continue.dev: Create .continue/mcpServers/your-server.yaml');
console.log('- LM Studio: Open Program → Install → Edit mcp.json');
console.log('- Goose: Run "goose extension add /path/to/server"');
```

### Example Setup Script (Python)

```python
#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

CLIENTS = {
    'claude': {
        'darwin': '~/Library/Application Support/Claude/claude_desktop_config.json',
        'win32': '%APPDATA%/Claude/claude_desktop_config.json',
        'linux': '~/.config/Claude/claude_desktop_config.json'
    },
    'cursor': {
        'global': '~/.cursor/mcp.json'
    }
}

def get_config_path(client):
    platform = sys.platform
    home = str(Path.home())
    
    if client == 'claude':
        config_path = CLIENTS['claude'].get(platform, CLIENTS['claude']['linux'])
        return config_path.replace('~', home).replace('%APPDATA%', os.getenv('APPDATA', ''))
    
    if client == 'cursor':
        return CLIENTS['cursor']['global'].replace('~', home)
    
    return None

def add_server_config(client, server_config):
    config_path = get_config_path(client)
    
    if not config_path:
        print(f'Please manually configure {client}')
        return
    
    try:
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        config = {}
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
        
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
        config['mcpServers']['your-server-name'] = server_config
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f'✓ Configured {client} at {config_path}')
    except Exception as e:
        print(f'✗ Failed to configure {client}: {str(e)}')

# Usage
server_config = {
    'command': 'python',
    'args': ['-m', 'your_server_module']
}

print('🚀 Setting up MCP server integration...\n')

add_server_config('claude', server_config)
add_server_config('cursor', server_config)

print('\n📝 Manual setup required for:')
print('- VS Code: Run "MCP: Add Server" command')
print('- Continue.dev: Create .continue/mcpServers/your-server.yaml')
print('- LM Studio: Open Program → Install → Edit mcp.json')
print('- Goose: Run "goose extension add /path/to/server"')
```

---

## Best Practices

1. **Use Absolute Paths**: Always use absolute paths for command executables and scripts
2. **Environment Variables**: Store sensitive data in environment variables, never hardcode
3. **Test Locally First**: Test your server manually before configuring clients
4. **Document Requirements**: List all dependencies and prerequisites clearly
5. **Provide Examples**: Include working example configurations for each client
6. **Version Compatibility**: Specify minimum client versions required
7. **Security**: Warn users about security implications of MCP servers
8. **Error Handling**: Implement proper error handling and logging in your server
9. **Input Variables**: Use input variables for sensitive data in VS Code
10. **Server Naming**: Use descriptive, unique names following camelCase convention

---

## Additional Resources

- **MCP Specification**: https://modelcontextprotocol.io/
- **MCP GitHub**: https://github.com/modelcontextprotocol
- **MCP Servers Repository**: https://github.com/modelcontextprotocol/servers
- **VS Code MCP Documentation**: https://code.visualstudio.com/docs/copilot/customization/mcp-servers
- **Continue.dev MCP Guide**: https://docs.continue.dev/customize/deep-dives/mcp
- **Cursor MCP Documentation**: https://docs.cursor.com/context/model-context-protocol
- **Goose Documentation**: https://block.github.io/goose/

---

## License

Include information about your MCP server's license here.

## Support

Provide support channels for users (GitHub issues, Discord, email, etc.)