/**
 * Winding Numbers Visualization
 * 3D torus with animated (p,q) winding paths showing particle topologies
 */

import React, { useRef, useMemo, useState, useEffect, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Text } from '@react-three/drei';
import { useControls, folder } from 'leva';
import * as THREE from 'three';
import {
  createGoldenTorus,
  calculateWindingPath,
  calculateGeodesicLength,
  calculateResonance,
  isResonant,
  resonanceColor,
  PHI,
  createTubePath,
} from '../../utils/three/goldenGeometry';
import { getParticle, PARTICLES } from '../../data/visualizations/windingNumbers';
import './WindingNumbersVisualization.scss';

interface WindingPathProps {
  p: number;
  q: number;
  R: number;
  r: number;
  color: THREE.Color;
  animate: boolean;
  speed: number;
}

function WindingPath({ p, q, R, r, color, animate, speed }: WindingPathProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [progress, setProgress] = useState(0);

  const points = useMemo(() => {
    return calculateWindingPath(p, q, R, r, 500);
  }, [p, q, R, r]);

  const geometry = useMemo(() => {
    const displayPoints = points.slice(0, Math.floor(points.length * (animate ? progress : 1)));
    if (displayPoints.length < 2) return null;
    return createTubePath(displayPoints, 0.03, 8);
  }, [points, progress, animate]);

  useFrame((_, delta) => {
    if (animate) {
      setProgress((prev) => {
        const next = prev + speed * delta;
        return next > 1 ? 0 : next;
      });
    }
  });

  if (!geometry) return null;

  return (
    <mesh ref={meshRef} geometry={geometry}>
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.3} />
    </mesh>
  );
}

interface TorusWithWindingProps {
  epoch: number;
  particleName: string;
  showTorus: boolean;
  showPath: boolean;
  animatePath: boolean;
  pathSpeed: number;
}

function TorusWithWinding({
  epoch,
  particleName,
  showTorus,
  showPath,
  animatePath,
  pathSpeed,
}: TorusWithWindingProps) {
  const torusRef = useRef<THREE.Mesh>(null);
  const particle = getParticle(particleName);

  const { p, q } = useMemo(() => {
    if (!particle) return { p: 1, q: 1 };
    return particle.getWindingNumbers(epoch);
  }, [particle, epoch]);

  const k_res = useMemo(() => calculateResonance(epoch), [epoch]);
  const resonant = useMemo(() => isResonant(k_res), [k_res]);
  const pathColor = useMemo(() => resonanceColor(k_res), [k_res]);

  const R = 2;
  const r = R / PHI;

  const torusGeometry = useMemo(() => createGoldenTorus(R, r), [R, r]);

  useFrame((_, delta) => {
    if (torusRef.current && showTorus) {
      torusRef.current.rotation.y += 0.2 * delta;
    }
  });

  return (
    <group>
      {showTorus && (
        <mesh ref={torusRef} geometry={torusGeometry}>
          <meshStandardMaterial
            color="#404040"
            transparent
            opacity={0.3}
            wireframe={false}
            side={THREE.DoubleSide}
          />
        </mesh>
      )}

      {showPath && particle && (
        <WindingPath
          p={p}
          q={q}
          R={R}
          r={r}
          color={pathColor}
          animate={animatePath}
          speed={pathSpeed}
        />
      )}

      {/* Particle label */}
      {particle && (
        <Text
          position={[0, R + r + 0.5, 0]}
          fontSize={0.3}
          color={particle.color}
          anchorX="center"
          anchorY="middle"
        >
          {particle.symbol}
        </Text>
      )}

      {/* Info labels */}
      <Text
        position={[-3, 2.5, 0]}
        fontSize={0.15}
        color="#ffffff"
        anchorX="left"
        anchorY="middle"
      >
        {`Epoch N = ${epoch}`}
      </Text>
      <Text
        position={[-3, 2.2, 0]}
        fontSize={0.15}
        color="#ffffff"
        anchorX="left"
        anchorY="middle"
      >
        {`k_res = ${k_res} (${resonant ? 'Resonant' : 'Anti-resonant'})`}
      </Text>
      <Text
        position={[-3, 1.9, 0]}
        fontSize={0.15}
        color="#ffffff"
        anchorX="left"
        anchorY="middle"
      >
        {`Winding: (p=${p}, q=${q})`}
      </Text>
      <Text
        position={[-3, 1.6, 0]}
        fontSize={0.15}
        color="#ffffff"
        anchorX="left"
        anchorY="middle"
      >
        {`l_Ω = ${calculateGeodesicLength(p, q).toFixed(3)}`}
      </Text>
    </group>
  );
}

