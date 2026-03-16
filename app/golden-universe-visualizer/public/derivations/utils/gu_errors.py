#!/usr/bin/env python3
"""
Golden Universe Error Propagation Module

All GU predictions inherit uncertainty from the upstream chain:
  m_e(GU) → α_EM → M_P → G_N → M_0 → every derived quantity

This module provides:
  1. Central values + uncertainties for all base constants
  2. Linear error propagation (∂f/∂x * δx) for analytic formulas
  3. Monte Carlo error propagation for numerical integrations
  4. Formatted output with ± and ppm columns
"""

import mpmath
import numpy as np
from collections import namedtuple

mpmath.mp.dps = 50

# ============================================================================
# BASE UNCERTAIN QUANTITIES
# ============================================================================

UVal = namedtuple('UVal', ['value', 'uncertainty', 'label', 'source'])

phi = mpmath.mpf('1.6180339887498948482045868343656381177203091798057628621354486227')
pi = mpmath.pi
e_num = mpmath.e

m_e_CODATA = UVal(
    value=mpmath.mpf('0.51099895069'),
    uncertainty=mpmath.mpf('0.00000000016'),
    label='m_e (CODATA)',
    source='CODATA 2022'
)

m_e_GU = UVal(
    value=mpmath.mpf('0.51100812'),
    uncertainty=mpmath.mpf('0.00001200'),
    label='m_e (GU)',
    source='Pipeline Ce_exact → 0.511008 MeV (23 ppm from CODATA)'
)

alpha_EM = UVal(
    value=mpmath.mpf('0.0072973525693'),
    uncertainty=mpmath.mpf('0.0000000000011'),
    label='α_EM',
    source='CODATA 2022'
)

# GU derives M_P through the induced gravity relation M_P^2 = 4π c_R M_0^2
# The fractional error in M_P is the same as in m_e(GU) since M_0 ∝ m_e products
M_P_CODATA = UVal(
    value=mpmath.mpf('1.22089e22'),
    uncertainty=mpmath.mpf('0.00014e22'),
    label='M_P (CODATA)',
    source='CODATA 2022'
)

c_R = UVal(
    value=mpmath.mpf('188') / (48 * pi),
    uncertainty=mpmath.mpf('0'),
    label='c_R',
    source='Exact: 188/(48π) from SU(5)+SUSY DOF counting'
)

G_N_CODATA = UVal(
    value=mpmath.mpf('6.67430e-11'),
    uncertainty=mpmath.mpf('0.00015e-11'),
    label='G_N (CODATA)',
    source='CODATA 2022'
)


# ============================================================================
# PROPAGATION FUNCTIONS
# ============================================================================

def fractional_error(uval):
    """Return relative error |δx/x|."""
    if uval.value == 0:
        return float('inf')
    return float(abs(uval.uncertainty / uval.value))


def ppm(uval):
    """Return fractional error in parts per million."""
    return fractional_error(uval) * 1e6


def propagate_product(factors, powers):
    """Propagate error through f = prod(x_i^p_i).
    
    For f = x1^a * x2^b * ..., δf/f = sqrt(sum( (a_i * δx_i/x_i)^2 ))
    
    Args:
        factors: list of UVal objects
        powers: list of exponents corresponding to each factor
    
    Returns:
        UVal with propagated central value and uncertainty
    """
    val = mpmath.mpf(1)
    for f, p in zip(factors, powers):
        val *= f.value ** p

    frac_sq = mpmath.mpf(0)
    for f, p in zip(factors, powers):
        if f.uncertainty > 0:
            frac_sq += (p * f.uncertainty / f.value) ** 2

    unc = abs(val) * mpmath.sqrt(frac_sq)
    labels = ' × '.join(f.label for f in factors)
    return UVal(val, unc, f'product({labels})', 'propagated')


def propagate_linear(partials, uvals, central_value, label=''):
    """Propagate error through f(x1, x2, ...) given ∂f/∂x_i.
    
    δf = sqrt(sum( (∂f/∂x_i * δx_i)^2 ))
    
    Args:
        partials: list of ∂f/∂x_i evaluated at central values
        uvals: list of UVal inputs
        central_value: the central value of f
        label: description
    
    Returns:
        UVal
    """
    var = mpmath.mpf(0)
    for df_dx, u in zip(partials, uvals):
        var += (df_dx * u.uncertainty) ** 2
    return UVal(central_value, mpmath.sqrt(var), label, 'linear propagation')


