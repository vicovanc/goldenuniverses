# Quick Start: Golden Universe 3D Visualizations

## 🚀 Getting Started

### 1. Dependencies Already Installed ✅
```bash
# Already completed - no action needed
npm install @react-three/fiber @react-three/drei @react-three/postprocessing three leva
```

### 2. Run the Development Server
```bash
npm run dev
```

### 3. Import and Use

#### Option A: Use the Gallery (Recommended)
```tsx
import { VisualizationGallery } from './components/Visualizations';

function App() {
  return <VisualizationGallery />;
}
```

#### Option B: Use Individual Visualizations
```tsx
import { WindingNumbersVisualization } from './components/Visualizations';

function App() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <WindingNumbersVisualization />
    </div>
  );
}
```

## 📦 What's Included

### 5 Complete Visualizations

1. **WindingNumbersVisualization** - 3D torus with (p,q) winding paths
2. **PhaseSpaceVisualization** - Interactive phase space trajectories
3. **MemoryEvolutionVisualization** - Memory integral M(t) evolution
4. **EpochLadderVisualization** - Particle formation timeline
5. **FieldDynamicsVisualization** - Omega field dynamics

### Utilities
- `goldenGeometry.ts` - Golden ratio geometry helpers
- `shaders.ts` - Custom GLSL shaders
- `animations.ts` - Animation controllers

### Data
- `windingNumbers.ts` - Particle winding data
- `phaseSpace.ts` - Phase space trajectories

## 🎮 Controls

### Mouse
- **Left Drag**: Orbit camera
- **Right Drag**: Pan camera
- **Scroll**: Zoom in/out

### Touch
- **One Finger**: Orbit
- **Two Fingers**: Pan/Zoom

### GUI
- **Top Right**: Leva control panel
- Adjust parameters in real-time

## 📁 File Structure

```
src/
├── components/Visualizations/
│   ├── WindingNumbersVisualization.tsx/.scss
│   ├── PhaseSpaceVisualization.tsx/.scss
│   ├── MemoryEvolutionVisualization.tsx/.scss
│   ├── EpochLadderVisualization.tsx/.scss
│   ├── FieldDynamicsVisualization.tsx/.scss
│   ├── VisualizationGallery.tsx/.scss
│   ├── index.ts
│   └── README.md
├── utils/three/
│   ├── goldenGeometry.ts
│   ├── shaders.ts
│   ├── animations.ts
│   └── index.ts
└── data/visualizations/
    ├── windingNumbers.ts
    ├── phaseSpace.ts
    └── index.ts
```

## 🔧 Common Use Cases

### 1. Show Electron Winding at Epoch 100
```tsx
import { WindingNumbersVisualization } from './components/Visualizations';

// The component has GUI controls to:
// - Set N = 100
// - Select particle = "Electron"
// - View the (p,q) winding path
```

### 2. Display Phase Space Trajectory
```tsx
import { PhaseSpaceVisualization } from './components/Visualizations';

// Interactive controls to:
// - Toggle 2D/3D mode
// - Show energy gradient
// - Animate particle motion
```

### 3. Visualize Memory Decay
```tsx
import { MemoryEvolutionVisualization } from './components/Visualizations';

// Parameters available:
// - M0: Initial amplitude
// - tau: Decay time
// - omega: Frequency (default φ)
```

### 4. Show Epoch Ladder
```tsx
import { EpochLadderVisualization } from './components/Visualizations';

// Features:
// - Scroll through epochs 0-1000
// - See when particles form
// - Auto-play animation
```

### 5. Field Dynamics
```tsx
import { FieldDynamicsVisualization } from './components/Visualizations';

// Control:
// - Field amplitude
// - Wave frequency
// - Surface resolution
```

## 🎨 Customization Examples

### Change Colors
```tsx
// In windingNumbers.ts
const PARTICLES = [
  {
    name: 'Electron',
    color: '#00ffff', // Change this hex color
    // ...
  }
];
```

### Adjust Camera Position
```tsx
// In any visualization component
<PerspectiveCamera
  makeDefault
  position={[8, 6, 8]}  // Change X, Y, Z
/>
```

### Modify Animation Speed
```tsx
// In controls
const controls = useControls({
  Animation: folder({
    speed: { value: 1.5, min: 0.1, max: 3 } // Adjust defaults
  })
});
```

## 🐛 Troubleshooting

### Issue: Black screen
**Solution**: Check browser WebGL support
```javascript
// In browser console
const gl = document.createElement('canvas').getContext('webgl2');
console.log(gl ? 'WebGL 2.0 supported' : 'WebGL 2.0 not supported');
```

### Issue: Low FPS
**Solutions**:
- Reduce resolution in GUI
- Lower particle count
- Disable energy gradient
- Close other apps

### Issue: GUI not showing
**Solution**: Check CSS import
```tsx
// Make sure Leva styles are imported
import 'leva/dist/styles.css'; // If needed
```

## 📚 Learn More

- **Full Documentation**: See `VISUALIZATION_IMPLEMENTATION_GUIDE.md`
- **Component Docs**: See `src/components/Visualizations/README.md`
- **Three.js Docs**: https://threejs.org/docs/
- **React Three Fiber**: https://docs.pmnd.rs/react-three-fiber/

## 🎯 Key Concepts

### Golden Ratio (φ)
```typescript
const PHI = (1 + Math.sqrt(5)) / 2; // 1.618...
```

### Winding Numbers
- **p**: Poloidal winding (around minor axis)
- **q**: Toroidal winding (around major axis)
- Path traces (p,q) times around torus

### Resonance
```typescript
k_res = round(N / φ²)
isResonant = k_res % 2 === 0  // Even = green, Odd = red
```

### Phase Space
- **ρ**: Radial coordinate
- **θ**: Angular coordinate
- **π_ρ**: Radial momentum
- **π_θ**: Angular momentum

## ✨ Quick Tips

1. **Start with Gallery**: See all visualizations in one place
2. **Use GUI Controls**: Real-time parameter adjustment
3. **Try Presets**: Camera preset buttons for best views
4. **Enable Animation**: Watch evolution over time
5. **Fullscreen Mode**: For presentations and demos

## 🚀 Next Steps

1. **Integrate into App**: Add to your router/navigation
2. **Customize**: Adjust colors, parameters, layouts
3. **Extend**: Add new visualizations following patterns
4. **Share**: Export images/videos (feature coming)

## 📝 Example Integration

```tsx
// App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { VisualizationGallery } from './components/Visualizations';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/visualizations" element={<VisualizationGallery />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## 🎉 You're Ready!

All visualizations are fully implemented and ready to use. Start the dev server and explore!

```bash
npm run dev
```

Navigate to the visualizations page and enjoy exploring the Golden Universe in 3D!
