# Golden Universe 3D Visualizations

Interactive Three.js visualizations for exploring the Golden Ratio universe theory.

## Components

### 1. WindingNumbersVisualization
**File:** `WindingNumbersVisualization.tsx`

3D torus with animated (p,q) winding paths showing particle topologies.

**Features:**
- Golden ratio torus geometry (R, r = R/φ)
- Animated winding paths for each particle
- Epoch slider (N = 0 to 1000)
- Resonance indicator (k_res = round(N/φ²))
- Color coding: green (resonant), red (anti-resonant)
- Geodesic length display: l_Ω = 2π√(p² + q²/φ²)
- Interactive camera controls

**Controls:**
- `N`: Epoch number (0-1000)
- `particle`: Select particle type
- `showTorus`: Toggle torus visibility
- `showPath`: Toggle winding path
- `animatePath`: Enable path animation
- `pathSpeed`: Animation speed

**Physics:**
Each Standard Model particle has unique winding numbers (p,q) that determine its topology on the torus. Resonance states occur at even k_res values.

### 2. PhaseSpaceVisualization
**File:** `PhaseSpaceVisualization.tsx`

Interactive 2D/3D phase space trajectory plots.

**Features:**
- 2D mode: (ρ, π_ρ) plane
- 3D mode: (ρ, π_ρ, θ) space
- Multiple trajectory overlays
- Energy density gradient coloring
- Real-time particle markers
- Multiple trajectory types (harmonic, golden, torus knots)

**Controls:**
- `mode`: Toggle 2D/3D view
- `showEnergy`: Display energy gradient
- `showParticles`: Show moving particles
- `animate`: Enable animation
- `speed`: Animation speed

**Trajectories:**
- Harmonic Oscillator: Simple periodic motion
- Golden Ratio: Quasi-periodic with φ frequency
- Torus Knots: (p,q) winding paths
- Damped Oscillator: Decaying spiral

### 3. MemoryEvolutionVisualization
**File:** `MemoryEvolutionVisualization.tsx`

Time evolution of the memory integral M(t).

**Features:**
- Memory function: M(t) = M₀ exp(-t/τ) cos(ωt)
- Decay envelope visualization
- Energy bar indicator
- Parameter controls

**Controls:**
- `M0`: Initial memory amplitude
- `tau`: Decay time constant
- `omega`: Oscillation frequency (default: φ)
- `tMax`: Time range

**Physics:**
The memory integral tracks how the system "remembers" past states. Decay at rate 1/τ with oscillations at golden ratio frequency.

### 4. EpochLadderVisualization
**File:** `EpochLadderVisualization.tsx`

Animated descent through epochs showing particle formation timeline.

**Features:**
- Vertical ladder from N=0 to N=1000
- Particle formation markers
- Resonance state coloring
- 3D particle cloud
- Auto-scroll to current epoch

**Controls:**
- `N`: Current epoch
- `autoPlay`: Auto-advance epochs
- `speed`: Animation speed
- `showParticles`: Toggle particle cloud

**Key Epochs:**
- N=50: Electron neutrino
- N=80: Up/down quarks
- N=100: Electron
- N=300: Muon
- N=600: Tau
- N=1000: Complete Standard Model

### 5. FieldDynamicsVisualization
**File:** `FieldDynamicsVisualization.tsx`

Real-time Omega field evolution with energy visualization.

**Features:**
- 3D field surface: Ω(r,t) = A exp(-r²/2) cos(ωr - φt)
- Energy particle system
- Field lines (optional)
- GPU-accelerated computation
- Custom shaders

**Controls:**
- `amplitude`: Field amplitude A
- `frequency`: Wave frequency ω
- `resolution`: Surface mesh resolution
- `showSurface`: Toggle field surface
- `showFieldLines`: Toggle field lines
- `showParticles`: Toggle energy particles

**Physics:**
Omega field represents the fundamental quantum field. Wave packets propagate with golden ratio phase velocity.

## Usage

### Basic Setup

```tsx
import { WindingNumbersVisualization } from '@/components/Visualizations';

function App() {
  return <WindingNumbersVisualization />;
}
```

