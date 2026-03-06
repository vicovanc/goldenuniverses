import { lazyLoadWithRetry, LazyLoad } from '@/utils/lazyLoad';

/**
 * Lazy-loaded route components for better performance
 * Each major section is loaded only when needed
 */

// Pages
export const HomePage = LazyLoad(
  lazyLoadWithRetry(() => import('@/pages/Home'))
);

export const TheoryPage = LazyLoad(
  lazyLoadWithRetry(() => import('@/pages/Theory'))
);

export const DerivationsPage = LazyLoad(
  lazyLoadWithRetry(() => import('@/pages/Derivations'))
);

export const CalculationsPage = LazyLoad(
  lazyLoadWithRetry(() => import('@/pages/Calculations'))
);

export const VisualizationsPage = LazyLoad(
  lazyLoadWithRetry(() => import('@/pages/Visualizations'))
);

// Major components (for code splitting)
export const TheoryExplorer = LazyLoad(
  lazyLoadWithRetry(() => import('@/components/Theory/TheoryExplorer'))
);

export const LawsBrowser = LazyLoad(
  lazyLoadWithRetry(() => import('@/components/Theory/LawsBrowser'))
);

export const LagrangianExplorer = LazyLoad(
  lazyLoadWithRetry(() => import('@/components/Theory/LagrangianExplorer'))
);

// Visualizations (heavy 3D components)
export const PhaseSpaceVisualization = LazyLoad(
  lazyLoadWithRetry(() => import('@/components/Visualizations/PhaseSpaceVisualization'))
);

export const WindingNumbersVisualization = LazyLoad(
  lazyLoadWithRetry(() => import('@/components/Visualizations/WindingNumbersVisualization'))
);

export const FieldDynamicsVisualization = LazyLoad(
  lazyLoadWithRetry(() => import('@/components/Visualizations/FieldDynamicsVisualization'))
);

export const MemoryEvolutionVisualization = LazyLoad(
  lazyLoadWithRetry(() => import('@/components/Visualizations/MemoryEvolutionVisualization'))
);

export const EpochLadderVisualization = LazyLoad(
  lazyLoadWithRetry(() => import('@/components/Visualizations/EpochLadderVisualization'))
);
