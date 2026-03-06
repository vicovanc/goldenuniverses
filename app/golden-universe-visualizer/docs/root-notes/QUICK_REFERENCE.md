# Golden Universe 3D Visualizations - Quick Reference Card

## 🚀 Quick Start

```bash
# Already installed - ready to use!
npm run dev
```

## 📦 Import

```tsx
// Gallery (recommended)
import { VisualizationGallery } from './components/Visualizations';

// Individual components
import {
  WindingNumbersVisualization,
  PhaseSpaceVisualization,
  MemoryEvolutionVisualization,
  EpochLadderVisualization,
  FieldDynamicsVisualization
} from './components/Visualizations';

// Utilities
import { PHI, calculateWindingPath } from './utils/three/goldenGeometry';
import { AnimationController } from './utils/three/animations';

// Data
import { PARTICLES, getParticle } from './data/visualizations/windingNumbers';
import { TRAJECTORIES } from './data/visualizations/phaseSpace';
```

## 🎯 Components at a Glance

| Component | Purpose | Key Feature |
|-----------|---------|-------------|
| **WindingNumbers** | 3D torus topology | (p,q) winding paths, resonance |
| **PhaseSpace** | Trajectory plots | 2D/3D mode, energy gradient |
| **MemoryEvolution** | M(t) time series | Decay envelope, oscillation |
| **EpochLadder** | Particle timeline | Formation epochs, N=0-1000 |
| **FieldDynamics** | Ω field surface | Real-time evolution, particles |

## 🎮 Controls

| Action | Mouse | Touch |
|--------|-------|-------|
| Orbit | Left drag | 1 finger |
| Pan | Right drag | 2 fingers |
| Zoom | Scroll | Pinch |

## 🔧 Key Constants

```typescript
PHI = 1.618033988749895      // Golden ratio
PHI_SQUARED = 2.618033988749895  // φ²
INV_PHI = 0.618033988749895   // 1/φ
```

## 📐 Key Formulas

```typescript
// Winding path
points = calculateWindingPath(p, q, R, r)

// Geodesic length
l_Ω = 2π√(p² + q²/φ²)

// Resonance
k_res = round(N / φ²)
isResonant = (k_res % 2 === 0)

// Memory
M(t) = M₀ exp(-t/τ) cos(ωt)

// Field
Ω(r,t) = A exp(-r²/2) cos(ωr - φt)
```

## 🎨 Particles

| Particle | Symbol | p | Formation Epoch |
|----------|--------|---|-----------------|
| Electron | e | 1 | N=100 |
| Muon | μ | 2 | N=300 |
| Tau | τ | 3 | N=600 |
| Up | u | 1 | N=80 |
| Charm | c | 2 | N=400 |
| Top | t | 3 | N=900 |

## 📊 Performance Tips

```typescript
// Reduce resolution
controls.resolution = 32  // vs 128

// Lower particle count
controls.particleCount = 50  // vs 500

// Disable heavy features
controls.showEnergy = false
controls.showParticles = false
```

## 🐛 Quick Fixes

**Black screen?**
```javascript
// Check WebGL
console.log(!!document.createElement('canvas').getContext('webgl2'))
```

**Low FPS?**
- Reduce resolution
- Lower particle count
- Disable energy gradient

**Types missing?**
```bash
npm install @types/three
```

## 📁 Key Files

```
src/
├── components/Visualizations/
│   ├── WindingNumbersVisualization.tsx    # Torus
│   ├── PhaseSpaceVisualization.tsx        # Phase
│   ├── MemoryEvolutionVisualization.tsx   # Memory
│   ├── EpochLadderVisualization.tsx       # Epochs
│   ├── FieldDynamicsVisualization.tsx     # Field
│   └── VisualizationGallery.tsx           # Gallery
├── utils/three/
│   ├── goldenGeometry.ts                  # Geometry
│   ├── shaders.ts                         # GLSL
│   └── animations.ts                      # Animate
└── data/visualizations/
    ├── windingNumbers.ts                  # Particles
    └── phaseSpace.ts                      # Trajectories
```

## 🔗 Usage Examples

### Example 1: Show Electron at Epoch 100
```tsx
<WindingNumbersVisualization />
// GUI: Set N=100, particle="Electron"
```

### Example 2: Phase Space Trajectory
```tsx
<PhaseSpaceVisualization />
// GUI: Toggle 2D/3D, select trajectories
```

### Example 3: Memory Decay
```tsx
<MemoryEvolutionVisualization />
// GUI: Adjust M0, tau, omega
```

### Example 4: Particle Timeline
```tsx
<EpochLadderVisualization />
// GUI: Slide N=0-1000, auto-play
```

### Example 5: Field Evolution
```tsx
<FieldDynamicsVisualization />
// GUI: Amplitude, frequency, resolution
```

## 📚 Documentation

- **Quick Start:** `QUICKSTART_VISUALIZATIONS.md`
- **Full Guide:** `VISUALIZATION_IMPLEMENTATION_GUIDE.md`
- **Summary:** `VISUALIZATION_SUMMARY.md`
- **Component Docs:** `src/components/Visualizations/README.md`

## ✅ Checklist

- [x] Dependencies installed
- [x] Components created
- [x] Utilities implemented
- [x] Data populated
- [x] Documentation written
- [x] TypeScript compiled
- [ ] Integrated into app (your step)
- [ ] Routes configured (your step)

## 🎉 You're Ready!

```tsx
// Add to your app
import { VisualizationGallery } from './components/Visualizations';

function App() {
  return <VisualizationGallery />;
}
```

---

**Status:** ✅ Complete | **Files:** 24 | **Ready:** Yes
