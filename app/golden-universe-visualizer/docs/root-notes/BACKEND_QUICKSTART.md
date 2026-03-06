# Backend Quick Start Guide

Get the Golden Universe backend API up and running in 5 minutes!

## Prerequisites

- Node.js installed (v18+)
- Python 3 installed (for calculations)
- Project dependencies installed (`npm install` already run)

## Quick Start (3 Steps)

### 1. Initialize Database

```bash
npm run db:init
```

This creates the SQLite database with all necessary tables and indexes.

### 2. Seed Database (Optional but Recommended)

```bash
npm run db:seed
```

This populates the database with:
- Theory documents from `Theory Development/` folder
- All 42 derivations from `42 Derivations/` folder
- Sample equations

### 3. Start Server

```bash
# Development mode (with auto-reload)
npm run server:dev

# Or start both frontend and backend together
npm start
```

## Verify Installation

### Option 1: Browser
Open http://localhost:3001/api/health

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2026-02-25T...",
  "uptime": 5.123,
  "checks": {
    "database": true,
    "filesystem": true,
    "python": true
  }
}
```

### Option 2: cURL
```bash
curl http://localhost:3001/api/health
```

### Option 3: Test Script
```bash
./test-backend.sh
```

## Explore the API

### Interactive Documentation
Open http://localhost:3001/api-docs for Swagger UI

### Key Endpoints

**Get All Theories:**
```bash
curl http://localhost:3001/api/theories
```

**Get Derivation #1:**
```bash
curl http://localhost:3001/api/derivations/1
```

**Search Everything:**
```bash
curl "http://localhost:3001/api/search?q=golden+ratio"
```

**Execute Calculation:**
```bash
curl -X POST http://localhost:3001/api/calculations \
  -H "Content-Type: application/json" \
  -d '{"scriptName":"golden_universe_master_calculator.py"}'
```

**Get Equations:**
```bash
curl http://localhost:3001/api/equations
```

## WebSocket Connection

Connect to `ws://localhost:3001` for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:3001');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log(message.type, message.data);
};
```

## Connect Frontend to Backend

The frontend already has the API client set up in `src/services/backendApi.ts`:

```typescript
import { backendApi } from '@/services/backendApi';

// Use in your components
const theories = await backendApi.getTheories();
const derivation = await backendApi.getDerivation(1);
const results = await backendApi.search('electron');
```

## Environment Configuration

All settings are in `.env` file:

```env
PORT=3001
NODE_ENV=development
DB_PATH=./data/golden-universe.db
CORS_ORIGIN=http://localhost:5173,http://localhost:3000
PYTHON_PATH=python3
```

## Available Scripts

```bash
npm run server          # Start production server
npm run server:dev      # Start development server (auto-reload)
npm run server:build    # Build TypeScript to JavaScript
npm run db:init         # Initialize database schema
npm run db:seed         # Seed database with content
npm start               # Start frontend + backend together
```

## Troubleshooting

### Database locked error
- Stop all running server instances
- Delete `data/golden-universe.db` and re-run `npm run db:init`

### Python not found
- Set `PYTHON_PATH=python3` in `.env`
- Or install Python: https://www.python.org/downloads/

### Port 3001 already in use
- Change `PORT=3002` in `.env`
- Update `VITE_API_BASE_URL` to match

### CORS errors
- Add your frontend URL to `CORS_ORIGIN` in `.env`
- Restart the server

## Development Workflow

1. **Start servers:**
   ```bash
   npm start
   ```

2. **Make changes to server code**
   - Server auto-reloads on file changes

3. **Test endpoints:**
   - Use Swagger UI: http://localhost:3001/api-docs
   - Use cURL or Postman
   - Run test script: `./test-backend.sh`

4. **Check health:**
   ```bash
   curl http://localhost:3001/api/health/metrics
   ```

## What's Running?

When you run `npm start`, you get:

- **Frontend (Vite):** http://localhost:5173
- **Backend (Express):** http://localhost:3001
- **API Docs:** http://localhost:3001/api-docs
- **WebSocket:** ws://localhost:3001

## Next Steps

1. ✅ Server is running
2. ✅ Database is initialized
3. ✅ Data is seeded
4. 🔄 Integrate with frontend components
5. 🔄 Test calculation execution
6. 🔄 Test WebSocket real-time updates

## Quick Reference

| Action | Command |
|--------|---------|
| Start everything | `npm start` |
| Start backend only | `npm run server:dev` |
| Initialize DB | `npm run db:init` |
| Seed DB | `npm run db:seed` |
| Test backend | `./test-backend.sh` |
| View docs | Open http://localhost:3001/api-docs |
| Check health | `curl http://localhost:3001/api/health` |

## Support

For detailed documentation, see:
- `SERVER_README.md` - Complete server documentation
- `BACKEND_IMPLEMENTATION.md` - Implementation details
- http://localhost:3001/api-docs - Interactive API documentation

**You're all set! Start building amazing features!** 🚀
