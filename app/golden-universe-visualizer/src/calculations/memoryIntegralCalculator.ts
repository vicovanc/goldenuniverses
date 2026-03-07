/**
 * Memory Integral Calculator
 * Calculate R_mem evolution and RG flow
 */

import { getPythonEngine } from '../services/pythonEngine/pythonEngine';
import type { MemoryIntegralResult } from '../services/pythonEngine/pythonTypes';

export interface RGFlowPoint {
  k: number;
  R_mem: string;
  lambda_eff: string;
  beta_function?: string;
}

export class MemoryIntegralCalculator {
  /**
   * Calculate memory integral evolution
   */
  static async calculateEvolution(
    k_initial: number,
    k_final: number,
    steps: number = 100,
    beta: number = 1.0
  ): Promise<MemoryIntegralResult> {
    const engine = getPythonEngine();

    const code = `
import json
import numpy as np

k_initial = ${k_initial}
k_final = ${k_final}
steps = ${steps}
beta = ${beta}

# Generate k values (log scale)
k_values = np.logspace(np.log10(k_initial), np.log10(k_final), steps)

trajectory = []

for k in k_values:
    # Memory integral R_mem(k)
    # Simplified model: R_mem ∝ k^(-2) with corrections
    R_mem_val = 1.0 / (k**2 + 0.1)

    # Effective coupling λ_eff(k)
    # Running with RG flow: λ_eff = λ_0 / (1 + β·log(k/k_0))
    k_0 = k_initial
    lambda_0 = mp.mpf('0.51097951228960997824303381840723004398203106664718')
    lambda_eff = lambda_0 / (1 + beta * mp.log(k / k_0))

    trajectory.append({
        'k': float(k),
        'R_mem': str(mp.mpf(R_mem_val)),
        'lambda_eff': str(lambda_eff)
    })

result = {
    'trajectory': trajectory,
    'final_value': str(mp.mpf(trajectory[-1]['R_mem'])),
    'k_initial': k_initial,
    'k_final': k_final,
    'steps': steps
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as MemoryIntegralResult;
  }

  /**
   * Calculate R_mem at specific scale k
   */
  static async calculateAtScale(k: number): Promise<{
    k: number;
    R_mem: string;
    lambda_eff: string;
  }> {
    const engine = getPythonEngine();

    const code = `
import json

k = ${k}

# Memory integral at scale k
R_mem_val = 1.0 / (k**2 + 0.1)

# Effective coupling
lambda_0 = mp.mpf('0.51097951228960997824303381840723004398203106664718')
lambda_eff = lambda_0 / (1 + mp.log(k + 1))

result = {
    'k': k,
    'R_mem': str(mp.mpf(R_mem_val)),
    'lambda_eff': str(lambda_eff)
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      k: number;
      R_mem: string;
      lambda_eff: string;
    };
  }

  /**
   * Calculate beta function for RG flow
   */
  static async calculateBetaFunction(k: number): Promise<{
    k: number;
    beta: string;
    d_lambda_dk: string;
  }> {
    const engine = getPythonEngine();

    const code = `
import json

k = ${k}

# Beta function: β(λ) = k·dλ/dk
# For Golden Universe: β ∝ λ² (asymptotic freedom)

lambda_0 = mp.mpf('0.51097951228960997824303381840723004398203106664718')
lambda_k = lambda_0 / (1 + mp.log(k + 1))

# β(λ) ≈ -λ²/(4π) (simplified)
beta_val = -lambda_k**2 / (4 * mp.pi)

# Derivative
d_lambda_dk = -lambda_0 / ((1 + mp.log(k + 1))**2 * (k + 1))

result = {
    'k': k,
    'lambda_k': str(lambda_k),
    'beta': str(beta_val),
    'd_lambda_dk': str(d_lambda_dk)
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      k: number;
      beta: string;
      d_lambda_dk: string;
    };
  }

  /**
   * Solve RG flow equation numerically
   */
  static async solveRGFlow(
    k_initial: number,
    k_final: number,
    lambda_initial: number,
    steps: number = 100
  ): Promise<{
    trajectory: RGFlowPoint[];
    fixed_points: Array<{ k: number; lambda: string }>;
  }> {
    const engine = getPythonEngine();

    const code = `
import json
import numpy as np

k_initial = ${k_initial}
k_final = ${k_final}
lambda_initial = ${lambda_initial}
steps = ${steps}

# RG flow equation: dλ/dt = β(λ), where t = log(k)
# β(λ) = -λ²/(4π) (asymptotically free)

k_values = np.logspace(np.log10(k_initial), np.log10(k_final), steps)
trajectory = []

lambda_k = mp.mpf(lambda_initial)

for i, k in enumerate(k_values):
    if i > 0:
        # Euler method: λ_{i+1} = λ_i + β(λ_i)·Δt
        dk = k - k_values[i-1]
        beta_val = -lambda_k**2 / (4 * mp.pi)
        lambda_k = lambda_k + beta_val * (dk / k)

    # Memory integral
    R_mem_val = 1.0 / (k**2 + 0.1)

    trajectory.append({
        'k': float(k),
        'R_mem': str(mp.mpf(R_mem_val)),
        'lambda_eff': str(lambda_k),
        'beta_function': str(-lambda_k**2 / (4 * mp.pi))
    })

# Find fixed points (where β = 0)
fixed_points = []
if abs(lambda_k) < 0.01:
    fixed_points.append({
        'k': float(k_final),
        'lambda': str(lambda_k)
    })

result = {
    'trajectory': trajectory,
    'fixed_points': fixed_points,
    'lambda_final': str(lambda_k)
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      trajectory: RGFlowPoint[];
      fixed_points: Array<{ k: number; lambda: string }>;
    };
  }