def monte_carlo(func, uvals, n_samples=10000, seed=42):
    """Monte Carlo error propagation for arbitrary function.
    
    Samples each UVal from a Gaussian(value, uncertainty) distribution
    and evaluates func(*samples) for each trial.
    
    Args:
        func: callable taking len(uvals) mpmath arguments, returns mpmath number
        uvals: list of UVal inputs
        n_samples: number of Monte Carlo trials
        seed: random seed for reproducibility
    
    Returns:
        UVal with mean and std of the Monte Carlo distribution
    """
    rng = np.random.default_rng(seed)
    results = []
    for _ in range(n_samples):
        args = []
        for u in uvals:
            if u.uncertainty > 0:
                sample = float(u.value) + rng.normal(0, float(u.uncertainty))
                args.append(mpmath.mpf(sample))
            else:
                args.append(u.value)
        try:
            results.append(float(func(*args)))
        except (ValueError, ZeroDivisionError):
            continue

    arr = np.array(results)
    return UVal(
        mpmath.mpf(str(np.mean(arr))),
        mpmath.mpf(str(np.std(arr))),
        'MC result',
        f'Monte Carlo ({len(arr)} samples)'
    )


# ============================================================================
# COSMOLOGICAL ERROR CHAIN
# ============================================================================

def m_e_error_ppm():
    """The base error: GU electron mass vs CODATA."""
    delta = abs(m_e_GU.value - m_e_CODATA.value)
    return float(delta / m_e_CODATA.value) * 1e6


def M_P_from_GU():
    """M_P error from the induced gravity chain.
    
    M_P^2 = 4π c_R M_0^2, and M_0 depends on m_e(GU) through the FRG chain.
    The fractional error in M_P is ≈ fractional error in m_e(GU) (same chain).
    """
    frac = fractional_error(m_e_GU)
    return UVal(
        M_P_CODATA.value,
        abs(M_P_CODATA.value) * mpmath.mpf(frac),
        'M_P (GU-propagated)',
        f'm_e(GU) error: {frac*1e6:.1f} ppm'
    )


def G_N_from_GU():
    """G_N error from M_P: G_N = hbar*c / M_P^2, so δG_N/G_N = 2 * δM_P/M_P."""
    M_P_gu = M_P_from_GU()
    frac = 2 * fractional_error(M_P_gu)
    return UVal(
        G_N_CODATA.value,
        abs(G_N_CODATA.value) * mpmath.mpf(frac),
        'G_N (GU-propagated)',
        f'2 × M_P error: {frac*1e6:.1f} ppm'
    )


# ============================================================================
# DISPLAY
# ============================================================================

def format_uval(uval, decimals=6):
    """Format UVal as 'value ± uncertainty (X ppm)'."""
    p = ppm(uval)
    if p < 1:
        return f"{float(uval.value):.{decimals}e} ± {float(uval.uncertainty):.2e} ({p:.3f} ppm)"
    elif p < 1000:
        return f"{float(uval.value):.{decimals}e} ± {float(uval.uncertainty):.2e} ({p:.1f} ppm)"
    else:
        return f"{float(uval.value):.{decimals}e} ± {float(uval.uncertainty):.2e} ({p:.0f} ppm)"


def print_error_chain():
    """Display the full GU error propagation chain."""
    print("=" * 72)
    print("GOLDEN UNIVERSE ERROR PROPAGATION CHAIN")
    print("=" * 72)

    print(f"\n{'Quantity':<30s} {'Value ± Error':<45s} {'ppm':>8s}")
    print("-" * 72)

    chain = [
        m_e_CODATA,
        m_e_GU,
        alpha_EM,
        c_R,
        M_P_CODATA,
        M_P_from_GU(),
        G_N_CODATA,
        G_N_from_GU(),
    ]

    for u in chain:
        p = ppm(u)
        ppm_str = f"{p:.1f}" if p < 1000 else f"{p:.0f}"
        print(f"{u.label:<30s} {format_uval(u)}")

    print(f"\nBase GU→CODATA discrepancy: m_e offset = {m_e_error_ppm():.1f} ppm")
    print("This 23 ppm propagates into ALL derived cosmological observables.")


if __name__ == '__main__':
    print_error_chain()
