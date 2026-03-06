# Python Calculation Engine with Pyodide

Complete implementation of the Golden Universe calculation engine running Python directly in the browser using Pyodide (Python in WebAssembly).

## Overview

This implementation provides:
- **Pyodide Integration**: Python 3.11 running in WebAssembly
- **Web Worker Architecture**: Non-blocking calculations in background thread
- **High-Precision Math**: 50+ decimal places using mpmath
- **Queue Management**: Handle multiple concurrent calculations
- **React UI Components**: Interactive interfaces for calculations
- **Preset Calculations**: Ready-to-run Golden Universe formulas
- **Result Comparison**: Compare with CODATA experimental values

## Architecture

```
src/
├── services/pythonEngine/
│   ├── pythonEngine.ts         # Main engine wrapper
│   ├── pythonWorker.ts         # Web Worker for Python execution
│   ├── calculationQueue.ts     # Queue management
│   └── pythonTypes.ts          # TypeScript type definitions
│
├── calculations/
│   ├── particleMassCalculator.ts    # Particle masses (e, μ, τ, p)
│   ├── constantsCalculator.ts       # G, α, c_R
│   ├── windingNumberCalculator.ts   # (p,q) winding numbers
│   ├── resonanceChecker.ts          # N/φ² resonances
│   └── memoryIntegralCalculator.ts  # R_mem evolution
│
├── components/Calculations/
│   ├── CalculationRunner.tsx        # Main interface with code editor
│   ├── ParticleMassCalculator.tsx   # Dedicated particle mass UI
│   ├── ResultsComparison.tsx        # CODATA comparison
│   └── CalculationHistory.tsx       # Previous calculations log
│
└── data/calculations/
    └── presetCalculations.ts        # Preset calculation definitions
```

## Installation

No additional npm packages are required! Pyodide is loaded from CDN at runtime.

The existing project already has all necessary dependencies:
- React 19.2.0
- TypeScript 5.9.3
- Vite 7.3.1

## Usage

### 1. Initialize the Engine

```typescript
import { getPythonEngine } from './services/pythonEngine';

const engine = getPythonEngine();

// Initialize (loads Pyodide and scientific packages)
await engine.initialize();
```

### 2. Calculate Electron Mass

```typescript
import { ParticleMassCalculator } from './calculations/particleMassCalculator';

const result = await ParticleMassCalculator.calculateElectron({
  precision: 50,
  includeCorrections: true,
});

console.log(result.mass_MeV);           // "0.51099906774"
console.log(result.error_ppm);          // 23
console.log(result.epoch.N);            // 111
console.log(result.winding);            // { p: -41, q: 70 }
```

### 3. Calculate Newton's G

```typescript
import { ConstantsCalculator } from './calculations/constantsCalculator';

const result = await ConstantsCalculator.calculateNewtonsG();

console.log(result.theoretical_value);   // "6.67433e-11"
console.log(result.error_ppm);           // 47
```

### 4. Find Resonances

```typescript
import { ResonanceChecker } from './calculations/resonanceChecker';

const resonances = await ResonanceChecker.findResonances(1, 200, 0.5);

resonances.forEach(r => {
  console.log(`N=${r.N}, k=${r.k_res}, δ=${r.delta}`);
});
```

### 5. Execute Custom Python Code

```typescript
const code = `
# Calculate with high precision
mp.dps = 50

# Golden ratio and electron mass
phi = PHI
m_e = calculate_electron_mass(NU_E)

result = {
    'phi': str(phi),
    'mass': m_e
}

to_json(result)
`;

const result = await engine.execute(code);
console.log(result);
```

## React Components

### CalculationRunner

Main interface with code editor and preset selection:

```tsx
import { CalculationRunner } from './components/Calculations';

function App() {
  return <CalculationRunner />;
}
```

Features:
- Monaco-style code editor
- Preset calculation library
- Real-time execution
- JSON result display
- Syntax highlighting

### ParticleMassCalculator

Dedicated UI for particle mass calculations:

```tsx
import { ParticleMassCalculatorUI } from './components/Calculations';

function App() {
  return <ParticleMassCalculatorUI />;
}
```

Features:
- Visual particle selection (e, μ, τ, p)
- Formula breakdown (3 terms)
- Epoch parameters display
- Winding numbers visualization
- CODATA comparison

### ResultsComparison

Compare theoretical predictions with experimental values:

```tsx
import { ResultsComparison } from './components/Calculations';

function App() {
  return <ResultsComparison />;
}
```

Features:
- Side-by-side comparison table
- Precision indicators (ppm)
- Match quality badges
- Sort by precision or name
- Export to CSV

### CalculationHistory

Track and export previous calculations:

```tsx
import { CalculationHistory } from './components/Calculations';

function App() {
  return <CalculationHistory />;
}
```

Features:
- Search and filter
- Export JSON/CSV
- Delete entries
- Execution time tracking
- Success/failure indicators

## Preset Calculations

The system includes 15+ preset calculations:

### Particle Masses
- **electron_mass_23ppm**: Electron mass (23 ppm accuracy)
- **muon_mass**: Muon mass with generation factor
- **tau_mass**: Tau mass with generation factor
- **proton_mass_5term**: Proton mass (5-term ansatz)

### Fundamental Constants
- **newtons_g_47ppm**: Newton's G (47 ppm accuracy)
- **fine_structure_alpha**: α = (e^φ/π²)/70
- **lambda_rec_beta**: Memory kernel ratio

### Resonances
- **electron_resonance**: N=111 resonance check
- **resonance_scan_1_200**: Find all resonances
- **strong_resonances**: Strong resonances (δ < 0.1)

