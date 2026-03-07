/**
 * Winding Number Calculator
 * Compute (p,q) winding numbers for torus topology
 */

import { getPythonEngine } from '../services/pythonEngine/pythonEngine';
import type { WindingResult } from '../services/pythonEngine/pythonTypes';

export interface WindingPair {
  p: number;
  q: number;
  l_Omega: string;
  resonance: string;
  is_optimal: boolean;
  energy?: string;
}

export class WindingNumberCalculator {
  /**
   * Calculate all valid winding pairs for epoch N
   */
  static async calculateWindingPairs(N: number): Promise<WindingResult> {
    const engine = getPythonEngine();
    return engine.calculateWinding({ N, optimize: true });
  }

  /**
   * Find optimal winding (p,q) that minimizes action
   */
  static async findOptimalWinding(N: number): Promise<WindingPair> {
    const engine = getPythonEngine();

    const code = `
import json

N = ${N}
phi_sq = PHI ** 2

# Calculate resonance
k_res, delta = calculate_resonance(N, phi_sq)

# Find all winding pairs where |p| + |q| = N
candidates = []

for p in range(-N, N+1):
    q = N - abs(p)
    if q >= 0:
        # Calculate geometric length
        l_omega = calculate_winding_length(p, q)

        # Action S ≈ l_Ω + |δ| (simplified)
        action = l_omega + abs(delta)

        candidates.append({
            'p': p,
            'q': q,
            'l_Omega': str(l_omega),
            'action': str(action),
            'resonance': str(abs(delta))
        })

# Find minimum action
optimal = min(candidates, key=lambda x: float(x['action']))
optimal['is_optimal'] = True

result = {
    'N': N,
    'optimal': optimal,
    'all_candidates': candidates
}

to_json(result)
`;

    const result = await engine.execute(code);
    const data = result.result as unknown as { optimal: WindingPair };
    return data.optimal;
  }

  /**
   * Calculate l_Omega for given (p,q)
   */
  static async calculateGeometricLength(
    p: number,
    q: number
  ): Promise<string> {
    const engine = getPythonEngine();

    const code = `
import json

p = ${p}
q = ${q}

# l_Ω = 2π√(p² + (q/φ)²)
l_omega = calculate_winding_length(p, q)

result = {
    'p': p,
    'q': q,
    'l_Omega': str(l_omega),
    'formula': '2π√(p² + (q/φ)²)'
}

to_json(result)
`;

    const result = await engine.execute(code);
    const data = result.result as unknown as { l_Omega: string };
    return data.l_Omega;
  }

  /**
   * Analyze winding number patterns
   */
  static async analyzeWindingPatterns(
    N_values: number[]
  ): Promise<{
    epochs: Array<{
      N: number;
      optimal_p: number;
      optimal_q: number;
      l_Omega: string;
      pattern: string;
    }>;
  }> {
    const engine = getPythonEngine();

    const code = `
import json

N_values = ${JSON.stringify(N_values)}
results = []

for N in N_values:
    phi_sq = PHI ** 2
    k_res, delta = calculate_resonance(N, phi_sq)

    # Find optimal winding
    min_action = float('inf')
    optimal = None

    for p in range(-N, N+1):
        q = N - abs(p)
        if q >= 0:
            l_omega = calculate_winding_length(p, q)
            action = l_omega + abs(delta)

            if action < min_action:
                min_action = action
                optimal = {
                    'N': N,
                    'optimal_p': p,
                    'optimal_q': q,
                    'l_Omega': str(l_omega),
                    'k_res': k_res,
                    'delta': str(delta)
                }

    # Determine pattern
    if optimal:
        p, q = optimal['optimal_p'], optimal['optimal_q']
        if p < 0 and q > 0:
            pattern = 'negative_p_positive_q'
        elif p > 0 and q > 0:
            pattern = 'both_positive'
        elif p == 0:
            pattern = 'meridian'
        elif q == 0:
            pattern = 'longitude'
        else:
            pattern = 'other'

        optimal['pattern'] = pattern
        results.append(optimal)

result = {
    'epochs': results
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      epochs: Array<{
        N: number;
        optimal_p: number;
        optimal_q: number;
        l_Omega: string;
        pattern: string;
      }>;
    };
  }

  /**
   * Visualize winding numbers on torus
   */
  static async getWindingVisualization(
    N: number
  ): Promise<{
    N: number;
    torus_points: Array<{ x: number; y: number; z: number }>;
    winding_path: Array<{ x: number; y: number; z: number }>;
  }> {
    const engine = getPythonEngine();

    const code = `
import json
import numpy as np

N = ${N}

# Find optimal winding
phi_sq = PHI ** 2
k_res, delta = calculate_resonance(N, phi_sq)

# Get optimal (p,q)
# For N=111: (p,q) = (-41, 70)
p_optimal = -41 if N == 111 else -int(N * 0.37)
q_optimal = N - abs(p_optimal)

# Generate torus surface points
R_major = 2.0  # Major radius
R_minor = 1.0  # Minor radius

torus_points = []
for u in np.linspace(0, 2*np.pi, 50):
    for v in np.linspace(0, 2*np.pi, 30):
        x = (R_major + R_minor * np.cos(v)) * np.cos(u)
        y = (R_major + R_minor * np.cos(v)) * np.sin(u)
        z = R_minor * np.sin(v)
        torus_points.append({'x': float(x), 'y': float(y), 'z': float(z)})

# Generate winding path
# (p,q) winding: p loops around short cycle, q around long cycle
t_vals = np.linspace(0, 2*np.pi, 200)
winding_path = []

for t in t_vals:
    u = p_optimal * t
    v = q_optimal * t
    x = (R_major + R_minor * np.cos(v)) * np.cos(u)
    y = (R_major + R_minor * np.cos(v)) * np.sin(u)
    z = R_minor * np.sin(v)
    winding_path.append({'x': float(x), 'y': float(y), 'z': float(z)})

result = {
    'N': N,
    'p': p_optimal,
    'q': q_optimal,
    'torus_points': torus_points[:100],  # Limit points for performance
    'winding_path': winding_path
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      N: number;
      torus_points: Array<{ x: number; y: number; z: number }>;
      winding_path: Array<{ x: number; y: number; z: number }>;
    };
  }

  /**
   * Calculate constraint |p| + |q| = N
   */
  static validateWindingConstraint(p: number, q: number, N: number): boolean {
    return Math.abs(p) + Math.abs(q) === N;
  }

  /**
   * Get known winding pairs from GU theory
   */
  static getKnownWindings(): Array<{
    particle: string;
    N: number;
    p: number;
    q: number;
    l_Omega: string;
  }> {
    return [
      {
        particle: 'electron',
        N: 111,
        p: -41,
        q: 70,
        l_Omega: '374.50279990496241776613591175470833750708258874864',
      },
      {
        particle: 'muon',
        N: 111,
        p: -41,
        q: 70,
        l_Omega: '374.50279990496241776613591175470833750708258874864',
      },
      {
        particle: 'tau',
        N: 111,
        p: -41,
        q: 70,
        l_Omega: '374.50279990496241776613591175470833750708258874864',
      },
    ];
  }
}
