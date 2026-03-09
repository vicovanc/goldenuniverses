# Python Serverless Execution for Vercel

## Overview

This solution provides real Python execution on Vercel using their Python runtime, replacing the problematic Pyodide implementation.

## Architecture

```
Frontend → /api/python/exec → Vercel Python Function → Execute Code → Return Results
```

## Key Files

1. **`/api/python/exec.py`** - Python serverless function
   - Runs actual Python code in Vercel's Python 3.9 runtime
   - Includes all Golden Universe constants and functions
   - Handles numpy, scipy, and mpmath calculations

2. **`/api/requirements.txt`** - Python dependencies
   - numpy==1.24.3
   - scipy==1.10.1
   - mpmath==1.3.0

3. **`vercel.json`** - Configuration
   - Configures Python runtime for the serverless function
   - Routes `/api/python/exec` to the Python handler

## How It Works

### 1. Request Flow
- Frontend sends POST request to `/api/python/exec`
- Request body contains: `{ "code": "python code here" }`
- Python function executes code with Golden Universe setup
- Returns: `{ "success": true, "data": { "output": "...", "executionTime": 123 }}`

### 2. Pre-loaded Functions
The serverless function includes all Golden Universe functions:
- `calculate_electron_mass(nu)` - Calculate particle masses
- `calculate_newtons_g()` - Newton's gravitational constant
- `calculate_fine_structure()` - Fine structure constant
- `calculate_resonance(N, phi_sq)` - Resonance calculations
- `calculate_winding_length(p, q)` - Winding number calculations

### 3. Available Constants
- `PHI` - Golden ratio
- `PI`, `E` - Mathematical constants
- `M_P_MeV`, `M_E_MeV` - Proton and electron masses
- `N_E`, `DELTA_E`, `NU_E` - Winding numbers
- `ALPHA` - Fine structure constant

## Deployment Steps

1. **Ensure files are in place**:
   ```
   api/
   ├── python/
   │   └── exec.py
   └── requirements.txt
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel --prod
   ```

3. **Test the deployment**:
   ```bash
   # Test with curl
   curl -X POST https://your-app.vercel.app/api/python/exec \
     -H "Content-Type: application/json" \
     -d '{"code": "print(calculate_electron_mass(137.036))"}'

   # Or use the test script
   python test-vercel-python.py https://your-app.vercel.app/api/python/exec
   ```

## Local Development

For local development, the system uses the Express backend server:

```bash
# Start backend server
npm run server:dev

# Frontend will use localhost:3001
npm run dev
```

## Example Usage

### JavaScript/TypeScript
```javascript
const response = await fetch('/api/python/exec', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: `
result = calculate_electron_mass(NU_E)
print(f"Electron mass: {result} MeV")
`
  })
});

const data = await response.json();
console.log(data.data.output); // "Electron mass: 0.511 MeV"
```

### Python Test
```python
import requests

response = requests.post(
    'https://your-app.vercel.app/api/python/exec',
    json={'code': 'print(PHI ** 34)'}
)
print(response.json()['data']['output'])
```

## Advantages Over Pyodide

1. **Full Python Runtime**: Not limited to Pyodide's package restrictions
2. **Faster Execution**: No WebAssembly overhead
3. **Better Compatibility**: Works with all your existing scripts
4. **Server-Side**: More secure, no client-side code exposure
5. **Reliable**: No browser compatibility issues

## Limitations

- **10 second timeout**: Vercel functions have a max duration
- **No file I/O**: Can't read/write files on serverless
- **Stateless**: Each execution is independent

## Troubleshooting

### "Module not found" errors
- Add missing packages to `/api/requirements.txt`
- Redeploy to Vercel

### Timeout errors
- Optimize calculations to run under 10 seconds
- Break large calculations into smaller chunks

### CORS errors
- The Python function includes CORS headers
- Check browser console for specific error messages

### Local testing
```bash
# Test local backend
curl -X POST http://localhost:3001/api/python/exec \
  -H "Content-Type: application/json" \
  -d '{"code": "print(1+1)"}'
```

## Security Considerations

- Code execution is sandboxed in Vercel's environment
- No file system access
- 10-second timeout prevents infinite loops
- Consider adding rate limiting for production