### Advanced
- **electron_winding**: (p,q) = (-41, 70)
- **all_leptons**: Calculate e, μ, τ together
- **complete_c_e_breakdown**: Full C_e formula

Access presets:

```typescript
import { PRESET_CALCULATIONS, getFeaturedPresets } from './data/calculations/presetCalculations';

const featured = getFeaturedPresets();
const electronPreset = PRESET_CALCULATIONS.find(p => p.id === 'electron_mass_23ppm');
```

## Python Functions Available

The Pyodide environment pre-loads these functions:

### Constants
```python
PHI              # Golden ratio φ = 1.618...
PI               # π = 3.14159...
E                # e = 2.71828...
PHI_SQ           # φ² = 2.618...
M_P_MeV          # Planck mass = 1.2209 × 10²² MeV
N_E              # Electron epoch = 111
DELTA_E          # Detuning = 0.39822...
P_E, Q_E         # Winding = -41, 70
L_OMEGA_E        # Geometric length = 374.502...
LAMBDA_REC_BETA  # Memory ratio = 0.51097...
NU_E             # Optimal ν = 0.91168...
```

### Functions
```python
epoch_pi(n)                    # π_n = n·sin(π/n)
epoch_phi(n)                   # φ_n = F_{n+1}/F_n
calculate_winding_length(p, q) # l_Ω = 2π√(p² + (q/φ)²)
calculate_resonance(N)         # k_res, δ = N/φ² - k
calculate_C_e_complete(ν)      # Complete C_e formula
calculate_electron_mass(ν)     # Electron mass
calculate_newtons_g()          # Newton's G
calculate_fine_structure()     # Fine structure α
```

## Performance

- **Initialization**: ~5-10 seconds (one-time, cached)
- **Simple calculation**: 10-50 ms
- **Electron mass**: 50-100 ms
- **Resonance scan (200 epochs)**: 200-500 ms
- **Memory**: ~50 MB for Pyodide + packages

## Precision

All calculations use mpmath with 50 decimal places:

```python
mp.dps = 50  # 50 decimal places

phi = mp.phi  # 1.6180339887498948482045868343656381177203091798058...
```

Results are returned as strings to preserve precision:

```typescript
result.mass_MeV  // "0.51099906774..." (string)
parseFloat(result.mass_MeV)  // 0.51099906774 (number)
```

## Error Handling

The engine includes comprehensive error handling:

```typescript
try {
  const result = await engine.execute(code);
  if (result.success) {
    console.log(result.result);
  } else {
    console.error(result.error);
  }
} catch (error) {
  console.error('Execution failed:', error);
}
```

## Queue Management

Multiple calculations are queued and executed efficiently:

```typescript
import { getCalculationQueue } from './services/pythonEngine';

const queue = getCalculationQueue();

// Add with priority
const id1 = queue.enqueue(input1, priority: 10);
const id2 = queue.enqueue(input2, priority: 5);

// Check status
const status = queue.getStatus(id1);
console.log(status.status);  // 'queued' | 'running' | 'completed'

// Subscribe to updates
const unsubscribe = queue.subscribe(id1, (calc) => {
  console.log(`Progress: ${calc.progress}%`);
});

// Get statistics
const stats = queue.getStats();
console.log(`Queued: ${stats.queued}, Running: ${stats.running}`);
```

## Export Results

### JSON Export
```typescript
const history = getCalculationHistory();
const dataStr = JSON.stringify(history, null, 2);
// Download or save
```

### CSV Export
```typescript
const headers = ['Timestamp', 'Type', 'Result', 'Error (ppm)'];
const csv = generateCSV(history);
// Download or save
```

### Share via URL
```typescript
const url = new URL(window.location.href);
url.searchParams.set('preset', 'electron_mass_23ppm');
// Share URL
```

## Browser Compatibility

Requires WebAssembly support:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14.1+
- ✅ Edge 90+

## Troubleshooting

### Engine won't initialize
- Check browser WebAssembly support
- Verify CDN access to `cdn.jsdelivr.net`
- Check browser console for errors

### Slow calculations
- First run is slower (Pyodide loading)
- Subsequent calculations are cached
- Use Web Worker to avoid blocking UI

### Memory issues
- Clear calculation history
- Reduce concurrent calculations
- Use `queue.setMaxConcurrent(1)`

## Advanced Usage

### Custom Precision

```typescript
const code = `
mp.dps = 100  # 100 decimal places

result = mp.sqrt(2)
str(result)
`;

const result = await engine.execute(code);
```

### Numerical Integration

```python
from scipy import integrate

def integrand(x):
    return float(mp.exp(-x**2))

result, error = integrate.quad(integrand, 0, mp.inf)
```

### Root Finding

```python
from scipy import optimize

def equation(x):
    return float(x**2 - 2)

root = optimize.brentq(equation, 0, 2)
```

## Production Deployment

For production, consider:

1. **Host Pyodide locally**: Download from CDN and serve from your domain
2. **Service Worker caching**: Cache Pyodide files for offline use
3. **Progressive loading**: Load packages on-demand
4. **Error tracking**: Monitor initialization failures
5. **Performance monitoring**: Track execution times

## Future Enhancements

Planned features:
- [ ] 3D visualization of torus winding
- [ ] Interactive parameter sliders
- [ ] Batch calculation mode
- [ ] LaTeX formula rendering
- [ ] Share calculation links
- [ ] Collaborative sessions
- [ ] Jupyter notebook export

## License

Part of the Golden Universe Visualizer project.

## Support

For issues or questions:
- Check browser console for errors
- Review TypeScript types for API usage
- See preset calculations for examples
- Consult Pyodide documentation: https://pyodide.org
