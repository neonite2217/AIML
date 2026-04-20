# AI-HR Assistant Workflow Examples

This document provides practical examples of how to use the AI-HR Assistant system for common HR tasks and workflows.

## 🚀 Basic Workflows

### 1. Daily Late Arrival Check

**Prompt:**
```
"Check who was late today and show me their details"
```

**Expected Output:**
```
Today's Late Arrivals (5 employees):

1. Bob Smith (Finance)
   Email: bob.smith@neo.corp
   
2. Ethan Brown (Marketing)
   Email: ethan.brown@neo.corp
   
3. Kevin Lee (Finance)
   Email: kevin.lee@neo.corp
   
4. Samir Kapoor (HR)
   Email: samir.kapoor@neo.corp
   
5. Anita Kumar (HR)
   Email: anita.kumar@neo.corp
```

### 2. Send Late Arrival Notifications

**Prompt:**
```
"Send email notifications to all employees who were late today asking for explanations"
```

**Expected Actions:**
1. Query database for late employees
2. Generate personalized emails
3. Send via Gmail MCP
4. Log notifications in system

**Sample Email Generated:**
```
To: bob.smith@neo.corp
Subject: Late Arrival Notice - January 4, 2025

Hi Bob Smith,

We noticed you arrived late today (January 4, 2025). Please reply to this email with the reason for your late arrival for our records.

This information helps us understand attendance patterns and provide appropriate support when needed.

Best regards,
HR Team
Neo Corp
```

### 3. Process Email Responses

**Prompt:**
```
"Check for replies to late arrival emails and save the explanations to Obsidian"
```

**Expected Actions:**
1. Check Gmail for replies
2. Extract employee explanations
3. Create/update Obsidian notes
4. Mark notifications as processed

**Sample Obsidian Note:**
```markdown
# Employee: Bob Smith (ID: 2)
## Department: Finance
## Contact: bob.smith@neo.corp

### Attendance History
- **2025-01-04**: Late arrival
  - **Reason**: Traffic jam due to accident on Highway 101
  - **Response received**: 2025-01-04 10:30 AM
  - **Follow-up needed**: No

- **2025-01-03**: Present
- **2025-01-02**: Present

### Notes
- Generally punctual employee
- Traffic-related delays are occasional
- No pattern of chronic lateness
```

## 🔄 Advanced Workflows

### 4. Complete Late Arrival Management

**Prompt:**
```
"Run the complete late arrival workflow: detect, notify, process responses, and document everything"
```

**Workflow Steps:**
1. **Detection Phase**
   - Query PostgreSQL for today's late arrivals
   - Identify employees and their details
   - Check for repeat offenders

2. **Notification Phase**
   - Generate personalized email notifications
   - Send emails via Gmail MCP
   - Log notification attempts

3. **Response Processing Phase**
   - Monitor Gmail for replies
   - Extract and categorize explanations
   - Identify employees who haven't responded

4. **Documentation Phase**
   - Create/update Obsidian employee records
   - Log explanations and follow-up actions
   - Generate summary reports

### 5. Weekly Attendance Analysis

**Prompt:**
```
"Analyze attendance patterns for the past week and create a summary report in Obsidian"
```

**Analysis Includes:**
- Department-wise attendance rates
- Repeat late arrivals
- Absence patterns
- Recommendations for follow-up

**Sample Report:**
```markdown
# Weekly Attendance Report
## Week of January 1-7, 2025

### Summary Statistics
- Total Employees: 50
- Average Attendance Rate: 94.2%
- Late Arrivals: 12 incidents
- Absences: 8 incidents

### Department Breakdown
| Department | Attendance Rate | Late Arrivals | Absences |
|------------|----------------|---------------|----------|
| IT         | 96.7%          | 2             | 1        |
| Finance    | 93.8%          | 4             | 2        |
| HR         | 95.2%          | 2             | 1        |
| Sales      | 92.5%          | 3             | 2        |
| Marketing  | 94.1%          | 1             | 2        |

### Action Items
- Follow up with Kevin Lee (Finance) - 3 late arrivals this week
- Schedule meeting with Sales team regarding attendance
- Review flexible work policies for Marketing department
```

