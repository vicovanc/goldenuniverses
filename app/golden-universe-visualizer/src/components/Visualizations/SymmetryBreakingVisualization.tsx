/**
 * Symmetry Breaking Visualization
 * Shows how perfect φ symmetry breaks to create particles
 */

import React, { useRef, useMemo, useState, useEffect, Suspense } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Text, Sphere, Line } from '@react-three/drei';
import { useControls, folder } from 'leva';
import * as THREE from 'three';
import './SymmetryBreakingVisualization.scss';

const PHI = 1.618033988749895;
const PARTICLES = [
  { name: 'Electron', mass: 0.511, color: '#00ff00', generation: 1 },
  { name: 'Muon', mass: 105.66, color: '#ffff00', generation: 2 },
  { name: 'Tau', mass: 1776.82, color: '#ff00ff', generation: 3 },
  { name: 'Up Quark', mass: 2.3, color: '#ff0000', generation: 1 },
  { name: 'Down Quark', mass: 4.8, color: '#0000ff', generation: 1 },
];

interface SymmetryFieldProps {
  time: number;
  breakingStrength: number;
  showField: boolean;
}

function SymmetryField({ time, breakingStrength, showField }: SymmetryFieldProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const geometryRef = useRef<THREE.BufferGeometry>(null);

  useFrame(({ clock }) => {
    if (!geometryRef.current) return;

    const positions = geometryRef.current.attributes.position;
    const colors = geometryRef.current.attributes.color;

    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i);
      const y = positions.getY(i);
      const z = positions.getZ(i);

      // Calculate field strength with symmetry breaking
      const r = Math.sqrt(x * x + y * y + z * z);
      const theta = Math.atan2(y, x);
      const phi = Math.acos(z / (r + 0.001));

      // Perfect symmetry field
      const symmetricField = Math.sin(r * PHI - clock.elapsedTime) / (r + 1);

      // Breaking perturbation
      const breaking = breakingStrength * Math.sin(theta * 3 + phi * 2) *
                      Math.cos(clock.elapsedTime * 0.5);

      // Combined field
      const field = symmetricField * (1 + breaking);

      // Update vertex position based on field
      const scale = 1 + field * 0.1;
      positions.setXYZ(
        i,
        x * scale,
        y * scale,
        z * scale
      );

      // Color based on symmetry breaking
      const breakingIntensity = Math.abs(breaking);
      colors.setXYZ(
        i,
        1 - breakingIntensity,
        1 - breakingIntensity * 0.5,
        1
      );
    }

    positions.needsUpdate = true;
    colors.needsUpdate = true;
  });

  const geometry = useMemo(() => {
    const geo = new THREE.IcosahedronGeometry(3, 4);
    const colors = new Float32Array(geo.attributes.position.count * 3);
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    return geo;
  }, []);

  useEffect(() => {
    geometryRef.current = geometry;
  }, [geometry]);

  if (!showField) return null;

  return (
    <mesh ref={meshRef} geometry={geometry}>
      <meshStandardMaterial
        vertexColors
        wireframe
        transparent
        opacity={0.3}
        emissive={new THREE.Color(0x4444ff)}
        emissiveIntensity={0.2}
      />
    </mesh>
  );
}

interface ParticleEmergenceProps {
  epoch: number;
  breakingStrength: number;
  showParticles: boolean;
}

function ParticleEmergence({ epoch, breakingStrength, showParticles }: ParticleEmergenceProps) {
  const groupRef = useRef<THREE.Group>(null);

  // Calculate which particles exist at this epoch
  const visibleParticles = useMemo(() => {
    const threshold = breakingStrength * epoch / 100;
    return PARTICLES.filter((p, i) => threshold > i * 0.3);
  }, [epoch, breakingStrength]);

  useFrame(({ clock }) => {
    if (!groupRef.current) return;

    groupRef.current.children.forEach((child, i) => {
      const angle = (i / visibleParticles.length) * Math.PI * 2;
      const radius = 2 + Math.sin(clock.elapsedTime + i) * 0.5;

      child.position.x = Math.cos(angle) * radius;
      child.position.y = Math.sin(clock.elapsedTime * 0.5 + i) * 0.5;
      child.position.z = Math.sin(angle) * radius;

      child.rotation.y = clock.elapsedTime * 0.5;
    });
  });

  if (!showParticles) return null;

  return (
    <group ref={groupRef}>
      {visibleParticles.map((particle, i) => (
        <group key={particle.name}>
          <Sphere
            args={[0.2 * Math.cbrt(particle.mass / 0.511), 16, 16]}
            position={[0, 0, 0]}
          >
            <meshStandardMaterial
              color={particle.color}
              emissive={particle.color}
              emissiveIntensity={0.5}
              metalness={0.3}
              roughness={0.4}
            />
          </Sphere>
          <Text
            position={[0, 0.5, 0]}
            fontSize={0.15}
            color={particle.color}
            anchorX="center"
            anchorY="middle"
          >
            {particle.name}
          </Text>
        </group>
      ))}
    </group>
  );
}

interface SymmetryAxesProps {
  showAxes: boolean;
  breakingStrength: number;
}

