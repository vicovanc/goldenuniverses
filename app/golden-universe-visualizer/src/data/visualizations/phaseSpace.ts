/**
 * Phase space trajectory data
 * Calculated trajectories in (ρ, θ, π_ρ, π_θ) coordinates
 */

export interface PhaseSpacePoint {
  rho: number; // radial coordinate
  theta: number; // angular coordinate
  pi_rho: number; // radial momentum
  pi_theta: number; // angular momentum
  t: number; // time parameter
  energy?: number; // energy density
}

export interface PhaseSpaceTrajectory {
  id: string;
  name: string;
  description: string;
  points: PhaseSpacePoint[];
  color: string;
  type: 'periodic' | 'quasi-periodic' | 'chaotic';
}

/**
 * Generate a simple harmonic oscillator trajectory
 */
export function generateHarmonicTrajectory(
  amplitude: number = 1,
  frequency: number = 1,
  samples: number = 200
): PhaseSpacePoint[] {
  const points: PhaseSpacePoint[] = [];
  const dt = (2 * Math.PI) / samples;

  for (let i = 0; i <= samples; i++) {
    const t = i * dt;
    const rho = amplitude * Math.cos(frequency * t);
    const pi_rho = -amplitude * frequency * Math.sin(frequency * t);
    const theta = t;
    const pi_theta = 1;
    const energy = 0.5 * (pi_rho * pi_rho + frequency * frequency * rho * rho);

    points.push({ rho, theta, pi_rho, pi_theta, t, energy });
  }

  return points;
}

/**
 * Generate a golden ratio quasi-periodic trajectory
 */
export function generateGoldenTrajectory(
  amplitude: number = 1,
  samples: number = 500
): PhaseSpacePoint[] {
  const PHI = (1 + Math.sqrt(5)) / 2;
  const points: PhaseSpacePoint[] = [];
  const dt = 0.05;

  for (let i = 0; i <= samples; i++) {
    const t = i * dt;
    const rho = amplitude * Math.cos(t) * Math.cos(PHI * t);
    const pi_rho = -amplitude * (Math.sin(t) * Math.cos(PHI * t) + PHI * Math.cos(t) * Math.sin(PHI * t));
    const theta = t / PHI;
    const pi_theta = PHI;
    const energy = 0.5 * (pi_rho * pi_rho + rho * rho);

    points.push({ rho, theta, pi_rho, pi_theta, t, energy });
  }

  return points;
}

/**
 * Generate a torus knot trajectory
 */
export function generateTorusKnotTrajectory(
  p: number = 2,
  q: number = 3,
  R: number = 2,
  r: number = 1,
  samples: number = 500
): PhaseSpacePoint[] {
  const points: PhaseSpacePoint[] = [];
  const dt = (2 * Math.PI * q) / samples;

  for (let i = 0; i <= samples; i++) {
    const t = i * dt;
    const theta = t;
    const phi = (p / q) * t;

    const rho = Math.sqrt((R + r * Math.cos(phi)) ** 2 + (r * Math.sin(phi)) ** 2);
    const pi_rho = 0;
    const pi_theta = p;
    const energy = 0.5 * (pi_rho * pi_rho + pi_theta * pi_theta / (rho * rho));

    points.push({ rho, theta: theta % (2 * Math.PI), pi_rho, pi_theta, t, energy });
  }

  return points;
}

/**
 * Generate a damped oscillator trajectory
 */
export function generateDampedTrajectory(
  amplitude: number = 1,
  frequency: number = 1,
  damping: number = 0.1,
  samples: number = 300
): PhaseSpacePoint[] {
  const points: PhaseSpacePoint[] = [];
  const dt = 0.1;

  for (let i = 0; i <= samples; i++) {
    const t = i * dt;
    const envelope = Math.exp(-damping * t);
    const rho = amplitude * envelope * Math.cos(frequency * t);
    const pi_rho = amplitude * envelope * (-damping * Math.cos(frequency * t) - frequency * Math.sin(frequency * t));
    const theta = t;
    const pi_theta = 1;
    const energy = 0.5 * envelope * envelope * (pi_rho * pi_rho + frequency * frequency * rho * rho);

    points.push({ rho, theta, pi_rho, pi_theta, t, energy });
  }

  return points;
}

/**
 * Predefined trajectories for visualization
 */
export const TRAJECTORIES: PhaseSpaceTrajectory[] = [
  {
    id: 'harmonic',
    name: 'Harmonic Oscillator',
    description: 'Simple harmonic motion - periodic trajectory',
    points: generateHarmonicTrajectory(1, 1, 200),
    color: '#00ff00',
    type: 'periodic',
  },
  {
    id: 'golden',
    name: 'Golden Ratio Oscillator',
    description: 'Quasi-periodic trajectory with φ frequency ratio',
    points: generateGoldenTrajectory(1, 500),
    color: '#ffd700',
    type: 'quasi-periodic',
  },
  {
    id: 'torus_21',
    name: 'Torus Knot (2,1)',
    description: 'Winding path with p=2, q=1',
    points: generateTorusKnotTrajectory(2, 1, 2, 0.8, 400),
    color: '#ff00ff',
    type: 'periodic',
  },
  {
    id: 'torus_32',
    name: 'Torus Knot (3,2)',
    description: 'Winding path with p=3, q=2',
    points: generateTorusKnotTrajectory(3, 2, 2, 0.8, 500),
    color: '#00ffff',
    type: 'periodic',
  },
  {
    id: 'damped',
    name: 'Damped Oscillator',
    description: 'Decaying spiral trajectory',
    points: generateDampedTrajectory(1, 1, 0.05, 300),
    color: '#ff4040',
    type: 'periodic',
  },
];

/**
 * Get trajectory by ID
 */
export function getTrajectory(id: string): PhaseSpaceTrajectory | undefined {
  return TRAJECTORIES.find((t) => t.id === id);
}

/**
 * Calculate energy bounds for a trajectory
 */
export function calculateEnergyBounds(
  points: PhaseSpacePoint[]
): { min: number; max: number } {
  let min = Infinity;
  let max = -Infinity;

  points.forEach((p) => {
    if (p.energy !== undefined) {
      min = Math.min(min, p.energy);
      max = Math.max(max, p.energy);
    }
  });

  return { min, max };
}

/**
 * Sample trajectory at regular intervals
 */
export function sampleTrajectory(
  trajectory: PhaseSpaceTrajectory,
  numSamples: number
): PhaseSpacePoint[] {
  const step = Math.floor(trajectory.points.length / numSamples);
  return trajectory.points.filter((_, i) => i % step === 0);
}
