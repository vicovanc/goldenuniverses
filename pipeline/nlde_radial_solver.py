#!/usr/bin/env python3
"""
NLDE RADIAL SOLVER - PHASE 1: BASIC IMPLEMENTATION
===================================================

Implements shooting method for radial Dirac equation.

Theory: NLDE_DESIGN.md
Date: 2026-02-10

Radial Dirac equation for spherically symmetric potential:
    dF/dr = -(κ/r) F + [E + V(r)] G
    dG/dr = +(κ/r) G - [E - V(r)] F

where:
    F(r): Large component (radial)
    G(r): Small component (radial)
    κ: Angular momentum quantum number (κ = -1 for s-wave)
    E: Energy eigenvalue
    V(r): Effective potential

Boundary conditions:
    r → 0: F(r) ~ r^|κ|, G(r) ~ r^(|κ|-1)
    r → ∞: F(r), G(r) → 0 exponentially

"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# Optional matplotlib
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# Physical constants (in natural units ℏ = c = 1)
M_P_GEV = 1.22e19  # Planck mass in GeV
M_E_GEV = 0.511e-3  # Electron mass in GeV

print("="*80)
print("NLDE RADIAL SOLVER - PHASE 1")
print("="*80)
print("\nImplementing:")
print("  • Radial Dirac equation integrator")
print("  • Shooting method for eigenvalue search")
print("  • Validation with Coulomb potential (hydrogen)")
print()


class RadialDiracSolver:
    """
    Solves radial Dirac equation using shooting method.

    Finds bound state eigenvalues E for given potential V(r).
    """

    def __init__(self, V_potential, kappa=-1, m_central=1.0):
        """
        Parameters
        ----------
        V_potential : callable
            Effective potential V(r) as function of radius r
        kappa : int
            Angular momentum quantum number (κ = -1 for s-wave)
        m_central : float
            Central mass scale (for dimensionless units)
        """
        self.V = V_potential
        self.kappa = kappa
        self.m_central = m_central

    def radial_dirac_rhs(self, r, y, E):
        """
        Right-hand side of radial Dirac equation.

        Parameters
        ----------
        r : float
            Radial coordinate
        y : array [F, G]
            State vector [large component, small component]
        E : float
            Energy eigenvalue (trial)

        Returns
        -------
        dydr : array [dF/dr, dG/dr]
        """
        F, G = y

        # Avoid singularity at r=0
        if r < 1e-10:
            r = 1e-10

        # Potential at r
        V_r = self.V(r)

        # Radial Dirac equations
        dF_dr = -(self.kappa / r) * F + (E + V_r) * G
        dG_dr = +(self.kappa / r) * G - (E - V_r) * F

        return np.array([dF_dr, dG_dr])

    def integrate_outward(self, E, r_max=20.0, n_points=1000):
        """
        Integrate radial Dirac equation from r=0 to r=r_max.

        Parameters
        ----------
        E : float
            Trial energy eigenvalue
        r_max : float
            Maximum radius for integration
        n_points : int
            Number of grid points

        Returns
        -------
        r_grid : array
            Radial grid
        F : array
            Large component F(r)
        G : array
            Small component G(r)
        """
        # Initial conditions at small r (not exactly 0)
        r_min = 1e-5

        # For s-wave (κ = -1): F ~ r, G ~ const
        if self.kappa == -1:
            F_0 = r_min
            G_0 = 1.0
        else:
            # General case: F ~ r^|κ|, G ~ r^(|κ|-1)
            abs_kappa = abs(self.kappa)
            F_0 = r_min**abs_kappa
            G_0 = r_min**(abs_kappa - 1) if abs_kappa > 1 else 1.0

        y0 = np.array([F_0, G_0])

        # Logarithmic grid near origin, linear at large r
        r_grid_log = np.geomspace(r_min, 1.0, n_points // 4)
        r_grid_lin = np.linspace(1.0, r_max, 3 * n_points // 4)
        r_grid = np.concatenate([r_grid_log, r_grid_lin[1:]])

        # Integrate with high accuracy
        sol = solve_ivp(
            lambda r, y: self.radial_dirac_rhs(r, y, E),
            (r_min, r_max),
            y0,
            t_eval=r_grid,
            method='DOP853',  # 8th order Runge-Kutta
            rtol=1e-10,
            atol=1e-12
        )

        if not sol.success:
            raise RuntimeError(f"Integration failed: {sol.message}")

        F = sol.y[0, :]
        G = sol.y[1, :]

        return r_grid, F, G

    def boundary_condition(self, E, r_max=20.0):
        """
        Compute boundary condition at r=r_max.

        For bound states, we require F(r_max) ≈ 0.

        Parameters
        ----------
        E : float
            Trial energy
        r_max : float
            Maximum radius

        Returns
        -------
        F_boundary : float
            Value of F at r_max (should be 0 for eigenvalue)
        """
        try:
            r_grid, F, G = self.integrate_outward(E, r_max)
            return F[-1]
        except:
            # Integration failed - return large value
            return 1e10 if E > 0 else -1e10

    def find_eigenvalue(self, E_min, E_max, r_max=20.0, tol=1e-8):
        """
        Find eigenvalue E using shooting method + Brent's method.

        Parameters
        ----------
        E_min : float
            Lower bound for energy
        E_max : float
            Upper bound for energy
        r_max : float
            Integration radius
        tol : float
            Tolerance for eigenvalue

        Returns
        -------
        E_eigenvalue : float
            Converged eigenvalue
        r_grid : array
            Radial grid
        F : array
            Eigenfunction (large component)
        G : array
            Eigenfunction (small component)
        """
        print(f"\n  Searching for eigenvalue in [{E_min:.6f}, {E_max:.6f}]")

        # Use Brent's method (robust bracketing)
        try:
            E_eigenvalue = brentq(
                lambda E: self.boundary_condition(E, r_max),
                E_min,
                E_max,
                xtol=tol,
                rtol=tol,
                maxiter=100
            )

            print(f"  ✅ Eigenvalue found: E = {E_eigenvalue:.10f}")

            # Get final wavefunction
            r_grid, F, G = self.integrate_outward(E_eigenvalue, r_max)

            # Normalize (post-hoc)
            # WARNING: For nonlinear equations (NLDE with lock/Soler terms),
            # normalizing AFTER solving is NOT self-consistent because the
            # equations depend on |ψ|². A proper fix requires iterating
            # (ε, u₀) with normalization enforced inside the shooting loop.
            # This is acceptable for the LINEAR Dirac case (hydrogen test).
            norm = np.sqrt(np.trapz(F**2 + G**2, r_grid))
            F = F / norm
            G = G / norm

            print(f"  ✅ Wavefunction normalized: ∫(F²+G²)dr = {np.trapz(F**2 + G**2, r_grid):.6f}")
            print(f"     (post-hoc normalization — valid for linear; needs iteration for NLDE)")

            return E_eigenvalue, r_grid, F, G

        except ValueError as e:
            print(f"  ❌ Eigenvalue search failed: {e}")
            raise


# ============================================================
# TEST 1: HYDROGEN ATOM (COULOMB POTENTIAL)
# ============================================================

print("="*80)
print("TEST 1: HYDROGEN ATOM (COULOMB POTENTIAL)")
print("="*80)

def coulomb_potential(r, Z=1, alpha_em=1.0/137.036):
    """
    Coulomb potential: V(r) = -Z α / r

    In atomic units, this gives hydrogen energy levels:
    E_n = -α² m_e / (2n²)

    For ground state (n=1):
    E_1 ≈ -13.6 eV = -1.33 × 10^-5 m_e
    """
    return -Z * alpha_em / r


print("\nSetup:")
print("  Potential: V(r) = -α_EM / r")
print(f"  α_EM = 1/137.036")
print(f"  Mass scale: m_e = {M_E_GEV*1e6:.3f} keV")

# Create solver
solver = RadialDiracSolver(
    V_potential=coulomb_potential,
    kappa=-1,  # s-wave
    m_central=1.0  # In units of m_e
)

# Expected ground state energy
alpha_em = 1.0 / 137.036
E_theory = -alpha_em**2 / 2.0

print(f"\nTheoretical ground state:")
print(f"  E_1 (theory) = -α²/2 = {E_theory:.10f} m_e")
print(f"  E_1 (theory) = {E_theory * M_E_GEV * 1e6:.6f} keV")

# Solve for eigenvalue
E_min = -alpha_em**2  # More bound than n=1
E_max = -alpha_em**2 / 10.0  # Less bound than n=1

try:
    E_numerical, r_grid, F, G = solver.find_eigenvalue(
        E_min=E_min,
        E_max=E_max,
        r_max=50.0,  # 50 Bohr radii
        tol=1e-10
    )

    # Comparison
    error = abs(E_numerical - E_theory) / abs(E_theory) * 100

    print(f"\nNumerical result:")
    print(f"  E_1 (numerical) = {E_numerical:.10f} m_e")
    print(f"  E_1 (numerical) = {E_numerical * M_E_GEV * 1e6:.6f} keV")
    print(f"\n  Error: {error:.6f}%")

    if error < 0.1:
        print(f"  ✅ EXCELLENT agreement (< 0.1%)")
    elif error < 1.0:
        print(f"  ✅ GOOD agreement (< 1%)")
    else:
        print(f"  ⚠️  Needs improvement (> 1%)")

    # Analyze wavefunction
    r_peak = r_grid[np.argmax(F**2)]
    r_avg = np.trapz(r_grid * (F**2 + G**2), r_grid)

    print(f"\nWavefunction properties:")
    print(f"  Peak at: r = {r_peak:.3f} (Bohr radii)")
    print(f"  <r> = {r_avg:.3f} (Bohr radii)")
    print(f"  Theory: <r> = 3/2 = 1.5 (Bohr radii)")

    # Save results
    results = {
        'E_theory': float(E_theory),
        'E_numerical': float(E_numerical),
        'error_percent': float(error),
        'r_peak': float(r_peak),
        'r_avg': float(r_avg)
    }

    import json
    with open('/Users/Cristiana_1/Documents/Golden Universe/nlde_hydrogen_test.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved: nlde_hydrogen_test.json")

    # Plot wavefunction (if matplotlib available)
    if HAS_MATPLOTLIB:
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

            # Radial probability density
            ax1.plot(r_grid, r_grid**2 * (F**2 + G**2), 'b-', linewidth=2, label='r²(F²+G²)')
            ax1.axvline(r_peak, color='r', linestyle='--', alpha=0.7, label=f'Peak: r={r_peak:.2f}')
            ax1.set_xlabel('r (Bohr radii)')
            ax1.set_ylabel('Radial probability density')
            ax1.set_title(f'Hydrogen 1s State (E = {E_numerical:.6f} m_e)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.set_xlim(0, 10)

            # Components F and G
            ax2.plot(r_grid, F, 'b-', linewidth=2, label='F(r) [large]')
            ax2.plot(r_grid, G, 'r-', linewidth=2, label='G(r) [small]')
            ax2.axhline(0, color='k', linestyle='-', alpha=0.3)
            ax2.set_xlabel('r (Bohr radii)')
            ax2.set_ylabel('Wavefunction components')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_xlim(0, 10)

            plt.tight_layout()
            plt.savefig('/Users/Cristiana_1/Documents/Golden Universe/nlde_hydrogen_wavefunction.png', dpi=150)
            print(f"✅ Plot saved: nlde_hydrogen_wavefunction.png")

        except Exception as e:
            print(f"⚠️  Could not create plot: {e}")
    else:
        print(f"⚠️  matplotlib not available, skipping plot")

except Exception as e:
    print(f"\n❌ Test failed: {e}")
    import traceback
    traceback.print_exc()


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "="*80)
print("PHASE 1 SUMMARY")
print("="*80)

print("\n✅ Implemented:")
print("  • RadialDiracSolver class")
print("  • Shooting method with Brent's algorithm")
print("  • Hydrogen atom validation test")

print("\n📊 Validation:")
if error < 0.1:
    print("  ✅ Hydrogen ground state: < 0.1% error")
    print("  ✅ Radial solver WORKING correctly!")
else:
    print(f"  ⚠️  Hydrogen ground state: {error:.3f}% error")
    print("  ⚠️  May need refinement")

print("\n➡️  Next steps (Phase 2):")
print("  1. Implement memory potential Σ_memory(r)")
print("  2. Test with attractive Yukawa potential")
print("  3. Connect to m̄★ parameter")

print("\n" + "="*80)
print("DONE")
print("="*80 + "\n")