### 6. Employee Follow-up Management

**Prompt:**
```
"Identify employees who haven't responded to late arrival emails and create follow-up tasks"
```

**Follow-up Actions:**
1. Check notification status
2. Identify non-responders
3. Create escalation tasks
4. Schedule manager notifications

## 📊 Reporting Workflows

### 7. Monthly Attendance Dashboard

**Prompt:**
```
"Create a comprehensive monthly attendance dashboard with trends and insights"
```

**Dashboard Components:**
- Overall attendance trends
- Department comparisons
- Individual employee patterns
- Seasonal variations
- Recommendations

### 8. Performance Review Integration

**Prompt:**
```
"Prepare attendance data for performance reviews for employees in the IT department"
```

**Output Format:**
```markdown
# IT Department - Attendance Summary for Performance Reviews

## Charlie Patel (ID: 3)
- Attendance Rate: 98.5%
- Late Arrivals: 1 (traffic-related)
- Absences: 0
- Overall: Excellent attendance record

## George Davis (ID: 7)
- Attendance Rate: 96.2%
- Late Arrivals: 2 (both medical appointments)
- Absences: 1 (sick leave)
- Overall: Good attendance, medical reasons documented

[Continue for all IT employees...]
```

## 🔧 Troubleshooting Workflows

### 9. System Health Check

**Prompt:**
```
"Perform a system health check on all MCP servers and database connections"
```

**Health Check Items:**
- PostgreSQL connection status
- Gmail MCP functionality
- Obsidian vault accessibility
- Recent data synchronization
- Error log review

### 10. Data Validation

**Prompt:**
```
"Validate attendance data integrity and check for any inconsistencies"
```

**Validation Checks:**
- Missing attendance records
- Duplicate entries
- Invalid status values
- Employee record consistency
- Date range validation

## 🎯 Specialized Use Cases

### 11. Holiday and Vacation Management

**Prompt:**
```
"Process vacation requests and update attendance records accordingly"
```

### 12. Sick Leave Tracking

**Prompt:**
```
"Track sick leave patterns and identify employees who may need wellness support"
```

### 13. Remote Work Coordination

**Prompt:**
```
"Coordinate remote work schedules and update attendance tracking accordingly"
```

### 14. Compliance Reporting

**Prompt:**
```
"Generate compliance reports for labor law requirements and audit purposes"
```

## 📝 Custom Workflow Templates

### Template 1: New Employee Onboarding

```
"Set up attendance tracking for new employee [Name] in [Department] starting [Date]"
```

### Template 2: Department Restructuring

```
"Update attendance records and reporting for employees moving from [Old Dept] to [New Dept]"
```

### Template 3: Policy Violation Investigation

```
"Investigate attendance policy violations for [Employee Name] and prepare documentation"
```

### Template 4: Seasonal Adjustment Analysis

```
"Analyze attendance patterns during [Season/Period] and recommend policy adjustments"
```

## 🔄 Automation Triggers

### Scheduled Workflows

**Daily (9:00 AM):**
```
"Run daily attendance check and send notifications for late arrivals"
```

**Weekly (Monday 8:00 AM):**
```
"Generate weekly attendance summary and identify trends"
```

**Monthly (1st of month):**
```
"Create monthly attendance dashboard and performance metrics"
```

### Event-Driven Workflows

**On Email Response:**
```
"Process new email responses and update employee records"
```

**On Policy Change:**
```
"Update all affected employee records and notification templates"
```

**On Manager Request:**
```
"Generate custom attendance report for specific employee or department"
```

## 💡 Best Practices

### 1. Prompt Structure
- Be specific about the desired outcome
- Include relevant time periods
- Specify output format when needed
- Use consistent terminology

### 2. Data Management
- Regular data validation checks
- Backup important records
- Maintain audit trails
- Document policy changes

### 3. Communication
- Use professional email templates
- Maintain consistent messaging
- Respect employee privacy
- Follow company policies

### 4. Follow-up
- Set clear timelines for responses
- Escalate appropriately
- Document all interactions
- Monitor resolution status

---

*These workflows demonstrate the power of MCP server orchestration for HR automation. Customize prompts and processes to match your organization's specific needs and policies.*