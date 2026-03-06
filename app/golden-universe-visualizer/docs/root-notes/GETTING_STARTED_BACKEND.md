# Getting Started with Golden Universe Backend

## 🚀 Quick Start in 3 Steps

### Step 1: Initialize Database
```bash
npm run db:init
```
✅ Creates SQLite database with schema

### Step 2: Seed Content
```bash
npm run db:seed
```
✅ Loads theories, derivations, and equations

### Step 3: Start Server
```bash
npm start
```
✅ Starts frontend (5173) and backend (3001)

---

## 🎯 Verify Installation

Open in browser: http://localhost:3001/api/health

**Expected Response:**
```json
{
  "status": "ok",
  "checks": {
    "database": true,
    "filesystem": true,
    "python": true
  }
}
```

If you see this ✅ **YOU'RE READY!**

---

## 📚 Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:3001/api |
| API Docs | http://localhost:3001/api-docs |
| Health Check | http://localhost:3001/api/health |
| WebSocket | ws://localhost:3001 |

---

## 🧪 Test the API

### Option 1: Browser
Visit http://localhost:3001/api-docs and try any endpoint

### Option 2: Command Line
```bash
./test-backend.sh
```

### Option 3: Manual cURL
```bash
# Get all theories
curl http://localhost:3001/api/theories

# Search
curl "http://localhost:3001/api/search?q=golden+ratio"

# Get derivation 1
curl http://localhost:3001/api/derivations/1
```

---

## 💻 Using in Your Code

### Import the API Client
```typescript
import { backendApi } from '@/services/backendApi';
```

### Make API Calls
```typescript
// Get theories
const { data } = await backendApi.getTheories();

// Search
const results = await backendApi.search('electron');

// Execute calculation
const job = await backendApi.executeCalculation('script.py', {
  param: 'value'
});
```

### WebSocket for Real-Time Updates
```typescript
import { wsClient } from '@/services/websocket';

wsClient.connect();

wsClient.onCalculationProgress((data) => {
  console.log('Progress:', data.progress);
});

wsClient.onCalculationCompleted((data) => {
  console.log('Done!', data.result);
});
```

---

## 🎓 Learning Path

### 1. Explore API Documentation
Visit http://localhost:3001/api-docs

Try each endpoint:
- **Theories** - Read theory documents
- **Derivations** - Access all 42 derivations
- **Equations** - Browse equation catalog
- **Calculations** - Execute Python scripts
- **Search** - Full-text search

### 2. Test WebSocket
Open browser console:
```javascript
const ws = new WebSocket('ws://localhost:3001');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

### 3. Review Code
Look at:
- `server/routes/` - API endpoints
- `server/controllers/` - Business logic
- `src/services/backendApi.ts` - Client usage
- `src/services/websocket.ts` - WebSocket client

---

## 📖 Documentation Files

Read in this order:

1. **BACKEND_QUICKSTART.md** - 5-minute guide (⭐ START HERE)
2. **SERVER_README.md** - Complete server docs
3. **BACKEND_IMPLEMENTATION.md** - Technical details
4. **BACKEND_COMPLETE.md** - Full summary

---

## 🛠️ Available Commands

```bash
# Database
npm run db:init           # Create schema
npm run db:seed           # Load data

# Server
npm run server            # Production mode
npm run server:dev        # Development mode (auto-reload)
npm run server:build      # Build TypeScript

# Combined
npm start                 # Frontend + Backend
npm run start:all         # Same as above

# Frontend only
npm run dev               # Vite dev server

# Testing
./test-backend.sh         # Test all endpoints
```

---

## ✅ Pre-flight Checklist

Before you start coding:

- [ ] Database initialized (`npm run db:init`)
- [ ] Data seeded (`npm run db:seed`)
- [ ] Server running (`npm start`)
- [ ] Health check passed (http://localhost:3001/api/health)
- [ ] API docs accessible (http://localhost:3001/api-docs)
- [ ] Test script passes (`./test-backend.sh`)

**All checked?** You're ready to build! 🎉

---

## 🎯 Your First Integration

### Replace Mock Data with Real API

**Before:**
```typescript
const theories = [
  { id: 1, title: 'Mock Theory' }
];
```

**After:**
```typescript
import { backendApi } from '@/services/backendApi';

const { data: theories } = await backendApi.getTheories();
```

### Add Real-Time Calculation Updates

```typescript
import { backendApi, wsClient } from '@/services';

// Start calculation
const { data } = await backendApi.executeCalculation('script.py');

// Listen for updates
wsClient.connect();
wsClient.onCalculationProgress((progress) => {
  setProgress(progress.progress);
});
wsClient.onCalculationCompleted((result) => {
  setResult(result.data);
});
```

---

## 🔧 Common Issues

### Port 3001 already in use
```bash
# Change port in .env
PORT=3002

# Update frontend API URL
VITE_API_BASE_URL=http://localhost:3002/api
```

### Database locked
```bash
# Stop server, remove DB, reinitialize
rm data/golden-universe.db
npm run db:init
npm run db:seed
```

### Python not found
```bash
# Set Python path in .env
PYTHON_PATH=python3

# Or install Python
brew install python3  # macOS
```

### CORS errors
```bash
# Add your origin to .env
CORS_ORIGIN=http://localhost:5173,http://your-origin
```

---

## 🎓 Next Steps

### Week 1: Learn the API
- [ ] Read BACKEND_QUICKSTART.md
- [ ] Explore http://localhost:3001/api-docs
- [ ] Test all endpoints
- [ ] Try WebSocket connection

### Week 2: Integration
- [ ] Replace mock data in components
- [ ] Add API error handling
- [ ] Implement loading states
- [ ] Connect WebSocket

### Week 3: Features
- [ ] Build theory browser
- [ ] Create derivation viewer
- [ ] Add calculation interface
- [ ] Implement search

---

## 🌟 Quick Tips

1. **Always check health first**
   ```bash
   curl http://localhost:3001/api/health
   ```

2. **Use Swagger for testing**
   - Interactive UI
   - Try requests
   - See responses

3. **Check server logs**
   - Detailed request logging
   - Error messages
   - Performance metrics

4. **Cache is your friend**
   - Responses are cached
   - Reduces load times
   - Auto-expires

5. **WebSocket for real-time**
   - Calculation progress
   - Live updates
   - No polling needed

---

## 📞 Get Help

### Documentation
- http://localhost:3001/api-docs
- SERVER_README.md
- BACKEND_IMPLEMENTATION.md

### Testing
- `./test-backend.sh`
- http://localhost:3001/api/health
- http://localhost:3001/api/health/metrics

### Code Examples
- `src/services/backendApi.ts`
- `src/services/websocket.ts`
- `server/routes/` (all route files)

---

## 🎉 You're All Set!

**Your backend is ready. Start building!**

```bash
npm start
```

Then open:
- Frontend: http://localhost:5173
- API Docs: http://localhost:3001/api-docs

**Happy coding!** 💻✨