function Scene() {
  const controls = useControls({
    Epoch: folder({
      N: { value: 100, min: 0, max: 1000, step: 10 },
    }),
    Particle: folder({
      particle: {
        value: 'Electron',
        options: PARTICLES.map((p) => p.name),
      },
    }),
    Display: folder({
      showTorus: true,
      showPath: true,
      animatePath: { value: true, label: 'Animate Path' },
      pathSpeed: { value: 0.5, min: 0.1, max: 2, step: 0.1 },
      showGrid: { value: true, label: 'Show Grid' },
    }),
    Camera: folder({
      preset: {
        value: 'default',
        options: ['default', 'top', 'side', 'front'],
      },
    }),
  }); // Remove store option that's causing the error

  const cameraPosition = useMemo(() => {
    const positions: Record<string, [number, number, number]> = {
      default: [5, 3, 5],
      top: [0, 8, 0],
      side: [8, 0, 0],
      front: [0, 0, 8],
    };
    return positions[controls.preset as keyof typeof positions] || positions.default;
  }, [controls.preset]);

  return (
    <>
      <PerspectiveCamera makeDefault position={cameraPosition} />
      <OrbitControls enableDamping dampingFactor={0.05} />

      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} intensity={1} />
      <directionalLight position={[-5, -5, -5]} intensity={0.3} />
      <pointLight position={[0, 0, 0]} intensity={0.5} color="#ffffff" />

      <TorusWithWinding
        epoch={controls.N}
        particleName={controls.particle}
        showTorus={controls.showTorus}
        showPath={controls.showPath}
        animatePath={controls.animatePath}
        pathSpeed={controls.pathSpeed}
      />

      {controls.showGrid && <gridHelper args={[20, 20, '#444444', '#666666']} />}
    </>
  );
}

export function WindingNumbersVisualization() {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    // Small delay to ensure DOM is ready
    const timer = setTimeout(() => {
      setIsReady(true);
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  if (!isReady) {
    return (
      <div className="winding-numbers-visualization">
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100%',
          color: 'white'
        }}>
          Loading visualization...
        </div>
      </div>
    );
  }

  return (
    <div className="winding-numbers-visualization">
      <Canvas
        gl={{
          preserveDrawingBuffer: true,
          antialias: true,
          alpha: false,
          powerPreference: 'high-performance',
          failIfMajorPerformanceCaveat: false,
        }}
        camera={{ position: [5, 3, 5], fov: 50 }}
        onCreated={({ gl }) => {
          gl.setPixelRatio(Math.min(window.devicePixelRatio, 2));
          // Prevent context loss
          const canvas = gl.domElement;
          canvas.addEventListener('webglcontextlost', (e) => {
            e.preventDefault();
            console.warn('WebGL context lost, preventing default behavior');
          });
          canvas.addEventListener('webglcontextrestored', () => {
            console.log('WebGL context restored');
          });
        }}
        frameloop="always"
        dpr={[1, 2]}
      >
        <Suspense fallback={null}>
          <Scene />
        </Suspense>
      </Canvas>
    </div>
  );
}

export default WindingNumbersVisualization;
