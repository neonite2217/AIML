# AI HR Assistant with MCP Servers

An intelligent HR automation system that demonstrates the power of integrating multiple MCP (Model Context Protocol) servers with Claude Desktop. This project automates late arrival management through seamless integration of database queries, email notifications, and knowledge management. Demonstrating multi-server MCP orchestration with Claude Desktop, this project showcases how to integrate multiple existing MCP servers to create powerful automated workflows.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![MCP](https://img.shields.io/badge/MCP-Multi--Server-orange)

## 🎯 Overview

This system automates late arrival management through seamless integration of database queries, email notifications, and knowledge management - all orchestrated through Claude Desktop's natural language interface.

## Note:
All the plugins are provided by Docker and come with the docker toolkit.
This system showcases how existing MCP servers can be orchestrated together to create powerful automation workflows. Rather than building MCP servers from scratch, this project focuses on **integration skills** and **workflow automation**.

### Architecture
```
PostgreSQL MCP → Claude Desktop → Gmail MCP → Obsidian MCP
     ↓              ↓              ↓           ↓
Employee Data → AI Orchestration → Notifications → Documentation
```

### Core Workflow
1. **🔍 Detect** late employees from PostgreSQL attendance records
2. **📧 Notify** employees via automated Gmail messages  
3. **💬 Process** responses and manage follow-ups
4. **📝 Document** outcomes in Obsidian knowledge base

### MCP Server Stack
- **PostgreSQL MCP** - Employee and attendance data management
- **Gmail MCP** - Automated email notifications and response handling
- **Obsidian MCP** - Knowledge base for tracking explanations and decisions
- **Claude Desktop** - Natural language orchestration layer

## 🚀 Quick Start

### Prerequisites
- macOS with Homebrew (or Linux with package manager)
- Docker Desktop with MCP Toolkit enabled
- Claude Desktop application
- Gmail account with app-specific password
- Obsidian vault (optional but recommended)

### 1. Database Setup

**Install PostgreSQL:**
```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Verify installation
psql --version
```

**Create Demo Database:**
```bash
# Create demo user
psql postgres -c "CREATE USER hradmin WITH PASSWORD 'hrpass';"
psql postgres -c "ALTER USER hradmin CREATEDB;"

# Connect and create database
psql postgres -U hradmin
```

```sql
-- Create the main database
CREATE DATABASE companydb;
\c companydb

-- Create employees table
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  department TEXT NOT NULL
);

-- Create attendance tracking table
CREATE TABLE attendance (
  id SERIAL PRIMARY KEY,
  employee_id INT REFERENCES employees(id),
  date DATE NOT NULL,
  status TEXT CHECK (status IN ('present', 'late', 'absent'))
);
```

### 2. Load Demo Data

**Insert Sample Employees:**
```sql
INSERT INTO employees (name, email, department) VALUES
('Alice Johnson','alice.johnson@neo.corp','HR'),
('Bob Smith','bob.smith@neo.corp','Finance'),
('Charlie Patel','charlie.patel@neo.corp','IT'),
('Diana Gupta','diana.gupta@neo.corp','Sales'),
('Ethan Brown','ethan.brown@neo.corp','Marketing'),
('Farah Khan','farah.khan@neo.corp','Finance'),
('George Davis','george.davis@neo.corp','IT'),
('Hannah Li','hannah.li@neo.corp','HR'),
('Ian Wong','ian.wong@neo.corp','Operations'),
('Jasmine Mehta','jasmine.mehta@neo.corp','IT'),
-- ... (see demo-data/sample-employees.sql for full dataset)
('Anita Kumar','anita.kumar@neo.corp','HR'),
('William Adams','william.adams@neo.corp','Sales');

-- Add today's late arrivals for demo
INSERT INTO attendance (employee_id, date, status) VALUES
(2, CURRENT_DATE, 'late'),    -- Bob Smith
(5, CURRENT_DATE, 'late'),    -- Ethan Brown  
(11, CURRENT_DATE, 'late'),   -- Kevin Lee
(19, CURRENT_DATE, 'late'),   -- Samir Kapoor
(27, CURRENT_DATE, 'late');   -- Anita Kumar
```

### 3. Configure MCP Servers

**PostgreSQL MCP Configuration:**
```json
{
  "mcpServers": {
    "postgresql": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "DATABASE_URL=postgresql://hradmin:hrpass@host.docker.internal:5432/companydb",
        "mcp/postgresql"
      ]
    }
  }
}
```

**Gmail MCP Configuration:**
```json
{
  "mcpServers": {
    "gmail": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GMAIL_EMAIL=hr.demo@neo.corp",
        "-e", "GMAIL_APP_PASSWORD=your-16-char-app-password",
        "mcp/gmail"
      ]
    }
  }
}
```

**Obsidian MCP Configuration:**
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/path/to/obsidian/vault:/vault",
        "mcp/obsidian"
      ]
    }
  }
}
```

### 4. Complete Claude Desktop Config

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
```json
{
  "mcpServers": {
    "postgresql": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "DATABASE_URL=postgresql://hradmin:hrpass@host.docker.internal:5432/companydb",
        "mcp/postgresql"
      ]
    },
    "gmail": {
      "command": "docker", 
      "args": [
        "run", "-i", "--rm",
        "-e", "GMAIL_EMAIL=hr.demo@neo.corp",
        "-e", "GMAIL_APP_PASSWORD=your-app-password",
        "mcp/gmail"
      ]
    },
    "obsidian": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", 
        "-v", "/Users/yourusername/Documents/Obsidian Vault:/vault",
        "mcp/obsidian"
      ]
    }
  }
}
```

## 💻 Usage Examples

### Basic Queries

**Test Database Connection:**
```
"What's the name of employee with id 27?"
```
*Expected: Anita Kumar*

**Check Today's Late Arrivals:**
```
"Who was late today?"
```
*Expected: Bob Smith, Ethan Brown, Kevin Lee, Samir Kapoor, Anita Kumar*

### Automated Workflows

**Send Late Arrival Notifications:**
```
"Email all employees who were late today asking for explanations"
```

**Process Email Responses:**
```
"Check for replies to the late arrival emails and save explanations to Obsidian"
```

**Complete Workflow:**
```
"Run the complete late arrival workflow: 
1. Find who was late today
2. Email them for explanations  
3. Process any replies
4. Document everything in Obsidian"
```

### Advanced Operations

**Department Analysis:**
```
"Show me late arrival patterns by department for the last month"
```

**Follow-up Management:**
```
"Create follow-up tasks in Obsidian for employees who haven't responded to late arrival emails"
```

**Reporting:**
```
"Generate a weekly attendance report and save it to Obsidian"
```

## 📊 Demo Workflow

### Step 1: Detection
**Query Executed:**
```sql
SELECT e.name, e.email, a.date
FROM employees e
JOIN attendance a ON e.id = a.employee_id
WHERE a.status='late' AND a.date = CURRENT_DATE;
```

### Step 2: Notification
**Email Template:**
```
To: anita.kumar@neo.corp, bob.smith@neo.corp, ...
Subject: Late Arrival Notice - [Date]

