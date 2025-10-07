hi this is documentation for s project of mine and I want to segmentizse it but my README.md has it all kinda looks clumsy so I want to clear the clutter
ai-hr-assistant/
├── README.md                  # Overview + demo + repo structure
├── docs/
│   ├── setup-guide.md         # Step-by-step installation and Postgres setup
│   ├── workflow-examples.md   # Demo workflows: late detection, replies, paycuts
│   └── troubleshooting.md     # Common issues + fixes
├── database/
│   ├── schema.sql             # Tables creation
│   ├── sample-data.sql        # 50 employees + attendance
│   └── queries.sql            # Demo queries for Client
└── examples/
   #  queries for client  # Full demo scenarios: multiple late employees

# AI HR Assistant with MCP Servers

An intelligent HR automation system that demonstrates the power of integrating multiple MCP (Model Context Protocol) servers with Claude Desktop. This project automates late arrival management through seamless integration of database queries, email notifications, and knowledge management.

## 🎯 Project Overview

This system showcases how existing MCP servers can be orchestrated together to create powerful automation workflows. Rather than building MCP servers from scratch, this project focuses on **integration skills** and **workflow automation**.

### Core Workflow
1. **Detect** late employees from PostgreSQL attendance records
2. **Notify** employees via automated Gmail messages
3. **Process** responses and manage follow-ups
4. **Document** outcomes in Obsidian knowledge base

## 🏗️ Architecture

### MCP Server Stack
- **PostgreSQL MCP** → Employee and attendance data management
- **Gmail MCP** → Automated email notifications and response handling  
- **Obsidian MCP** → Knowledge base for tracking explanations and decisions
- **Claude Desktop** → Natural language orchestration layer

### Data Flow
```
PostgreSQL → Claude → Gmail → Employee Response → Claude → Obsidian
```

## 🚀 Quick Start

### Prerequisites
- macOS with Homebrew installed
- Docker Desktop with MCP support
- Claude Desktop application
- Gmail account with app-specific password

### 1. Database Setup

Install and start PostgreSQL:
```bash
brew install postgresql@15
brew services start postgresql@15
```

Verify installation:
```bash
psql --version
# Should show: psql (PostgreSQL) 15.14 (Homebrew)
```

### 2. Create Database Schema

Connect to PostgreSQL with demo credentials:
```bash
# First, create the demo user (if it doesn't exist)
psql postgres -c "CREATE USER hradmin WITH PASSWORD 'hrpass';"
psql postgres -c "ALTER USER hradmin CREATEDB;"

# Connect as the demo user
psql postgres -U hradmin
```

Set up the company database:
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

### 3. Populate Sample Data

