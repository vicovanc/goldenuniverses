# Golden Universe API Server

A comprehensive Node.js/Express backend API for the Golden Universe app that serves content, manages calculations, and provides data endpoints.

## Features

- **RESTful API** - Complete REST API for theories, derivations, equations, and calculations
- **SQLite Database** - Fast, embedded database with full-text search capabilities
- **Python Integration** - Execute Python calculations with queue management
- **WebSocket Support** - Real-time updates for calculation progress
- **LaTeX Rendering** - Server-side LaTeX to HTML conversion using KaTeX
- **Markdown Support** - Full markdown rendering with syntax highlighting
- **Caching** - Built-in caching system for improved performance
- **API Documentation** - Swagger/OpenAPI interactive documentation
- **Health Monitoring** - Health checks and performance metrics
- **Rate Limiting** - Protection against abuse with configurable limits
- **CORS** - Cross-origin resource sharing configuration
- **Error Handling** - Comprehensive error handling and logging

## Directory Structure

```
server/
├── config/           # Configuration files
│   └── config.ts     # Main configuration
├── controllers/      # Business logic
│   ├── theoriesController.ts
│   ├── derivationsController.ts
│   ├── calculationsController.ts
│   └── equationsController.ts
├── database/         # Database setup and migrations
│   ├── schema.ts     # Database schema and initialization
│   └── seed.ts       # Database seeding
├── middleware/       # Express middleware
│   ├── cors.ts       # CORS configuration
│   ├── errorHandler.ts
│   ├── validation.ts
│   └── rateLimiter.ts
├── models/           # Data models
├── routes/           # API routes
│   ├── index.ts      # Main router
│   ├── theories.ts
│   ├── derivations.ts
│   ├── calculations.ts
│   ├── equations.ts
│   ├── search.ts
│   └── health.ts
├── services/         # Business services
│   ├── pythonExecutor.ts
│   └── websocket.ts
├── utils/            # Helper functions
│   ├── contentRenderer.ts
│   └── cache.ts
├── server.ts         # Main server file
└── swagger.json      # API documentation
```

## Installation

Dependencies are already installed. If needed, reinstall:

```bash
npm install
```

## Configuration

Create or update `.env` file:

```env
# Server
PORT=3001
NODE_ENV=development

# Database
DB_PATH=./data/golden-universe.db

# CORS
CORS_ORIGIN=http://localhost:5173,http://localhost:3000

# Python
PYTHON_PATH=python3
PYTHON_SCRIPTS_PATH=../../../pipeline
PYTHON_TIMEOUT=300000

# Content Paths
CONTENT_PATH=../../..
DERIVATIONS_PATH=../../../42 Derivations
THEORIES_PATH=../../../Theory Development

# Cache
CACHE_TTL=3600
CACHE_CHECK_PERIOD=600

# WebSocket
WS_ENABLED=true
WS_PING_INTERVAL=30000
```

## Database Setup

### Initialize Database

Create the database schema:

```bash
npm run db:init
```

### Seed Database

Populate the database with content:

```bash
npm run db:seed
```

This will:
- Load theory documents from the Theory Development folder
- Index all 42 derivations
- Create sample equations
- Set up full-text search indexes

## Running the Server

### Development Mode

Run with auto-reload:

```bash
npm run server:dev
```

### Production Mode

Build and run:

```bash
npm run server:build
npm run server
```

### Run Frontend + Backend Together

Start both Vite dev server and API server:

```bash
npm start
# or
npm run start:all
```

## API Endpoints

### Theories

- `GET /api/theories` - List all theories
- `GET /api/theories/:id` - Get specific theory (supports `?render=true` for LaTeX)
- `GET /api/theories/search?q=query` - Search theories
- `GET /api/theories/stats` - Get theory statistics

### Derivations

- `GET /api/derivations` - List all 42 derivations
- `GET /api/derivations/:number` - Get derivation by number (1-42)
- `GET /api/derivations/:number/files/:filename` - Get file content
- `GET /api/derivations/stats` - Get derivation statistics

### Equations

- `GET /api/equations` - List all equations (supports `?category=cat&render=true`)
- `GET /api/equations/:id` - Get equation by ID
- `GET /api/equations/categories` - Get equation categories
- `GET /api/equations/search?q=query` - Search equations

### Calculations

- `POST /api/calculations` - Execute Python calculation
  ```json
  {
    "scriptName": "golden_universe_master_calculator.py",
    "parameters": { "mode": "full" }
  }
  ```
- `GET /api/calculations/:jobId` - Get calculation status
- `GET /api/calculations/:jobId/result` - Get calculation result
- `GET /api/calculations` - Get calculation history
- `GET /api/calculations/results` - Get precision results table
- `POST /api/calculations/cancel` - Cancel current calculation

