/**
 * Winding numbers data for Standard Model particles
 * Based on the Golden Universe theory's topological classification
 */

import { PHI_SQUARED } from '../../utils/three/goldenGeometry';

export interface ParticleWindingData {
  name: string;
  symbol: string;
  type: 'lepton' | 'quark' | 'boson';
  generation?: 1 | 2 | 3;
  mass: number; // GeV
  charge: number; // elementary charge units
  getWindingNumbers: (epoch: number) => { p: number; q: number };
  color: string; // hex color for visualization
  formationEpoch?: number; // epoch where particle first appears
}

export const PARTICLES: ParticleWindingData[] = [
  // Leptons - Generation 1
  {
    name: 'Electron',
    symbol: 'e',
    type: 'lepton',
    generation: 1,
    mass: 0.000511,
    charge: -1,
    getWindingNumbers: (N) => ({ p: 1, q: Math.round(N / PHI_SQUARED) }),
    color: '#00ffff',
    formationEpoch: 100,
  },
  {
    name: 'Electron Neutrino',
    symbol: 'νₑ',
    type: 'lepton',
    generation: 1,
    mass: 0.0000001,
    charge: 0,
    getWindingNumbers: (N) => ({ p: 1, q: Math.round(N / PHI_SQUARED) - 1 }),
    color: '#4080ff',
    formationEpoch: 50,
  },

  // Leptons - Generation 2
  {
    name: 'Muon',
    symbol: 'μ',
    type: 'lepton',
    generation: 2,
    mass: 0.1057,
    charge: -1,
    getWindingNumbers: (N) => ({ p: 2, q: Math.round(N / PHI_SQUARED) }),
    color: '#ff00ff',
    formationEpoch: 300,
  },
  {
    name: 'Muon Neutrino',
    symbol: 'νᵤ',
    type: 'lepton',
    generation: 2,
    mass: 0.0000002,
    charge: 0,
    getWindingNumbers: (N) => ({ p: 2, q: Math.round(N / PHI_SQUARED) - 1 }),
    color: '#ff40ff',
    formationEpoch: 250,
  },

  // Leptons - Generation 3
  {
    name: 'Tau',
    symbol: 'τ',
    type: 'lepton',
    generation: 3,
    mass: 1.777,
    charge: -1,
    getWindingNumbers: (N) => ({ p: 3, q: Math.round(N / PHI_SQUARED) }),
    color: '#ffff00',
    formationEpoch: 600,
  },
  {
    name: 'Tau Neutrino',
    symbol: 'ντ',
    type: 'lepton',
    generation: 3,
    mass: 0.0000003,
    charge: 0,
    getWindingNumbers: (N) => ({ p: 3, q: Math.round(N / PHI_SQUARED) - 1 }),
    color: '#ffff40',
    formationEpoch: 550,
  },

  // Quarks - Generation 1
  {
    name: 'Up',
    symbol: 'u',
    type: 'quark',
    generation: 1,
    mass: 0.0022,
    charge: 2 / 3,
    getWindingNumbers: (N) => ({ p: 1, q: Math.round((N / (3 * PHI_SQUARED)) * 2) }),
    color: '#ff0000',
    formationEpoch: 80,
  },
  {
    name: 'Down',
    symbol: 'd',
    type: 'quark',
    generation: 1,
    mass: 0.0047,
    charge: -1 / 3,
    getWindingNumbers: (N) => ({ p: 1, q: Math.round(N / (3 * PHI_SQUARED)) }),
    color: '#00ff00',
    formationEpoch: 80,
  },

  // Quarks - Generation 2
  {
    name: 'Charm',
    symbol: 'c',
    type: 'quark',
    generation: 2,
    mass: 1.275,
    charge: 2 / 3,
    getWindingNumbers: (N) => ({ p: 2, q: Math.round((N / (3 * PHI_SQUARED)) * 2) }),
    color: '#ff4040',
    formationEpoch: 400,
  },
  {
    name: 'Strange',
    symbol: 's',
    type: 'quark',
    generation: 2,
    mass: 0.095,
    charge: -1 / 3,
    getWindingNumbers: (N) => ({ p: 2, q: Math.round(N / (3 * PHI_SQUARED)) }),
    color: '#40ff40',
    formationEpoch: 350,
  },

  // Quarks - Generation 3
  {
    name: 'Top',
    symbol: 't',
    type: 'quark',
    generation: 3,
    mass: 173.0,
    charge: 2 / 3,
    getWindingNumbers: (N) => ({ p: 3, q: Math.round((N / (3 * PHI_SQUARED)) * 2) }),
    color: '#ff8080',
    formationEpoch: 900,
  },
  {
    name: 'Bottom',
    symbol: 'b',
    type: 'quark',
    generation: 3,
    mass: 4.18,
    charge: -1 / 3,
    getWindingNumbers: (N) => ({ p: 3, q: Math.round(N / (3 * PHI_SQUARED)) }),
    color: '#80ff80',
    formationEpoch: 800,
  },
];

/**
 * Get particle by name
 */
export function getParticle(name: string): ParticleWindingData | undefined {
  return PARTICLES.find(
    (p) => p.name.toLowerCase() === name.toLowerCase() || p.symbol === name
  );
}

/**
 * Get all particles of a given type
 */
export function getParticlesByType(
  type: 'lepton' | 'quark' | 'boson'
): ParticleWindingData[] {
  return PARTICLES.filter((p) => p.type === type);
}

/**
 * Get all particles in a generation
 */
export function getParticlesByGeneration(generation: 1 | 2 | 3): ParticleWindingData[] {
  return PARTICLES.filter((p) => p.generation === generation);
}

/**
 * Get particles that form at or before a given epoch
 */
export function getParticlesAtEpoch(epoch: number): ParticleWindingData[] {
  return PARTICLES.filter((p) => p.formationEpoch && p.formationEpoch <= epoch);
}

/**
 * Epoch ladder data - key epochs where particles form
 */
export const EPOCH_LADDER = [
  { N: 0, description: 'Initial singularity', particles: [] },
  { N: 50, description: 'Electron neutrino forms', particles: ['νₑ'] },
  { N: 80, description: 'First generation quarks (u, d)', particles: ['u', 'd'] },
  { N: 100, description: 'Electron forms', particles: ['e'] },
  { N: 250, description: 'Muon neutrino forms', particles: ['νᵤ'] },
  { N: 300, description: 'Muon forms', particles: ['μ'] },
  { N: 350, description: 'Strange quark forms', particles: ['s'] },
  { N: 400, description: 'Charm quark forms', particles: ['c'] },
  { N: 550, description: 'Tau neutrino forms', particles: ['ντ'] },
  { N: 600, description: 'Tau forms', particles: ['τ'] },
  { N: 800, description: 'Bottom quark forms', particles: ['b'] },
  { N: 900, description: 'Top quark forms', particles: ['t'] },
  { N: 1000, description: 'Complete Standard Model', particles: [] },
];

/**
 * Calculate resonance data for an epoch range
 */
export function calculateResonanceData(
  startEpoch: number,
  endEpoch: number,
  step: number = 10
): Array<{ N: number; k_res: number; isResonant: boolean }> {
  const data = [];
  for (let N = startEpoch; N <= endEpoch; N += step) {
    const k_res = Math.round(N / PHI_SQUARED);
    data.push({
      N,
      k_res,
      isResonant: k_res % 2 === 0,
    });
  }
  return data;
}