Insert the demo dataset (50 employees):
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
('Kevin Lee','kevin.lee@neo.corp','Finance'),
('Laura Miller','laura.miller@neo.corp','Sales'),
('Michael Thomas','michael.thomas@neo.corp','Marketing'),
('Nina Shah','nina.shah@neo.corp','Operations'),
('Omar Ali','omar.ali@neo.corp','IT'),
('Priya Nair','priya.nair@neo.corp','Finance'),
('Quentin White','quentin.white@neo.corp','Sales'),
('Riya Desai','riya.desai@neo.corp','Marketing'),
('Samir Kapoor','samir.kapoor@neo.corp','HR'),
('Tina Roy','tina.roy@neo.corp','Finance'),
('Uma Verma','uma.verma@neo.corp','IT'),
('Victor Chen','victor.chen@neo.corp','Sales'),
('Wendy Zhao','wendy.zhao@neo.corp','Marketing'),
('Xavier Brooks','xavier.brooks@neo.corp','Finance'),
('Yara Ibrahim','yara.ibrahim@neo.corp','Operations'),
('Zane Parker','zane.parker@neo.corp','IT'),
('Anita Kumar','anita.kumar@neo.corp','HR'),
('Brian Carter','brian.carter@neo.corp','Finance'),
('Chloe Wright','chloe.wright@neo.corp','IT'),
('Dev Patel','dev.patel@neo.corp','Sales'),
('Elena Rossi','elena.rossi@neo.corp','Marketing'),
('Faisal Ahmed','faisal.ahmed@neo.corp','Operations'),
('Grace Turner','grace.turner@neo.corp','HR'),
('Henry Lopez','henry.lopez@neo.corp','Finance'),
('Isla Fernandez','isla.fernandez@neo.corp','IT'),
('Jack Murphy','jack.murphy@neo.corp','Sales'),
('Kiran Das','kiran.das@neo.corp','Marketing'),
('Liam Scott','liam.scott@neo.corp','Operations'),
('Maya Singh','maya.singh@neo.corp','Finance'),
('Noah Kim','noah.kim@neo.corp','IT'),
('Olivia Moore','olivia.moore@neo.corp','HR'),
('Peter Zhang','peter.zhang@neo.corp','Sales'),
('Qadir Malik','qadir.malik@neo.corp','Finance'),
('Rachel Green','rachel.green@neo.corp','Marketing'),
('Sofia Torres','sofia.torres@neo.corp','Operations'),
('Thomas Hall','thomas.hall@neo.corp','IT'),
('Usha Menon','usha.menon@neo.corp','Finance'),
('Vikram Rao','vikram.rao@neo.corp','HR'),
('William Adams','william.adams@neo.corp','Sales');
```

Add sample attendance data with our demo late employees:
```sql
-- Mark some employees as late today (including our test case Anita Kumar - ID 27)
INSERT INTO attendance (employee_id, date, status) VALUES
(2, CURRENT_DATE, 'late'),    -- Bob Smith (our test employees)
(5, CURRENT_DATE, 'late'),    -- Ethan Brown  
(11, CURRENT_DATE, 'late'),   -- Kevin Lee
(19, CURRENT_DATE, 'late'),   -- Samir Kapoor
(27, CURRENT_DATE, 'late');   -- Anita Kumar 
```

**Verify your demo data:**
```sql
-- Check if employee 27 (Anita Kumar) is in the database
SELECT id, name, email FROM employees WHERE id = 27;

-- See today's late arrivals
SELECT e.id, e.name, e.email, a.status 
FROM employees e 
JOIN attendance a ON e.id = a.employee_id 
WHERE a.date = CURRENT_DATE AND a.status = 'late';
```

### 4. Configure MCP Servers

#### PostgreSQL MCP Configuration
Connection string format:
```
postgresql://username:password@host:port/database
```

**For this demo dataset, use:**
```
postgresql://hradmin:hrpass@localhost:5432/companydb
```

> **Note**: If using Docker Desktop's PostgreSQL MCP plugin, you may need to use `host.docker.internal` instead of `localhost`:
> ```
> postgresql://hradmin:hrpass@host.docker.internal:5432/companydb
> ```

**Troubleshooting Connection Issues:**
1. First ensure you can connect directly: `psql -d companydb -U hradmin`
2. If using Docker Desktop, restart the application after config changes
3. Verify the MCP plugin is enabled and running in Docker Desktop

#### Gmail MCP Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an app-specific password
3. Configure the Gmail MCP server with your credentials

**Demo Configuration Example:**
```json
{
  "email": "hr.demo@neo.corp",
  "app_password": "your-16-char-app-password"
}
```

#### Obsidian MCP Setup
1. Create or specify your Obsidian vault path
2. Configure the Obsidian MCP server to access your vault

## 📋 Usage Examples

### Basic Queries

**Test the MCP connection:**
```
"What's the name of employee with id 27?"
```
*Expected result: Anita Kumar*

**Check today's late arrivals:**
```
"Who was late today?"
```
*Expected result: Bob Smith, Ethan Brown, Kevin Lee, Samir Kapoor, Anita Kumar*

**Send notifications:**
```
"Email all employees who were late today asking for explanations"
```

**Process responses:**
```
"Check for replies to the late arrival emails and save them to Obsidian"
```

### Advanced Workflow
```
"Run the complete late arrival workflow: find who was late, email them, 
process any replies, and document everything in Obsidian"
```

## 🔄 Detailed Workflow

### Step 1: Detection
Query executed:
```sql
SELECT e.name, e.email, a.date
FROM employees e
JOIN attendance a ON e.id = a.employee_id
WHERE a.status='late' AND a.date = CURRENT_DATE;
```

### Step 2: Notification
Automated email template sent to late employees:
```
To: samir.kapoor@neo.corp, anita.kumar@neo.corp, ...
Subject: Late Arrival Notice - [Date]
Body: Hi [Name], we noticed you arrived late today. 
Please reply with the reason for documentation purposes.

