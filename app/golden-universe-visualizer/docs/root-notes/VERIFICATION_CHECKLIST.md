# Pyodide Fix Verification Checklist

## Pre-Flight Checks
- [x] pythonWorker.ts uses `importScripts()` instead of fetch + eval
- [x] pythonEngine.ts creates classic worker (no `type: 'module'`)
- [x] vite.config.ts uses `worker.format: 'iife'`
- [x] terser is installed in devDependencies
- [x] Worker message handler is properly defined

## Expected Behavior After Fix

### On Page Load (Calculations Page)
1. No console errors related to `self.loadPyodide is not a function`
2. Progress messages should appear in console:
   - "loading_pyodide" (10%)
   - "loading_packages" (30%)
   - "initializing_constants" (60%)
   - "loading_functions" (80%)
   - "ready" (100%)

### During Initialization
1. Pyodide loads from CDN: https://cdn.jsdelivr.net/pyodide/v0.25.0/full/
2. Scientific packages load: numpy, scipy, mpmath
3. Golden Universe constants are initialized
4. Helper functions are loaded

### Python Execution Test
Run this code to verify calculations work:
```python
import mpmath as mp
mp.dps = 50
PHI = mp.phi
result = str(PHI)
print(f"Golden ratio: {result}")
```

Expected output: `Golden ratio: 1.6180339887498948482045868343656381177203091798058`

### UI Test
1. Navigate to http://localhost:3000/calculations
2. Click "Particle Mass Calculator"
3. Select "Electron" and click "Calculate"
4. Should see result with ~23 ppm error
5. No errors in console

## Common Issues (If They Occur)

### CORS Errors
If you see CORS errors when loading Pyodide:
- Verify the headers in vite.config.ts:
  ```typescript
  headers: {
    'Cross-Origin-Embedder-Policy': 'require-corp',
    'Cross-Origin-Opener-Policy': 'same-origin',
  }
  ```

### Worker Not Loading
If worker doesn't initialize:
- Check that importScripts is being called correctly
- Verify Pyodide CDN is accessible
- Check browser console for specific error messages

### Import Errors in Worker
If you see module import errors:
- Verify worker format is 'iife' in vite.config.ts
- Ensure worker is created without `type: 'module'`

## Testing Commands

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Success Criteria
✅ Dev server starts without worker errors
✅ Calculations page loads without console errors
✅ Pyodide initializes and shows "ready" status
✅ Can execute Python calculations successfully
✅ Results display correctly in UI
✅ All 371 calculations are available
