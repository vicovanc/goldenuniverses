#!/usr/bin/env python3
"""
LATTICE EPOCH SCANNER - Find ALL Particle Epochs from Geometric Resonance
Based on successful N_e=111 discovery for electron
Following exact methodology from GU theory
"""

import mpmath
import numpy as np
import json
from typing import Dict, List, Tuple

# Set 50-decimal precision
mpmath.mp.dps = 50

# Fundamental constants
phi = mpmath.mpf('1.6180339887498948482045868343656381177203091798057628621354486227')
pi = mpmath.pi
e = mpmath.e

# Reference masses (CODATA 2018) in MeV
CODATA_MASSES = {
    'electron': 0.51099895,
    'muon': 105.6583755,
    'tau': 1776.86,
    'up': 2.16,  # Current quark mass
    'down': 4.67,
    'strange': 93,
    'charm': 1270,
    'bottom': 4180,
    'top': 172760,
    'W': 80379,
    'Z': 91187.6,
    'Higgs': 125100
}

class LatticeEpochScanner:
    """
    Scan the geometric lattice for particle epoch resonances.

    Core Principle (from N_e=111 success):
    - Resonance condition: N/φ² ≈ integer
    - Quality metric: |N/φ² - round(N/φ²)| < threshold
    - Stability: d²V/dN² has minimum
    """

    def __init__(self, precision=50):
        mpmath.mp.dps = precision
        self.phi = phi
        self.phi_sq = phi * phi
        self.M_P = mpmath.mpf('1.22089e22')  # Planck mass in MeV

    def scan_resonances(self, N_min=1, N_max=200, threshold=0.01):
        """
        Scan for ALL resonant epochs in range.

        The electron was found at N=111 with:
        111/φ² = 42.398... ≈ 42 (0.95% deviation)
        """
        resonances = []

        for N in range(N_min, N_max + 1):
            # Core resonance condition
            ratio = N / self.phi_sq
            k_nearest = round(float(ratio))
            deviation = abs(ratio - k_nearest)
            quality = float(deviation / k_nearest) if k_nearest > 0 else float('inf')

            # Additional criteria from GU theory
            # 1. Phase coherence: exp(2πi N/φ²) should have structure
            phase = mpmath.exp(2j * pi * N / self.phi_sq)
            phase_quality = abs(mpmath.im(phase))

            # 2. Octave resonance: N should relate to powers of 2
            octave = mpmath.log(N, 2)
            octave_quality = abs(octave - round(float(octave)))

            # 3. Golden ratio powers: Check if N ≈ φ^m for integer m
            golden_power = mpmath.log(N, self.phi)
            golden_quality = abs(golden_power - round(float(golden_power)))

            # Combined quality metric
            total_quality = quality + 0.1*phase_quality + 0.05*octave_quality

            if quality < threshold:
                resonances.append({
                    'N': N,
                    'k': k_nearest,
                    'deviation': float(deviation),
                    'quality': quality,
                    'phase_quality': float(phase_quality),
                    'octave_quality': float(octave_quality),
                    'golden_quality': float(golden_quality),
                    'total_quality': float(total_quality),
                    'predicted_mass': float(self.M_P * (2*pi/self.phi**N))
                })

        # Sort by quality
        resonances.sort(key=lambda x: x['total_quality'])
        return resonances

    def find_lepton_epochs(self):
        """
        Find epochs for electron, muon, tau.

        From theory:
        - Electron: N_e = 111 ✓ (confirmed)
        - Muon: N_μ ≈ N_e - ΔN_μ
        - Tau: N_τ ≈ N_e - ΔN_τ

        Where ΔN determined by mass ratios:
        m_μ/m_e ≈ φ^ΔN_μ → ΔN_μ ≈ log_φ(206.77)
        """
        results = {}

        # Electron (known)
        N_e = 111
        results['electron'] = {
            'N': N_e,
            'resonance': float(N_e/self.phi_sq),
            'k': 42,
            'quality': 0.0095  # Known 0.95% deviation
        }

        # Muon
        mass_ratio_mu = CODATA_MASSES['muon'] / CODATA_MASSES['electron']
        Delta_N_mu = mpmath.log(mass_ratio_mu, self.phi)
        N_mu_options = [
            N_e - round(float(Delta_N_mu)),
            N_e - round(float(Delta_N_mu)) - 1,
            N_e - round(float(Delta_N_mu)) + 1
        ]

        # Find best muon epoch
        best_mu = None
        best_mu_quality = float('inf')
        for N in N_mu_options:
            if N > 0:
                ratio = N / self.phi_sq
                k = round(float(ratio))
                quality = abs(ratio - k) / k if k > 0 else float('inf')
                if float(quality) < best_mu_quality:
                    best_mu = N
                    best_mu_quality = float(quality)

        results['muon'] = {
            'N': best_mu,
            'resonance': float(best_mu/self.phi_sq) if best_mu else None,
            'k': round(float(best_mu/self.phi_sq)) if best_mu else None,
            'quality': best_mu_quality,
            'Delta_N': round(float(Delta_N_mu))
        }

        # Tau (similar process)
        mass_ratio_tau = CODATA_MASSES['tau'] / CODATA_MASSES['electron']
        Delta_N_tau = mpmath.log(mass_ratio_tau, self.phi)
        N_tau_options = [
            N_e - round(float(Delta_N_tau)),
            N_e - round(float(Delta_N_tau)) - 1,
            N_e - round(float(Delta_N_tau)) + 1
        ]

        best_tau = None
        best_tau_quality = float('inf')
        for N in N_tau_options:
            if N > 0:
                ratio = N / self.phi_sq
                k = round(float(ratio))
                quality = abs(ratio - k) / k if k > 0 else float('inf')
                if float(quality) < best_tau_quality:
                    best_tau = N
                    best_tau_quality = float(quality)

        results['tau'] = {
            'N': best_tau,
            'resonance': float(best_tau/self.phi_sq) if best_tau else None,
            'k': round(float(best_tau/self.phi_sq)) if best_tau else None,
            'quality': best_tau_quality,
            'Delta_N': round(float(Delta_N_tau))
        }

        return results

    def find_quark_epochs(self):
        """
        Find epochs for all 6 quarks.

        Strategy:
        1. Use mass hierarchy: u < d < s < c < b < t
        2. Apply resonance condition N/φ² ≈ integer
        3. Check SU(5) GUT constraints
        """
        results = {}

        # Starting point: if electron is at N=111
        # Quarks should be at lower N (higher energy scale)

        for quark, mass in [('up', 2.16), ('down', 4.67), ('strange', 93),
                            ('charm', 1270), ('bottom', 4180), ('top', 172760)]:

            # Estimate N from mass scale
            # m ≈ M_P * (2π/φ^N) → N ≈ log_φ(M_P*2π/m)
            estimated_N = mpmath.log(self.M_P * 2 * pi / mass, self.phi)

            # Search nearby integers for best resonance
            N_options = [round(float(estimated_N)) + offset for offset in range(-3, 4)]

            best_N = None
            best_quality = float('inf')

            for N in N_options:
                if 1 <= N <= 200:  # Reasonable range
                    ratio = N / self.phi_sq
                    k = round(float(ratio))
                    quality = abs(ratio - k) / k if k > 0 else float('inf')

                    if float(quality) < best_quality:
                        best_N = N
                        best_quality = float(quality)

            results[quark] = {
                'N': best_N,
                'estimated_N': float(estimated_N),
                'resonance': float(best_N/self.phi_sq) if best_N else None,
                'k': round(float(best_N/self.phi_sq)) if best_N else None,
                'quality': best_quality,
                'mass_MeV': mass
            }

        return results

    def find_gauge_boson_epochs(self):
        """
        Find epochs for W, Z, photon, gluons.

        From GU theory:
        - Gauge bosons emerge at symmetry breaking scales
        - Should show strong resonances
        """
        results = {}

        # W and Z bosons
        for boson, mass in [('W', 80379), ('Z', 91187.6)]:
            estimated_N = mpmath.log(self.M_P * 2 * pi / mass, self.phi)
            N_options = [round(float(estimated_N)) + offset for offset in range(-3, 4)]

            best_N = None
            best_quality = float('inf')

            for N in N_options:
                if 1 <= N <= 200:
                    ratio = N / self.phi_sq
                    k = round(float(ratio))
                    quality = abs(ratio - k) / k if k > 0 else float('inf')

                    if float(quality) < best_quality:
                        best_N = N
                        best_quality = float(quality)

            results[boson] = {
                'N': best_N,
                'resonance': float(best_N/self.phi_sq) if best_N else None,
                'k': round(float(best_N/self.phi_sq)) if best_N else None,
                'quality': best_quality
            }

        # Photon (massless, but has characteristic scale)
        results['photon'] = {
            'N': 137,  # Related to fine structure constant 1/137
            'note': 'Massless, but α^(-1) ≈ 137 suggests this epoch'
        }

        # Gluons (8 types, related to QCD scale)
        results['gluons'] = {
            'N': 95,  # From GU's QCD analysis
            'note': '8 gluons emerge at QCD scale'
        }

        return results

    def find_su5_multiplets(self):
        """
        Find epochs consistent with SU(5) GUT structure.

        SU(5) representations:
        - 5̄: (d_R^c, ν_e, e)
        - 10: (u_R^c, d_R^c, u_L, d_L, e_R^c)
        - 24: gauge bosons
        """
        print("\n=== SU(5) MULTIPLET ANALYSIS ===")

        # Check if found epochs respect SU(5) structure
        leptons = self.find_lepton_epochs()
        quarks = self.find_quark_epochs()

        # First generation should be in same multiplet
        first_gen = {
            'electron': leptons['electron']['N'],
            'up': quarks['up']['N'] if quarks['up']['N'] else 0,
            'down': quarks['down']['N'] if quarks['down']['N'] else 0
        }

        # Check if they cluster
        clustering = np.std([first_gen['electron'],
                            first_gen['up'],
                            first_gen['down']])

        return {
            'first_generation': first_gen,
            'clustering': float(clustering),
            'su5_compatible': clustering < 5  # Within 5 epochs
        }

    def verify_mass_predictions(self, epochs):
        """
        Calculate predicted masses from found epochs.
        Compare with CODATA values.
        """
        predictions = {}

        for particle, data in epochs.items():
            if isinstance(data, dict) and 'N' in data and data['N']:
                N = data['N']

                # Basic formula (like electron)
                # m = M_P * (2π C/φ^N)
                # For now, assume C ≈ 1 for order estimation
                predicted_mass = float(self.M_P * 2 * pi / self.phi**N)

                if particle in CODATA_MASSES:
                    actual_mass = CODATA_MASSES[particle]
                    error_percent = abs(predicted_mass - actual_mass) / actual_mass * 100

                    predictions[particle] = {
                        'N': N,
                        'predicted_MeV': predicted_mass,
                        'actual_MeV': actual_mass,
                        'error_percent': error_percent,
                        'C_needed': actual_mass / predicted_mass
                    }

        return predictions

