import type { SidebarSection } from './types';
import { THEORY_LAWS } from '@/data/theoryContent';

// Create a mapping of law formulas
const lawFormulas: { [key: number]: string } = {};
THEORY_LAWS.forEach(law => {
  lawFormulas[law.id] = law.formula;
});

export const SIDEBAR_SECTIONS: SidebarSection[] = [
  {
    id: 'theory',
    title: 'THEORY',
    icon: '◉',
    defaultExpanded: true,
    items: [
      {
        id: 'theory-law-0',
        label: 'Law 0: Foundational Symmetry',
        path: '/theory/law-0',
        tooltip: 'The foundational principle of symmetry in the Golden Universe',
        metadata: {
          preview: lawFormulas[0] || 'S₀ = φⁿ where φ = (1+√5)/2'
        }
      },
      {
        id: 'theory-laws-1-10',
        label: 'Laws 1-10: Core Principles',
        path: '/theory/laws-1-10',
        badge: 10,
        children: [
          { id: 'theory-law-1', label: 'Law 1: Quantum Action', path: '/theory/law-1' },
          { id: 'theory-law-2', label: 'Law 2: Phase Structure', path: '/theory/law-2' },
          { id: 'theory-law-3', label: 'Law 3: Memory Formation', path: '/theory/law-3' },
          { id: 'theory-law-4', label: 'Law 4: Winding Numbers', path: '/theory/law-4' },
          { id: 'theory-law-5', label: 'Law 5: Energy Conservation', path: '/theory/law-5' },
          { id: 'theory-law-6', label: 'Law 6: Force Unification', path: '/theory/law-6' },
          { id: 'theory-law-7', label: 'Law 7: Mass Generation', path: '/theory/law-7' },
          { id: 'theory-law-8', label: 'Law 8: Charge Quantization', path: '/theory/law-8' },
          { id: 'theory-law-9', label: 'Law 9: Spin Emergence', path: '/theory/law-9' },
          { id: 'theory-law-10', label: 'Law 10: Coupling Constants', path: '/theory/law-10' },
        ],
      },
      {
        id: 'theory-laws-11-20',
        label: 'Laws 11-20: Field Dynamics',
        path: '/theory/laws-11-20',
        badge: 10,
        children: [
          { id: 'theory-law-11', label: 'Law 11: Gauge Invariance', path: '/theory/law-11' },
          { id: 'theory-law-12', label: 'Law 12: Symmetry Breaking', path: '/theory/law-12' },
          { id: 'theory-law-13', label: 'Law 13: Higgs Mechanism', path: '/theory/law-13' },
          { id: 'theory-law-14', label: 'Law 14: Vacuum Structure', path: '/theory/law-14' },
          { id: 'theory-law-15', label: 'Law 15: Particle Spectrum', path: '/theory/law-15' },
          { id: 'theory-law-16', label: 'Law 16: Neutrino Oscillations', path: '/theory/law-16' },
          { id: 'theory-law-17', label: 'Law 17: CP Violation', path: '/theory/law-17' },
          { id: 'theory-law-18', label: 'Law 18: Dark Matter', path: '/theory/law-18' },
          { id: 'theory-law-19', label: 'Law 19: Dark Energy', path: '/theory/law-19' },
          { id: 'theory-law-20', label: 'Law 20: Cosmological Constant', path: '/theory/law-20' },
        ],
      },
      {
        id: 'theory-laws-21-30',
        label: 'Laws 21-30: Gravitational Theory',
        path: '/theory/laws-21-30',
        badge: 10,
        children: [
          { id: 'theory-law-21', label: 'Law 21: Spacetime Geometry', path: '/theory/law-21' },
          { id: 'theory-law-22', label: 'Law 22: Gravitational Waves', path: '/theory/law-22' },
          { id: 'theory-law-23', label: 'Law 23: Black Hole Physics', path: '/theory/law-23' },
          { id: 'theory-law-24', label: 'Law 24: Hawking Radiation', path: '/theory/law-24' },
          { id: 'theory-law-25', label: 'Law 25: Holography', path: '/theory/law-25' },
          { id: 'theory-law-26', label: 'Law 26: Entropy Bounds', path: '/theory/law-26' },
          { id: 'theory-law-27', label: 'Law 27: Quantum Gravity', path: '/theory/law-27' },
          { id: 'theory-law-28', label: 'Law 28: String Theory', path: '/theory/law-28' },
          { id: 'theory-law-29', label: 'Law 29: Loop Quantum Gravity', path: '/theory/law-29' },
          { id: 'theory-law-30', label: 'Law 30: Emergent Spacetime', path: '/theory/law-30' },
        ],
      },
      {
        id: 'theory-laws-31-38',
        label: 'Laws 31-38: Advanced Topics',
        path: '/theory/laws-31-38',
        badge: 8,
        children: [
          { id: 'theory-law-31', label: 'Law 31: Quantum Information', path: '/theory/law-31' },
          { id: 'theory-law-32', label: 'Law 32: Entanglement', path: '/theory/law-32' },
          { id: 'theory-law-33', label: 'Law 33: Decoherence', path: '/theory/law-33' },
          { id: 'theory-law-34', label: 'Law 34: Measurement Problem', path: '/theory/law-34' },
          { id: 'theory-law-35', label: 'Law 35: Many Worlds', path: '/theory/law-35' },
          { id: 'theory-law-36', label: 'Law 36: Consciousness', path: '/theory/law-36' },
          { id: 'theory-law-37', label: 'Law 37: Observer Effect', path: '/theory/law-37' },
          { id: 'theory-law-38', label: 'Law 38: Final Unification', path: '/theory/law-38' },
        ],
      },
      {
        id: 'theory-lagrangian',
        label: 'Lagrangian Structure',
        path: '/theory/lagrangian',
        tooltip: 'Complete Lagrangian formulation of the theory',
      },
      {
        id: 'theory-symmetry-breaking',
        label: 'Symmetry Breaking',
        path: '/theory/symmetry-breaking',
        tooltip: 'Mechanism and consequences of symmetry breaking',
      },
    ],
  },
  {
    id: 'derivations',
    title: 'DERIVATIONS',
    icon: '◈',
    defaultExpanded: true,
    items: [
      {
        id: 'deriv-all',
        label: 'See Derivations',
        path: '/derivations',
        icon: '◎',
        tooltip: 'Browse all mathematical derivations',
      },
    ],
  },
  {
    id: 'calculations',
    title: 'CALCULATIONS',
    icon: '◐',
    defaultExpanded: true,
    items: [
      {
        id: 'calc-quick',
        label: 'Quick Calculate',
        path: '/calculations/quick',
        icon: '◆',
        tooltip: 'Fast access to common calculations',
      },
      {
        id: 'calc-particle-masses',
        label: 'Particle Masses',
        path: '/calculations/particle-masses',
        icon: '◉',
        tooltip: 'Calculate masses of all fundamental particles',
      },
    ],
  },
  {
    id: 'visualizations',
    title: 'VISUALIZATIONS',
    icon: '◳',
    defaultExpanded: true,
    items: [
      {
        id: 'viz-main',
        label: 'See Visualizations',
        path: '/visualizations',
        icon: '◎',
        tooltip: 'View all interactive visualizations',
      },
    ],
  },
  {
    id: 'explanations',
    title: 'EXPLANATIONS',
    icon: '◧',
    defaultExpanded: false,
    items: [
      {
        id: 'exp-electron',
        label: 'What is the Electron?',
        path: '/explanations/electron',
        icon: '◦',
        tooltip: 'Deep dive into electron structure',
      },
      {
        id: 'exp-proton',
        label: 'What is the Proton?',
        path: '/explanations/proton',
        icon: '◎',
        tooltip: 'Understanding the proton',
      },
      {
        id: 'exp-gravity',
        label: 'What is Gravity?',
        path: '/explanations/gravity',
        icon: '○',
        tooltip: 'Understanding gravitational force',
      },
      {
        id: 'exp-consciousness',
        label: 'Consciousness',
        path: '/explanations/consciousness',
        icon: '◯',
        tooltip: 'The role of consciousness in quantum mechanics',
      },
    ],
  },
  {
    id: 'results',
    title: 'RESULTS',
    icon: '◲',
    defaultExpanded: false,
    items: [
      {
        id: 'results-precision',
        label: 'Precision Table',
        path: '/results/precision',
        badge: 'NEW',
        tooltip: 'Comparison of predicted vs measured values',
      },
      {
        id: 'results-comparison',
        label: 'Comparison Charts',
        path: '/results/comparison',
        tooltip: 'Visual comparison with experimental data',
      },
      {
        id: 'results-achievements',
        label: 'Key Achievements',
        path: '/results/achievements',
        badge: 15,
        tooltip: 'Major theoretical breakthroughs',
      },
      {
        id: 'results-predictions',
        label: 'Predictions',
        path: '/results/predictions',
        badge: 'TESTABLE',
        tooltip: 'Testable predictions of the theory',
      },
    ],
  },
];
