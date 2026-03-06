/**
 * TypeScript type definitions for Python engine interoperability
 */

// Calculation input/output types
export interface CalculationInput {
  type: 'particle_mass' | 'constant' | 'winding' | 'resonance' | 'memory_integral' | 'custom';
  params: Record<string, number | string | boolean>;
  code?: string; // For custom calculations
  precision?: number; // Decimal places (default 50)
}

export interface CalculationResult {
  success: boolean;
  result?: CalculationOutput;
  error?: string;
  executionTime: number; // milliseconds
  timestamp: number;
}

export interface CalculationOutput {
  value: string; // High-precision number as string
  components?: Record<string, string>; // Breakdown of calculation
  metadata?: {
    precision: number;
    method: string;
    iterations?: number;
    converged?: boolean;
  };
  comparison?: {
    experimental: string;
    theoretical: string;
    error_ppm: number;
    error_percent: number;
  };
}

// Particle mass calculation
export interface ParticleMassParams {
  particle: 'electron' | 'muon' | 'tau' | 'proton' | 'neutron';
  epoch?: number; // N value (default 111 for electron)
  includeCorrections?: boolean; // QED, EW corrections
  precision?: number;
}

export interface ParticleMassResult extends CalculationOutput {
  particle: string;
  epoch: {
    N: number;
    k_res: number;
    delta: string;
    pi_n: string;
    phi_n: string;
  };
  winding: {
    p: number;
    q: number;
    l_Omega: string;
  };
  coupling: {
    nu_optimal: string;
    C_value: string;
    components: {
      detuning: string;
      elliptic: string;
      memory: string;
    };
  };
  mass_MeV: string;
}

// Fundamental constants
export interface ConstantsParams {
  constant: 'G' | 'alpha' | 'c_R' | 'M_P' | 'fine_structure';
  precision?: number;
}

export interface ConstantsResult extends CalculationOutput {
  constant_name: string;
  formula: string;
  derivation_steps: string[];
  theoretical_value: string;
  experimental_value?: string;
  error_ppm?: number;
}

// Winding numbers
export interface WindingParams {
  N: number; // Epoch number
  optimize?: boolean; // Find optimal (p,q)
}

export interface WindingResult extends CalculationOutput {
  N: number;
  winding_pairs: Array<{
    p: number;
    q: number;
    l_Omega: string;
    resonance: string;
    is_optimal: boolean;
  }>;
  optimal_winding?: {
    p: number;
    q: number;
  };
}

// Resonance conditions
export interface ResonanceParams {
  N_min: number;
  N_max: number;
  tolerance?: number; // Default 0.5
}

export interface ResonanceResult extends CalculationOutput {
  resonances: Array<{
    N: number;
    k_res: number;
    ratio: string; // N/φ²
    delta: string; // Detuning
    resonance_strength: number;
  }>;
}

// Memory integral evolution
export interface MemoryIntegralParams {
  k_initial: number;
  k_final: number;
  steps?: number; // Number of RG steps
  beta?: number; // RG flow parameter
}

export interface MemoryIntegralResult extends CalculationOutput {
  trajectory: Array<{
    k: number;
    R_mem: string;
    lambda_eff: string;
  }>;
  final_value: string;
}

// Python engine status
export interface PythonEngineStatus {
  ready: boolean;
  loading: boolean;
  error?: string;
  loadedPackages: string[];
  version?: string;
}

// Queue management
export interface QueuedCalculation {
  id: string;
  input: CalculationInput;
  status: 'queued' | 'running' | 'completed' | 'failed';
  priority: number;
  submittedAt: number;
  startedAt?: number;
  completedAt?: number;
  result?: CalculationResult;
  progress?: number; // 0-100
}

// Calculation history
export interface CalculationHistoryEntry {
  id: string;
  input: CalculationInput;
  result: CalculationResult;
  timestamp: number;
  notes?: string;
}

// Preset calculations
export interface PresetCalculation {
  id: string;
  name: string;
  description: string;
  category: 'particle_mass' | 'constant' | 'resonance' | 'advanced';
  input: CalculationInput;
  expectedResult?: Partial<CalculationOutput>;
  tags: string[];
}

// CODATA comparison
export interface CODATAValue {
  name: string;
  value: string;
  uncertainty: string;
  unit: string;
  year: number;
}

export interface ComparisonResult {
  theoretical: string;
  experimental: string;
  codata?: CODATAValue;
  error_absolute: string;
  error_ppm: number;
  error_percent: number;
  sigma?: number; // Standard deviations from experimental
  match_quality: 'excellent' | 'good' | 'fair' | 'poor';
}

// Worker message types
export type WorkerMessageType =
  | 'init'
  | 'load_packages'
  | 'execute'
  | 'cancel'
  | 'status';

export interface WorkerMessage {
  type: WorkerMessageType;
  id: string;
  payload?: unknown;
}

export interface WorkerResponse {
  type: 'ready' | 'progress' | 'result' | 'error';
  id: string;
  payload?: unknown;
}

// Export options
export interface ExportFormat {
  format: 'json' | 'csv' | 'markdown' | 'latex';
  includeMetadata?: boolean;
  precision?: number;
}

export interface ExportData {
  calculations: CalculationHistoryEntry[];
  metadata: {
    exportedAt: number;
    totalCalculations: number;
    version: string;
  };
}
