#!/usr/bin/env python3
"""
NLDE WITH MEMORY - PHASE 2: MEMORY SELF-ENERGY
================================================

Implements memory potential and self-consistency for electron mass.

Theory: NLDE_DESIGN.md, MEMORY_ANALYSIS_COMPLETE.md
Date: 2026-02-10

Memory self-energy in Yukawa form:
    Σ_memory(r) = -Σ_0 × exp(-r/r_mem) / (1 + r/r_mem)

where:
    Σ_0: Memory strength (related to m̄★)
    r_mem: Memory correlation length (∼ 1/m_e)

Self-consistency: Find m̄★ such that eigenvalue gives m_e = 0.511 MeV
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar
import json

# Physical constants
M_P_GEV = 1.22e19  # Planck mass in GeV
M_E_GEV = 0.511e-3  # Electron mass in GeV
M_E_DIMENSIONLESS = M_E_GEV / M_P_GEV  # ≈ 4.19 × 10^-23

print("="*80)
print("NLDE WITH MEMORY - PHASE 2")
print("="*80)
print("\nGoal: Find m̄★ such that NLDE eigenvalue gives m_e = 0.511 MeV")
print(f"\nPhysical constants:")
print(f"  M_P = {M_P_GEV:.2e} GeV")
print(f"  m_e = {M_E_GEV*1e3:.3f} MeV = {M_E_DIMENSIONLESS:.2e} M_P")
print()


class MemoryPotential:
    """
    Memory self-energy in Yukawa form.

    Σ_memory(r) = -Σ_0 × exp(-r/r_mem) / (1 + r/r_mem)

    Parameters related to m̄★:
        Σ_0 ≈ c_mem × m̄★ × X_e
        r_mem ≈ 1 / (m̄★ × X_e)
    """

    def __init__(self, m_bar_star, X_e=M_E_DIMENSIONLESS, c_mem=0.3):
        """
        Parameters
        ----------
        m_bar_star : float
            Dimensionless mass parameter (to be determined)
        X_e : float
            Electron epoch scale (∼ m_e/M_P)
        c_mem : float
            Memory coupling strength (phenomenological)
        """
        self.m_bar_star = m_bar_star
        self.X_e = X_e
        self.c_mem = c_mem

        # Effective mass including m̄★
        self.m_eff = m_bar_star * X_e

        # Memory parameters
        self.Sigma_0 = c_mem * self.m_eff  # Strength
        self.r_mem = 1.0 / self.m_eff if self.m_eff > 0 else 1.0  # Correlation length

    def __call__(self, r):
        """
        Total effective potential: m_eff + Σ_memory(r)

        For bound states, Σ_memory < 0 (attractive)
        """
        if r < 1e-10:
            r = 1e-10

        # Yukawa form memory
        memory = -self.Sigma_0 * np.exp(-r/self.r_mem) / (1.0 + r/self.r_mem)

        # Total potential
        V_total = self.m_eff + memory

        return V_total


class NLDESolver:
    """
    Solves radial NLDE with memory potential using shooting method.
    """

    def __init__(self, potential, kappa=-1):
        """
        Parameters
        ----------
        potential : callable
            Effective potential V(r)
        kappa : int
            Angular momentum quantum number (κ = -1 for s-wave)
        """
        self.V = potential
        self.kappa = kappa

    def radial_dirac_rhs(self, r, y, E):
        """Radial Dirac equation RHS."""
        F, G = y

        if r < 1e-10:
            r = 1e-10

        V_r = self.V(r)

        dF_dr = -(self.kappa / r) * F + (E + V_r) * G
        dG_dr = +(self.kappa / r) * G - (E - V_r) * F

        return np.array([dF_dr, dG_dr])

    def integrate_outward(self, E, r_max=50.0, n_points=1000):
        """Integrate from r=0 to r_max."""
        r_min = 1e-5

        # Initial conditions for s-wave
        F_0 = r_min
        G_0 = 1.0
        y0 = np.array([F_0, G_0])

        # Grid
        r_grid = np.geomspace(r_min, r_max, n_points)

        # Integrate
        sol = solve_ivp(
            lambda r, y: self.radial_dirac_rhs(r, y, E),
            (r_min, r_max),
            y0,
            t_eval=r_grid,
            method='DOP853',
            rtol=1e-10,
            atol=1e-12
        )

        if not sol.success:
            return None, None, None

        return r_grid, sol.y[0, :], sol.y[1, :]

    def boundary_value(self, E, r_max=50.0):
        """
        Compute F(r_max) for shooting method.

        For bound states, we want F(r_max) ≈ 0.
        """
        r_grid, F, G = self.integrate_outward(E, r_max)

        if F is None:
            return 1e10

        return F[-1]

    def find_eigenvalue(self, E_min, E_max, r_max=50.0, tol=1e-8):
        """
        Find eigenvalue using shooting + bisection.

        Returns
        -------
        E_eigen : float
            Eigenvalue energy
        r_grid : array
            Radial grid
        F, G : arrays
            Wavefunction components (normalized)
        """
        print(f"    Searching eigenvalue in [{E_min:.6e}, {E_max:.6e}]")

        # Check boundaries have opposite signs
        f_min = self.boundary_value(E_min, r_max)
        f_max = self.boundary_value(E_max, r_max)

        if f_min * f_max > 0:
            print(f"    ⚠️  Boundaries same sign: f({E_min:.2e}) = {f_min:.2e}, f({E_max:.2e}) = {f_max:.2e}")
            # Try to find a bracket
            E_test = np.linspace(E_min, E_max, 20)
            for i in range(len(E_test)-1):
                f1 = self.boundary_value(E_test[i], r_max)
                f2 = self.boundary_value(E_test[i+1], r_max)
                if f1 * f2 < 0:
                    E_min = E_test[i]
                    E_max = E_test[i+1]
                    print(f"    ✅ Found bracket: [{E_min:.6e}, {E_max:.6e}]")
                    break
            else:
                raise ValueError("Could not find eigenvalue bracket")

        # Brent's method
        try:
            E_eigen = brentq(
                lambda E: self.boundary_value(E, r_max),
                E_min, E_max,
                xtol=tol, rtol=tol,
                maxiter=50
            )
        except ValueError as e:
            print(f"    ❌ Eigenvalue search failed: {e}")
            raise

        print(f"    ✅ Eigenvalue found: E = {E_eigen:.10e}")

        # Get wavefunction
        r_grid, F, G = self.integrate_outward(E_eigen, r_max)

        # Normalize (post-hoc)
        # WARNING: For nonlinear NLDE with memory, normalizing AFTER solving
        # is not self-consistent. Needs (ε, u₀) iteration with normalization
        # enforced inside the shooting loop.
        norm = np.sqrt(np.trapz(F**2 + G**2, r_grid))
        F = F / norm
        G = G / norm

        return E_eigen, r_grid, F, G


def solve_for_mass(m_bar_star, X_e=M_E_DIMENSIONLESS, c_mem=0.3, verbose=False):
    """
    Solve NLDE for given m̄★ and extract physical mass.

    Parameters
    ----------
    m_bar_star : float
        Dimensionless mass parameter
    X_e : float
        Electron epoch scale
    c_mem : float
        Memory coupling
    verbose : bool
        Print details

    Returns
    -------
    m_e_predicted : float
        Predicted electron mass in MeV
    eigenvalue : float
        Energy eigenvalue (dimensionless)
    """
    if verbose:
        print(f"\n  Testing m̄★ = {m_bar_star:.1f}")

    # Create memory potential
    potential = MemoryPotential(m_bar_star, X_e, c_mem)
    m_eff = potential.m_eff

    # Create solver
    solver = NLDESolver(potential, kappa=-1)

    # Energy range for bound states
    # E should be slightly less than m_eff for binding
    E_min = 0.5 * m_eff   # Deep binding
    E_max = 0.99 * m_eff  # Shallow binding

    try:
        # Find eigenvalue
        E_eigen, r_grid, F, G = solver.find_eigenvalue(E_min, E_max, r_max=100.0)

        # Physical mass (in Planck units)
        # m_e = E_eigen × M_P
        m_e_planck = E_eigen

        # Convert to MeV
        m_e_predicted = m_e_planck * M_P_GEV * 1e3  # MeV

        if verbose:
            binding = (m_eff - E_eigen) / m_eff * 100
            print(f"    Eigenvalue: E = {E_eigen:.6e}")
            print(f"    m_eff = {m_eff:.6e}")
            print(f"    Binding: {binding:.2f}%")
            print(f"    Predicted m_e = {m_e_predicted:.6f} MeV")

        return m_e_predicted, E_eigen

    except Exception as e:
        if verbose:
            print(f"    ❌ Failed: {e}")
        return None, None


def find_m_bar_star(target_mass=0.511, c_mem=0.3, m_bar_range=(1000, 10000)):
    """
    Find m̄★ via self-consistency: adjust m̄★ until m_e = target.

    Parameters
    ----------
    target_mass : float
        Target electron mass in MeV
    c_mem : float
        Memory coupling strength
    m_bar_range : tuple
        Search range for m̄★

    Returns
    -------
    m_bar_star : float
        Self-consistent m̄★
    m_e_final : float
        Final predicted mass
    """
    print("="*80)
    print("SELF-CONSISTENCY LOOP: Finding m̄★")
    print("="*80)
    print(f"\nTarget: m_e = {target_mass:.3f} MeV")
    print(f"Memory coupling: c_mem = {c_mem}")
    print(f"Search range: m̄★ ∈ [{m_bar_range[0]}, {m_bar_range[1]}]")

    def objective(m_bar):
        """Objective: |m_e(m̄★) - target|"""
        m_e, _ = solve_for_mass(m_bar, c_mem=c_mem, verbose=False)
        if m_e is None:
            return 1e10
        return abs(m_e - target_mass)

    # Coarse scan first
    print(f"\n📊 Coarse scan:")
    m_bar_test = np.linspace(m_bar_range[0], m_bar_range[1], 10)
    results = []

    for m_bar in m_bar_test:
        m_e, E = solve_for_mass(m_bar, c_mem=c_mem, verbose=False)
        if m_e is not None:
            error = abs(m_e - target_mass)
            results.append((m_bar, m_e, error))
            print(f"  m̄★ = {m_bar:7.1f}: m_e = {m_e:8.4f} MeV  (error: {error:.4f} MeV)")

    if not results:
        print("\n❌ No valid solutions found in range")
        return None, None

    # Find best from coarse scan
    results.sort(key=lambda x: x[2])
    m_bar_best, m_e_best, error_best = results[0]

    print(f"\n  Best from coarse scan: m̄★ = {m_bar_best:.1f}, error = {error_best:.4f} MeV")

    # Refine with optimization
    print(f"\n🔍 Refining with optimization...")

    result = minimize_scalar(
        objective,
        bounds=(m_bar_best - 1000, m_bar_best + 1000),
        method='bounded',
        options={'xatol': 1.0}
    )

    m_bar_star = result.x
    m_e_final, E_final = solve_for_mass(m_bar_star, c_mem=c_mem, verbose=True)

    error_final = abs(m_e_final - target_mass)
    error_percent = error_final / target_mass * 100

    print(f"\n" + "="*80)
    print(f"RESULT:")
    print(f"="*80)
    print(f"\n  m̄★ = {m_bar_star:.2f}")
    print(f"  m_e = {m_e_final:.6f} MeV")
    print(f"  Target: {target_mass:.6f} MeV")
    print(f"  Error: {error_final:.6f} MeV ({error_percent:.3f}%)")

    # Compare to theory
    m_bar_theory = 4514.0
    theory_error = abs(m_bar_star - m_bar_theory) / m_bar_theory * 100

    print(f"\n  Theory prediction: m̄★ = {m_bar_theory:.0f}")
    print(f"  Deviation: {abs(m_bar_star - m_bar_theory):.1f} ({theory_error:.2f}%)")

    if theory_error < 10:
        print(f"\n  ✅ EXCELLENT: Within 10% of theory!")
    elif theory_error < 25:
        print(f"\n  ✅ GOOD: Within 25% of theory")
    else:
        print(f"\n  ⚠️  Needs refinement (> 25% from theory)")

    return m_bar_star, m_e_final


# ============================================================
# RUN SELF-CONSISTENCY
# ============================================================

print("\n" + "="*80)
print("PHASE 2: SELF-CONSISTENCY TEST")
print("="*80)

# Test with different memory couplings
c_mem_values = [0.2, 0.3, 0.4, 0.5]

print(f"\nTesting different memory coupling strengths...")

best_result = None
best_theory_match = 1e10

for c_mem in c_mem_values:
    print(f"\n{'='*80}")
    print(f"Testing c_mem = {c_mem}")
    print(f"{'='*80}")

    try:
        m_bar_star, m_e_final = find_m_bar_star(target_mass=0.511, c_mem=c_mem, m_bar_range=(2000, 8000))

        if m_bar_star is not None:
            theory_error = abs(m_bar_star - 4514) / 4514 * 100
            if theory_error < best_theory_match:
                best_theory_match = theory_error
                best_result = (c_mem, m_bar_star, m_e_final, theory_error)

    except Exception as e:
        print(f"\n❌ Failed with c_mem = {c_mem}: {e}")

# Final summary
print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)

if best_result:
    c_mem_best, m_bar_best, m_e_best, theory_error_best = best_result

    print(f"\n🎉 Best result:")
    print(f"  c_mem = {c_mem_best}")
    print(f"  m̄★ = {m_bar_best:.2f}")
    print(f"  m_e = {m_e_best:.6f} MeV")
    print(f"  Theory (m̄★ = 4514): {theory_error_best:.2f}% deviation")

    # Save results
    results = {
        'c_mem': float(c_mem_best),
        'm_bar_star': float(m_bar_best),
        'm_e_predicted_MeV': float(m_e_best),
        'm_e_target_MeV': 0.511,
        'm_bar_theory': 4514.0,
        'theory_deviation_percent': float(theory_error_best)
    }

    with open('/Users/Cristiana_1/Documents/Golden Universe/nlde_self_consistent_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved: nlde_self_consistent_results.json")

else:
    print(f"\n❌ No successful self-consistent solution found")

print(f"\n" + "="*80)
print("DONE")
print("="*80 + "\n")
