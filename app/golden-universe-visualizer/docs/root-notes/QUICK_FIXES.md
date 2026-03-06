# Golden Universe Visualizer - Quick Fixes Guide

## Critical Fixes Required (Do First)

### 1. Create Search Data Files
**Files to create:**
- `/public/data/content-index.json`
- `/public/data/derivations-map.json`
- `/public/data/equations-catalog.json`

**Schema example for content-index.json:**
```json
{
  "theories": [
    {
      "id": "theory-1",
      "title": "Foundation Laws",
      "filename": "foundation-laws.md",
      "path": "theories/foundation-laws",
      "content": "...",
      "metadata": {
        "description": "Core laws",
        "tags": ["foundation"]
      },
      "wordCount": 1000,
      "equations": [],
      "createdAt": "2024-01-01",
      "modifiedAt": "2024-03-01"
    }
  ],
  "derivations": [...],
  "pythonFiles": [...]
}
```

**Action:** Create build script in `scripts/generate-search-index.ts` to auto-generate from source files.

---

### 2. Fix Python Engine Fallback
**File:** `src/services/pythonEngine/pythonEngine.ts`

**Current problematic code (lines 37-40):**
```typescript
this.initialize().catch(err => {
  console.error('Failed to auto-initialize Python engine:', err);
});
```

**Replace with:**
```typescript
private initTimeout: NodeJS.Timeout | null = null;

private async safeInitialize(): Promise<void> {
  try {
    // Set timeout for Pyodide loading
    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Pyodide load timeout')), 30000)
    );
    
    await Promise.race([this.initialize(), timeoutPromise]);
  } catch (err) {
    console.warn('Python engine failed, falling back to sync calculator:', err);
    this.updateStatus({
      ready: false,
      loading: false,
      error: 'Using fallback calculator',
    });
    // Fallback: Use synchronous calculator instead
    this.useFallback = true;
  }
}

constructor() {
  this.initializeWorker();
  this.safeInitialize().catch(err => {
    console.error('Critical: Python engine unavailable:', err);
  });
}
```

**Then in execute() method:**
```typescript
async execute(code: string): Promise<CalculationResult> {
  if (this.useFallback) {
    // Use synchronous calculator from goldenUniverseCalculator.ts
    return GoldenUniverseCalculator.electron();
  }
  // ... existing worker code
}
```

---

### 3. Initialize Search on App Load
**File:** `src/App.tsx`

**Add to App component:**
```typescript
import { searchService } from '@/services/searchService';

function App() {
  useEffect(() => {
    // Initialize search index on app load
    searchService.buildIndex().catch(err => {
      console.warn('Search index initialization failed:', err);
    });
  }, []);

  return (
    // ... existing code
  );
}
```

---

### 4. Implement Neutrino Oscillation Calculator
**Create file:** `src/calculations/neutrinoOscillationCalculator.ts`

```typescript
export interface NeutrinoParams {
  theta12: number;  // Solar mixing angle
  theta23: number;  // Atmospheric mixing angle
  theta13: number;  // Reactor mixing angle
  deltaCP: number;  // CP-violating phase
  dm2_21: number;   // Solar mass-squared difference
  dm2_31: number;   // Atmospheric mass-squared difference
  energy: number;   // Neutrino energy in GeV
  distance: number; // Propagation distance in km
}

export interface NeutrinoResult {
  particle: string;
  P_ee: number;           // Electron survival probability
  P_em: number;
  P_et: number;
  oscillation_length: number;
  components?: {
    [key: string]: number;
  };
}

export class NeutrinoOscillationCalculator {
  static calculate(params: NeutrinoParams): NeutrinoResult {
    // Implement oscillation probability formula:
    // P(νe → νe) = 1 - sin²(2θ12)sin²(Δm²_21·L/4E)·cos⁴(θ13)
    // Plus muon and tau probabilities
    
    const { theta12, theta23, theta13, deltaCP, dm2_21, dm2_31, energy, distance } = params;
    
    // Convert angles to radians and distances
    const t12 = theta12 * Math.PI / 180;
    const t23 = theta23 * Math.PI / 180;
    const t13 = theta13 * Math.PI / 180;
    const L = distance;
    const E = energy;
    
    // Oscillation phase
    const phase_21 = (dm2_21 * L) / (4 * E);
    const phase_31 = (dm2_31 * L) / (4 * E);
    
    // Electron survival probability
    const P_ee = 1 - Math.sin(2*t12)**2 * Math.sin(phase_21)**2 * Math.cos(t13)**4;
    
    // Muon appearance probability
    const P_em = Math.sin(2*t13)**2 * Math.sin(t23)**2 * Math.sin(phase_31)**2;
    
    // Tau appearance probability
    const P_et = Math.sin(2*t13)**2 * Math.cos(t23)**2 * Math.sin(phase_31)**2;
    
    const oscillation_length = 2 * Math.PI / Math.sqrt(dm2_21);
    
    return {
      particle: 'neutrino',
      P_ee,
      P_em,
      P_et,
      oscillation_length,
      components: {
        theta12,
        theta23,
        theta13,
        deltaCP,
        dm2_21,
        dm2_31,
        energy,
        distance,
      }
    };
  }
}
```

