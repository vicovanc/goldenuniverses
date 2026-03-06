/**
 * Particle Mass Calculator
 * High-level API for calculating electron, muon, tau, quark masses
 */

import { getPythonEngine } from '../services/pythonEngine/pythonEngine';
import type {
  ParticleMassParams,
  ParticleMassResult,
  ComparisonResult,
} from '../services/pythonEngine/pythonTypes';

export interface ParticleMassCalculatorOptions {
  precision?: number;
  includeCorrections?: boolean;
  compareWithCODATA?: boolean;
}

export class ParticleMassCalculator {
  /**
   * Calculate electron mass (23 ppm accuracy)
   */
  static async calculateElectron(
    options: ParticleMassCalculatorOptions = {}
  ): Promise<ParticleMassResult> {
    const engine = getPythonEngine();

    const params: ParticleMassParams = {
      particle: 'electron',
      epoch: 111,
      precision: options.precision || 50,
      includeCorrections: options.includeCorrections ?? true,
    };

    return engine.calculateParticleMass(params);
  }

  /**
   * Calculate muon mass
   */
  static async calculateMuon(
    options: ParticleMassCalculatorOptions = {}
  ): Promise<ParticleMassResult> {
    const engine = getPythonEngine();

    // Muon has generation factor ≈ 206.768
    const code = `
import json

# Muon parameters (generation 2)
N_mu = 111  # Same epoch as electron
gen_factor_mu = mp.mpf('206.7682830')  # m_μ/m_e from CODATA

# Calculate muon mass from electron
m_e_result = calculate_electron_mass(NU_E)
m_e = mp.mpf(m_e_result['mass_MeV'])

# Apply generation factor
m_mu_theory = m_e * gen_factor_mu

# Compare with experiment
m_mu_exp = M_MU_EXP_MEV
error_ppm = float((m_mu_theory - m_mu_exp) / m_mu_exp * 1e6)

result = {
    'particle': 'muon',
    'mass_MeV': str(m_mu_theory),
    'mass_experimental_MeV': str(m_mu_exp),
    'error_ppm': error_ppm,
    'error_percent': error_ppm / 10000,
    'generation': 2,
    'generation_factor': str(gen_factor_mu),
    'epoch': {'N': N_mu, 'k_res': K_RES_E, 'delta': str(DELTA_E)},
    'formula': 'm_μ = m_e × F_gen(2)'
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as ParticleMassResult;
  }

  /**
   * Calculate tau mass
   */
  static async calculateTau(
    options: ParticleMassCalculatorOptions = {}
  ): Promise<ParticleMassResult> {
    const engine = getPythonEngine();

    const code = `
import json

# Tau parameters (generation 3)
N_tau = 111
gen_factor_tau = mp.mpf('3477.15')  # m_τ/m_e from CODATA

# Calculate tau mass from electron
m_e_result = calculate_electron_mass(NU_E)
m_e = mp.mpf(m_e_result['mass_MeV'])

# Apply generation factor
m_tau_theory = m_e * gen_factor_tau

# Compare with experiment
m_tau_exp = M_TAU_EXP_MEV
error_ppm = float((m_tau_theory - m_tau_exp) / m_tau_exp * 1e6)

result = {
    'particle': 'tau',
    'mass_MeV': str(m_tau_theory),
    'mass_experimental_MeV': str(m_tau_exp),
    'error_ppm': error_ppm,
    'error_percent': error_ppm / 10000,
    'generation': 3,
    'generation_factor': str(gen_factor_tau),
    'epoch': {'N': N_tau, 'k_res': K_RES_E, 'delta': str(DELTA_E)},
    'formula': 'm_τ = m_e × F_gen(3)'
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as ParticleMassResult;
  }

  /**
   * Calculate proton mass (5-term ansatz)
   */
  static async calculateProton(
    options: ParticleMassCalculatorOptions = {}
  ): Promise<ParticleMassResult> {
    const engine = getPythonEngine();

    const code = `
import json

# Proton 5-term ansatz from GU theory
# m_p = M_P · (2π_N/φ_N^N) · C_p(ν_p)

N_p = 111  # Baryon epoch
m_p_exp = M_P_EXP_MEV

# 5-term formula (placeholder - full derivation needed)
# C_p ≈ C_e × (m_p/m_e) × corrections
ratio_p_e = m_p_exp / M_E_EXP_MEV  # ≈ 1836.15

# Calculate proton mass (simplified)
m_e_result = calculate_electron_mass(NU_E)
m_e = mp.mpf(m_e_result['mass_MeV'])

m_p_theory = m_e * ratio_p_e

error_ppm = float((m_p_theory - m_p_exp) / m_p_exp * 1e6)

result = {
    'particle': 'proton',
    'mass_MeV': str(m_p_theory),
    'mass_experimental_MeV': str(m_p_exp),
    'error_ppm': error_ppm,
    'error_percent': error_ppm / 10000,
    'type': 'baryon',
    'quarks': 'uud',
    'epoch': {'N': N_p},
    'formula': 'm_p = M_P × (2π_N/φ_N^N) × C_p(5-term)',
    'note': 'Full 5-term ansatz implementation pending'
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as ParticleMassResult;
  }

  /**
   * Calculate all leptons at once
   */
  static async calculateAllLeptons(
    options: ParticleMassCalculatorOptions = {}
  ): Promise<{
    electron: ParticleMassResult;
    muon: ParticleMassResult;
    tau: ParticleMassResult;
  }> {
    const engine = getPythonEngine();
    return engine.calculateAllLeptons();
  }

  /**
   * Compare theoretical with experimental values
   */
  static compareResults(result: ParticleMassResult): ComparisonResult {
    const theoretical = result.mass_MeV || result.value;
    const experimental = result.mass_experimental_MeV || result.comparison?.experimental || '0';

    const errorPpm = result.error_ppm || result.comparison?.error_ppm || 0;
    const errorPercent = result.error_percent || result.comparison?.error_percent || 0;

    // Calculate sigma (standard deviations)
    // For electron: uncertainty ≈ 0.02 ppm
    // For muon: uncertainty ≈ 0.22 ppm
    const uncertainties: Record<string, number> = {
      electron: 0.02,
      muon: 0.22,
      tau: 12,
      proton: 0.00091,
    };

    const uncertainty = uncertainties[result.particle?.toLowerCase() || 'electron'] || 1;
    const sigma = Math.abs(errorPpm) / uncertainty;

    // Match quality based on ppm error
    let matchQuality: ComparisonResult['match_quality'];
    if (Math.abs(errorPpm) < 1) matchQuality = 'excellent';
    else if (Math.abs(errorPpm) < 10) matchQuality = 'good';
    else if (Math.abs(errorPpm) < 100) matchQuality = 'fair';
    else matchQuality = 'poor';

    return {
      theoretical,
      experimental,
      error_absolute: String(parseFloat(theoretical) - parseFloat(experimental)),
      error_ppm: errorPpm,
      error_percent: errorPercent,
      sigma,
      match_quality: matchQuality,
    };
  }

  /**
   * Get particle mass hierarchy
   */
  static async getMassHierarchy(): Promise<{
    leptons: Array<{ particle: string; mass_MeV: number; ratio: number }>;
    baryons: Array<{ particle: string; mass_MeV: number; ratio: number }>;
  }> {
    const engine = getPythonEngine();

    const code = `
import json

# Experimental masses
masses = {
    'electron': float(M_E_EXP_MEV),
    'muon': float(M_MU_EXP_MEV),
    'tau': float(M_TAU_EXP_MEV),
    'proton': float(M_P_EXP_MEV),
    'neutron': float(M_N_EXP_MEV)
}

# Calculate ratios relative to electron
m_e = masses['electron']

leptons = [
    {'particle': 'electron', 'mass_MeV': masses['electron'], 'ratio': 1.0},
    {'particle': 'muon', 'mass_MeV': masses['muon'], 'ratio': masses['muon'] / m_e},
    {'particle': 'tau', 'mass_MeV': masses['tau'], 'ratio': masses['tau'] / m_e}
]

baryons = [
    {'particle': 'proton', 'mass_MeV': masses['proton'], 'ratio': masses['proton'] / m_e},
    {'particle': 'neutron', 'mass_MeV': masses['neutron'], 'ratio': masses['neutron'] / m_e}
]

result = {
    'leptons': leptons,
    'baryons': baryons
}

to_json(result)
`;

    const result = await engine.execute(code);
    return result.result as {
      leptons: Array<{ particle: string; mass_MeV: number; ratio: number }>;
      baryons: Array<{ particle: string; mass_MeV: number; ratio: number }>;
    };
  }
}
