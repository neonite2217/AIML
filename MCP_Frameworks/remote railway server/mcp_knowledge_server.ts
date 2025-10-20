// src/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import Database from 'better-sqlite3';
import { z } from 'zod';
import express from 'express';
import { config } from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Database setup with configurable path
const DB_PATH = process.env.DATABASE_PATH || path.join(__dirname, '../knowledge.db');
const db = new Database(DB_PATH);

// Enable WAL mode for better concurrency
db.pragma('journal_mode = WAL');

// Initialize database tables with better schema
db.exec(`
  CREATE TABLE IF NOT EXISTS knowledge_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    tags TEXT,
    metadata TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    entries TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE INDEX IF NOT EXISTS idx_category ON knowledge_entries(category);
  CREATE INDEX IF NOT EXISTS idx_tags ON knowledge_entries(tags);
  CREATE INDEX IF NOT EXISTS idx_title ON knowledge_entries(title);
  CREATE INDEX IF NOT EXISTS idx_created_at ON knowledge_entries(created_at DESC);
`);

// Validation schemas
const KnowledgeEntrySchema = z.object({
  category: z.string().min(1, 'Category is required'),
  title: z.string().min(1, 'Title is required'),
  content: z.string().min(1, 'Content is required'),
  tags: z.array(z.string()).optional().default([]),
  metadata: z.record(z.any()).optional().default({}),
});

const SearchQuerySchema = z.object({
  query: z.string().optional(),
  category: z.string().optional(),
  tags: z.array(z.string()).optional(),
  limit: z.number().min(1).max(100).default(10),
});

const UpdateKnowledgeSchema = z.object({
  id: z.number().int().positive(),
  category: z.string().optional(),
  title: z.string().optional(),
  content: z.string().optional(),
  tags: z.array(z.string()).optional(),
  metadata: z.record(z.any()).optional(),
});

