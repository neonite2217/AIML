# MCP Framework Collection

A comprehensive collection of Model Context Protocol (MCP) servers and integrations showcasing different deployment patterns, technologies, and use cases.

## 🚀 Projects Overview

### 1. [AI-HR Assistant](./AI-HR/) - **PostgreSQL + Gmail + Obsidian Integration**
**Technologies:** PostgreSQL MCP, Gmail MCP, Obsidian MCP, Claude Desktop  
**Type:** Multi-server orchestration  
**Deployment:** Local MCP servers with Docker Desktop  

An intelligent HR automation system demonstrating MCP server orchestration for late arrival management.

**Key Features:**
- Automated late employee detection from PostgreSQL
- Email notifications via Gmail MCP
- Knowledge base documentation in Obsidian
- Complete workflow automation

---

### 2. [ClaudeOPS](./ClaudeOPS/) - **System Administration & DevOps**
**Technologies:** Python, Docker, FastMCP, System Commands  
**Type:** Local MCP server  
**Deployment:** Docker container with stdio transport  

Transform Claude into your personal system administrator with secure command execution.

**Key Features:**
- Containerized command execution
- Multi-OS package management (apt, brew, yum, dnf)
- Git operations and project management
- File system operations with security controls
- System monitoring and performance tracking

---

### 3. [Remote Railway Server](./remote%20railway%20server/) - **Knowledge Base Server**
**Technologies:** TypeScript, SQLite, Express, Railway/Sevalla  
**Type:** Remote MCP server  
**Deployment:** Cloud-hosted with REST API + MCP protocol  

Production-ready knowledge management server with persistent storage.

**Key Features:**
- SQLite database with full-text search
- REST API for web/mobile integrations
- Context management for grouped knowledge
- Auto-scaling cloud deployment
- Secure API key authentication

---

### 4. [Claude News](./Claude%20news/) - **Multi-Protocol Info Suite**
**Technologies:** CoinGecko SSE, OpenWeather API, Local Python servers  
**Type:** Mixed local/remote servers  
**Deployment:** SSE remote + stdio local  

Information aggregation system combining remote and local MCP servers.

**Key Features:**
- Real-time crypto prices via CoinGecko SSE
- Weather data with OpenWeather API
- News aggregation with local servers
- Mixed transport protocols demonstration

---

## 🏗️ Architecture Patterns Demonstrated

### 1. **Multi-Server Orchestration** (AI-HR)
```
Claude Desktop → PostgreSQL MCP → Gmail MCP → Obsidian MCP
```
Shows how to coordinate multiple existing MCP servers for complex workflows.

### 2. **Containerized Local Server** (ClaudeOPS)
```
Claude Desktop → Docker Container → System Commands
```
Demonstrates secure local command execution with Docker isolation.

### 3. **Cloud-Hosted Remote Server** (Railway Server)
```
Claude Desktop → HTTPS → Railway/Sevalla → SQLite
```
Production deployment pattern with persistent storage and REST API.

### 4. **Hybrid Local/Remote** (Claude News)
```
Claude Desktop → SSE Remote + stdio Local → Multiple APIs
```
Mixed transport protocols for different data sources.

---

## 🛠️ Technologies Used

| Technology | Projects | Purpose |
|------------|----------|---------|
| **Docker** | ClaudeOPS, AI-HR | Containerization & isolation |
| **PostgreSQL** | AI-HR | Relational database |
| **SQLite** | Railway Server | Lightweight persistent storage |
| **TypeScript** | Railway Server | Type-safe server development |
| **Python** | ClaudeOPS | System administration tools |
| **FastMCP** | ClaudeOPS | Python MCP framework |
| **Express.js** | Railway Server | REST API server |
| **SSE** | Claude News | Server-sent events transport |
| **Railway/Sevalla** | Railway Server | Cloud deployment platform |

---

## 🚀 Quick Start Guide

### Prerequisites
- Docker Desktop with MCP Toolkit enabled
- Claude Desktop application
- Node.js 20+ (for TypeScript projects)
- Python 3.8+ (for Python projects)

### 1. Choose Your Project

**For HR/Business Automation:**
```bash
cd "AI-HR"
# Follow setup guide for PostgreSQL + Gmail + Obsidian integration
```

