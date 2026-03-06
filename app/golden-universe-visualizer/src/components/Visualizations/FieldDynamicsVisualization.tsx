/**
 * Field Dynamics Visualization
 * Shows the evolution of the Omega field Ω(r,t) with real-time dynamics
 */

import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Text, Plane } from '@react-three/drei';
import { useControls, folder } from 'leva';
import * as THREE from 'three';
import { PHI, PHI_SQUARED } from '../../utils/three/goldenGeometry';
import {
  createEnergyDensityMaterial,
  fieldVertexShader,
  energyDensityShader,
} from '../../utils/three/shaders';
import './FieldDynamicsVisualization.scss';

interface FieldSurfaceProps {
  resolution: number;
  size: number;
  amplitude: number;
  frequency: number;
  time: number;
}

function FieldSurface({ resolution, size, amplitude, frequency, time }: FieldSurfaceProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const materialRef = useRef<THREE.ShaderMaterial>(null);

  // Create geometry with custom vertices
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(size, size, resolution, resolution);
    return geo;
  }, [size, resolution]);

  // Update vertices based on field equation
  useFrame(() => {
    if (!meshRef.current) return;

    const positions = geometry.attributes.position;
    const halfSize = size / 2;

    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i);
      const y = positions.getY(i);

      // Normalized coordinates
      const nx = x / halfSize;
      const ny = y / halfSize;
      const r = Math.sqrt(nx * nx + ny * ny);

      // Field equation: Ω(r,t) = A * exp(-r²/2) * cos(ω*r - φ*t)
      const omega = frequency * PHI;
      const phase = omega * r - time;
      const envelope = Math.exp(-r * r * 0.5);
      const z = amplitude * envelope * Math.cos(phase);

      positions.setZ(i, z);
    }

    positions.needsUpdate = true;
    geometry.computeVertexNormals();

    // Update shader uniforms
    if (materialRef.current) {
      materialRef.current.uniforms.time.value = time;
    }
  });

  const shaderMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        energy: { value: 0.5 },
        colorStart: { value: new THREE.Vector3(0.1, 0.2, 0.8) },
        colorEnd: { value: new THREE.Vector3(0.8, 0.2, 0.1) },
      },
      vertexShader: fieldVertexShader,
      fragmentShader: energyDensityShader,
      side: THREE.DoubleSide,
    });
  }, []);

  return (
    <mesh ref={meshRef} geometry={geometry} material={shaderMaterial} rotation={[-Math.PI / 2, 0, 0]}>
      <shaderMaterial ref={materialRef} attach="material" {...shaderMaterial} />
    </mesh>
  );
}

interface FieldLineProps {
  x: number;
  y: number;
  size: number;
  amplitude: number;
  frequency: number;
  time: number;
  color: string;
}

function FieldLine({ x, y, size, amplitude, frequency, time, color }: FieldLineProps) {
  const points = useMemo(() => {
    const pts: THREE.Vector3[] = [];
    const samples = 50;
    const halfSize = size / 2;

    for (let i = 0; i <= samples; i++) {
      const t = (i / samples - 0.5) * size;
      const r = Math.sqrt((x + t) * (x + t) + y * y) / halfSize;
      const omega = frequency * PHI;
      const phase = omega * r - time;
      const envelope = Math.exp(-r * r * 0.5);
      const z = amplitude * envelope * Math.cos(phase);

      pts.push(new THREE.Vector3(x + t, z, y));
    }

    return pts;
  }, [x, y, size, amplitude, frequency, time]);

  return (
    <mesh>
      <tubeGeometry args={[new THREE.CatmullRomCurve3(points), 50, 0.02, 8, false]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.3} />
    </mesh>
  );
}

interface EnergyParticlesProps {
  count: number;
  size: number;
  amplitude: number;
  frequency: number;
  time: number;
}

