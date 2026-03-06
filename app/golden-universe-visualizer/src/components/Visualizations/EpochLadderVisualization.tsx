/**
 * Epoch Ladder Visualization
 * Animated descent through epochs N=0 to N=1000 showing particle formation
 */

import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Text, Line } from '@react-three/drei';
import { useControls, folder } from 'leva';
import * as THREE from 'three';
import {
  EPOCH_LADDER,
  getParticlesAtEpoch,
  ParticleWindingData,
  getParticle,
} from '../../data/visualizations/windingNumbers';
import { calculateResonance, isResonant, PHI_SQUARED } from '../../utils/three/goldenGeometry';
import './EpochLadderVisualization.scss';

interface EpochRungProps {
  epoch: number;
  index: number;
  currentEpoch: number;
  particles: string[];
}

function EpochRung({ epoch, index, currentEpoch, particles }: EpochRungProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const isActive = currentEpoch >= epoch;
  const isCurrent = Math.abs(currentEpoch - epoch) < 20;

  const yPosition = -index * 0.3;
  const k_res = calculateResonance(epoch);
  const resonant = isResonant(k_res);

  const color = isActive ? (resonant ? '#00ff00' : '#ff0000') : '#333333';

  useFrame(() => {
    if (meshRef.current && isCurrent) {
      meshRef.current.scale.x = 1 + 0.1 * Math.sin(Date.now() * 0.003);
    }
  });

  return (
    <group position={[0, yPosition, 0]}>
      {/* Rung bar */}
      <mesh ref={meshRef} position={[0, 0, 0]}>
        <boxGeometry args={[3, 0.1, 0.1]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={isActive ? 0.5 : 0}
        />
      </mesh>

      {/* Epoch label */}
      <Text
        position={[-2, 0, 0]}
        fontSize={0.12}
        color={isActive ? '#ffffff' : '#666666'}
        anchorX="right"
      >
        N = {epoch}
      </Text>

      {/* Resonance indicator */}
      <Text
        position={[2.2, 0, 0]}
        fontSize={0.1}
        color={isActive ? (resonant ? '#00ff00' : '#ff0000') : '#666666'}
        anchorX="left"
      >
        k = {k_res}
      </Text>

      {/* Particle labels */}
      {particles.length > 0 && isActive && (
        <Text position={[0, 0.2, 0]} fontSize={0.08} color="#ffd700" anchorX="center">
          {particles.join(', ')}
        </Text>
      )}

      {/* Connecting lines */}
      {index > 0 && (
        <Line
          points={[
            [0, 0.05, 0],
            [0, 0.3, 0],
          ]}
          color={isActive ? '#666666' : '#222222'}
          lineWidth={1}
        />
      )}
    </group>
  );
}

interface ParticleCloudProps {
  epoch: number;
}

function ParticleCloud({ epoch }: ParticleCloudProps) {
  const particlesRef = useRef<THREE.Points>(null);
  const particles = useMemo(() => getParticlesAtEpoch(epoch), [epoch]);

  const positions = useMemo(() => {
    const pos = new Float32Array(particles.length * 3);
    particles.forEach((particle, i) => {
      const angle = (i / particles.length) * Math.PI * 2;
      const radius = 4 + Math.random();
      pos[i * 3] = Math.cos(angle) * radius;
      pos[i * 3 + 1] = Math.random() * 2 - 1;
      pos[i * 3 + 2] = Math.sin(angle) * radius;
    });
    return pos;
  }, [particles]);

  const colors = useMemo(() => {
    const col = new Float32Array(particles.length * 3);
    particles.forEach((particle, i) => {
      const p = getParticle(particle.symbol);
      if (p) {
        const color = new THREE.Color(p.color);
        col[i * 3] = color.r;
        col[i * 3 + 1] = color.g;
        col[i * 3 + 2] = color.b;
      }
    });
    return col;
  }, [particles]);

  useFrame((_, delta) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y += delta * 0.2;
    }
  });

  if (particles.length === 0) return null;

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={positions.length / 3}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={colors.length / 3}
          array={colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.15} vertexColors sizeAttenuation={true} />
    </points>
  );
}

