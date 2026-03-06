# Integration Guide: Python Calculation Engine

This guide shows how to integrate the Python calculation engine into your Golden Universe visualizer app.

## Quick Start

### 1. Add Calculation Page to Router

```tsx
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CalculationRunner } from './components/Calculations';
import { ParticleMassCalculatorUI } from './components/Calculations';
import { ResultsComparison } from './components/Calculations';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/calculations" element={<CalculationRunner />} />
        <Route path="/particles" element={<ParticleMassCalculatorUI />} />
        <Route path="/comparison" element={<ResultsComparison />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### 2. Test the Engine

Visit `http://localhost:5173/pyodide-loader.html` to test the standalone implementation.

## All Files Created

**Services (Python Engine):**
- ✅ `src/services/pythonEngine/pythonEngine.ts` - Main engine wrapper
- ✅ `src/services/pythonEngine/pythonWorker.ts` - Web Worker
- ✅ `src/services/pythonEngine/calculationQueue.ts` - Queue manager
- ✅ `src/services/pythonEngine/pythonTypes.ts` - TypeScript types
- ✅ `src/services/pythonEngine/index.ts` - Exports

**Calculations (Modules):**
- ✅ `src/calculations/particleMassCalculator.ts` - e, μ, τ, p masses
- ✅ `src/calculations/constantsCalculator.ts` - G, α, c_R
- ✅ `src/calculations/windingNumberCalculator.ts` - (p,q) winding
- ✅ `src/calculations/resonanceChecker.ts` - N/φ² resonances
- ✅ `src/calculations/memoryIntegralCalculator.ts` - R_mem
- ✅ `src/calculations/index.ts` - Exports

**Components (UI):**
- ✅ `src/components/Calculations/CalculationRunner.tsx` + `.scss`
- ✅ `src/components/Calculations/ParticleMassCalculator.tsx` + `.scss`
- ✅ `src/components/Calculations/ResultsComparison.tsx` + `.scss`
- ✅ `src/components/Calculations/CalculationHistory.tsx` + `.scss`
- ✅ `src/components/Calculations/index.ts` - Exports

**Data:**
- ✅ `src/data/calculations/presetCalculations.ts` - 15+ presets

**Documentation:**
- ✅ `PYTHON_ENGINE_README.md` - Complete API docs
- ✅ `public/pyodide-loader.html` - Standalone test page

## Quick Example

```tsx
import { ParticleMassCalculator } from './calculations';

async function calculateElectron() {
  const result = await ParticleMassCalculator.calculateElectron();
  console.log(`Electron mass: ${result.mass_MeV} MeV`);
  console.log(`Error: ${result.error_ppm} ppm`);
}
```

See `PYTHON_ENGINE_README.md` for full documentation!