// MCP Server Implementation
class KnowledgeBaseServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'knowledge-base-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.setupHandlers();
  }

  private setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'add_knowledge',
          description: 'Add a new knowledge entry to the database',
          inputSchema: {
            type: 'object',
            properties: {
              category: { 
                type: 'string', 
                description: 'Knowledge category (e.g., tech, personal, reference)' 
              },
              title: { type: 'string', description: 'Entry title' },
              content: { type: 'string', description: 'Main content' },
              tags: { 
                type: 'array', 
                items: { type: 'string' }, 
                description: 'Tags for categorization' 
              },
              metadata: { type: 'object', description: 'Additional metadata' },
            },
            required: ['category', 'title', 'content'],
          },
        },
        {
          name: 'search_knowledge',
          description: 'Search knowledge base with filters',
          inputSchema: {
            type: 'object',
            properties: {
              query: { type: 'string', description: 'Search query for title and content' },
              category: { type: 'string', description: 'Filter by category' },
              tags: { 
                type: 'array', 
                items: { type: 'string' }, 
                description: 'Filter by tags (matches any)' 
              },
              limit: { 
                type: 'number', 
                description: 'Max results (1-100)', 
                default: 10,
                minimum: 1,
                maximum: 100
              },
            },
          },
        },
        {
          name: 'get_knowledge',
          description: 'Get a specific knowledge entry by ID',
          inputSchema: {
            type: 'object',
            properties: {
              id: { type: 'number', description: 'Entry ID' },
            },
            required: ['id'],
          },
        },
        {
          name: 'update_knowledge',
          description: 'Update an existing knowledge entry',
          inputSchema: {
            type: 'object',
            properties: {
              id: { type: 'number', description: 'Entry ID' },
              category: { type: 'string', description: 'New category' },
              title: { type: 'string', description: 'New title' },
              content: { type: 'string', description: 'New content' },
              tags: { type: 'array', items: { type: 'string' }, description: 'New tags' },
              metadata: { type: 'object', description: 'New metadata' },
            },
            required: ['id'],
          },
        },
        {
          name: 'delete_knowledge',
          description: 'Delete a knowledge entry',
          inputSchema: {
            type: 'object',
            properties: {
              id: { type: 'number', description: 'Entry ID to delete' },
            },
            required: ['id'],
          },
        },
        {
          name: 'list_categories',
          description: 'List all unique categories with entry counts',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'list_tags',
          description: 'List all unique tags with usage counts',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'create_context',
          description: 'Create a named context with specific entries',
          inputSchema: {
            type: 'object',
            properties: {
              name: { type: 'string', description: 'Context name' },
              description: { type: 'string', description: 'Context description' },
              entryIds: { 
                type: 'array', 
                items: { type: 'number' }, 
                description: 'IDs of entries to include' 
              },
            },
            required: ['name'],
          },
        },
        {
          name: 'get_stats',
          description: 'Get database statistics',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
      ],
    }));

    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      const contexts = db.prepare('SELECT name, description FROM contexts').all();
      
      return {
        resources: contexts.map((ctx: any) => ({
          uri: `context://${ctx.name}`,
          name: ctx.name,
          description: ctx.description || 'Saved context',
          mimeType: 'application/json',
        })),
      };
    });

    // Read resource content
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const contextName = request.params.uri.replace('context://', '');
      const context = db.prepare('SELECT * FROM contexts WHERE name = ?').get(contextName) as any;
      
      if (!context) {
        throw new Error(`Context ${contextName} not found`);
      }

      const entryIds = JSON.parse(context.entries || '[]');
      
      if (entryIds.length === 0) {
        return {
          contents: [
            {
              uri: request.params.uri,
              mimeType: 'application/json',
              text: JSON.stringify({ context, entries: [] }, null, 2),
            },
          ],
        };
      }

      const placeholders = entryIds.map(() => '?').join(',');
      const entries = db.prepare(
        `SELECT * FROM knowledge_entries WHERE id IN (${placeholders})`
      ).all(...entryIds);

      return {
        contents: [
          {
            uri: request.params.uri,
            mimeType: 'application/json',
            text: JSON.stringify({ context, entries }, null, 2),
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'add_knowledge': {
            const validated = KnowledgeEntrySchema.parse(args);
            const stmt = db.prepare(`
              INSERT INTO knowledge_entries (category, title, content, tags, metadata)
              VALUES (?, ?, ?, ?, ?)
            `);
            
            const result = stmt.run(
              validated.category,
              validated.title,
              validated.content,
              JSON.stringify(validated.tags),
              JSON.stringify(validated.metadata)
            );

            const entry = db.prepare('SELECT * FROM knowledge_entries WHERE id = ?')
              .get(result.lastInsertRowid);

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: true,
                    id: result.lastInsertRowid,
                    message: `Added knowledge entry: "${validated.title}" in ${validated.category}`,
                    entry
                  }, null, 2),
                },
              ],
            };
          }

          case 'search_knowledge': {
            const validated = SearchQuerySchema.parse(args);
            let query = 'SELECT * FROM knowledge_entries WHERE 1=1';
            const params: any[] = [];

            if (validated.query) {
              query += ' AND (title LIKE ? OR content LIKE ?)';
              const searchTerm = `%${validated.query}%`;
              params.push(searchTerm, searchTerm);
            }

            if (validated.category) {
              query += ' AND category = ?';
              params.push(validated.category);
            }

            if (validated.tags && validated.tags.length > 0) {
              query += ' AND (';
              query += validated.tags.map(() => 'tags LIKE ?').join(' OR ');
              query += ')';
              validated.tags.forEach(tag => params.push(`%"${tag}"%`));
            }

            query += ` ORDER BY updated_at DESC LIMIT ?`;
            params.push(validated.limit);

            const results = db.prepare(query).all(...params);

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: true,
                    count: results.length,
                    results
                  }, null, 2),
                },
              ],
            };
          }

          case 'get_knowledge': {
            const { id } = args as { id: number };
            const entry = db.prepare('SELECT * FROM knowledge_entries WHERE id = ?').get(id);

            if (!entry) {
              return {
                content: [
                  {
                    type: 'text',
                    text: JSON.stringify({
                      success: false,
                      error: `Entry with ID ${id} not found`
                    }),
                  },
                ],
              };
            }

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({ success: true, entry }, null, 2),
                },
              ],
            };
          }

          case 'update_knowledge': {
            const validated = UpdateKnowledgeSchema.parse(args);
            const { id, ...updates } = validated;
            
            const fields = [];
            const values = [];

            for (const [key, value] of Object.entries(updates)) {
              if (value !== undefined) {
                fields.push(`${key} = ?`);
                values.push(
                  key === 'tags' || key === 'metadata' ? JSON.stringify(value) : value
                );
              }
            }

            if (fields.length === 0) {
              return {
                content: [
                  {
                    type: 'text',
                    text: JSON.stringify({
                      success: false,
                      error: 'No updates provided'
                    }),
                  },
                ],
              };
            }

            values.push(id);
            const stmt = db.prepare(`
              UPDATE knowledge_entries 
              SET ${fields.join(', ')}, updated_at = CURRENT_TIMESTAMP 
              WHERE id = ?
            `);
            
            const result = stmt.run(...values);

            if (result.changes === 0) {
              return {
                content: [
                  {
                    type: 'text',
                    text: JSON.stringify({
                      success: false,
                      error: `Entry with ID ${id} not found`
                    }),
                  },
                ],
              };
            }

            const entry = db.prepare('SELECT * FROM knowledge_entries WHERE id = ?').get(id);

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: true,
                    message: `Updated entry ${id}`,
                    entry
                  }, null, 2),
                },
              ],
            };
          }

          case 'delete_knowledge': {
            const { id } = args as { id: number };
            const stmt = db.prepare('DELETE FROM knowledge_entries WHERE id = ?');
            const result = stmt.run(id);

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: result.changes > 0,
                    message: result.changes > 0 
                      ? `Deleted entry ${id}` 
                      : `Entry ${id} not found`,
                    changes: result.changes
                  }, null, 2),
                },
              ],
            };
          }

          case 'list_categories': {
            const categories = db.prepare(`
              SELECT category, COUNT(*) as count 
              FROM knowledge_entries 
              GROUP BY category 
              ORDER BY count DESC
            `).all();

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({ success: true, categories }, null, 2),
                },
              ],
            };
          }

          case 'list_tags': {
            const entries = db.prepare('SELECT tags FROM knowledge_entries').all() as any[];
            const tagCounts: Record<string, number> = {};

            entries.forEach(entry => {
              const tags = JSON.parse(entry.tags || '[]');
              tags.forEach((tag: string) => {
                tagCounts[tag] = (tagCounts[tag] || 0) + 1;
              });
            });

            const tags = Object.entries(tagCounts)
              .map(([tag, count]) => ({ tag, count }))
              .sort((a, b) => b.count - a.count);

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({ success: true, tags }, null, 2),
                },
              ],
            };
          }

          case 'create_context': {
            const { name, description, entryIds } = args as any;
            const stmt = db.prepare(`
              INSERT OR REPLACE INTO contexts (name, description, entries, updated_at)
              VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            `);
            
            stmt.run(name, description || '', JSON.stringify(entryIds || []));

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: true,
                    message: `Created/updated context "${name}"`,
                    entryCount: (entryIds || []).length
                  }, null, 2),
                },
              ],
            };
          }

          case 'get_stats': {
            const stats = db.prepare(`
              SELECT 
                COUNT(*) as total_entries,
                COUNT(DISTINCT category) as categories
              FROM knowledge_entries
            `).get();

            const contexts = db.prepare('SELECT COUNT(*) as count FROM contexts').get() as any;
            const recentEntries = db.prepare(
              'SELECT COUNT(*) as count FROM knowledge_entries WHERE created_at > datetime("now", "-7 days")'
            ).get() as any;

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: true,
                    ...stats,
                    total_contexts: contexts.count,
                    recent_entries_7d: recentEntries.count
                  }, null, 2),
                },
              ],
            };
          }

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
              }),
            },
          ],
          isError: true,
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Knowledge Base MCP Server running on stdio...');
    console.error(`Database: ${DB_PATH}`);
  }
}

