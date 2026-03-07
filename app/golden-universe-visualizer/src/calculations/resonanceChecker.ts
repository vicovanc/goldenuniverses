/**
 * Resonance Checker
 * Check N/φ² resonance conditions and find resonant epochs
 */

import { getPythonEngine } from '../services/pythonEngine/pythonEngine';
import type { ResonanceResult } from '../services/pythonEngine/pythonTypes';

export interface ResonancePoint {
  N: number;
  k_res: number;
  ratio: string;
  delta: string;
  resonance_strength: number;
  is_strong: boolean;
}

export class ResonanceChecker {
  /**
   * Check if epoch N is in resonance
   */
  static async checkResonance(
    N: number,
    tolerance: number = 0.5
  ): Promise<{
    is_resonant: boolean;
    k_res: number;
    delta: string;
    strength: number;
  }> {
    const engine = getPythonEngine();

    const code = `
import json

N = ${N}
tolerance = ${tolerance}
phi_sq = PHI ** 2

# Calculate resonance
k_res, delta = calculate_resonance(N, phi_sq)

# Check if within tolerance
is_resonant = abs(delta) < tolerance

# Resonance strength (inverse of detuning)
strength = 1.0 / (abs(delta) + 0.01)

result = {
    'is_resonant': is_resonant,
    'N': N,
    'k_res': int(k_res),
    'delta': str(delta),
    'ratio': str(N / phi_sq),
    'strength': float(strength),
    'tolerance': tolerance
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      is_resonant: boolean;
      k_res: number;
      delta: string;
      strength: number;
    };
  }

  /**
   * Find all resonances in range [N_min, N_max]
   */
  static async findResonances(
    N_min: number,
    N_max: number,
    tolerance: number = 0.5
  ): Promise<ResonancePoint[]> {
    const engine = getPythonEngine();

    const result = await engine.findResonances({ N_min, N_max, tolerance });

    return result.resonances.map(r => ({
      ...r,
      is_strong: Math.abs(parseFloat(r.delta)) < 0.1,
    }));
  }

  /**
   * Find strong resonances (δ < 0.1)
   */
  static async findStrongResonances(
    N_min: number,
    N_max: number
  ): Promise<ResonancePoint[]> {
    const resonances = await this.findResonances(N_min, N_max, 0.1);
    return resonances.filter(r => r.is_strong);
  }

  /**
   * Calculate resonance spectrum
   */
  static async calculateResonanceSpectrum(
    N_max: number = 500,
    step: number = 1
  ): Promise<{
    spectrum: Array<{ N: number; delta: number; strength: number }>;
    peaks: ResonancePoint[];
  }> {
    const engine = getPythonEngine();

    const code = `
import json

N_max = ${N_max}
step = ${step}
phi_sq = PHI ** 2

spectrum = []
peaks = []

for N in range(1, N_max + 1, step):
    k_res, delta = calculate_resonance(N, phi_sq)
    delta_abs = abs(delta)
    strength = 1.0 / (delta_abs + 0.01)

    spectrum.append({
        'N': N,
        'delta': float(delta_abs),
        'strength': float(strength)
    })

    # Identify peaks (strong resonances)
    if delta_abs < 0.1:
        peaks.append({
            'N': N,
            'k_res': int(k_res),
            'ratio': str(N / phi_sq),
            'delta': str(delta),
            'resonance_strength': float(strength),
            'is_strong': True
        })

result = {
    'spectrum': spectrum,
    'peaks': peaks,
    'N_max': N_max
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      spectrum: Array<{ N: number; delta: number; strength: number }>;
      peaks: ResonancePoint[];
    };
  }

