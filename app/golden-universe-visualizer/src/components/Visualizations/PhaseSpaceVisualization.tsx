/**
 * Phase Space Visualization
 * Interactive 2D/3D phase space trajectory plots with multiple overlays
 */

import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Line, Text, Html } from '@react-three/drei';
import { useControls, folder, button } from 'leva';
import * as THREE from 'three';
import {
  TRAJECTORIES,
  PhaseSpaceTrajectory,
  PhaseSpacePoint,
  calculateEnergyBounds,
} from '../../data/visualizations/phaseSpace';
import { goldenGradientColor } from '../../utils/three/goldenGeometry';
import './PhaseSpaceVisualization.scss';

interface TrajectoryLineProps {
  trajectory: PhaseSpaceTrajectory;
  mode: '2d' | '3d';
  showEnergy: boolean;
  animate: boolean;
  speed: number;
}

function TrajectoryLine({ trajectory, mode, showEnergy, animate, speed }: TrajectoryLineProps) {
  const [progress, setProgress] = useState(1);

  const points = useMemo(() => {
    const displayPoints = trajectory.points.slice(
      0,
      Math.floor(trajectory.points.length * progress)
    );

    return displayPoints.map((p: PhaseSpacePoint) => {
      if (mode === '2d') {
        return new THREE.Vector3(p.rho * 2, p.pi_rho * 2, 0);
      } else {
        return new THREE.Vector3(p.rho * 2, p.pi_rho * 2, p.theta);
      }
    });
  }, [trajectory.points, progress, mode]);

  const colors = useMemo(() => {
    if (!showEnergy) {
      const baseColor = new THREE.Color(trajectory.color);
      return points.map(() => baseColor);
    }

    const energyBounds = calculateEnergyBounds(trajectory.points);
    return trajectory.points.slice(0, Math.floor(trajectory.points.length * progress)).map((p) => {
      const normalizedEnergy = p.energy
        ? (p.energy - energyBounds.min) / (energyBounds.max - energyBounds.min)
        : 0;
      return goldenGradientColor(normalizedEnergy, 0.6);
    });
  }, [trajectory, points.length, showEnergy, progress]);

  useFrame((_, delta) => {
    if (animate) {
      setProgress((prev) => {
        const next = prev + speed * delta * 0.2;
        return next > 1 ? 0 : next;
      });
    } else {
      setProgress(1);
    }
  });

  if (points.length < 2) return null;

  return (
    <Line
      points={points}
      color={trajectory.color}
      lineWidth={2}
      vertexColors={showEnergy ? colors : undefined}
    />
  );
}

interface ParticleMarkerProps {
  trajectory: PhaseSpaceTrajectory;
  mode: '2d' | '3d';
  animate: boolean;
  speed: number;
}

function ParticleMarker({ trajectory, mode, animate, speed }: ParticleMarkerProps) {
  const markerRef = useRef<THREE.Mesh>(null);
  const [index, setIndex] = useState(0);

  useFrame((_, delta) => {
    if (animate) {
      setIndex((prev) => {
        const next = prev + speed * delta * 50;
        return next >= trajectory.points.length ? 0 : Math.floor(next);
      });
    }

    if (markerRef.current) {
      markerRef.current.rotation.x += delta;
      markerRef.current.rotation.y += delta;
    }
  });

  const position = useMemo(() => {
    const p = trajectory.points[index] || trajectory.points[0];
    if (mode === '2d') {
      return new THREE.Vector3(p.rho * 2, p.pi_rho * 2, 0);
    } else {
      return new THREE.Vector3(p.rho * 2, p.pi_rho * 2, p.theta);
    }
  }, [trajectory.points, index, mode]);

  return (
    <mesh ref={markerRef} position={position}>
      <sphereGeometry args={[0.08, 16, 16]} />
      <meshStandardMaterial color={trajectory.color} emissive={trajectory.color} emissiveIntensity={0.5} />
    </mesh>
  );
}

interface AxesProps {
  mode: '2d' | '3d';
}

