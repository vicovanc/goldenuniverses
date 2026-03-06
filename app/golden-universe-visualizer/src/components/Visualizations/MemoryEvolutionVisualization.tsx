/**
 * Memory Evolution Visualization
 * Shows the time evolution of the memory integral M(t)
 */

import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Line, Text } from '@react-three/drei';
import { useControls, folder } from 'leva';
import * as THREE from 'three';
import { PHI } from '../../utils/three/goldenGeometry';
import './MemoryEvolutionVisualization.scss';

interface MemoryDataPoint {
  t: number;
  M: number;
  energy: number;
}

/**
 * Calculate memory integral evolution
 * M(t) ≈ M₀ exp(-t/τ) cos(ωt + φ)
 */
function calculateMemoryEvolution(
  tMax: number = 10,
  samples: number = 500,
  M0: number = 1,
  tau: number = 5,
  omega: number = PHI
): MemoryDataPoint[] {
  const points: MemoryDataPoint[] = [];
  const dt = tMax / samples;

  for (let i = 0; i <= samples; i++) {
    const t = i * dt;
    const decay = Math.exp(-t / tau);
    const oscillation = Math.cos(omega * t);
    const M = M0 * decay * oscillation;
    const energy = 0.5 * M * M;

    points.push({ t, M, energy });
  }

  return points;
}

interface MemoryPlotProps {
  data: MemoryDataPoint[];
  color: string;
  showEnvelope: boolean;
  animate: boolean;
  progress: number;
}

function MemoryPlot({ data, color, showEnvelope, animate, progress }: MemoryPlotProps) {
  const displayCount = animate ? Math.floor(data.length * progress) : data.length;
  const displayData = data.slice(0, displayCount);

  const points = useMemo(() => {
    return displayData.map((p) => new THREE.Vector3(p.t * 0.8, p.M * 2, 0));
  }, [displayData]);

  const envelopePoints = useMemo(() => {
    if (!showEnvelope) return null;

    const M0 = data[0].M;
    const tau = 5;
    const upper = data.map((p) => {
      const decay = Math.exp(-p.t / tau);
      return new THREE.Vector3(p.t * 0.8, M0 * decay * 2, 0);
    });
    const lower = data.map((p) => {
      const decay = Math.exp(-p.t / tau);
      return new THREE.Vector3(p.t * 0.8, -M0 * decay * 2, 0);
    });

    return { upper, lower };
  }, [data, showEnvelope]);

  if (points.length < 2) return null;

  return (
    <group>
      <Line points={points} color={color} lineWidth={3} />

      {envelopePoints && (
        <>
          <Line
            points={envelopePoints.upper}
            color="#ffaa00"
            lineWidth={1}
            dashed
            dashScale={0.5}
          />
          <Line
            points={envelopePoints.lower}
            color="#ffaa00"
            lineWidth={1}
            dashed
            dashScale={0.5}
          />
        </>
      )}
    </group>
  );
}

interface EnergyBarProps {
  data: MemoryDataPoint[];
  animate: boolean;
  progress: number;
}

function EnergyBar({ data, animate, progress }: EnergyBarProps) {
  const displayIndex = animate ? Math.floor(data.length * progress) : data.length - 1;
  const currentEnergy = data[displayIndex]?.energy || 0;

  const barRef = useRef<THREE.Mesh>(null);

  useFrame(() => {
    if (barRef.current) {
      barRef.current.scale.y = currentEnergy;
      const color = new THREE.Color().setHSL(0.6 - currentEnergy * 0.4, 0.8, 0.5);
      (barRef.current.material as THREE.MeshStandardMaterial).color = color;
    }
  });

  return (
    <group position={[9, 0, 0]}>
      <mesh ref={barRef} position={[0, 0, 0]}>
        <boxGeometry args={[0.3, 2, 0.3]} />
        <meshStandardMaterial />
      </mesh>

      <Text position={[0, 2.5, 0]} fontSize={0.15} color="#ffffff" anchorX="center">
        Energy
      </Text>

      <Text position={[0, -2.5, 0]} fontSize={0.12} color="#aaaaaa" anchorX="center">
        {currentEnergy.toFixed(3)}
      </Text>
    </group>
  );
}

function Scene() {
  const [progress, setProgress] = useState(1);

  const controls = useControls({
    Parameters: folder({
      M0: { value: 1, min: 0.1, max: 2, step: 0.1, label: 'Initial Memory' },
      tau: { value: 5, min: 1, max: 10, step: 0.5, label: 'Decay Time τ' },
      omega: { value: PHI, min: 0.5, max: 3, step: 0.1, label: 'Frequency ω' },
      tMax: { value: 10, min: 5, max: 20, step: 1, label: 'Time Range' },
    }),
    Display: folder({
      showEnvelope: { value: true, label: 'Show Envelope' },
      showEnergy: { value: true, label: 'Show Energy' },
      showGrid: { value: true, label: 'Show Grid' },
    }),
    Animation: folder({
      animate: true,
      speed: { value: 0.5, min: 0.1, max: 2, step: 0.1 },
    }),
  });

  const data = useMemo(
    () =>
      calculateMemoryEvolution(controls.tMax, 500, controls.M0, controls.tau, controls.omega),
    [controls.M0, controls.tau, controls.omega, controls.tMax]
  );

  useFrame((_, delta) => {
    if (controls.animate) {
      setProgress((prev) => {
        const next = prev + controls.speed * delta * 0.2;
        return next > 1 ? 0 : next;
      });
    } else {
      setProgress(1);
    }
  });

  return (
    <>
      <PerspectiveCamera makeDefault position={[0, 0, 10]} />
      <OrbitControls enableDamping dampingFactor={0.05} enableRotate={false} />

      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 5, 5]} intensity={0.8} />

      {/* Axes */}
      <Line points={[[0, 0, 0], [controls.tMax * 0.8, 0, 0]]} color="#ffffff" lineWidth={1} />
      <Line points={[[0, -3, 0], [0, 3, 0]]} color="#ffffff" lineWidth={1} />

      <Text position={[controls.tMax * 0.8 + 0.5, 0, 0]} fontSize={0.2} color="#ffffff">
        t
      </Text>
      <Text position={[0, 3.2, 0]} fontSize={0.2} color="#ffffff">
        M(t)
      </Text>

      {controls.showGrid && (
        <gridHelper args={[controls.tMax, 20, '#444444', '#222222']} rotation={[0, 0, 0]} />
      )}

      <MemoryPlot
        data={data}
        color="#00ffff"
        showEnvelope={controls.showEnvelope}
        animate={controls.animate}
        progress={progress}
      />

      {controls.showEnergy && (
        <EnergyBar data={data} animate={controls.animate} progress={progress} />
      )}

      {/* Info text */}
      <Text position={[-7, 2.5, 0]} fontSize={0.15} color="#ffffff" anchorX="left">
        {`M(t) = M₀ exp(-t/τ) cos(ωt)`}
      </Text>
      <Text position={[-7, 2.1, 0]} fontSize={0.12} color="#aaaaaa" anchorX="left">
        {`M₀ = ${controls.M0.toFixed(2)}, τ = ${controls.tau.toFixed(1)}, ω = ${controls.omega.toFixed(2)}`}
      </Text>
    </>
  );
}

export function MemoryEvolutionVisualization() {
  return (
    <div className="memory-evolution-visualization">
      <Canvas>
        <Scene />
      </Canvas>
    </div>
  );
}

export default MemoryEvolutionVisualization;