Best regards,
HR Team
```

### Step 3: Response Processing
- **With explanation**: Saved to Obsidian under employee's record
- **No response**: Flagged for follow-up action

### Step 4: Documentation
Obsidian entries format:
```markdown
# Employee: Anita Kumar (ID: 27)
## Attendance Notes

- [2025-09-24] Late arrival - Traffic due to road construction on Highway 101
- [2025-09-23] On time
- [2025-09-22] On time

# Employee: Samir Kapoor (ID: 19)  
## Attendance Notes

- [2025-09-24] Late arrival - Medical appointment ran over
- [2025-09-23] On time
```

## 🎥 Demo

[Watch the complete workflow demonstration](your-demo-video-link)

## 📁 Project Structure

```
ai-hr-assistant/
├── README.md                  # Overview + demo + repo structure
├── docs/
│   ├── setup-guide.md         # Step-by-step installation and Postgres setup
│   ├── workflow-examples.md   # Demo workflows: late detection, replies, paycuts
│   └── troubleshooting.md     # Common issues + fixes
├── database/
│   ├── schema.sql             # Tables creation
│   ├── sample-data.sql        # 50 employees + attendance
│   └── queries.sql            # Demo queries for Client
└── examples/
   #  queries for client  # Full demo scenarios: multiple late employees
```

## 🛠️ Troubleshooting

### Common Issues

**PostgreSQL Connection Failed**
- Ensure PostgreSQL service is running: `brew services list`
- Test direct connection: `psql -d companydb -U hradmin` (password: `hrpass`)
- Verify database exists: `psql -d companydb -U hradmin -c "\l"`
- Check connection string: `postgresql://hradmin:hrpass@localhost:5432/companydb`
- For Docker Desktop: Try `postgresql://hradmin:hrpass@host.docker.internal:5432/companydb`

**Gmail Authentication**
- Use app-specific password, not regular password
- Ensure 2FA is enabled on Gmail account
- Verify IMAP/SMTP access is enabled

**Obsidian Access**
- Confirm vault path is correct
- Check file permissions
- Ensure Obsidian isn't blocking external access

## ✅ What This Project Demonstrates

- **Integration Skills**: Connecting multiple MCP servers seamlessly
- **Workflow Automation**: Converting manual processes into automated systems  
- **Error Handling**: Graceful management of failed operations
- **Documentation**: Clear, reproducible setup instructions
- **Best Practices**: Professional code organization and configuration management

## 🚧 Future Enhancements

- **Slack integration** for team notifications
- **Calendar MCP** for meeting conflict detection  
- **Analytics dashboard** for attendance patterns
- **Multi-language support** for global teams
- **Mobile notifications** via push services

## 📝 Contributing

This project welcomes contributions! Areas for improvement:
- Additional MCP server integrations
- Enhanced email templates
- Better error handling
- Performance optimizations
- Extended documentation

## 📄 License

MIT License - feel free to use this project as a foundation for your own MCP integrations.

---

*This project showcases beginner-friendly MCP server orchestration. No custom servers were built - this demonstrates configuration and integration skills using existing tools.*