### Gallery View

```tsx
import { VisualizationGallery } from '@/components/Visualizations';

function App() {
  return <VisualizationGallery />;
}
```

## Utilities

### Golden Geometry (`utils/three/goldenGeometry.ts`)

```typescript
import {
  PHI,
  createGoldenTorus,
  calculateWindingPath,
  calculateGeodesicLength
} from '@/utils/three/goldenGeometry';

// Create torus with golden proportions
const torus = createGoldenTorus(2, 2/PHI);

// Calculate winding path
const points = calculateWindingPath(p, q, R, r);

// Get geodesic length
const length = calculateGeodesicLength(p, q);
```

### Shaders (`utils/three/shaders.ts`)

Custom GLSL shaders for field visualization:
- `fieldVertexShader`: Basic vertex shader
- `energyDensityShader`: Energy-based coloring
- `phaseSpaceShader`: Golden ratio patterns
- `windingPathShader`: Animated path rendering

### Animations (`utils/three/animations.ts`)

```typescript
import { AnimationController, easing, cameraPresets } from '@/utils/three/animations';

// Create animation controller
const controller = new AnimationController();
controller.play();
controller.on('update', (state) => {
  // Handle animation state
});

// Animate camera
animateCameraToPreset(camera, cameraPresets.top);
```

## Data

### Winding Numbers (`data/visualizations/windingNumbers.ts`)

Particle data with winding number calculations:

```typescript
import { PARTICLES, getParticle, getWindingNumbers } from '@/data/visualizations/windingNumbers';

// Get particle info
const electron = getParticle('Electron');

// Calculate winding numbers at epoch
const { p, q } = electron.getWindingNumbers(100);
```

### Phase Space (`data/visualizations/phaseSpace.ts`)

Trajectory data and generators:

```typescript
import { TRAJECTORIES, generateGoldenTrajectory } from '@/data/visualizations/phaseSpace';

// Get predefined trajectory
const harmonic = TRAJECTORIES.find(t => t.id === 'harmonic');

// Generate custom trajectory
const golden = generateGoldenTrajectory(amplitude, samples);
```

## Performance Optimization

### LOD (Level of Detail)
- Automatically reduces geometry complexity at distance
- Configurable thresholds

### Instanced Rendering
- Used for particle systems
- Minimal draw calls

### GPU Computation
- Custom shaders for field calculations
- WebGL 2.0 required

### Target Performance
- 60 FPS on modern hardware
- 30 FPS minimum on integrated GPUs
- Mobile: 30 FPS with reduced quality

## Controls

### Mouse
- **Left click + drag**: Orbit camera
- **Right click + drag**: Pan camera
- **Scroll wheel**: Zoom in/out

### Touch
- **One finger**: Orbit
- **Two fingers**: Pan and zoom

### GUI
- **Leva controls**: Top-right panel
- **Real-time parameter adjustment**
- **Collapsible folders**

## Browser Support

- **Chrome/Edge**: Full support (recommended)
- **Firefox**: Full support
- **Safari**: Limited (WebGL 2.0 issues)
- **Mobile**: iOS Safari 15+, Chrome Android

## Dependencies

```json
{
  "@react-three/fiber": "^8.x",
  "@react-three/drei": "^9.x",
  "@react-three/postprocessing": "^2.x",
  "three": "^0.160.x",
  "leva": "^0.9.x"
}
```

## Future Enhancements

1. **VR Support**: WebXR integration for immersive viewing
2. **Export**: PNG/SVG export for trajectories
3. **Recording**: Video capture of animations
4. **Multi-particle**: Compare multiple particles simultaneously
5. **Custom Shaders**: User-defined field equations
6. **Performance**: WebGPU support when available

## Contributing

When adding new visualizations:

1. Create component in `src/components/Visualizations/`
2. Add data files in `src/data/visualizations/`
3. Create utilities in `src/utils/three/` if needed
4. Add to `VisualizationGallery.tsx`
5. Update this README

## License

Part of the Golden Universe project.
