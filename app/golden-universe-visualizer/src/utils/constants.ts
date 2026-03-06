import type { NavigationItem } from '@/types';

export const NAVIGATION_ITEMS: NavigationItem[] = [
  {
    id: 'home',
    label: 'Home',
    path: '/',
  },
  {
    id: 'theory',
    label: 'Theory',
    path: '/theory',
    children: [
      {
        id: 'theory-golden-ratio',
        label: 'Golden Ratio',
        path: '/theory/golden-ratio',
      },
      {
        id: 'theory-fibonacci',
        label: 'Fibonacci Sequence',
        path: '/theory/fibonacci',
      },
      {
        id: 'theory-geometry',
        label: 'Sacred Geometry',
        path: '/theory/geometry',
      },
    ],
  },
  {
    id: 'derivations',
    label: 'Derivations',
    path: '/derivations',
    children: [
      {
        id: 'derivations-phi',
        label: 'Phi Derivation',
        path: '/derivations/phi',
      },
      {
        id: 'derivations-relationships',
        label: 'Mathematical Relationships',
        path: '/derivations/relationships',
      },
    ],
  },
  {
    id: 'calculations',
    label: 'Calculations',
    path: '/calculations',
    children: [
      {
        id: 'calculations-interactive',
        label: 'Interactive Calculator',
        path: '/calculations/interactive',
      },
      {
        id: 'calculations-series',
        label: 'Series Calculations',
        path: '/calculations/series',
      },
    ],
  },
  {
    id: 'visualizations',
    label: 'Visualizations',
    path: '/visualizations',
    children: [
      {
        id: 'visualizations-spiral',
        label: 'Golden Spiral',
        path: '/visualizations/spiral',
      },
      {
        id: 'visualizations-rectangle',
        label: 'Golden Rectangle',
        path: '/visualizations/rectangle',
      },
      {
        id: 'visualizations-3d',
        label: '3D Models',
        path: '/visualizations/3d',
      },
    ],
  },
  {
    id: 'results',
    label: 'Results',
    path: '/results',
  },
  {
    id: 'explanations',
    label: 'Explanations',
    path: '/explanations',
    children: [
      {
        id: 'explanations-documents',
        label: 'Complete Theory Papers',
        path: '/explanations/documents',
      },
      {
        id: 'explanations-overview',
        label: 'Theory Overview',
        path: '/explanations/overview',
      },
      {
        id: 'explanations-foundation',
        label: 'Foundation Laws (0-5)',
        path: '/explanations/foundation',
      },
      {
        id: 'explanations-symmetry',
        label: 'Symmetry Laws (6-15)',
        path: '/explanations/symmetry',
      },
      {
        id: 'explanations-particles',
        label: 'Particle Laws (16-25)',
        path: '/explanations/particles',
      },
      {
        id: 'explanations-cosmology',
        label: 'Cosmological Laws (26-30)',
        path: '/explanations/cosmology',
      },
      {
        id: 'explanations-advanced',
        label: 'Advanced Laws (31-38)',
        path: '/explanations/advanced',
      },
      {
        id: 'explanations-lagrangian',
        label: 'Lagrangian Structure',
        path: '/explanations/lagrangian',
      },
      {
        id: 'explanations-validations',
        label: 'Experimental Validations',
        path: '/explanations/validations',
      },
      {
        id: 'explanations-calculations',
        label: 'Python Calculations',
        path: '/explanations/calculations',
      },
      {
        id: 'explanations-concepts',
        label: 'Key Concepts',
        path: '/explanations/concepts',
      },
    ],
  },
  {
    id: 'about',
    label: 'About',
    path: '/about',
  },
];

export const THEME_COLORS = {
  dark: {
    background: '#0a0a0a',
    surface: '#1a1a1a',
    surfaceHover: '#252525',
    primary: '#c9a84e',
    primaryHover: '#d4b56a',
    text: '#e0e0e0',
    textSecondary: '#a0a0a0',
    border: '#333333',
    accent: '#ffd700',
  },
  light: {
    background: '#ffffff',
    surface: '#f5f5f5',
    surfaceHover: '#eeeeee',
    primary: '#b8941e',
    primaryHover: '#c9a530',
    text: '#1a1a1a',
    textSecondary: '#666666',
    border: '#dddddd',
    accent: '#ffa500',
  },
};

export const API_ENDPOINTS = {
  THEORY: '/theory',
  DERIVATIONS: '/derivations',
  CALCULATIONS: '/calculations',
  VISUALIZATIONS: '/visualizations',
};

export const APP_CONFIG = {
  name: 'Golden Universe Visualizer',
  version: '1.0.0',
  description: 'Interactive visualization and exploration of the Golden Ratio and its mathematical properties',
};
