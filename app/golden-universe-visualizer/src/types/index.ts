export interface NavigationItem {
  id: string;
  label: string;
  icon?: string;
  path: string;
  children?: NavigationItem[];
}

export interface TheorySection {
  id: string;
  title: string;
  content: string;
  equations?: string[];
  references?: string[];
}

export interface DerivationStep {
  id: string;
  equation: string;
  explanation: string;
  dependencies?: string[];
}

export interface Derivation {
  id: string;
  title: string;
  description: string;
  steps: DerivationStep[];
  references?: string[];
}

export interface CalculationInput {
  name: string;
  value: number;
  unit?: string;
}

export interface CalculationResult {
  name: string;
  value: number;
  unit?: string;
  formula?: string;
}

export interface Calculation {
  id: string;
  title: string;
  description: string;
  inputs: CalculationInput[];
  results: CalculationResult[];
}

export interface VisualizationData {
  id: string;
  type: 'chart' | 'graph' | '3d' | 'interactive';
  title: string;
  data: unknown;
  config?: Record<string, unknown>;
}

export interface AppState {
  currentSection: string;
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark';
  loading: boolean;
  error: string | null;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: unknown;
}
