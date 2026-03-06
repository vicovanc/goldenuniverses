import { TheoryLaw } from '@/types/theory';
import { SearchResult } from '@/types/search';

/**
 * Mock theory law data for testing
 */
export const mockTheoryLaw: TheoryLaw = {
  id: 'lagrangian',
  category: 'Fundamental Equations',
  name: 'Master Lagrangian',
  equation: '\\mathcal{L} = \\frac{1}{2}\\partial_\\mu\\phi\\partial^\\mu\\phi - V(\\phi)',
  latex: '\\mathcal{L} = \\frac{1}{2}\\partial_\\mu\\phi\\partial^\\mu\\phi - V(\\phi)',
  description: 'The fundamental Lagrangian density of the Golden Universe theory',
  variables: [
    {
      symbol: '\\phi',
      name: 'Field',
      description: 'The fundamental scalar field',
    },
    {
      symbol: 'V(\\phi)',
      name: 'Potential',
      description: 'The field potential',
    },
  ],
  derivation: 'Derived from first principles...',
  relatedLaws: ['field-equations', 'conservation'],
  examples: [
    {
      description: 'Simple harmonic potential',
      calculation: 'V(\\phi) = \\frac{1}{2}m^2\\phi^2',
    },
  ],
};

/**
 * Mock calculation result
 */
export const mockCalculationResult = {
  id: 'calc-1',
  type: 'particle_mass',
  timestamp: Date.now(),
  parameters: {
    n: 1,
    phi: 1.618033988749895,
  },
  result: {
    mass: 0.511,
    unit: 'MeV',
    accuracy: 0.99,
  },
  status: 'completed' as const,
};

/**
 * Mock search results
 */
export const mockSearchResults: SearchResult[] = [
  {
    id: 'result-1',
    type: 'theory',
    title: 'Master Lagrangian',
    content: 'The fundamental equation describing the Golden Universe',
    category: 'Fundamental Equations',
    relevance: 0.95,
    url: '/theory/lagrangian',
  },
  {
    id: 'result-2',
    type: 'calculation',
    title: 'Particle Mass Calculator',
    content: 'Calculate particle masses using golden ratio',
    category: 'Calculations',
    relevance: 0.87,
    url: '/calculations/particle-mass',
  },
  {
    id: 'result-3',
    type: 'visualization',
    title: 'Phase Space Visualization',
    content: 'Interactive phase space dynamics',
    category: 'Visualizations',
    relevance: 0.75,
    url: '/visualizations/phase-space',
  },
];

/**
 * Mock visualization data
 */
export const mockVisualizationData = {
  id: 'vis-1',
  name: 'Phase Space',
  type: 'phase-space',
  data: {
    points: Array.from({ length: 100 }, (_, i) => ({
      x: Math.cos(i * 0.1),
      y: Math.sin(i * 0.1),
      z: i * 0.01,
    })),
  },
  config: {
    colorScheme: 'golden',
    showGrid: true,
    animate: true,
  },
};

/**
 * Mock navigation tree data
 */
export const mockNavigationTree = {
  id: 'root',
  label: 'Theory',
  path: '/theory',
  children: [
    {
      id: 'fundamentals',
      label: 'Fundamentals',
      path: '/theory/fundamentals',
      children: [
        {
          id: 'lagrangian',
          label: 'Lagrangian',
          path: '/theory/fundamentals/lagrangian',
        },
        {
          id: 'field-equations',
          label: 'Field Equations',
          path: '/theory/fundamentals/field-equations',
        },
      ],
    },
    {
      id: 'applications',
      label: 'Applications',
      path: '/theory/applications',
      children: [],
    },
  ],
};

/**
 * Mock API responses
 */
export const mockApiResponses = {
  calculations: {
    success: {
      success: true,
      data: mockCalculationResult,
    },
    error: {
      success: false,
      error: 'Calculation failed',
    },
  },
  search: {
    success: {
      success: true,
      results: mockSearchResults,
      total: mockSearchResults.length,
    },
    empty: {
      success: true,
      results: [],
      total: 0,
    },
  },
  theory: {
    success: {
      success: true,
      data: mockTheoryLaw,
    },
  },
};

/**
 * Mock user preferences
 */
export const mockUserPreferences = {
  theme: 'dark',
  language: 'en',
  accessibility: {
    highContrast: false,
    reducedMotion: false,
    fontSize: 'medium',
  },
  notifications: {
    enabled: true,
    sound: false,
  },
};

/**
 * Mock performance metrics
 */
export const mockPerformanceMetrics = {
  fps: 60,
  memory: {
    used: 50,
    total: 100,
    limit: 200,
  },
  loadTime: 1234,
  renderTime: 16,
};

/**
 * Mock WebSocket messages
 */
export const mockWebSocketMessages = {
  calculationProgress: {
    type: 'calculation_progress',
    data: {
      id: 'calc-1',
      progress: 0.5,
      status: 'running',
    },
  },
  calculationComplete: {
    type: 'calculation_complete',
    data: mockCalculationResult,
  },
  error: {
    type: 'error',
    data: {
      message: 'Connection failed',
      code: 'WS_ERROR',
    },
  },
};

/**
 * Golden ratio constant for testing
 */
export const PHI = 1.618033988749895;
export const GOLDEN_RATIO = PHI;

/**
 * Mock constants data
 */
export const mockConstants = {
  planck: 6.62607015e-34,
  speedOfLight: 299792458,
  electronMass: 9.1093837015e-31,
  protonMass: 1.67262192369e-27,
  goldenRatio: PHI,
  phi: PHI,
};
