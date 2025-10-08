# MCP Knowledge Base Server - Complete Deployment Guide

## 🚀 Quick Start

This guide will help you deploy a production-ready MCP (Model Context Protocol) server on Sevalla that provides persistent knowledge management for Claude and other AI models.

## 📋 Prerequisites

- Node.js 20+ installed locally
- Git installed
- Sevalla account ([sign up here](https://sevalla.com))
- Basic knowledge of TypeScript/Node.js

## 🏗️ Project Structure

```
mcp-knowledge-server/
├── src/
│   └── index.ts          # Main server code
├── package.json
├── tsconfig.json
├── sevalla.yml           # Sevalla deployment config
├── .env.example          # Environment variables template
├── .gitignore
└── README.md
```

## 📦 Step 1: Set Up Project

```bash
# Create project directory
mkdir mcp-knowledge-server
cd mcp-knowledge-server

# Initialize npm
npm init -y

# Install dependencies
npm install @modelcontextprotocol/sdk better-sqlite3 express zod dotenv

# Install dev dependencies
npm install -D @types/node @types/express @types/better-sqlite3 typescript tsx

# Create source directory
mkdir src
```

## 📝 Step 2: Create Configuration Files

### package.json
```json
{
  "name": "mcp-knowledge-server",
  "version": "1.0.0",
  "description": "MCP server for personal knowledge management",
  "main": "dist/index.js",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "engines": {
    "node": ">=20.0.0"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "express": "^4.18.2",
    "better-sqlite3": "^9.2.2",
    "zod": "^3.22.4",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "@types/node": "^20.10.5",
    "@types/express": "^4.17.21",
    "@types/better-sqlite3": "^7.6.8",
    "typescript": "^5.3.3",
    "tsx": "^4.6.2"
  }
}
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "node",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "allowSyntheticDefaultImports": true,
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### .env.example
```bash
# Enable web API (set to 'true' for Sevalla deployment)
ENABLE_WEB_API=true

# Port for web API
PORT=3000

# Database path (use /app/data/knowledge.db for Sevalla persistent storage)
DATABASE_PATH=./knowledge.db

# API Key for authentication (generate a secure random string)
API_KEY=your-secret-api-key-here

# Node environment
NODE_ENV=production
```

### .gitignore
```
node_modules/
dist/
*.db
*.db-shm
*.db-wal
.env
.DS_Store
*.log
```

## ☁️ Step 3: Sevalla Configuration

Create `sevalla.yml`:

```yaml
name: mcp-knowledge-server
type: nodejs

build:
  node_version: "20"
  build_command: |
    npm ci --only=production
    npm run build

runtime:
  start_command: npm start

environment:
  ENABLE_WEB_API: "true"
  NODE_ENV: "production"
  DATABASE_PATH: "/app/data/knowledge.db"

ports:
  - port: 3000
    protocol: http

volumes:
  - name: knowledge-data
    mount_path: /app/data
    size: 1GB

health_check:
  http_path: /health
  interval: 30
  timeout: 10
  healthy_threshold: 2
  unhealthy_threshold: 3

resources:
  instances: 1
  memory: 512MB
  cpu: 0.5

auto_scaling:
  enabled: true
  min_instances: 1
  max_instances: 3
  target_cpu: 70
  target_memory: 80
```

## 🚀 Step 4: Deploy to Sevalla

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: MCP Knowledge Base Server"

# Install Sevalla CLI (if not already installed)
npm install -g @sevalla/cli

# Login to Sevalla
sevalla login

# Create a new application
sevalla apps create mcp-knowledge-server

# Link your repository
sevalla git:remote -a mcp-knowledge-server

# Set environment variables
sevalla config:set API_KEY=$(openssl rand -hex 32) -a mcp-knowledge-server

# Deploy
git push sevalla main
```

## 🔗 Step 5: Connect Claude Desktop

Once deployed, you'll get a URL like `https://mcp-knowledge-server-xyz.sevalla.app`

### Option A: MCP Protocol (Recommended)

**Note:** Direct MCP over HTTP is not yet standardized. For now, use the REST API or run the server locally with stdio.

### Option B: Local MCP Server

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or 
`%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "knowledge-base": {
      "command": "node",
      "args": ["/path/to/your/dist/index.js"],
      "env": {
        "DATABASE_PATH": "/path/to/knowledge.db"
      }
    }
  }
}
```

## 🧪 Testing Your Deployment

```bash
# Check health
curl https://your-app.sevalla.app/health

# Get stats (requires API key)
curl -H "x-api-key: YOUR_API_KEY" \
  https://your-app.sevalla.app/stats

# Search knowledge base
curl -X POST https://your-app.sevalla.app/search \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "deployment",
    "limit": 5
  }'
```

## 💡 Usage Examples

Once connected to Claude, you can:

### Add Knowledge
```
Add this to my knowledge base:
Category: devops
Title: Sevalla Environment Variables
Content: To set env vars in Sevalla: sevalla config:set KEY=value
Tags: sevalla, devops, configuration
```

### Search Knowledge
```
Search my knowledge base for "Docker deployment tips"
```

### Get Statistics
```
Show me statistics about my knowledge base
```

### List Categories
```
What categories do I have in my knowledge base?
```

### Create Context
```
Create a context called "project-alpha" with entries 1, 2, and 5
```

## 🔧 Advanced Configuration

### Custom Domain

```bash
sevalla domains:add yourdomain.com -a mcp-knowledge-server
sevalla domains:verify yourdomain.com
```

### Automated Backups

Add to your `sevalla.yml`:

```yaml
backup:
  enabled: true
  schedule: "0 2 * * *"  # Daily at 2 AM UTC
  retention_days: 30
  volumes:
    - knowledge-data
```

### Monitoring & Alerts

```bash
# Set up CPU alert
sevalla alerts:create \
  --metric cpu \
  --threshold 80 \
  --duration 5m \
  --email your@email.com

# Set up memory alert
sevalla alerts:create \
  --metric memory \
  --threshold 90 \
  --duration 3m \
  --email your@email.com
```

### Database Optimization

For better performance with large datasets:

```typescript
// Add to your database initialization
db.pragma('cache_size = -64000');  // 64MB cache
db.pragma('temp_store = MEMORY');
db.pragma('synchronous = NORMAL');
```

## 🔐 Security Best Practices

1. **Always use API keys** in production
2. **Enable HTTPS only** (Sevalla provides this automatically)
3. **Rotate API keys** regularly
4. **Monitor access logs** for suspicious activity
5. **Keep dependencies updated**: `npm audit fix`
6. **Use environment variables** for sensitive data
7. **Implement rate limiting** for public endpoints

### Add Rate Limiting

```bash
npm install express-rate-limit
```

```typescript
import rateLimit from 'express-rate-limit';

// Add to your Express app
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later.'
});

app.use('/search', limiter);
app.use('/stats', limiter);
```

## 📊 Monitoring & Debugging

### View Logs

```bash
# View real-time logs
sevalla logs -a mcp-knowledge-server --tail

# View last 100 lines
sevalla logs -a mcp-knowledge-server -n 100

# Filter for errors
sevalla logs -a mcp-knowledge-server | grep ERROR
```

### Database Management

```bash
# Access your app's shell
sevalla run bash -a mcp-knowledge-server

# Inside the shell, check database
cd /app/data
ls -lh knowledge.db
sqlite3 knowledge.db "SELECT COUNT(*) FROM knowledge_entries;"
```

### Performance Monitoring

```bash
# Check resource usage
sevalla ps -a mcp-knowledge-server

# View metrics
sevalla metrics -a mcp-knowledge-server
```

## 🐛 Troubleshooting

### Issue: Database Not Persisting

**Solution:** Ensure volume is properly mounted

```yaml
# In sevalla.yml
volumes:
  - name: knowledge-data
    mount_path: /app/data  # Must match DATABASE_PATH
    size: 1GB
```

### Issue: Connection Timeout

**Solution:** Check health endpoint and logs

```bash
curl https://your-app.sevalla.app/health
sevalla logs -a mcp-knowledge-server --tail
```

### Issue: High Memory Usage

**Solution:** Optimize database configuration

```typescript
// Add to database initialization
db.pragma('cache_size = -32000');  // Reduce to 32MB
db.pragma('mmap_size = 30000000000');  // Use memory-mapped I/O
```

### Issue: Slow Searches

**Solution:** Add more indexes

```sql
CREATE INDEX IF NOT EXISTS idx_content_fts ON knowledge_entries(content);
CREATE INDEX IF NOT EXISTS idx_updated_desc ON knowledge_entries(updated_at DESC);
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Sevalla

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Run tests
        run: npm test
      
      - name: Deploy to Sevalla
        env:
          SEVALLA_API_KEY: ${{ secrets.SEVALLA_API_KEY }}
        run: |
          npm install -g @sevalla/cli
          sevalla deploy -a mcp-knowledge-server --no-prompt
```

## 📈 Scaling Considerations

### Horizontal Scaling

```yaml
# In sevalla.yml
auto_scaling:
  enabled: true
  min_instances: 2
  max_instances: 10
  target_cpu: 60
  target_memory: 70
```

### Database Optimization for Scale

```typescript
// Consider using connection pooling
import { Pool } from 'generic-pool';

// For very large datasets, consider:
// 1. Implementing full-text search (SQLite FTS5)
// 2. Adding caching layer (Redis)
// 3. Archiving old entries
// 4. Implementing pagination
```

### Full-Text Search Example

```sql
-- Create FTS5 virtual table
CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
  title, 
  content,
  content='knowledge_entries',
  content_rowid='id'
);

-- Populate FTS index
INSERT INTO knowledge_fts(rowid, title, content)
  SELECT id, title, content FROM knowledge_entries;

-- Create triggers to keep FTS updated
CREATE TRIGGER IF NOT EXISTS knowledge_ai AFTER INSERT ON knowledge_entries BEGIN
  INSERT INTO knowledge_fts(rowid, title, content) 
  VALUES (new.id, new.title, new.content);
END;
```

## 🎯 Best Practices

### 1. Data Organization

- Use consistent category naming (lowercase, hyphenated)
- Tag entries with multiple relevant tags
- Include metadata for additional context
- Regular cleanup of outdated entries

### 2. Performance

- Index frequently queried fields
- Use prepared statements (already implemented)
- Implement caching for common queries
- Archive old data periodically

### 3. Maintenance

- Regular database backups
- Monitor database size
- Clean up unused contexts
- Update dependencies monthly

### 4. Development Workflow

```bash
# Local development
npm run dev

# Run tests (add test script)
npm test

# Build for production
npm run build

# Preview production build
NODE_ENV=production npm start
```

## 🔌 Integration Examples

### With Notion API

```typescript
// Add to your tools
{
  name: 'sync_to_notion',
  description: 'Sync knowledge entry to Notion',
  inputSchema: {
    type: 'object',
    properties: {
      entryId: { type: 'number' },
      notionPageId: { type: 'string' }
    }
  }
}
```

### With Obsidian

```typescript
// Export to Markdown
function exportToMarkdown(entry: any): string {
  return `---
title: ${entry.title}
category: ${entry.category}
tags: ${JSON.parse(entry.tags).join(', ')}
created: ${entry.created_at}
---

${entry.content}
`;
}
```

### With Slack

```typescript
// Notify team of new entries
import { WebClient } from '@slack/web-api';

async function notifySlack(entry: any) {
  const slack = new WebClient(process.env.SLACK_TOKEN);
  await slack.chat.postMessage({
    channel: '#knowledge-base',
    text: `New entry added: *${entry.title}* in ${entry.category}`
  });
}
```

## 📚 API Reference

### REST Endpoints

#### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "service": "mcp-knowledge-server",
  "timestamp": "2025-10-03T12:00:00Z"
}
```

#### GET /stats
Get database statistics (requires API key)

**Headers:**
- `x-api-key`: Your API key

**Response:**
```json
{
  "total_entries": 42,
  "categories": 5,
  "total_contexts": 3
}
```

#### POST /search
Search knowledge base (requires API key)

**Headers:**
- `x-api-key`: Your API key
- `Content-Type`: application/json

**Body:**
```json
{
  "query": "search term",
  "category": "tech",
  "limit": 10
}
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "results": [...]
}
```

## 🆘 Support & Resources

- **Sevalla Documentation**: https://docs.sevalla.com
- **MCP Specification**: https://modelcontextprotocol.io
- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **GitHub Issues**: Create issues for bugs/features

## 🔮 Future Enhancements

Consider adding:

1. **Vector Search**: Semantic search using embeddings
2. **Multi-tenancy**: Support multiple users/organizations
3. **Export/Import**: Backup and restore functionality
4. **Web UI**: Browser-based management interface
5. **Analytics**: Track usage patterns and popular queries
6. **Webhooks**: Notify external services of changes
7. **GraphQL API**: More flexible querying
8. **Real-time Sync**: WebSocket support for live updates

## 📝 Example Usage Scripts

### Bulk Import

```typescript
// bulk-import.ts
import Database from 'better-sqlite3';

const db = new Database('./knowledge.db');
const entries = [
  {
    category: 'tech',
    title: 'Docker Basics',
    content: 'Docker is a containerization platform...',
    tags: ['docker', 'devops']
  },
  // ... more entries
];

const stmt = db.prepare(`
  INSERT INTO knowledge_entries (category, title, content, tags, metadata)
  VALUES (?, ?, ?, ?, ?)
`);

const insert = db.transaction((entries) => {
  for (const entry of entries) {
    stmt.run(
      entry.category,
      entry.title,
      entry.content,
      JSON.stringify(entry.tags),
      '{}'
    );
  }
});

insert(entries);
console.log(`Imported ${entries.length} entries`);
```

### Export to JSON

```bash
# Export entire database
curl -H "x-api-key: YOUR_KEY" \
  https://your-app.sevalla.app/search \
  -d '{"limit": 1000}' \
  > backup.json
```

## 🎉 Conclusion

You now have a production-ready MCP Knowledge Base Server running on Sevalla! This server provides:

✅ Persistent storage for AI conversations  
✅ Structured knowledge management  
✅ Full-text search capabilities  
✅ REST API for integrations  
✅ Auto-scaling and monitoring  
✅ Secure authentication  

Happy building! 🚀