def main():
    """Run complete lattice epoch scan."""

    print("="*80)
    print("GEOMETRIC LATTICE EPOCH SCANNER")
    print("Finding ALL particle epochs from resonance principle")
    print("="*80)

    scanner = LatticeEpochScanner()

    # 1. Full resonance scan
    print("\n### STEP 1: SCANNING FULL LATTICE (N=1 to 200)")
    print("-"*80)
    all_resonances = scanner.scan_resonances(N_min=1, N_max=200, threshold=0.02)

    print(f"Found {len(all_resonances)} strong resonances")
    print("\nTop 20 resonances by quality:")
    for i, res in enumerate(all_resonances[:20]):
        print(f"{i+1:2d}. N={res['N']:3d}: {res['N']}/φ² = {res['k']:3d} + {res['deviation']:.4f} "
              f"(Q={res['quality']*100:.2f}%)")

    # 2. Lepton epochs
    print("\n### STEP 2: LEPTON EPOCHS")
    print("-"*80)
    lepton_epochs = scanner.find_lepton_epochs()
    for particle, data in lepton_epochs.items():
        if data['N']:
            print(f"{particle:8s}: N={data['N']:3d}, k={data['k']:3d}, "
                  f"quality={data['quality']*100:.2f}%")

    # 3. Quark epochs
    print("\n### STEP 3: QUARK EPOCHS")
    print("-"*80)
    quark_epochs = scanner.find_quark_epochs()
    for particle, data in quark_epochs.items():
        if data['N']:
            print(f"{particle:8s}: N={data['N']:3d}, k={data['k']:3d}, "
                  f"quality={data['quality']*100:.2f}%, "
                  f"mass={data['mass_MeV']:.2f} MeV")

    # 4. Gauge boson epochs
    print("\n### STEP 4: GAUGE BOSON EPOCHS")
    print("-"*80)
    gauge_epochs = scanner.find_gauge_boson_epochs()
    for particle, data in gauge_epochs.items():
        if 'N' in data:
            if data['N']:
                print(f"{particle:8s}: N={data['N']:3d}")
                if 'note' in data:
                    print(f"         Note: {data['note']}")

    # 5. Check SU(5) compatibility
    su5_check = scanner.find_su5_multiplets()

    # 6. Verify mass predictions
    print("\n### STEP 5: MASS PREDICTION VERIFICATION")
    print("-"*80)

    all_epochs = {**lepton_epochs, **quark_epochs}
    predictions = scanner.verify_mass_predictions(all_epochs)

    print("\nPredicted vs Actual masses (C=1 approximation):")
    for particle, pred in predictions.items():
        print(f"{particle:8s}: N={pred['N']:3d}, "
              f"predicted={pred['predicted_MeV']:.2e} MeV, "
              f"actual={pred['actual_MeV']:.2e} MeV, "
              f"C_needed={pred['C_needed']:.3f}")

    # Save results
    results = {
        'all_resonances': all_resonances[:50],  # Top 50
        'lepton_epochs': lepton_epochs,
        'quark_epochs': quark_epochs,
        'gauge_epochs': gauge_epochs,
        'su5_check': su5_check,
        'mass_predictions': predictions
    }

    with open('lattice_epochs.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print("\n### RESULTS SAVED TO lattice_epochs.json")

    # Summary
    print("\n" + "="*80)
    print("SUMMARY OF FOUND EPOCHS")
    print("="*80)

    confirmed_epochs = []

    # Confirmed high-quality resonances
    for particle in ['electron', 'muon', 'tau']:
        if particle in lepton_epochs and lepton_epochs[particle]['N']:
            data = lepton_epochs[particle]
            if data['quality'] < 0.02:  # <2% deviation
                confirmed_epochs.append((particle, data['N'], data['quality']))

    for particle in ['up', 'down', 'strange', 'charm', 'bottom', 'top']:
        if particle in quark_epochs and quark_epochs[particle]['N']:
            data = quark_epochs[particle]
            if data['quality'] < 0.02:
                confirmed_epochs.append((particle, data['N'], data['quality']))

    print("\nHIGH-CONFIDENCE EPOCHS (Q < 2%):")
    for particle, N, quality in sorted(confirmed_epochs, key=lambda x: x[1]):
        print(f"  {particle:10s}: N={N:3d} (Q={quality*100:.2f}%)")

    print("\nNEXT STEPS:")
    print("1. For each found epoch N, solve NLDE to get exact C_e factor")
    print("2. Include memory accumulation H[Ω]=ρ⁴ for bound states")
    print("3. Run FRG flow from M_P to each particle scale")
    print("4. Verify mass predictions match CODATA within 1%")

if __name__ == "__main__":
    main()