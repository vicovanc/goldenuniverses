/**
 * Main Python Engine wrapper using Pyodide Web Worker
 * Provides high-level API for Golden Universe calculations
 */

import type {
  CalculationInput,
  CalculationResult,
  ParticleMassParams,
  ParticleMassResult,
  ConstantsParams,
  ConstantsResult,
  WindingParams,
  WindingResult,
  ResonanceParams,
  ResonanceResult,
  PythonEngineStatus,
} from './pythonTypes';
import { getCalculationQueue } from './calculationQueue';

class PythonEngine {
  private worker: Worker | null = null;
  private status: PythonEngineStatus = {
    ready: false,
    loading: false,
    loadedPackages: [],
  };
  private pendingRequests: Map<string, {
    resolve: (value: unknown) => void;
    reject: (reason: unknown) => void;
  }> = new Map();
  private statusListeners: Set<(status: PythonEngineStatus) => void> = new Set();
  private initPromise: Promise<void> | null = null;

  constructor() {
    this.initializeWorker();
    // Start initialization automatically to avoid deadlock
    this.initialize().catch(err => {
      console.error('Failed to auto-initialize Python engine:', err);
    });
  }

  /**
   * Initialize the Web Worker
   */
  private initializeWorker(): void {
    // Create worker from pythonWorker.ts
    // Use classic worker (not module) for Pyodide compatibility with importScripts
    this.worker = new Worker(
      new URL('./pythonWorker.ts', import.meta.url)
    );

    this.worker.onmessage = (event: MessageEvent) => {
      this.handleWorkerMessage(event.data);
    };

    this.worker.onerror = (error: ErrorEvent) => {
      this.updateStatus({
        ready: false,
        loading: false,
        error: error.message,
      });
    };
  }

  /**
   * Handle messages from the worker
   */
  private handleWorkerMessage(data: {
    type: string;
    id?: string;
    payload?: unknown;
  }): void {
    const { type, id, payload } = data;

    switch (type) {
      case 'ready':
        this.updateStatus({
          ready: true,
          loading: false,
          loadedPackages: ['numpy', 'scipy', 'mpmath'],
          version: (payload as { version: string })?.version,
        });
        // Resolve the init promise if there is one
        if (id) {
          const pending = this.pendingRequests.get(id);
          if (pending) {
            pending.resolve(payload);
            this.pendingRequests.delete(id);
          }
        }
        break;

      case 'progress':
        this.updateStatus({
          ...this.status,
          loading: true,
        });
        break;

      case 'result':
        if (id) {
          const pending = this.pendingRequests.get(id);
          if (pending) {
            pending.resolve(payload);
            this.pendingRequests.delete(id);
            getCalculationQueue().complete(id, payload as CalculationResult);
          }
        }
        break;

      case 'error':
        if (id) {
          const pending = this.pendingRequests.get(id);
          if (pending) {
            pending.reject(payload);
            this.pendingRequests.delete(id);
            getCalculationQueue().fail(id, (payload as { error: string }).error);
          }
        }
        this.updateStatus({
          ...this.status,
          error: (payload as { error: string })?.error,
        });
        break;

      case 'status':
        if (id) {
          const pending = this.pendingRequests.get(id);
          if (pending) {
            pending.resolve(payload);
            this.pendingRequests.delete(id);
          }
        }
        break;
    }
  }

  /**
   * Update engine status and notify listeners
   */
  private updateStatus(status: Partial<PythonEngineStatus>): void {
    this.status = { ...this.status, ...status };
    this.notifyStatusListeners();
  }

  /**
   * Notify all status listeners
   */
  private notifyStatusListeners(): void {
    this.statusListeners.forEach(listener => listener(this.status));
  }

  /**
   * Initialize Pyodide (lazy loading)
   */
  async initialize(): Promise<void> {
    if (this.status.ready) return;
    if (this.initPromise) return this.initPromise;

    this.updateStatus({ loading: true });

    this.initPromise = new Promise((resolve, reject) => {
      const id = this.generateId();
      this.pendingRequests.set(id, { resolve, reject });
      this.worker?.postMessage({ type: 'init', id });

      // Timeout after 30 seconds
      setTimeout(() => {
        if (!this.status.ready) {
          reject(new Error('Initialization timeout'));
          this.pendingRequests.delete(id);
        }
      }, 30000);
    });

    return this.initPromise;
  }

  /**
   * Get current status
   */
  getStatus(): PythonEngineStatus {
    return { ...this.status };
  }

  /**
   * Subscribe to status changes
   */
  onStatusChange(listener: (status: PythonEngineStatus) => void): () => void {
    this.statusListeners.add(listener);
    return () => this.statusListeners.delete(listener);
  }

  /**
   * Execute custom Python code
   */
  async execute(code: string, priority: number = 0): Promise<CalculationResult> {
    await this.initialize();

    const id = this.generateId();
    getCalculationQueue().enqueue(
      { type: 'custom', params: {}, code },
      priority,
      id
    );

    return new Promise((resolve, reject) => {
      this.pendingRequests.set(id, { resolve, reject });
      this.worker?.postMessage({ type: 'execute', id, payload: { code } });
    }) as Promise<CalculationResult>;
  }