### Search

- `GET /api/search?q=query` - Full-text search across all content

### Health

- `GET /api/health` - Server health check
- `GET /api/health/metrics` - Performance metrics

### Documentation

- `GET /api-docs` - Swagger UI interactive documentation
- `GET /api` - API information and endpoints

## WebSocket Events

Connect to `ws://localhost:3001` for real-time updates:

### Client -> Server
- `ping` - Keep-alive ping
- `subscribe` - Subscribe to events

### Server -> Client
- `connected` - Connection established
- `calculation-queued` - Calculation added to queue
- `calculation-started` - Calculation started
- `calculation-progress` - Progress update
- `calculation-completed` - Calculation finished
- `calculation-failed` - Calculation failed

Example:
```javascript
const ws = new WebSocket('ws://localhost:3001');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log(message.type, message.data);
};
```

## Python Integration

### Calculation Execution

The server can execute Python scripts from the pipeline directory:

```javascript
// POST /api/calculations
{
  "scriptName": "golden_universe_master_calculator.py",
  "parameters": {
    "mode": "full",
    "precision": 15
  }
}
```

### Queue Management

- Calculations are queued and processed sequentially
- Real-time progress updates via WebSocket
- Results cached in database
- Configurable timeout (default: 5 minutes)

### Python Script Requirements

Scripts should:
1. Accept `--params` argument for JSON parameters
2. Output JSON to stdout for structured results
3. Use `PROGRESS:XX` format for progress updates (0-100)
4. Exit with code 0 on success

Example Python script:
```python
import json
import sys

# Parse parameters
if '--params' in sys.argv:
    params = json.loads(sys.argv[sys.argv.index('--params') + 1])

# Report progress
print("PROGRESS:50")

# Output result as JSON
result = {"value": 1.618033, "precision": 15}
print(json.dumps(result))
```

## Caching

The server implements a smart caching system:

- Theory and derivation data cached for 1 hour
- Search results cached for 10 minutes
- Calculation results cached indefinitely
- Automatic cleanup of expired cache entries
- Cache keys include render options

Clear cache programmatically:
```typescript
import Cache from './server/utils/cache';
Cache.clear();
```

## Error Handling

All errors return consistent JSON format:

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "stack": "Stack trace (dev only)"
  }
}
```

HTTP Status Codes:
- 200 - Success
- 400 - Bad Request
- 404 - Not Found
- 429 - Too Many Requests
- 500 - Internal Server Error
- 503 - Service Unavailable

## Rate Limiting

Default limits:
- General API: 100 requests per 15 minutes
- Calculations: 5 per minute
- Search: 30 per minute

Configure in `server/config/config.ts`.

## Development

### TypeScript Compilation

Check types:
```bash
npm run type-check
```

Build server:
```bash
npm run server:build
```

### Debugging

Enable detailed logging:
```env
NODE_ENV=development
```

View logs in real-time:
```bash
npm run server:dev
```

### Testing API

Use Swagger UI at `http://localhost:3001/api-docs` or:

```bash
# Health check
curl http://localhost:3001/api/health

# Get theories
curl http://localhost:3001/api/theories

# Search
curl "http://localhost:3001/api/search?q=golden+ratio"

# Execute calculation
curl -X POST http://localhost:3001/api/calculations \
  -H "Content-Type: application/json" \
  -d '{"scriptName":"golden_universe_master_calculator.py"}'
```

## Production Deployment

1. Set environment variables:
   ```env
   NODE_ENV=production
   PORT=3001
   ```

2. Build TypeScript:
   ```bash
   npm run server:build
   ```

3. Start server:
   ```bash
   npm run server
   ```

4. Use a process manager (PM2):
   ```bash
   npm install -g pm2
   pm2 start dist/server/server.js --name golden-universe-api
   pm2 save
   ```

## Security

- Helmet.js for security headers
- CORS with origin validation
- Rate limiting per IP
- Request validation
- SQL injection protection (parameterized queries)
- Path traversal protection
- Environment variable configuration

## Performance

- SQLite WAL mode for better concurrency
- Response compression (gzip)
- Database indexes on frequently queried fields
- Full-text search indexes
- Efficient caching system
- Connection pooling ready

## Troubleshooting

### Database locked
- Ensure only one instance is running
- Check file permissions on database file

### Python execution fails
- Verify Python path in config
- Check script exists in pipeline directory
- Ensure Python has required dependencies

### WebSocket connection fails
- Check firewall settings
- Verify WS_ENABLED=true in config
- Check browser console for errors

### CORS errors
- Add frontend URL to CORS_ORIGIN
- Check CORS middleware configuration

## License

Part of the Golden Universe project.