function Scene() {
  const [currentEpoch, setCurrentEpoch] = useState(0);
  const groupRef = useRef<THREE.Group>(null);

  const controls = useControls({
    Epoch: folder({
      N: {
        value: 0,
        min: 0,
        max: 1000,
        step: 10,
        onChange: (value) => setCurrentEpoch(value),
      },
    }),
    Animation: folder({
      autoPlay: false,
      speed: { value: 0.5, min: 0.1, max: 2, step: 0.1 },
    }),
    Display: folder({
      showParticles: { value: true, label: 'Show Particle Cloud' },
      showInfo: { value: true, label: 'Show Information' },
    }),
  });

  useFrame((_, delta) => {
    if (controls.autoPlay) {
      setCurrentEpoch((prev) => {
        const next = prev + controls.speed * delta * 50;
        return next > 1000 ? 0 : next;
      });
    }

    // Scroll ladder to keep current epoch in view
    if (groupRef.current) {
      const targetY = (currentEpoch / 1000) * EPOCH_LADDER.length * 0.3;
      groupRef.current.position.y += (targetY - groupRef.current.position.y) * 0.1;
    }
  });

  const currentParticles = useMemo(
    () => getParticlesAtEpoch(currentEpoch),
    [currentEpoch]
  );

  return (
    <>
      <PerspectiveCamera makeDefault position={[8, 0, 8]} />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        target={[0, 0, 0]}
        minDistance={5}
        maxDistance={20}
      />

      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 5, 5]} intensity={0.8} />
      <pointLight position={[0, 0, 0]} intensity={0.5} color="#ffffff" />

      {/* Epoch ladder */}
      <group ref={groupRef}>
        {EPOCH_LADDER.map((epochData, index) => (
          <EpochRung
            key={epochData.N}
            epoch={epochData.N}
            index={index}
            currentEpoch={currentEpoch}
            particles={epochData.particles}
          />
        ))}
      </group>

      {/* Particle cloud */}
      {controls.showParticles && <ParticleCloud epoch={currentEpoch} />}

      {/* Info panel */}
      {controls.showInfo && (
        <>
          <Text position={[0, 4, 0]} fontSize={0.3} color="#ffd700" anchorX="center">
            Epoch Ladder
          </Text>
          <Text position={[0, 3.5, 0]} fontSize={0.15} color="#ffffff" anchorX="center">
            Current Epoch: N = {Math.round(currentEpoch)}
          </Text>
          <Text position={[0, 3.2, 0]} fontSize={0.12} color="#aaaaaa" anchorX="center">
            Particles formed: {currentParticles.length}
          </Text>
          <Text position={[0, 2.9, 0]} fontSize={0.12} color="#aaaaaa" anchorX="center">
            {currentParticles.map((p) => p.symbol).join(', ') || 'None yet'}
          </Text>

          {/* Legend */}
          <group position={[-6, -3, 0]}>
            <mesh position={[0, 0, 0]}>
              <boxGeometry args={[0.3, 0.1, 0.1]} />
              <meshStandardMaterial color="#00ff00" />
            </mesh>
            <Text position={[0.5, 0, 0]} fontSize={0.1} color="#ffffff" anchorX="left">
              Resonant (even k)
            </Text>

            <mesh position={[0, -0.3, 0]}>
              <boxGeometry args={[0.3, 0.1, 0.1]} />
              <meshStandardMaterial color="#ff0000" />
            </mesh>
            <Text position={[0.5, -0.3, 0]} fontSize={0.1} color="#ffffff" anchorX="left">
              Anti-resonant (odd k)
            </Text>
          </group>
        </>
      )}
    </>
  );
}

export function EpochLadderVisualization() {
  return (
    <div className="epoch-ladder-visualization">
      <Canvas>
        <Scene />
      </Canvas>
    </div>
  );
}

export default EpochLadderVisualization;
