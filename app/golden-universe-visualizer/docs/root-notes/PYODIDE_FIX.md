# Pyodide Python Execution Fix

## Problem

The Pyodide Python engine was failing with the error:
```
Uncaught (in promise) TypeError: self.loadPyodide is not a function
```

This occurred because the Web Worker was trying to use `loadPyodide` before the Pyodide library was loaded into the worker context.

## Root Cause

The worker file (`src/services/pythonEngine/pythonWorker.ts`) was created as an ES6 module worker (`type: 'module'`), which means:
1. It cannot use `importScripts()` to load external scripts
2. The Pyodide CDN script was never loaded into the worker context
3. Therefore, `self.loadPyodide()` was undefined

## Solution

### 1. Dynamic Script Loading (pythonWorker.ts)

Added a `loadPyodideScript()` function that:
- Fetches the Pyodide script from CDN using `fetch()`
- Evaluates the script using `new Function()` to define `loadPyodide` globally
- Returns the `loadPyodide` function for use in the worker

```typescript
async function loadPyodideScript(): Promise<any> {
  const response = await fetch('https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js');
  if (!response.ok) {
    throw new Error(`Failed to load Pyodide script: ${response.status} ${response.statusText}`);
  }
  const scriptText = await response.text();
  const scriptFunc = new Function(scriptText);
  scriptFunc();

  const loadPyodide = (globalThis as any).loadPyodide;
  if (!loadPyodide) {
    throw new Error('loadPyodide function not found after loading script');
  }
  return loadPyodide;
}
```

### 2. Enhanced Error Handling

Added comprehensive error handling to:
- Check if the CDN fetch succeeded
- Verify `loadPyodide` is available after script execution
- Provide clear error messages for debugging

### 3. Vite Configuration (vite.config.ts)

Added worker configuration and COOP/COEP headers:

```typescript
server: {
  headers: {
    'Cross-Origin-Embedder-Policy': 'require-corp',
    'Cross-Origin-Opener-Policy': 'same-origin',
  },
},
worker: {
  format: 'es',
}
```

These headers are required for SharedArrayBuffer support in Pyodide (though not strictly necessary for basic usage).

### 4. Performance Optimization (index.html)

Added CDN preconnect to improve loading performance:

```html
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
<link rel="dns-prefetch" href="https://cdn.jsdelivr.net" />
```

## Files Modified

1. `/src/services/pythonEngine/pythonWorker.ts` - Main fix for loading Pyodide
2. `/vite.config.ts` - Worker configuration and COOP/COEP headers
3. `/index.html` - CDN preconnect for performance

## Testing

### Manual Testing

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Navigate to the Calculations page:
   ```
   http://localhost:3000/calculations
   ```

3. Wait for Pyodide to initialize (you should see progress indicators)

4. Select a preset calculation or enter custom Python code:
   ```python
   # Calculate electron mass
   result = calculate_electron_mass(NU_E)
   to_json(result)
   ```

5. Click "Run" - the calculation should execute without errors

### Expected Behavior

- No console errors about `loadPyodide`
- Progress messages showing: "Loading Pyodide" → "Loading packages" → "Initializing constants" → "Ready"
- Calculations execute and return results
- Results display with proper formatting

### Testing the Standalone HTML

You can also test Pyodide independently using the test file:

```bash
# Open in browser
open public/pyodide-loader.html
```

This standalone HTML file loads Pyodide directly and runs test calculations without the React app.

## Architecture

### Component Flow

```
User Action (Calculations page)
    ↓
getPythonEngine() (singleton)
    ↓
PythonEngine.initialize()
    ↓
Worker created with pythonWorker.ts
    ↓
loadPyodideScript() fetches and evaluates CDN script
    ↓
loadPyodide() initializes Pyodide runtime
    ↓
Scientific packages loaded (numpy, scipy, mpmath)
    ↓
Golden Universe constants initialized
    ↓
Ready for calculations
```

### Worker Communication

```typescript
Main Thread                    Worker Thread
-----------                    -------------
    |                              |
    |-- init message ----------->  |
    |                              | loadPyodideScript()
    |                              | loadPyodide()
    |  <-- progress updates -----  | loadPackage()
    |  <-- ready message --------  |
    |                              |
    |-- execute message -------->  |
    |                              | runPythonAsync()
    |  <-- result message -------  |
```

## Performance Considerations

1. **Lazy Loading**: Pyodide is only loaded when first needed (not on app startup)
2. **CDN Preconnect**: Reduces DNS lookup and TLS handshake time
3. **Caching**: Calculations can be cached (see `pythonEngineOptimized.ts`)
4. **Web Worker**: Non-blocking execution keeps UI responsive

## Troubleshooting

### If Pyodide still fails to load:

1. **Check Network**: Ensure CDN is accessible
   ```bash
   curl -I https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js
   ```

2. **Check Browser Console**: Look for CORS or Content-Security-Policy errors

3. **Check COOP/COEP Headers**: Some Pyodide features require these headers
   - Open DevTools → Network → Select HTML document
   - Check Response Headers for `Cross-Origin-Embedder-Policy` and `Cross-Origin-Opener-Policy`

4. **Clear Browser Cache**: Cached corrupt files can cause issues
   ```
   Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)
   ```

5. **Try Different Browser**: Test in Chrome, Firefox, Safari

### Common Errors

**Error: "Failed to fetch"**
- CDN is blocked or offline
- Check network connectivity
- Try using a different CDN (e.g., unpkg.com)

**Error: "loadPyodide function not found"**
- Script didn't execute properly
- Check browser compatibility (need ES6 support)
- Try the standalone HTML test file

**Error: "SharedArrayBuffer is not defined"**
- COOP/COEP headers not set correctly
- This is optional for basic Pyodide usage
- Check vite.config.ts server headers

## Alternative Approaches (Not Used)

### Option 1: Classic Worker (with importScripts)
```typescript
// Would require changing worker creation:
new Worker(url, { type: 'classic' })
// Then in worker:
importScripts('https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js');
```
**Reason not used**: Module workers are preferred for better TypeScript support and future compatibility.

### Option 2: Local Pyodide Package
```bash
npm install pyodide
```
**Reason not used**: Large package size (100MB+) significantly increases bundle size and build time.

### Option 3: Dynamic Import
```typescript
const { loadPyodide } = await import('https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.mjs');
```
**Reason not used**: Pyodide doesn't provide ES modules that can be imported this way.

## Future Improvements

1. **Offline Support**: Cache Pyodide files in Service Worker
2. **Version Management**: Allow switching Pyodide versions
3. **Package Management**: Dynamic loading of additional Python packages
4. **Progress Tracking**: More granular loading progress
5. **Error Recovery**: Automatic retry on failure
6. **Bundle Optimization**: Self-host Pyodide for faster loading

## References

- [Pyodide Documentation](https://pyodide.org/en/stable/)
- [Web Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API)
- [Vite Worker Support](https://vitejs.dev/guide/features.html#web-workers)
- [COOP/COEP Headers](https://web.dev/coop-coep/)