  /**
   * Analyze resonance at specific epochs (leptons, baryons)
   */
  static async analyzeParticleResonances(): Promise<{
    electron: ResonancePoint;
    muon: ResonancePoint;
    tau: ResonancePoint;
    proton: ResonancePoint;
  }> {
    const engine = getPythonEngine();

    const code = `
import json

phi_sq = PHI ** 2

# Known particle epochs
particles = {
    'electron': 111,
    'muon': 111,  # Same epoch, different generation
    'tau': 111,   # Same epoch, different generation
    'proton': 111 # Baryon epoch
}

results = {}

for particle, N in particles.items():
    k_res, delta = calculate_resonance(N, phi_sq)
    strength = 1.0 / (abs(delta) + 0.01)

    results[particle] = {
        'N': N,
        'k_res': int(k_res),
        'ratio': str(N / phi_sq),
        'delta': str(delta),
        'resonance_strength': float(strength),
        'is_strong': abs(delta) < 0.5
    }

to_json(results)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      electron: ResonancePoint;
      muon: ResonancePoint;
      tau: ResonancePoint;
      proton: ResonancePoint;
    };
  }

  /**
   * Calculate detuning for epoch N
   */
  static async calculateDetuning(N: number): Promise<{
    delta: string;
    k_res: number;
    exact_ratio: string;
  }> {
    const engine = getPythonEngine();

    const code = `
import json

N = ${N}
phi_sq = PHI ** 2

# Calculate detuning δ = N/φ² - k
k_res, delta = calculate_resonance(N, phi_sq)

result = {
    'N': N,
    'delta': str(delta),
    'k_res': int(k_res),
    'exact_ratio': str(N / phi_sq),
    'phi_squared': str(phi_sq)
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      delta: string;
      k_res: number;
      exact_ratio: string;
    };
  }

  /**
   * Find next resonance after N
   */
  static async findNextResonance(
    N: number,
    tolerance: number = 0.5
  ): Promise<ResonancePoint | null> {
    const engine = getPythonEngine();

    const code = `
import json

N_start = ${N}
tolerance = ${tolerance}
phi_sq = PHI ** 2

# Search for next resonance
next_resonance = None

for N in range(N_start + 1, N_start + 1000):
    k_res, delta = calculate_resonance(N, phi_sq)

    if abs(delta) < tolerance:
        strength = 1.0 / (abs(delta) + 0.01)
        next_resonance = {
            'N': N,
            'k_res': int(k_res),
            'ratio': str(N / phi_sq),
            'delta': str(delta),
            'resonance_strength': float(strength),
            'is_strong': abs(delta) < 0.1
        }
        break

result = {
    'next_resonance': next_resonance
}

to_json(result)
`;

    const result = await engine.execute(code);
    const data = result.result as unknown as { next_resonance: ResonancePoint | null };
    return data.next_resonance;
  }

  /**
   * Compare resonance with Fibonacci ratios
   */
  static async compareWithFibonacci(N: number): Promise<{
    N: number;
    resonance_ratio: string;
    nearest_fibonacci_ratio: string;
    fibonacci_n: number;
    difference: string;
  }> {
    const engine = getPythonEngine();

    const code = `
import json

N = ${N}
phi_sq = PHI ** 2

# Calculate N/φ²
resonance_ratio = N / phi_sq

# Compare with Fibonacci ratios F_{n+1}/F_n → φ
# Find nearest Fibonacci index
best_match = None
min_diff = float('inf')

for n in range(1, 200):
    fib_ratio = mp.fibonacci(n + 1) / mp.fibonacci(n)
    fib_sq = fib_ratio ** 2
    diff = abs(N / fib_sq - resonance_ratio)

    if diff < min_diff:
        min_diff = diff
        best_match = {
            'fibonacci_n': n,
            'fibonacci_ratio': str(fib_ratio),
            'difference': str(diff)
        }

result = {
    'N': N,
    'resonance_ratio': str(resonance_ratio),
    'nearest_fibonacci_ratio': best_match['fibonacci_ratio'] if best_match else 'None',
    'fibonacci_n': best_match['fibonacci_n'] if best_match else 0,
    'difference': best_match['difference'] if best_match else 'inf'
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      N: number;
      resonance_ratio: string;
      nearest_fibonacci_ratio: string;
      fibonacci_n: number;
      difference: string;
    };
  }

  /**
   * Get known resonant epochs
   */
  static getKnownResonances(): Array<{
    N: number;
    k_res: number;
    description: string;
  }> {
    return [
      { N: 111, k_res: 42, description: 'Lepton epoch (electron, muon, tau)' },
      { N: 42, k_res: 16, description: 'Strong resonance' },
      { N: 16, k_res: 6, description: 'Early epoch' },
      { N: 6, k_res: 2, description: 'Genesis epoch' },
    ];
  }
}