**Then create UI component:** `src/components/Calculations/NeutrinoOscillationCalculator.tsx`

---

## Moderate Fixes (Do Next)

### 5. Add DOMPurify for XSS Protection
**File:** `src/components/Theory/TheoryDocViewer.tsx`

```bash
npm install dompurify
npm install -D @types/dompurify
```

**Change line 325 from:**
```typescript
dangerouslySetInnerHTML={{ __html: getHtmlContent() }}
```

**To:**
```typescript
import DOMPurify from 'dompurify';

// ... in component:
dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(getHtmlContent()) }}
```

---

### 6. Wire Up Header Search
**File:** `src/components/Layout/AppHeader.tsx`

**Replace TODO handler (line 13-17):**
```typescript
import { useNavigate } from 'react-router-dom';

export function AppHeader() {
  const navigate = useNavigate();
  const [searchValue, setSearchValue] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchValue.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchValue)}`);
      setSearchValue('');
    }
  };
  
  // ... rest of component
}
```

---

### 7. Remove Duplicate Component
**Delete:** `src/components/Calculations/ParticleMassCalculator.tsx`
**Keep:** `src/components/Calculations/SimpleParticleCalculator.tsx`
**Update:** `src/pages/Calculations.tsx` to only use `SimpleParticleCalculator`

---

## Testing Checklist

After implementing fixes:

- [ ] Search index builds without errors
- [ ] Search finds results when index is ready
- [ ] Particle calculator displays results
- [ ] Neutrino calculator works with sample inputs
- [ ] Header search navigates to search page
- [ ] No XSS warnings in browser console
- [ ] Equation rendering shows all symbols correctly
- [ ] Theory TOC navigation works
- [ ] Print view removes sidebar

---

## Performance Optimization (Optional)

### Cache Pyodide
Add to `src/services/pythonEngine/pythonWorker.ts`:
```typescript
// Check IndexedDB for cached Pyodide
async function loadCachedPyodide() {
  const db = await idb.openDB('pyodide-cache', 1);
  const cached = await db.get('store', 'pyodide-v0.25.0');
  if (cached) {
    return cached;
  }
  // ... download and cache
}
```

---

## Files Modified Summary

| File | Change | Severity |
|------|--------|----------|
| pythonEngine.ts | Add fallback logic | CRITICAL |
| searchService.ts | Auto-initialize | CRITICAL |
| App.tsx | Init search | CRITICAL |
| neutrinoOscillationCalculator.ts | Create new | CRITICAL |
| TheoryDocViewer.tsx | Add DOMPurify | MEDIUM |
| AppHeader.tsx | Wire up search | MEDIUM |
| ParticleMassCalculator.tsx | Delete | MEDIUM |
| /public/data/ | Create JSON files | CRITICAL |

---

## Deployment Notes

1. Generate search data files BEFORE building
2. Test Pyodide fallback with disabled network
3. Test search with various query types
4. Verify equation rendering in prod
5. Check bundle size hasn't increased significantly

---

**Estimated Time:** 4-6 hours for all fixes
**Risk Level:** Low (backward compatible changes)
**Rollback:** Simple (all changes isolated)