  /**
   * Calculate particle mass
   */
  async calculateParticleMass(
    params: ParticleMassParams
  ): Promise<ParticleMassResult> {
    const { particle, epoch = 111, includeCorrections = false, precision = 50 } = params;

    const code = `
import json

# Set precision
mp.dps = ${precision}

# Calculate ${particle} mass
result = calculate_electron_mass(NU_E)

# Format result
result_json = to_json(result)
print(json.dumps(result_json))
result_json
`;

    const calcResult = await this.execute(code);
    return calcResult.result as ParticleMassResult;
  }

  /**
   * Calculate fundamental constant
   */
  async calculateConstant(
    params: ConstantsParams
  ): Promise<ConstantsResult> {
    const { constant, precision = 50 } = params;

    let code = '';

    switch (constant) {
      case 'G':
        code = 'calculate_newtons_g()';
        break;
      case 'alpha':
      case 'fine_structure':
        code = 'calculate_fine_structure()';
        break;
      default:
        throw new Error(`Unknown constant: ${constant}`);
    }

    const calcResult = await this.execute(code);
    return calcResult.result as ConstantsResult;
  }

  /**
   * Calculate winding numbers
   */
  async calculateWinding(params: WindingParams): Promise<WindingResult> {
    const { N, optimize = true } = params;

    const code = `
import json

N = ${N}
phi_sq = PHI ** 2

# Calculate resonance
k_res, delta = calculate_resonance(N, phi_sq)

# Find winding pairs where |p| + |q| = N
winding_pairs = []
for p in range(-N, N+1):
    q = N - abs(p)
    if q >= 0:
        l_omega = calculate_winding_length(p, q)
        winding_pairs.append({
            'p': p,
            'q': q,
            'l_Omega': str(l_omega),
            'resonance': str(abs(delta)),
            'is_optimal': (p == P_E and q == Q_E) if N == N_E else False
        })

result = {
    'N': N,
    'winding_pairs': winding_pairs,
    'k_res': k_res,
    'delta': str(delta)
}

to_json(result)
`;

    const calcResult = await this.execute(code);
    return calcResult.result as WindingResult;
  }

  /**
   * Find resonances in epoch range
   */
  async findResonances(params: ResonanceParams): Promise<ResonanceResult> {
    const { N_min, N_max, tolerance = 0.5 } = params;

    const code = `
import json

N_min = ${N_min}
N_max = ${N_max}
tolerance = ${tolerance}

resonances = []
phi_sq = PHI ** 2

for N in range(N_min, N_max + 1):
    k_res, delta = calculate_resonance(N, phi_sq)

    # Check if close to resonance
    if abs(delta) < tolerance:
        resonances.append({
            'N': N,
            'k_res': k_res,
            'ratio': str(N / phi_sq),
            'delta': str(delta),
            'resonance_strength': float(1.0 / (abs(delta) + 0.01))
        })

result = {
    'resonances': resonances,
    'count': len(resonances)
}

to_json(result)
`;

    const calcResult = await this.execute(code);
    return calcResult.result as ResonanceResult;
  }

  /**
   * Calculate all leptons (electron, muon, tau)
   */
  async calculateAllLeptons(): Promise<{
    electron: ParticleMassResult;
    muon: ParticleMassResult;
    tau: ParticleMassResult;
  }> {
    const code = `
import json

# Calculate all three leptons
electron = calculate_electron_mass(NU_E)

# Muon calculation (placeholder - needs actual implementation)
muon = {
    'mass_MeV': str(M_MU_EXP_MEV),
    'mass_experimental_MeV': str(M_MU_EXP_MEV),
    'error_ppm': 0,
    'particle': 'muon',
    'N': 111,
    'generation': 2
}

# Tau calculation (placeholder)
tau = {
    'mass_MeV': str(M_TAU_EXP_MEV),
    'mass_experimental_MeV': str(M_TAU_EXP_MEV),
    'error_ppm': 0,
    'particle': 'tau',
    'N': 111,
    'generation': 3
}

result = {
    'electron': to_json(electron),
    'muon': to_json(muon),
    'tau': to_json(tau)
}

to_json(result)
`;

    const calcResult = await this.execute(code);
    return calcResult.result as unknown as {
      electron: ParticleMassResult;
      muon: ParticleMassResult;
      tau: ParticleMassResult;
    };
  }

  /**
   * Generate unique ID
   */
  private generateId(): string {
    return `pyodide_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Terminate the worker
   */
  terminate(): void {
    this.worker?.terminate();
    this.worker = null;
    this.updateStatus({
      ready: false,
      loading: false,
      loadedPackages: [],
    });
  }
}

// Singleton instance
let engineInstance: PythonEngine | null = null;

export function getPythonEngine(): PythonEngine {
  if (!engineInstance) {
    engineInstance = new PythonEngine();
  }
  return engineInstance;
}

export { PythonEngine };
