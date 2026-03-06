#!/usr/bin/env python3
"""
NLDE DIMENSIONLESS SOLVER - NUMERICAL REFINEMENT
=================================================

Implements dimensionless formulation for better numerical stability.

All quantities in units where m_eff = 1:
    r̃ = r × m_eff (dimensionless radius)
    Ẽ = E / m_eff (dimensionless energy)
    Ṽ(r̃) = V(r) / m_eff (dimensionless potential)

Theory: NLDE_STATUS_AND_NEXT_STEPS.md
Date: 2026-02-10
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import json

print("="*80)
print("NLDE DIMENSIONLESS SOLVER")
print("="*80)
print("\nGoal: Fix numerical stability with dimensionless formulation")
print("Test: Simple attractive Yukawa potential")
print()


class DimensionlessNLDESolver:
    """
    Solves radial Dirac in dimensionless units (m_eff = 1).

    Equations:
        dF/dr̃ = -(κ/r̃) F + (Ẽ + Ṽ) G
        dG/dr̃ = +(κ/r̃) G - (Ẽ - Ṽ) F

    For bound states: Ẽ < 0 (negative binding relative to m_eff = 1)
    """

    def __init__(self, V_tilde_function, kappa=-1):
        """
        Parameters
        ----------
        V_tilde_function : callable
            Dimensionless potential Ṽ(r̃)
        kappa : int
            Angular momentum (κ = -1 for s-wave)
        """
        self.V_tilde = V_tilde_function
        self.kappa = kappa

    def rhs(self, r_tilde, y, E_tilde):
        """RHS of dimensionless radial Dirac."""
        F, G = y

        if r_tilde < 1e-8:
            r_tilde = 1e-8

        V = self.V_tilde(r_tilde)

        dF = -(self.kappa / r_tilde) * F + (E_tilde + V) * G
        dG = +(self.kappa / r_tilde) * G - (E_tilde - V) * F

        return np.array([dF, dG])

    def integrate(self, E_tilde, r_max=20.0, n_points=500):
        """
        Integrate from r̃=0 to r̃=r_max.

        Returns
        -------
        r_grid, F, G : arrays
            Grid and wavefunction components
        """
        r_min = 1e-4

        # Initial conditions for s-wave
        F0 = r_min
        G0 = 1.0
        y0 = np.array([F0, G0])

        # Logarithmic grid for better resolution near origin
        r_grid = np.geomspace(r_min, r_max, n_points)

        sol = solve_ivp(
            lambda r, y: self.rhs(r, y, E_tilde),
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

    def boundary_value(self, E_tilde, r_max=20.0):
        """
        Return F(r_max) for shooting.

        For bound states: F(r_max) should → 0
        """
        r_grid, F, G = self.integrate(E_tilde, r_max)

        if F is None:
            return 1e10  # Integration failed

        # Return value at boundary
        return F[-1]

    def find_bound_state(self, V_strength, r_max=20.0, verbose=True):
        """
        Find bound state for given potential strength.

        For attractive potential, bound state has E < 0.

        Returns
        -------
        E_eigen : float
            Eigenvalue (negative for bound state)
        r_grid, F, G : arrays
            Eigenfunction
        """
        # For bound states with attractive potential:
        # E must be negative (below m_eff = 1)
        # Typical: E ∈ [-V_strength, 0]

        E_min = -2.0 * abs(V_strength)  # Deep binding
        E_max = -0.001  # Shallow binding (just below threshold)

        if verbose:
            print(f"  Searching for bound state:")
            print(f"    Potential strength: V₀ = {V_strength:.4f}")
            print(f"    Energy range: Ẽ ∈ [{E_min:.4f}, {E_max:.4f}]")

        # Check boundaries
        f_min = self.boundary_value(E_min, r_max)
        f_max = self.boundary_value(E_max, r_max)

        if verbose:
            print(f"    Boundary values: F({r_max})_min = {f_min:.2e}, F({r_max})_max = {f_max:.2e}")

        if f_min * f_max > 0:
            if verbose:
                print(f"    ⚠️  Same sign - scanning for bracket...")

            # Scan to find bracket
            E_scan = np.linspace(E_min, E_max, 50)
            for i in range(len(E_scan)-1):
                f1 = self.boundary_value(E_scan[i], r_max)
                f2 = self.boundary_value(E_scan[i+1], r_max)

                if f1 * f2 < 0:
                    E_min = E_scan[i]
                    E_max = E_scan[i+1]
                    if verbose:
                        print(f"    ✅ Found bracket: [{E_min:.6f}, {E_max:.6f}]")
                    break
            else:
                if verbose:
                    print(f"    ❌ Could not find bracket")
                return None, None, None, None

        # Brent's method
        try:
            E_eigen = brentq(
                lambda E: self.boundary_value(E, r_max),
                E_min, E_max,
                xtol=1e-10,
                rtol=1e-10,
                maxiter=100
            )

            if verbose:
                print(f"    ✅ Eigenvalue: Ẽ = {E_eigen:.8f}")

            # Get final wavefunction
            r_grid, F, G = self.integrate(E_eigen, r_max)

            # Normalize (post-hoc)
            # WARNING: For nonlinear NLDE (lock/Soler terms), normalizing AFTER
            # solving is not self-consistent. Needs (ε, u₀) iteration loop.
            norm = np.sqrt(np.trapz(F**2 + G**2, r_grid))
            F = F / norm
            G = G / norm

            if verbose:
                # Compute properties
                r_avg = np.trapz(r_grid * (F**2 + G**2), r_grid)
                r_peak = r_grid[np.argmax(F**2)]

                print(f"    ✅ Wavefunction normalized")
                print(f"       <r̃> = {r_avg:.3f}")
                print(f"       r̃_peak = {r_peak:.3f}")

            return E_eigen, r_grid, F, G

        except ValueError as e:
            if verbose:
                print(f"    ❌ Brent's method failed: {e}")
            return None, None, None, None


# ============================================================
# TEST 1: YUKAWA POTENTIAL
# ============================================================

print("="*80)
print("TEST 1: YUKAWA POTENTIAL")
print("="*80)

def yukawa_potential(r_tilde, V0=-0.5, r0=1.0):
    """
    Attractive Yukawa potential (dimensionless):

    Ṽ(r̃) = -V₀ × exp(-r̃/r₀)

    Parameters
    ----------
    V0 : float
        Potential depth (positive for attractive)
    r0 : float
        Range parameter
    """
    return -abs(V0) * np.exp(-r_tilde/r0)

print("\nPotential: Ṽ(r̃) = -V₀ × exp(-r̃/r₀)")
print("Testing different potential strengths...")

V0_values = [0.1, 0.3, 0.5, 0.7, 1.0]

results = []

for V0 in V0_values:
    print(f"\n{'-'*80}")
    print(f"V₀ = {V0:.1f}, r₀ = 1.0")
    print(f"{'-'*80}")

    # Create solver
    solver = DimensionlessNLDESolver(
        lambda r: yukawa_potential(r, V0=V0, r0=1.0),
        kappa=-1
    )

    # Find bound state
    E, r, F, G = solver.find_bound_state(V0, r_max=30.0, verbose=True)

    if E is not None:
        # Success
        binding = abs(E)
        results.append({
            'V0': V0,
            'E': E,
            'binding': binding,
            'r_peak': r[np.argmax(F**2)]
        })

        print(f"\n  📊 Results:")
        print(f"     Binding energy: |Ẽ| = {binding:.6f}")
        print(f"     ✅ Bound state found!")
    else:
        print(f"\n  ❌ No bound state found")

# Summary
print("\n" + "="*80)
print("SUMMARY: YUKAWA TESTS")
print("="*80)

if results:
    print(f"\n✅ Found {len(results)} bound states\n")
    print(f"{'V₀':>6s} {'Ẽ':>12s} {'|Ẽ|':>12s} {'r̃_peak':>12s}")
    print("-"*50)
    for res in results:
        print(f"{res['V0']:6.1f} {res['E']:12.6f} {res['binding']:12.6f} {res['r_peak']:12.3f}")

    # Save
    with open('/Users/Cristiana_1/Documents/Golden Universe/nlde_yukawa_test.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved: nlde_yukawa_test.json")

    # Conclusion
    print(f"\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    print("\n✅ Dimensionless solver WORKS!")
    print("✅ Eigenvalue bracketing SUCCESSFUL")
    print("✅ Bound states found for attractive potentials")
    print("\n➡️  Ready to implement memory potential")

else:
    print("\n❌ No bound states found - needs further debugging")

print("\n" + "="*80)
print("DONE")
print("="*80 + "\n")