function SymmetryAxes({ showAxes, breakingStrength }: SymmetryAxesProps) {
  const linesRef = useRef<THREE.Group>(null);

  useFrame(({ clock }) => {
    if (!linesRef.current) return;

    // Rotate axes to show symmetry breaking
    linesRef.current.rotation.x = Math.sin(clock.elapsedTime * 0.2) * breakingStrength * 0.1;
    linesRef.current.rotation.y = clock.elapsedTime * 0.1;
    linesRef.current.rotation.z = Math.cos(clock.elapsedTime * 0.3) * breakingStrength * 0.1;
  });

  if (!showAxes) return null;

  const axisLength = 4;
  const goldenPoints = useMemo(() => {
    const points = [];
    for (let i = 0; i < 5; i++) {
      const angle = (i / 5) * Math.PI * 2;
      points.push([
        Math.cos(angle) * axisLength,
        0,
        Math.sin(angle) * axisLength
      ]);
    }
    return points;
  }, []);

  return (
    <group ref={linesRef}>
      {/* Perfect symmetry circle */}
      <Line
        points={goldenPoints}
        color="#ffd700"
        lineWidth={2}
        closed
      />

      {/* Broken symmetry ellipse */}
      <Line
        points={goldenPoints.map(p => [
          p[0] * (1 + breakingStrength * 0.3),
          p[1],
          p[2] * (1 - breakingStrength * 0.3)
        ])}
        color="#ff6b6b"
        lineWidth={1}
        closed
        dashed
      />

      {/* Central axes */}
      <Line points={[[-axisLength, 0, 0], [axisLength, 0, 0]]} color="#ff0000" lineWidth={1} />
      <Line points={[[0, -axisLength, 0], [0, axisLength, 0]]} color="#00ff00" lineWidth={1} />
      <Line points={[[0, 0, -axisLength], [0, 0, axisLength]]} color="#0000ff" lineWidth={1} />
    </group>
  );
}

function Scene() {
  const [time, setTime] = useState(0);

  const controls = useControls({
    Symmetry: folder({
      epoch: { value: 50, min: 0, max: 100, step: 1, label: 'Epoch (N)' },
      breakingStrength: { value: 0.5, min: 0, max: 1, step: 0.01, label: 'Breaking Strength' },
      autoEvolve: { value: true, label: 'Auto Evolve' },
      evolutionSpeed: { value: 1, min: 0.1, max: 3, step: 0.1, label: 'Evolution Speed' },
    }),
    Display: folder({
      showField: { value: true, label: 'Show Symmetry Field' },
      showParticles: { value: true, label: 'Show Particles' },
      showAxes: { value: true, label: 'Show Symmetry Axes' },
    }),
    Camera: folder({
      autoRotate: { value: true, label: 'Auto Rotate' },
      rotateSpeed: { value: 0.5, min: 0.1, max: 2, step: 0.1, label: 'Rotation Speed' },
    }),
  });

  useFrame(({ clock }) => {
    if (controls.autoEvolve) {
      setTime(clock.elapsedTime * controls.evolutionSpeed);
    }
  });

  return (
    <>
      <PerspectiveCamera makeDefault position={[6, 4, 6]} fov={50} />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        autoRotate={controls.autoRotate}
        autoRotateSpeed={controls.rotateSpeed}
      />

      {/* Lighting */}
      <ambientLight intensity={0.3} />
      <directionalLight position={[5, 5, 5]} intensity={0.8} castShadow />
      <directionalLight position={[-5, -5, -5]} intensity={0.3} />
      <pointLight position={[0, 0, 0]} intensity={0.5} color="#ffffff" />

      {/* Main visualization components */}
      <SymmetryField
        time={time}
        breakingStrength={controls.breakingStrength}
        showField={controls.showField}
      />

      <ParticleEmergence
        epoch={controls.epoch}
        breakingStrength={controls.breakingStrength}
        showParticles={controls.showParticles}
      />

      <SymmetryAxes
        showAxes={controls.showAxes}
        breakingStrength={controls.breakingStrength}
      />

      {/* Info display */}
      <Text
        position={[-3.5, 3, 0]}
        fontSize={0.15}
        color="#ffffff"
        anchorX="left"
        anchorY="middle"
      >
        {`Symmetry Breaking: ${(controls.breakingStrength * 100).toFixed(0)}%`}
      </Text>
      <Text
        position={[-3.5, 2.7, 0]}
        fontSize={0.15}
        color="#ffffff"
        anchorX="left"
        anchorY="middle"
      >
        {`Epoch: N = ${controls.epoch}`}
      </Text>
      <Text
        position={[-3.5, 2.4, 0]}
        fontSize={0.15}
        color="#ffd700"
        anchorX="left"
        anchorY="middle"
      >
        {`φ = ${PHI.toFixed(10)}`}
      </Text>
    </>
  );
}

export function SymmetryBreakingVisualization() {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsReady(true);
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  if (!isReady) {
    return (
      <div className="symmetry-breaking-visualization">
        <div className="loading-message">
          Loading symmetry breaking visualization...
        </div>
      </div>
    );
  }

  return (
    <div className="symmetry-breaking-visualization">
      <Canvas
        gl={{
          preserveDrawingBuffer: true,
          antialias: true,
          alpha: false,
          powerPreference: 'high-performance',
          failIfMajorPerformanceCaveat: false,
        }}
        shadows
        camera={{ position: [6, 4, 6], fov: 50 }}
        onCreated={({ gl }) => {
          gl.setPixelRatio(Math.min(window.devicePixelRatio, 2));
          const canvas = gl.domElement;
          canvas.addEventListener('webglcontextlost', (e) => {
            e.preventDefault();
            console.warn('WebGL context lost in SymmetryBreaking, preventing default');
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

export default SymmetryBreakingVisualization;