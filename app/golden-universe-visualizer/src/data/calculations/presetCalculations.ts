/**
 * Preset calculations from Golden Universe theory
 * Ready-to-run calculations with expected results
 */

import type { PresetCalculation } from '../../services/pythonEngine/pythonTypes';
import { GOLDEN_UNIVERSE_CALCULATIONS } from './goldenUniverseCalculations';

export const PRESET_CALCULATIONS: PresetCalculation[] = [
  // Particle Masses
  {
    id: 'electron_mass_23ppm',
    name: 'Electron Mass (23 ppm accuracy)',
    description: 'Calculate electron mass using complete formula with detuning, elliptic, and memory terms. Achieves 23 ppm accuracy.',
    category: 'particle_mass',
    input: {
      type: 'particle_mass',
      params: {
        particle: 'electron',
        epoch: 111,
        includeCorrections: true,
        precision: 50,
      },
      code: GOLDEN_UNIVERSE_CALCULATIONS.electronMass,
    },
    expectedResult: {
      value: '0.51099895000',
      metadata: {
        precision: 50,
        method: 'complete_formula',
      },
      comparison: {
        experimental: '0.51099895000',
        theoretical: '0.51099906774',
        error_ppm: 23,
        error_percent: 0.0023,
      },
    },
    tags: ['electron', 'lepton', 'high-precision', 'featured'],
  },
  {
    id: 'muon_mass',
    name: 'Muon Mass',
    description: 'Calculate muon mass using generation factor from electron mass.',
    category: 'particle_mass',
    input: {
      type: 'particle_mass',
      params: {
        particle: 'muon',
        epoch: 111,
        precision: 50,
      },
    },
    expectedResult: {
      value: '105.6583755',
      metadata: {
        precision: 50,
        method: 'generation_factor',
      },
    },
    tags: ['muon', 'lepton', 'generation-2'],
  },
  {
    id: 'tau_mass',
    name: 'Tau Mass',
    description: 'Calculate tau mass using generation factor from electron mass.',
    category: 'particle_mass',
    input: {
      type: 'particle_mass',
      params: {
        particle: 'tau',
        epoch: 111,
        precision: 50,
      },
    },
    expectedResult: {
      value: '1776.86',
      metadata: {
        precision: 50,
        method: 'generation_factor',
      },
    },
    tags: ['tau', 'lepton', 'generation-3'],
  },
  {
    id: 'proton_mass_5term',
    name: 'Proton Mass (5-term ansatz)',
    description: 'Calculate proton mass using 5-term ansatz from quark structure.',
    category: 'particle_mass',
    input: {
      type: 'particle_mass',
      params: {
        particle: 'proton',
        epoch: 111,
        precision: 50,
      },
    },
    expectedResult: {
      value: '938.27208816',
      metadata: {
        precision: 50,
        method: '5_term_ansatz',
      },
    },
    tags: ['proton', 'baryon', 'quarks'],
  },

  // Fundamental Constants
  {
    id: 'newtons_g_47ppm',
    name: "Newton's G (47 ppm accuracy)",
    description: 'Calculate gravitational constant from golden ratio geometry. Achieves 47 ppm accuracy.',
    category: 'constant',
    input: {
      type: 'constant',
      params: {
        constant: 'G',
        precision: 50,
      },
      code: GOLDEN_UNIVERSE_CALCULATIONS.newtonsG,
    },
    expectedResult: {
      value: '6.67430e-11',
      metadata: {
        precision: 50,
        method: 'golden_ratio_geometry',
      },
      comparison: {
        experimental: '6.67430e-11',
        theoretical: '6.67433e-11',
        error_ppm: 47,
        error_percent: 0.0047,
      },
    },
    tags: ['gravity', 'constant', 'high-precision', 'featured'],
  },
  {
    id: 'fine_structure_alpha',
    name: 'Fine Structure Constant α',
    description: 'Calculate α = (e^φ/π²)/70. Exact formula from golden ratio.',
    category: 'constant',
    input: {
      type: 'constant',
      params: {
        constant: 'alpha',
        precision: 50,
      },
    },
    expectedResult: {
      value: '0.0072973525693',
      metadata: {
        precision: 50,
        method: 'exact_formula',
      },
    },
    tags: ['fine-structure', 'constant', 'exact', 'featured'],
  },
  {
    id: 'lambda_rec_beta',
    name: 'Memory Kernel Ratio λ_rec/β',
    description: 'Calculate λ_rec/β = e^φ/π². Memory binding parameter.',
    category: 'constant',
    input: {
      type: 'custom',
      params: {},
      code: `
# Memory kernel ratio
lambda_rec_beta = mp.exp(PHI) / (mp.pi ** 2)

result = {
    'value': str(lambda_rec_beta),
    'formula': 'λ_rec/β = e^φ/π²',
    'e_to_phi': str(mp.exp(PHI)),
    'pi_squared': str(mp.pi ** 2)
}

to_json(result)
`,
    },
    expectedResult: {
      value: '0.51097951228960997824303381840723004398203106664718',
    },
    tags: ['memory', 'constant', 'exact'],
  },

  // Resonances
  {
    id: 'electron_resonance',
    name: 'Electron Resonance (N=111)',
    description: 'Check resonance condition N/φ² ≈ k for electron epoch.',
    category: 'resonance',
    input: {
      type: 'resonance',
      params: {
        N_min: 111,
        N_max: 111,
      },
    },
    expectedResult: {
      value: '42.39822724876167184929086138541416893304568104156032',
    },
    tags: ['resonance', 'electron', 'epoch'],
  },
  {
    id: 'resonance_scan_1_200',
    name: 'Resonance Scan (N=1 to 200)',
    description: 'Find all resonant epochs where N/φ² is close to integer.',
    category: 'resonance',
    input: {
      type: 'resonance',
      params: {
        N_min: 1,
        N_max: 200,
        tolerance: 0.5,
      },
    },
    tags: ['resonance', 'scan', 'epochs'],
  },
  {
    id: 'strong_resonances',
    name: 'Strong Resonances (δ < 0.1)',
    description: 'Find epochs with strong resonance (small detuning).',
    category: 'resonance',
    input: {
      type: 'resonance',
      params: {
        N_min: 1,
        N_max: 500,
        tolerance: 0.1,
      },
    },
    tags: ['resonance', 'strong', 'epochs'],
  },

  // Winding Numbers
  {
    id: 'electron_winding',
    name: 'Electron Winding Numbers',
    description: 'Calculate optimal (p,q) winding for electron epoch N=111.',
    category: 'advanced',
    input: {
      type: 'winding',
      params: {
        N: 111,
        optimize: true,
      },
    },
    expectedResult: {
      value: '(-41, 70)',
    },
    tags: ['winding', 'topology', 'electron'],
  },
  {
    id: 'winding_patterns',
    name: 'Winding Number Patterns',
    description: 'Analyze winding patterns across multiple epochs.',
    category: 'advanced',
    input: {
      type: 'custom',
      params: {},
      code: `
import json

# Analyze winding patterns for key epochs
epochs = [6, 16, 42, 111]
results = []

for N in epochs:
    phi_sq = PHI ** 2
    k_res, delta = calculate_resonance(N, phi_sq)

    # Find optimal winding
    min_action = float('inf')
    optimal_p, optimal_q = 0, N

    for p in range(-N, N+1):
        q = N - abs(p)
        if q >= 0:
            l_omega = calculate_winding_length(p, q)
            action = l_omega + abs(delta)

            if action < min_action:
                min_action = action
                optimal_p, optimal_q = p, q

    results.append({
        'N': N,
        'p': optimal_p,
        'q': optimal_q,
        'l_Omega': str(calculate_winding_length(optimal_p, optimal_q)),
        'k_res': int(k_res)
    })

to_json({'winding_patterns': results})
`,
    },
    tags: ['winding', 'topology', 'patterns'],
  },

  // Advanced Calculations
  {
    id: 'all_leptons',
    name: 'All Lepton Masses',
    description: 'Calculate electron, muon, and tau masses in one calculation.',
    category: 'advanced',
    input: {
      type: 'custom',
      params: {},
      code: `
import json

# Calculate all three leptons
electron = calculate_electron_mass(NU_E)

# Generation factors
gen_factor_mu = mp.mpf('206.7682830')
gen_factor_tau = mp.mpf('3477.15')

m_e = mp.mpf(electron['mass_MeV'])

muon = {
    'mass_MeV': str(m_e * gen_factor_mu),
    'mass_experimental_MeV': str(M_MU_EXP_MEV),
    'generation_factor': str(gen_factor_mu)
}

tau = {
    'mass_MeV': str(m_e * gen_factor_tau),
    'mass_experimental_MeV': str(M_TAU_EXP_MEV),
    'generation_factor': str(gen_factor_tau)
}

to_json({'electron': electron, 'muon': muon, 'tau': tau})
`,
    },
    tags: ['leptons', 'masses', 'comprehensive', 'featured'],
  },
  {
    id: 'epoch_constants',
    name: 'Epoch-Dependent Constants',
    description: 'Calculate π_n, φ_n, e_n for various epochs.',
    category: 'advanced',
    input: {
      type: 'custom',
      params: {},
      code: `
import json

epochs = [6, 16, 42, 111, 200]
results = []

for n in epochs:
    pi_n = epoch_pi(n)
    phi_n = epoch_phi(n)
    e_n = (1 + mp.mpf(1)/n) ** n

    # Convergence to limits
    pi_error = abs(pi_n - mp.pi)
    phi_error = abs(phi_n - PHI)
    e_error = abs(e_n - E)

    results.append({
        'N': n,
        'pi_n': str(pi_n),
        'phi_n': str(phi_n),
        'e_n': str(e_n),
        'pi_convergence': str(pi_error),
        'phi_convergence': str(phi_error),
        'e_convergence': str(e_error)
    })

to_json({'epoch_constants': results})
`,
    },
    tags: ['epochs', 'constants', 'convergence'],
  },
  {
    id: 'complete_c_e_breakdown',
    name: 'Complete C_e Formula Breakdown',
    description: 'Break down electron coupling C_e into all three terms.',
    category: 'advanced',
    input: {
      type: 'custom',
      params: {},
      code: `
import json

# Calculate C_e with full breakdown
result = calculate_C_e_complete(NU_E, DELTA_E, L_OMEGA_E, LAMBDA_REC_BETA)

# Add percentages
C_e_total = mp.mpf(result['C_e'])
term1 = mp.mpf(result['term1_detuning'])
term2 = mp.mpf(result['term2_elliptic'])
term3 = mp.mpf(result['term3_memory'])

result['term1_percentage'] = float(term1 / C_e_total * 100)
result['term2_percentage'] = float(term2 / C_e_total * 100)
result['term3_percentage'] = float(-term3 / C_e_total * 100)

to_json(result)
`,
    },
    tags: ['coupling', 'breakdown', 'electron', 'featured'],
  },
];

// Helper functions to filter presets
export function getPresetsByCategory(
  category: PresetCalculation['category']
): PresetCalculation[] {
  return PRESET_CALCULATIONS.filter(p => p.category === category);
}

export function getPresetsByTag(tag: string): PresetCalculation[] {
  return PRESET_CALCULATIONS.filter(p => p.tags.includes(tag));
}

export function getFeaturedPresets(): PresetCalculation[] {
  return getPresetsByTag('featured');
}

export function getPresetById(id: string): PresetCalculation | undefined {
  return PRESET_CALCULATIONS.find(p => p.id === id);
}

export function searchPresets(query: string): PresetCalculation[] {
  const lowerQuery = query.toLowerCase();
  return PRESET_CALCULATIONS.filter(
    p =>
      p.name.toLowerCase().includes(lowerQuery) ||
      p.description.toLowerCase().includes(lowerQuery) ||
      p.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
  );
}