  /**
   * Calculate memory kernel contribution to particle mass
   */
  static async calculateMemoryContribution(
    nu: number,
    l_omega: number,
    k: number = 1
  ): Promise<{
    kappa: string;
    memory_term: string;
    lambda_rec_beta: string;
  }> {
    const engine = getPythonEngine();

    const code = `
import json

nu = ${nu}
l_omega = ${l_omega}
k = ${k}

# Memory kernel: κ = 2√ν·K(ν)/l_Ω
K_nu = mp.ellipk(nu)
kappa = 2 * mp.sqrt(nu) * K_nu / l_omega

# Memory contribution: -(λ_rec/β)·κ/3
lambda_rec_beta = mp.mpf('0.51097951228960997824303381840723004398203106664718')
memory_term = -lambda_rec_beta * kappa / 3

result = {
    'nu': str(nu),
    'l_omega': str(l_omega),
    'K_nu': str(K_nu),
    'kappa': str(kappa),
    'lambda_rec_beta': str(lambda_rec_beta),
    'memory_term': str(memory_term),
    'formula': '-(λ_rec/β)·κ/3 where κ = 2√ν·K(ν)/l_Ω'
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as unknown as {
      kappa: string;
      memory_term: string;
      lambda_rec_beta: string;
    };
  }

  /**
   * Analyze memory effects on mass spectrum
   */
  static async analyzeMemoryEffects(
    particles: Array<{ name: string; nu: number; l_omega: number }>
  ): Promise<
    Array<{
      particle: string;
      kappa: string;
      memory_contribution: string;
      relative_effect: number;
    }>
  > {
    const engine = getPythonEngine();

    const code = `
import json

particles = ${JSON.stringify(particles)}
results = []

lambda_rec_beta = mp.mpf('0.51097951228960997824303381840723004398203106664718')

for p in particles:
    name = p['name']
    nu = mp.mpf(p['nu'])
    l_omega = mp.mpf(p['l_omega'])

    # Calculate κ
    K_nu = mp.ellipk(nu)
    kappa = 2 * mp.sqrt(nu) * K_nu / l_omega

    # Memory contribution
    memory_term = -lambda_rec_beta * kappa / 3

    # Relative effect (compared to leading term)
    # For electron: leading term ≈ 0.398 × K(ν)
    leading_approx = 0.398 * K_nu
    relative = abs(memory_term / leading_approx)

    results.append({
        'particle': name,
        'kappa': str(kappa),
        'memory_contribution': str(memory_term),
        'relative_effect': float(relative)
    })

to_json(results)
`;

    const result = await engine.execute(code);
    return result.result as unknown as Array<{
      particle: string;
      kappa: string;
      memory_contribution: string;
      relative_effect: number;
    }>;
  }

  /**
   * Calculate threshold effects in memory integral
   */
  static async calculateThresholdEffects(
    k_threshold: number,
    k_range: number = 10
  ): Promise<{
    below_threshold: RGFlowPoint[];
    at_threshold: RGFlowPoint;
    above_threshold: RGFlowPoint[];
  }> {
    const result = await this.calculateEvolution(
      k_threshold / k_range,
      k_threshold * k_range,
      100
    );

    const trajectory = result.trajectory;
    const threshold_index = Math.floor(trajectory.length / 2);

    return {
      below_threshold: trajectory.slice(0, threshold_index),
      at_threshold: trajectory[threshold_index],
      above_threshold: trajectory.slice(threshold_index + 1),
    };
  }
}