// REST API for web access (optional)
if (process.env.ENABLE_WEB_API === 'true') {
  const app = express();
  app.use(express.json({ limit: '10mb' }));

  const PORT = process.env.PORT || 3000;
  const API_KEY = process.env.API_KEY;

  // Simple API key middleware
  const authenticateAPI = (req: any, res: any, next: any) => {
    if (API_KEY && req.headers['x-api-key'] !== API_KEY) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    next();
  };

  app.get('/health', (req, res) => {
    res.json({ 
      status: 'ok', 
      service: 'mcp-knowledge-server',
      timestamp: new Date().toISOString()
    });
  });

  app.get('/stats', authenticateAPI, (req, res) => {
    try {
      const stats = db.prepare(`
        SELECT 
          COUNT(*) as total_entries,
          COUNT(DISTINCT category) as categories
        FROM knowledge_entries
      `).get();
      
      const contexts = db.prepare('SELECT COUNT(*) as count FROM contexts').get() as any;
      
      res.json({
        ...stats,
        total_contexts: contexts.count
      });
    } catch (error) {
      res.status(500).json({ error: (error as Error).message });
    }
  });

  app.post('/search', authenticateAPI, (req, res) => {
    try {
      const validated = SearchQuerySchema.parse(req.body);
      let query = 'SELECT * FROM knowledge_entries WHERE 1=1';
      const params: any[] = [];

      if (validated.query) {
        query += ' AND (title LIKE ? OR content LIKE ?)';
        const searchTerm = `%${validated.query}%`;
        params.push(searchTerm, searchTerm);
      }

      if (validated.category) {
        query += ' AND category = ?';
        params.push(validated.category);
      }

      query += ` ORDER BY updated_at DESC LIMIT ?`;
      params.push(validated.limit);

      const results = db.prepare(query).all(...params);
      res.json({ success: true, count: results.length, results });
    } catch (error) {
      res.status(400).json({ error: (error as Error).message });
    }
  });

  app.listen(PORT, () => {
    console.log(`Web API listening on port ${PORT}`);
    console.log(`API Key protection: ${API_KEY ? 'enabled' : 'disabled'}`);
  });
}

// Start MCP server
const server = new KnowledgeBaseServer();
server.run().catch(console.error);

// Graceful shutdown
process.on('SIGINT', () => {
  console.error('Shutting down gracefully...');
  db.close();
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.error('Received SIGTERM, shutting down...');
  db.close();
  process.exit(0);
});