Hi [Name],

We noticed you arrived late today. Please reply with the reason 
for documentation purposes.

Best regards,
HR Team
```

### Step 3: Response Processing
- **With explanation**: Saved to Obsidian under employee's record
- **No response**: Flagged for follow-up action

### Step 4: Documentation
**Obsidian Entry Format:**
```markdown
# Employee: Anita Kumar (ID: 27)
## Attendance Notes

- [2025-01-04] Late arrival - Traffic due to road construction
- [2025-01-03] On time
- [2025-01-02] On time

## Follow-up Actions
- [ ] Schedule meeting if pattern continues
- [ ] Update flexible work policy discussion
```

## 🗂️ Project Structure

```
AI-HR/
├── README.md                    # This file
├── docs/
│   ├── setup-guide.md          # Detailed setup instructions
│   ├── workflow-examples.md    # Demo workflows and use cases
│   └── troubleshooting.md      # Common issues and solutions
├── demo-data/
│   ├── schema.sql              # Database schema
│   ├── sample-employees.sql    # 50 demo employees
│   ├── sample-attendance.sql   # Demo attendance data
│   └── demo-queries.sql        # Example queries for testing
├── examples/
│   ├── email-templates/        # Email notification templates
│   ├── obsidian-templates/     # Obsidian note templates
│   └── workflow-scripts/       # Automation examples
└── config/
    ├── claude-desktop-config.json  # Complete Claude config
    ├── docker-compose.yml          # Multi-server setup
    └── environment-template.env    # Environment variables
```

## 🔧 Configuration Details

### PostgreSQL Connection
**Local Development:**
```
postgresql://hradmin:hrpass@localhost:5432/companydb
```

**Docker Desktop:**
```
postgresql://hradmin:hrpass@host.docker.internal:5432/companydb
```

### Gmail Setup
1. Enable 2-factor authentication
2. Generate app-specific password
3. Use format: `xxxx xxxx xxxx xxxx` (16 characters)

### Obsidian Integration
- Point to existing vault or create new one
- Templates automatically created in `Templates/` folder
- Employee notes stored in `HR/Employees/` folder

## 🛠️ Troubleshooting

### Database Connection Issues
```bash
# Test direct connection
psql -d companydb -U hradmin -h localhost

# Check if PostgreSQL is running
brew services list | grep postgresql
# or
sudo systemctl status postgresql
```

### Gmail Authentication Errors
- Verify 2FA is enabled
- Use app-specific password, not regular password
- Check IMAP/SMTP access is enabled in Gmail settings

### Docker Issues
```bash
# Check Docker is running
docker info

# Test MCP server containers
docker run --rm mcp/postgresql --help
docker run --rm mcp/gmail --help
docker run --rm mcp/obsidian --help
```

### Claude Desktop Not Showing Tools
1. Restart Claude Desktop completely
2. Check JSON syntax in config file
3. Verify all paths are absolute
4. Check Docker containers can start

## 📈 What This Demonstrates

### Integration Skills
- **Multi-server coordination** - Orchestrating 3 different MCP servers
- **Workflow automation** - Converting manual HR processes to AI-driven workflows
- **Error handling** - Graceful management of failed operations across services

### Best Practices
- **Configuration management** - Environment variables and secure credential storage
- **Documentation** - Clear setup instructions and troubleshooting guides
- **Testing** - Sample data and validation queries
- **Security** - Proper credential handling and access controls


## 📄 License

MIT License - See [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- **PostgreSQL MCP** - Database integration
- **Gmail MCP** - Email automation
- **Obsidian MCP** - Knowledge management
- **Docker MCP Toolkit** - Containerization platform
- **Claude Desktop** - AI orchestration interface

---

*This project demonstrates beginner-friendly MCP server orchestration using existing tools rather than building custom servers. Perfect for learning MCP integration patterns and workflow automation.*