function EnergyParticles({ count, size, amplitude, frequency, time }: EnergyParticlesProps) {
  const particlesRef = useRef<THREE.Points>(null);

  const [positions, velocities] = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const vel = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const r = Math.random() * size * 0.4;
      pos[i * 3] = Math.cos(angle) * r;
      pos[i * 3 + 1] = 0;
      pos[i * 3 + 2] = Math.sin(angle) * r;

      vel[i * 3] = (Math.random() - 0.5) * 0.1;
      vel[i * 3 + 1] = Math.random() * 0.1;
      vel[i * 3 + 2] = (Math.random() - 0.5) * 0.1;
    }

    return [pos, vel];
  }, [count, size]);

  useFrame((_, delta) => {
    if (!particlesRef.current) return;

    const pos = particlesRef.current.geometry.attributes.position.array as Float32Array;

    for (let i = 0; i < count; i++) {
      // Update positions
      pos[i * 3] += velocities[i * 3] * delta;
      pos[i * 3 + 1] += velocities[i * 3 + 1] * delta;
      pos[i * 3 + 2] += velocities[i * 3 + 2] * delta;

      // Calculate field value at particle position
      const x = pos[i * 3];
      const z = pos[i * 3 + 2];
      const r = Math.sqrt(x * x + z * z) / (size * 0.5);
      const omega = frequency * PHI;
      const phase = omega * r - time;
      const envelope = Math.exp(-r * r * 0.5);
      const fieldValue = amplitude * envelope * Math.cos(phase);

      pos[i * 3 + 1] = fieldValue;

      // Wrap around
      if (Math.abs(pos[i * 3]) > size * 0.5) pos[i * 3] *= -0.9;
      if (Math.abs(pos[i * 3 + 2]) > size * 0.5) pos[i * 3 + 2] *= -0.9;
    }

    particlesRef.current.geometry.attributes.position.needsUpdate = true;
  });

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.08} color="#ffff00" sizeAttenuation={true} />
    </points>
  );
}

function Scene() {
  const [time, setTime] = React.useState(0);

  const controls = useControls({
    'Field Parameters': folder({
      amplitude: { value: 1, min: 0.1, max: 2, step: 0.1 },
      frequency: { value: 2, min: 0.5, max: 5, step: 0.1 },
      resolution: { value: 64, min: 32, max: 128, step: 16 },
    }),
    Display: folder({
      showSurface: { value: true, label: 'Show Field Surface' },
      showFieldLines: { value: false, label: 'Show Field Lines' },
      showParticles: { value: true, label: 'Show Energy Particles' },
      particleCount: { value: 100, min: 50, max: 500, step: 50, label: 'Particle Count' },
    }),
    Animation: folder({
      animate: true,
      speed: { value: 1, min: 0.1, max: 3, step: 0.1 },
    }),
  });

  useFrame((_, delta) => {
    if (controls.animate) {
      setTime((prev) => prev + delta * controls.speed);
    }
  });

  const size = 8;
  const fieldLinePositions = [
    { x: 0, y: 0 },
    { x: 2, y: 0 },
    { x: -2, y: 0 },
    { x: 0, y: 2 },
    { x: 0, y: -2 },
  ];

  return (
    <>
      <PerspectiveCamera makeDefault position={[8, 6, 8]} />
      <OrbitControls enableDamping dampingFactor={0.05} />

      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 10, 5]} intensity={0.8} />
      <directionalLight position={[-5, -5, -5]} intensity={0.3} />
      <pointLight position={[0, 2, 0]} intensity={0.5} color="#ffffff" />

      {controls.showSurface && (
        <FieldSurface
          resolution={controls.resolution}
          size={size}
          amplitude={controls.amplitude}
          frequency={controls.frequency}
          time={time}
        />
      )}

      {controls.showFieldLines &&
        fieldLinePositions.map((pos, i) => (
          <FieldLine
            key={i}
            x={pos.x}
            y={pos.y}
            size={size}
            amplitude={controls.amplitude}
            frequency={controls.frequency}
            time={time}
            color="#00ffff"
          />
        ))}

      {controls.showParticles && (
        <EnergyParticles
          count={controls.particleCount}
          size={size}
          amplitude={controls.amplitude}
          frequency={controls.frequency}
          time={time}
        />
      )}

      {/* Info display */}
      <Text position={[0, 3, 0]} fontSize={0.3} color="#ffd700" anchorX="center">
        Field Dynamics
      </Text>
      <Text position={[0, 2.5, 0]} fontSize={0.15} color="#ffffff" anchorX="center">
        Ω(r,t) = A exp(-r²/2) cos(ωr - φt)
      </Text>
      <Text position={[0, 2.2, 0]} fontSize={0.12} color="#aaaaaa" anchorX="center">
        {`A = ${controls.amplitude.toFixed(2)}, ω = ${controls.frequency.toFixed(2)}, t = ${time.toFixed(2)}`}
      </Text>

      {/* Grid */}
      <gridHelper args={[size, 16, '#444444', '#222222']} position={[0, -0.1, 0]} />
    </>
  );
}

export function FieldDynamicsVisualization() {
  return (
    <div className="field-dynamics-visualization">
      <Canvas>
        <Scene />
      </Canvas>
    </div>
  );
}

export default FieldDynamicsVisualization;