**For System Administration:**
```bash
cd "ClaudeOPS"
# Run the installer script for containerized system tools
```

**For Knowledge Management:**
```bash
cd "remote railway server"
# Deploy to Railway/Sevalla for persistent knowledge base
```

**For Information Aggregation:**
```bash
cd "Claude news"
# Set up mixed local/remote servers for news and data
```

### 2. Installation Patterns

**Docker-based (ClaudeOPS, AI-HR):**
```bash
# Build and configure Docker containers
docker build -t project-name .
# Update Claude Desktop config
```

**Cloud Deployment (Railway Server):**
```bash
# Deploy to cloud platform
npm run build
railway deploy  # or sevalla deploy
```

**Local Servers (Claude News):**
```bash
# Install dependencies and run locally
pip install -r requirements.txt
python server.py
```

---

## 📚 Documentation Structure

Each project includes:

- **README.md** - Project overview and quick start
- **setup-guide.md** - Detailed installation instructions
- **demo-data/** - Sample data and configurations
- **docs/** - Additional documentation
- **examples/** - Usage examples and workflows

---

## 🔧 Configuration Examples

### Claude Desktop Config
```json
{
  "mcpServers": {
    "ai-hr": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "ai-hr-mcp"]
    },
    "claude-ops": {
      "command": "docker", 
      "args": ["run", "-i", "--rm", "claude-ops-mcp"]
    },
    "knowledge-base": {
      "command": "node",
      "args": ["/path/to/railway-server/dist/index.js"]
    }
  }
}
```

### Docker Compose (Multi-Server)
```yaml
version: '3.8'
services:
  ai-hr:
    build: ./AI-HR
    environment:
      - POSTGRES_URL=postgresql://user:pass@db:5432/hr
  
  claude-ops:
    build: ./ClaudeOPS
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
  
  knowledge-base:
    build: ./remote railway server
    ports:
      - "3000:3000"
```

---

## 🎯 Use Cases by Project

### AI-HR Assistant
- Employee attendance tracking
- Automated HR notifications
- Policy compliance monitoring
- Knowledge base management

### ClaudeOPS
- Development environment setup
- System maintenance automation
- Package management across OS
- Git workflow automation
- Performance monitoring

### Railway Server
- Personal knowledge management
- Team documentation
- Research organization
- Note-taking with AI integration

### Claude News
- Market data monitoring
- News aggregation
- Weather tracking
- Multi-source information feeds

---

## 🔐 Security Considerations

### Command Execution (ClaudeOPS)
- Containerized execution environment
- Command whitelisting
- Path restrictions
- Dangerous operation confirmations

### API Security (Railway Server)
- API key authentication
- Input validation with Zod
- Rate limiting ready
- HTTPS-only in production

### Data Privacy (AI-HR)
- Local database storage
- Encrypted email credentials
- Audit logging
- Access controls

---

## 🚧 Future Enhancements

### Planned Features
- [ ] Web UI for server management
- [ ] Multi-tenant support
- [ ] Vector search integration
- [ ] Real-time collaboration
- [ ] Mobile app support
- [ ] Analytics dashboard
- [ ] Webhook integrations
- [ ] GraphQL APIs

### Integration Roadmap
- [ ] Slack MCP integration
- [ ] Notion API connector
- [ ] GitHub Actions workflows
- [ ] Kubernetes deployment
- [ ] Monitoring & alerting
- [ ] Backup automation

---

## 🤝 Contributing

Contributions welcome! Each project has its own contribution guidelines:

1. **Fork** the repository
2. **Choose** a project to contribute to
3. **Follow** the project's specific setup guide
4. **Create** a feature branch
5. **Submit** a pull request with clear description

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-framework
cd mcp-framework

# Choose a project
cd "project-name"

# Follow project-specific setup
# See individual README files
```

---

## 📄 License

MIT License - See individual project LICENSE files for details.

---

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com) for MCP specification
- [Docker](https://docker.com) for containerization platform
- [Railway](https://railway.app) / [Sevalla](https://sevalla.com) for cloud hosting
- MCP community for tools and integrations

---

**Made with ❤️ for the MCP community**

*This collection demonstrates various MCP patterns from simple local servers to complex multi-server orchestrations and cloud deployments.*