function Axes({ mode }: AxesProps) {
  return (
    <group>
      {/* X axis (ρ) */}
      <Line points={[[-4, 0, 0], [4, 0, 0]]} color="#ff0000" lineWidth={1} />
      <Text position={[4.2, 0, 0]} fontSize={0.2} color="#ff0000">
        ρ
      </Text>

      {/* Y axis (π_ρ) */}
      <Line points={[[0, -4, 0], [0, 4, 0]]} color="#00ff00" lineWidth={1} />
      <Text position={[0, 4.2, 0]} fontSize={0.2} color="#00ff00">
        π_ρ
      </Text>

      {/* Z axis (θ) - only in 3D mode */}
      {mode === '3d' && (
        <>
          <Line points={[[0, 0, -4], [0, 0, 4]]} color="#0000ff" lineWidth={1} />
          <Text position={[0, 0, 4.2]} fontSize={0.2} color="#0000ff">
            θ
          </Text>
        </>
      )}

      {/* Grid on XY plane */}
      <gridHelper args={[8, 16, '#444444', '#222222']} rotation={[Math.PI / 2, 0, 0]} />
    </group>
  );
}

function Scene() {
  const [selectedTrajectories, setSelectedTrajectories] = useState<Set<string>>(
    new Set(['harmonic'])
  );

  const controls = useControls({
    Display: folder({
      mode: {
        value: '2d',
        options: { '2D (ρ, π_ρ)': '2d', '3D (ρ, π_ρ, θ)': '3d' },
      },
      showEnergy: { value: true, label: 'Energy Gradient' },
      showParticles: { value: true, label: 'Show Particles' },
      showAxes: { value: true, label: 'Show Axes' },
    }),
    Animation: folder({
      animate: true,
      speed: { value: 1, min: 0.1, max: 3, step: 0.1 },
    }),
    Trajectories: folder(
      TRAJECTORIES.reduce(
        (acc, traj) => {
          acc[traj.name] = button(() => {
            setSelectedTrajectories((prev) => {
              const next = new Set(prev);
              if (next.has(traj.id)) {
                next.delete(traj.id);
              } else {
                next.add(traj.id);
              }
              return next;
            });
          });
          return acc;
        },
        {} as Record<string, any>
      )
    ),
    Export: folder({
      exportPNG: button(() => {
        console.log('Export PNG not yet implemented');
      }),
      exportSVG: button(() => {
        console.log('Export SVG not yet implemented');
      }),
    }),
  });

  const cameraPosition = useMemo<[number, number, number]>(() => {
    if (controls.mode === '2d') {
      return [0, 0, 8];
    } else {
      return [6, 4, 6];
    }
  }, [controls.mode]);

  return (
    <>
      <PerspectiveCamera makeDefault position={cameraPosition} />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        enableRotate={controls.mode === '3d'}
      />

      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 5, 5]} intensity={0.8} />
      <pointLight position={[0, 0, 0]} intensity={0.3} color="#ffffff" />

      {controls.showAxes && <Axes mode={controls.mode as '2d' | '3d'} />}

      {TRAJECTORIES.filter((t) => selectedTrajectories.has(t.id)).map((trajectory) => (
        <group key={trajectory.id}>
          <TrajectoryLine
            trajectory={trajectory}
            mode={controls.mode as '2d' | '3d'}
            showEnergy={controls.showEnergy}
            animate={controls.animate}
            speed={controls.speed}
          />
          {controls.showParticles && (
            <ParticleMarker
              trajectory={trajectory}
              mode={controls.mode as '2d' | '3d'}
              animate={controls.animate}
              speed={controls.speed}
            />
          )}
        </group>
      ))}
    </>
  );
}

export function PhaseSpaceVisualization() {
  return (
    <div className="phase-space-visualization">
      <Canvas>
        <Scene />
      </Canvas>
      <div className="legend">
        <h3>Phase Space Trajectories</h3>
        {TRAJECTORIES.map((traj) => (
          <div key={traj.id} className="legend-item">
            <div className="color-box" style={{ backgroundColor: traj.color }} />
            <span className="name">{traj.name}</span>
            <span className="type">[{traj.type}]</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PhaseSpaceVisualization;
