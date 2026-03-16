#!/usr/bin/env python3
"""
10 — Full Coupled ODE System for the GU Cosmic Clock

Implements the canonical GU cosmology Lagrangian system with gate-governed closure status:

  L_total = L_Omega + L_X + L_int + L_mem

with current working closure assumptions:
  - beta(X) = X                         (canonical provisional)
  - lambda_rec(X) = X * e^phi / pi^2    (ratio-level closed, absolute gated)
  - H[Omega] = S_mem = S_coupling = Omega^dag Omega  (Closure 2)
  - Omega → Omega_eq(X)  adiabatic slaving           (Closure 3)
  - N = 70.5 e-folds from TK dilution                (Closure 4)

The system reduces to 3 coupled ODEs in e-fold time N:
  dX/dN, dX_dot/dN, dM/dN

where M is the local memory variable replacing the integral kernel.

Two V_X forms are run and compared:
  Form A: Plateau   V_X = V_0 (1 - exp(-X/mu))^2
  Form B: Axion     V_X = Lambda_X^4 (1 - cos(X/f_X))

Source: Formation doc Sections 16-17, Demonstration doc Ch.2-3
"""

import sys
sys.path.insert(0, '../utils')

import numpy as np
import json
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from pathlib import Path
from pathlib import Path
from importlib.machinery import SourceFileLoader

# ============================================================================
# CONSTANTS (natural units: M_P = 1)
# ============================================================================

phi_gr = 1.6180339887498948482
pi_val = np.pi
e_val = np.e

M_P = 1.0  # work in Planck units

lambda_rec_over_beta = np.exp(phi_gr) / (pi_val**2)  # e^phi / pi^2 ≈ 0.51098

# Closure mode flag used by all closure API functions.
# 'unique' is reserved for gate-passing canonical closure.
# 'provisional' is the currently admitted production fallback.
CLOSURE_MODE = 'provisional'

# GU phase transition epochs (X_c values in Planck units)
# X = M_P * phi^(-n), so X_c at epoch n_c is phi^(-n_c) in Planck units
X_GUT = phi_gr**(-67)
X_EW  = phi_gr**(-89)
X_QCD = phi_gr**(-95)

# Interaction coupling (constrained, see Closure 5)
g_0 = 0.1  # benchmark; to be scanned

# lambda_Omega ≈ phi/pi (from Demonstration doc)
lambda_Omega = phi_gr / pi_val


# ============================================================================
# CLOSURE API (single source of truth)
# ============================================================================

def _sanitize_closure_mode(closure_mode=None):
    mode = CLOSURE_MODE if closure_mode is None else closure_mode
    if mode not in ('unique', 'provisional'):
        raise ValueError(f"Unknown closure_mode={mode!r}; expected 'unique' or 'provisional'.")
    return mode


def beta_X(X, closure_mode=None):
    """Memory decay rate beta(X)."""
    _sanitize_closure_mode(closure_mode)
    return max(float(X), 1e-30)


def lambda_rec_X(X, closure_mode=None):
    """Memory reception strength lambda_rec(X)."""
    _sanitize_closure_mode(closure_mode)
    # Canonical global law is ratio-level: lambda_rec/beta = e^phi/pi^2.
    # Absolute lambda_rec(X) remains gate-controlled until uniqueness + falsification pass.
    return beta_X(X, closure_mode=closure_mode) * lambda_rec_over_beta


def g_OmegaX_X(X, closure_mode=None):
    """Omega-X interaction coupling g_{OmegaX}(X)."""
    mode = _sanitize_closure_mode(closure_mode)
    if mode == 'unique':
        # Canonical no-drift production value used when uniqueness gate passes.
        return float(g_0)
    # Provisional mode keeps one effective dial but no hidden X-shape by default.
    return float(g_0)


def H_Omega_history(X, regime="cosmology"):
    """Canonical history functional policy.

    - cosmology: minimal closure authority H[Omega] = Omega^dagger Omega -> h_X(X)
    - hamiltonian_exact: legacy exact-kernel notation may use rho^4-like composite response
      represented here by h_X(X)**2.
    """
    if regime == "hamiltonian_exact":
        h = h_X(X)
        return h * h
    return h_X(X)


def dg_OmegaX_dX(X, closure_mode=None, dX=None):
    """Numerical derivative of g_{OmegaX}(X)."""
    if dX is None:
        dX = max(abs(X) * 1e-8, 1e-50)
    return (
        g_OmegaX_X(X + dX, closure_mode=closure_mode) -
        g_OmegaX_X(X - dX, closure_mode=closure_mode)
    ) / (2.0 * dX)

print("=" * 80)
print("GOLDEN UNIVERSE: COUPLED ODE SYSTEM")
print("=" * 80)

# ============================================================================
# ADIABATIC HISTORY FUNCTION h(X) = |Omega_eq(X)|^2
# ============================================================================

def h_X(X):
    """Adiabatic history function: Omega_eq squared.
    
    h(X) = 0 when m_Omega^2(X) > 0  (symmetric phase)
    h(X) = -2 m_Omega^2 / lambda_Omega  when m_Omega^2 < 0  (broken phase)
    
    m_Omega^2(X) = M_0^2 [ X/X_c - (pi/phi)^alpha ]
    
    We implement smooth transitions at GUT, EW, QCD thresholds using tanh.
    """
    alpha = 1.0  # O(1) exponent from Demonstration doc
    pi_over_phi_alpha = (pi_val / phi_gr)**alpha

    result = 0.0

    thresholds = [
        (X_GUT, 0.1 * X_GUT),  # GUT transition
        (X_EW,  0.1 * X_EW),   # Electroweak transition
        (X_QCD, 0.1 * X_QCD),  # QCD confinement
    ]

    for X_c, Delta in thresholds:
        # m_Omega^2 changes sign at X_c * (pi/phi)^alpha
        X_crit = X_c * pi_over_phi_alpha
        # Smooth step: 1 below X_crit, 0 above
        step = 0.5 * (1.0 - np.tanh((X - X_crit) / Delta))
        # Condensate value: h = 2|m_Omega^2| / lambda_Omega (in M_P units)
        m_sq_magnitude = (X_crit / X_c) if X < X_crit else 0.0
        result += step * 2.0 * m_sq_magnitude / lambda_Omega

    return result


def dh_dX(X, dX=None):
    """Numerical derivative of h(X)."""
    if dX is None:
        dX = max(abs(X) * 1e-8, 1e-50)
    return (h_X(X + dX) - h_X(X - dX)) / (2 * dX)


# ============================================================================
# POTENTIAL FORMS
# ============================================================================

class PlateauPotential:
    """V_X = V_0 * (1 - exp(-sqrt(2/3) * X / M_P))^2  (Starobinsky-like)
    
    Canonical Starobinsky R^2 form. mu = sqrt(2/3)*M_P is fixed by the
    conformal transformation, NOT a free parameter. Only V_0 is set by A_s.
    """

    def __init__(self, N_target=70.5, A_s=2.1e-9):
        self.N_target = N_target
        self.A_s = A_s
        self.name = "Plateau"
        # V = V_0*(1-exp(-sqrt(2/3)*X/M_P))^2, so mu = M_P*sqrt(3/2)
        # gives the argument X/mu = sqrt(2/3)*X/M_P
        self.mu = M_P * np.sqrt(3.0 / 2.0)  # ≈ 1.2247 M_P (Starobinsky)
        # Analytic: epsilon = (4/3)/(e^y - 1)^2, N ≈ (3/4)*(e^y - y)
        # where y = X/mu.  At large N: y_star ≈ ln(4N/3).
        self.X_star = self.mu * np.log(4.0 * N_target / 3.0)
        exp_arg = np.exp(self.X_star / self.mu)
        epsilon_star = (4.0 / 3.0) / (exp_arg - 1.0)**2
        self.V_0 = 24.0 * pi_val**2 * M_P**4 * A_s * epsilon_star

    def V(self, X):
        arg = X / self.mu
        if arg > 500:
            return self.V_0
        return self.V_0 * (1.0 - np.exp(-arg))**2

    def dV(self, X):
        arg = X / self.mu
        if arg > 500:
            return 0.0
        ex = np.exp(-arg)
        return self.V_0 * 2.0 * (1.0 - ex) * ex / self.mu

    def ddV(self, X):
        arg = X / self.mu
        if arg > 500:
            return 0.0
        ex = np.exp(-arg)
        return self.V_0 * 2.0 * ex * (2.0 * ex - 1.0) / self.mu**2


class AxionPotential:
    """V_X = Lambda_X^4 * (1 - cos(X / f_X))  (Natural inflation)
    
    f_X must be super-Planckian for sufficient e-folds.
    f_X ~ 5-10 M_P is the typical range.
    """

    def __init__(self, N_target=70.5, A_s=2.1e-9):
        self.N_target = N_target
        self.A_s = A_s
        self.name = "Axion"
        self.f_X = 5.5 * M_P

        # X_end where epsilon = 1: cot(X_end/(2f)) = sqrt(2)*f/M_P
        cot_end = np.sqrt(2.0) * self.f_X / M_P
        self.X_end = 2.0 * self.f_X * np.arctan(1.0 / cot_end)

        # N = 2*(f/M_P)^2 * ln(cos(X_end/(2f)) / cos(X_*/(2f)))
        cos_half_end = np.cos(self.X_end / (2.0 * self.f_X))
        cos_half_star = cos_half_end * np.exp(-N_target * M_P**2 / (2.0 * self.f_X**2))
        if abs(cos_half_star) > 1.0:
            cos_half_star = np.sign(cos_half_star) * 0.01
        self.X_star = 2.0 * self.f_X * np.arccos(cos_half_star)

        epsilon_star = (M_P / self.f_X)**2 / 2.0 * \
            (np.sin(self.X_star / self.f_X))**2 / \
            (1.0 - np.cos(self.X_star / self.f_X))**2
        self.Lambda4 = 24.0 * pi_val**2 * M_P**4 * A_s * epsilon_star

    def V(self, X):
        return self.Lambda4 * (1.0 - np.cos(X / self.f_X))

    def dV(self, X):
        return self.Lambda4 * np.sin(X / self.f_X) / self.f_X

    def ddV(self, X):
        return self.Lambda4 * np.cos(X / self.f_X) / self.f_X**2


class LinearPotential:
    """V_X = V_0 * (1 - X / X_max)  for X < X_max, else 0.
    
    Simplest monotonic potential from Law 3.
    epsilon = 1/(2*(X_max - X)²/M_P²) → X_end = X_max - M_P/sqrt(2)
    N from X to X_end = ((X_max - X)² - M_P²/2) / (2*M_P²)
    n_s = 1 - 6/(1+4N), r = 16/(1+4N), eta = 0.
    
    NOTE: r = 0.057 for N=70.5, which EXCEEDS the BICEP/Keck limit r < 0.036.
    This form is included as a theory-band boundary, showing that GU's
    V_X freedom IS constrained by observation.
    """

    def __init__(self, N_target=70.5, A_s=2.1e-9):
        self.N_target = N_target
        self.A_s = A_s
        self.name = "Linear"
        N = N_target
        # epsilon_star = 1/(1 + 4*N)
        epsilon_star = 1.0 / (1.0 + 4.0 * N)
        # Set V_0 from A_s: V_0 ∝ A_s * epsilon_star at the flat end
        # V_star/epsilon_star = 24*pi²*M_P⁴*A_s → V_0 depends on parameterization
        # Use X_max as the free parameter. sigma = V_0/X_max.
        # V_star = V_0 * (1 - X_star/X_max), epsilon = M_P²/(2*(X_max-X)²)
        # At horizon exit: X_max - X_star = M_P*sqrt(1/(2*epsilon_star))
        #                                 = M_P*sqrt((1+4N)/2)
        self.X_max_minus_Xstar = M_P * np.sqrt((1.0 + 4.0 * N) / 2.0)
        # X_end: X_max - X_end = M_P/sqrt(2)
        self.X_max = 20.0 * M_P  # large enough that X > 0 during inflation
        self.X_star = self.X_max - self.X_max_minus_Xstar
        self.sigma = 1.0  # placeholder; V_0 sets the scale
        # V_star/V_0 = (X_max - X_star)/X_max = X_max_minus_Xstar/X_max
        V_ratio_star = self.X_max_minus_Xstar / self.X_max
        # A_s = V_star / (24*pi²*M_P⁴*epsilon_star) = V_0*V_ratio/(24*pi²*M_P⁴*epsilon_star)
        self.V_0 = 24.0 * pi_val**2 * M_P**4 * A_s * epsilon_star / V_ratio_star
        self.sigma = self.V_0 / self.X_max

    def V(self, X):
        val = self.V_0 * (1.0 - X / self.X_max)
        return max(val, 1e-100)

    def dV(self, X):
        if X >= self.X_max:
            return 0.0
        return -self.sigma

    def ddV(self, X):
        return 0.0


# ============================================================================
# EFFECTIVE POTENTIAL AND FORCES
# ============================================================================

def V_X(X, closure_mode=None, pot=None):
    """Canonical potential accessor used by all cosmology scripts.

    If a potential object is provided, it is treated as the selected closure
    branch for that run. Otherwise we default to the plateau branch.
    """
    _sanitize_closure_mode(closure_mode)
    if pot is None:
        # Keep a deterministic default for scripts that use the closure API directly.
        pot = PlateauPotential(N_target=70.5, A_s=2.1e-9)
    return pot.V(X)


def V_eff(X, M, pot=None, closure_mode=None):
    """V_eff = V_X + g_{OmegaX}(X) h(X) X + lambda_rec(X) h(X) M"""
    hX = h_X(X)
    gX = g_OmegaX_X(X, closure_mode=closure_mode)
    lam = lambda_rec_X(X, closure_mode=closure_mode)
    return V_X(X, closure_mode=closure_mode, pot=pot) + gX * hX * X + lam * hX * M


def F_int(X, closure_mode=None):
    """Interaction force: d/dX[g(X)h(X)X]."""
    gX = g_OmegaX_X(X, closure_mode=closure_mode)
    dgX = dg_OmegaX_dX(X, closure_mode=closure_mode)
    hX = h_X(X)
    dhX = dh_dX(X)
    return dgX * hX * X + gX * (hX + X * dhX)


def F_mem(X, M, closure_mode=None):
    """Memory force: d/dX[lambda_rec(X) h(X) M]."""
    lam = lambda_rec_X(X, closure_mode=closure_mode)
    dlam = lambda_rec_over_beta * beta_X(X, closure_mode=closure_mode)
    if beta_X(X, closure_mode=closure_mode) > 0:
        dlam = lambda_rec_over_beta  # d/dX of X*ratio under canonical beta=X
    hX = h_X(X)
    dhX = dh_dX(X)
    return dlam * hX * M + lam * dhX * M


# ============================================================================
# ODE SYSTEM (in e-fold time N)
# ============================================================================

def slow_roll_odes(N, y, pot):
    """Slow-roll approximation: X_N ≈ -M_P^2 * (V' + F_int + F_mem) / V_eff
    
    State: y = [X, M]
    """
    X, M_mem = y

    if X < 1e-100:
        return [0.0, 0.0]

    hX = h_X(X)

    # Forces
    dVdX = pot.dV(X)
    f_int = F_int(X, closure_mode=CLOSURE_MODE)
    f_mem = F_mem(X, M_mem, closure_mode=CLOSURE_MODE)

    # Effective potential
    v_eff = V_eff(X, M_mem, pot=pot, closure_mode=CLOSURE_MODE)
    if v_eff < 1e-100:
        return [0.0, 0.0]

    # Hubble
    H = np.sqrt(v_eff / (3.0 * M_P**2))

    # Slow-roll X evolution
    X_N = -M_P**2 * (dVdX + f_int + f_mem) / v_eff

    # Memory ODE: dM/dN = h(X)/H - (X/H)*M
    if H > 0:
        M_N = hX / H - (beta_X(X, closure_mode=CLOSURE_MODE) / H) * M_mem
    else:
        M_N = 0.0

    return [X_N, M_N]


def full_odes(N, y, pot):
    """Full second-order system (beyond slow-roll).
    
    State: y = [X, X_dot, M]
    where X_dot = dX/dt (cosmic time derivative)
    """
    X, X_dot, M_mem = y

    if X < 1e-100:
        return [0.0, 0.0, 0.0]

    hX = h_X(X)

    dVdX = pot.dV(X)
    f_int = F_int(X, closure_mode=CLOSURE_MODE)
    f_mem = F_mem(X, M_mem, closure_mode=CLOSURE_MODE)

    v_eff = V_eff(X, M_mem, pot=pot, closure_mode=CLOSURE_MODE)

    # Friedmann: 3 M_P^2 H^2 = (1/2) X_dot^2 + V_eff
    energy_density = 0.5 * X_dot**2 + v_eff
    if energy_density < 0:
        energy_density = abs(v_eff)
    H = np.sqrt(energy_density / (3.0 * M_P**2))

    if H < 1e-100:
        return [0.0, 0.0, 0.0]

    # Klein-Gordon: X_ddot + 3H X_dot + dV_eff/dX = 0
    X_ddot = -3.0 * H * X_dot - dVdX - f_int - f_mem

    # Convert to e-fold time: dX/dN = X_dot / H, etc.
    X_N = X_dot / H
    X_dot_N = X_ddot / H - X_dot  # d(X_dot)/dN = X_ddot/H - H_dot/H * X_dot ≈ X_ddot/H - X_dot

    # Memory
    M_N = hX / H - (beta_X(X, closure_mode=CLOSURE_MODE) / H) * M_mem

    return [X_N, X_dot_N, M_N]


# ============================================================================
# SLOW-ROLL PARAMETERS
# ============================================================================

def compute_slow_roll(X, M_mem, pot):
    """Compute effective slow-roll parameters including memory corrections."""
    v_eff = V_eff(X, M_mem, pot=pot, closure_mode=CLOSURE_MODE)
    if v_eff < 1e-100:
        return {'epsilon': 0, 'eta': 0, 'n_s': 1, 'r': 0}

    dVdX_total = pot.dV(X) + F_int(X, closure_mode=CLOSURE_MODE) + F_mem(X, M_mem, closure_mode=CLOSURE_MODE)

    # Numerical second derivative of the full effective gradient
    dX = max(abs(X) * 1e-6, 1e-50)
    grad_plus  = pot.dV(X + dX) + F_int(X + dX, closure_mode=CLOSURE_MODE) + F_mem(X + dX, M_mem, closure_mode=CLOSURE_MODE)
    grad_minus = pot.dV(X - dX) + F_int(X - dX, closure_mode=CLOSURE_MODE) + F_mem(X - dX, M_mem, closure_mode=CLOSURE_MODE)
    ddVdX2_total = (grad_plus - grad_minus) / (2.0 * dX)

    epsilon = 0.5 * M_P**2 * (dVdX_total / v_eff)**2
    eta = M_P**2 * ddVdX2_total / v_eff

    n_s = 1.0 - 6.0 * epsilon + 2.0 * eta
    r = 16.0 * epsilon

    return {'epsilon': epsilon, 'eta': eta, 'n_s': n_s, 'r': r}


def compute_eternal_inflation_metrics(X, M_mem, pot):
    """Compute quantum-diffusion vs classical-drift diagnostics.

    Eternal-inflation criterion (stochastic slow-roll):
      deltaX_quantum > deltaX_classical  per Hubble time (or per e-fold).

    We report:
      - Hubble scale H
      - classical drift per e-fold |dX/dN|
      - quantum step per e-fold H/(2π)
      - ratio R = deltaX_quantum / deltaX_classical
      - scalar power P_R = H^2 / (8π^2 ε M_P^2)
    """
    sr = compute_slow_roll(X, M_mem, pot)
    eps = max(sr['epsilon'], 1e-30)
    v_eff = max(V_eff(X, M_mem, pot=pot, closure_mode=CLOSURE_MODE), 1e-100)

    H = np.sqrt(v_eff / (3.0 * M_P**2))
    dX_dN_classical = M_P * np.sqrt(2.0 * eps)
    deltaX_quantum = H / (2.0 * pi_val)
    ratio_q_over_c = deltaX_quantum / max(dX_dN_classical, 1e-30)
    P_R = H**2 / (8.0 * pi_val**2 * M_P**2 * eps)

    return {
        'H': H,
        'dX_dN_classical': dX_dN_classical,
        'deltaX_quantum': deltaX_quantum,
        'ratio_q_over_c': ratio_q_over_c,
        'P_R': P_R,
        'eternal_local': ratio_q_over_c > 1.0,
    }


# ============================================================================
# INTEGRATION
# ============================================================================

def _make_epsilon_event():
    """Create a terminal event that fires when epsilon crosses 1.
    
    Accepts an extra `pot` positional arg because solve_ivp forwards
    args=(pot,) to event functions.
    """
    def event(N, y, pot):
        X, M_mem = y[0], y[-1]
        if X < 1e-100:
            return -1.0
        sr = compute_slow_roll(X, M_mem, pot)
        return 1.0 - sr['epsilon']
    event.terminal = True
    event.direction = -1
    return event


def run_inflation(pot, X_init=None, N_max=300, mode='slow_roll'):
    """Integrate the inflation system for a given potential.
    
    Uses scipy events to terminate exactly at epsilon=1.
    N_max=300 ensures the Plateau potential reaches end of inflation.
    
    Returns dict with trajectories and observables.
    """
    if X_init is None:
        N_buffer = 20
        if isinstance(pot, PlateauPotential):
            X_init = pot.mu * np.log(4.0 / 3.0 * (pot.N_target + N_buffer))
        elif isinstance(pot, AxionPotential):
            X_init = pot.X_star * 1.05
        elif isinstance(pot, LinearPotential):
            X_init = pot.X_star - 2.0 * M_P  # start slightly before horizon exit
        elif hasattr(pot, 'X_star'):
            X_init = pot.X_star * 1.1
        else:
            X_init = 6.0 * getattr(pot, 'f_X', getattr(pot, 'mu', 1.0))

    M_init = 0.0

    N_span = (0, N_max)
    N_eval = np.linspace(0, N_max, 10000)

    eps_event = _make_epsilon_event()

    if mode == 'slow_roll':
        y0 = [X_init, M_init]
        sol = solve_ivp(slow_roll_odes, N_span, y0, args=(pot,),
                        t_eval=N_eval, method='RK45',
                        rtol=1e-10, atol=1e-14, max_step=0.1,
                        events=eps_event)
    else:
        v_eff_init = V_eff(X_init, M_init, pot=pot, closure_mode=CLOSURE_MODE)
        H_init = np.sqrt(v_eff_init / (3.0 * M_P**2))
        X_dot_init = -pot.dV(X_init) / (3.0 * H_init)
        y0 = [X_init, X_dot_init, M_init]
        sol = solve_ivp(full_odes, N_span, y0, args=(pot,),
                        t_eval=N_eval, method='RK45',
                        rtol=1e-10, atol=1e-14, max_step=0.1,
                        events=eps_event)

    X_traj = sol.y[0]
    M_traj = sol.y[-1]
    N_traj = sol.t

    # Find end of inflation (epsilon = 1) from trajectory
    sr_list = []
    N_end_idx = len(N_traj) - 1
    for i in range(len(N_traj)):
        sr = compute_slow_roll(X_traj[i], M_traj[i], pot)
        sr_list.append(sr)
        if sr['epsilon'] > 1.0:
            N_end_idx = i
            break

    N_end = N_traj[N_end_idx]

    # Horizon exit at N* = N_end - N_target
    N_star = N_end - pot.N_target
    if N_star < 0:
        N_star = 0
    i_star = int(np.clip(np.searchsorted(N_traj, N_star), 0, N_end_idx))
    sr_star = compute_slow_roll(X_traj[i_star], M_traj[i_star], pot)

    return {
        'N': N_traj[:N_end_idx+1],
        'X': X_traj[:N_end_idx+1],
        'M': M_traj[:N_end_idx+1],
        'sr': sr_list,
        'N_end': N_end,
        'N_star': N_star,
        'sr_star': sr_star,
        'pot_name': pot.name,
        'i_star': i_star,
    }


def calibrate_potential(PotClass, A_s_target=2.1e-9, N_target=70.5,
                        max_iter=10, tol=0.01):
    """Iteratively recalibrate V_0 so A_s self-consistency holds.
    
    Runs inflation, measures actual epsilon at horizon exit, adjusts V_0,
    and repeats until A_s_computed matches A_s_target within tol (fractional).
    """
    pot = PotClass(N_target=N_target, A_s=A_s_target)
    for iteration in range(max_iter):
        res = run_inflation(pot, mode='slow_roll')
        X_star = res['X'][res['i_star']]
        M_star = res['M'][res['i_star']]
        sr = res['sr_star']
        eps_actual = sr['epsilon']

        v_at_star = V_eff(X_star, M_star, pot=pot, closure_mode=CLOSURE_MODE)
        A_s_computed = v_at_star / (24.0 * pi_val**2 * M_P**4 * eps_actual) if eps_actual > 0 else 1e-6

        ratio = A_s_computed / A_s_target
        if abs(ratio - 1.0) < tol:
            break

        # Scale V_0 down by ratio to bring A_s into line
        if hasattr(pot, 'V_0'):
            pot.V_0 /= ratio
        elif hasattr(pot, 'Lambda4'):
            pot.Lambda4 /= ratio

    return pot, res


# ============================================================================
# RUN BOTH POTENTIALS
# ============================================================================

def main():
    vx_ltotal = SourceFileLoader(
        "gu_vx_ltotal",
        str(
            Path(__file__).resolve().parent.parent
            / "43_VX_FROM_LTOTAL"
            / "01_vx_from_ltotal.py"
        ),
    ).load_module()
    vx_report = vx_ltotal.derive_vx_candidates()
    vx_report_path = (
        Path(__file__).resolve().parent.parent
        / "43_VX_FROM_LTOTAL"
        / "vx_from_ltotal_report.json"
    )
    vx_ltotal.write_report(vx_report, str(vx_report_path))

    print("\n### CALIBRATING POTENTIALS (iterative V_0 recalibration)")
    print("-" * 60)
    print(
        f"V_X from L_total candidates: {vx_report['candidate_count_admissible']}/"
        f"{vx_report['candidate_count_total']} admissible, uniqueness={vx_report['uniqueness_pass']}"
    )
    print(f"V_X report: {vx_report_path}")

    A_s_target = 2.1e-9

    pot_A, res_A = calibrate_potential(PlateauPotential, A_s_target=A_s_target)
    pot_B, res_B = calibrate_potential(AxionPotential, A_s_target=A_s_target)
    pot_C, res_C = calibrate_potential(LinearPotential, A_s_target=A_s_target)

    print(f"Plateau: V_0 = {pot_A.V_0:.4e} M_P^4, μ = {pot_A.mu:.6f} M_P")
    print(f"Axion:   Λ^4 = {pot_B.Lambda4:.4e} M_P^4, f_X = {pot_B.f_X:.4f} M_P")
    print(f"Linear:  V_0 = {pot_C.V_0:.4e} M_P^4, σ = {pot_C.sigma:.4e} M_P^3")

    results = {}

    print("\n### INFLATION RESULTS (after A_s recalibration)")
    print("-" * 60)

    for pot, res in [(pot_A, res_A), (pot_B, res_B), (pot_C, res_C)]:
        print(f"\n--- {pot.name} potential ---")
        results[pot.name] = res
        sr = res['sr_star']
        X_star = res['X'][res['i_star']]
        M_star = res['M'][res['i_star']]
        v_star = V_eff(X_star, M_star, pot=pot, closure_mode=CLOSURE_MODE)
        eps_actual = sr['epsilon']
        A_s_check = v_star / (24.0 * pi_val**2 * M_P**4 * eps_actual) if eps_actual > 0 else 0
        eternal_star = compute_eternal_inflation_metrics(X_star, M_star, pot)

        max_ratio = 0.0
        i_max_ratio = 0
        for i in range(len(res['N'])):
            metrics_i = compute_eternal_inflation_metrics(res['X'][i], res['M'][i], pot)
            if metrics_i['ratio_q_over_c'] > max_ratio:
                max_ratio = metrics_i['ratio_q_over_c']
                i_max_ratio = i
        has_eternal_region = max_ratio > 1.0

        print(f"Inflation ends at N_end = {res['N_end']:.2f} e-folds")
        print(f"Horizon exit at N* = {res['N_star']:.2f}")
        print(f"At horizon exit:")
        print(f"  ε = {eps_actual:.6e}")
        print(f"  η = {sr['eta']:.6e}")
        print(f"  n_s = {sr['n_s']:.6f}  (Planck 2018: 0.9649 ± 0.0042)")
        print(f"  r = {sr['r']:.6e}  (Planck+BICEP: r < 0.036)")
        print(f"  A_s (self-check) = {A_s_check:.4e}  (target: {A_s_target:.4e})")
        print(f"  Memory M at exit = {res['M'][res['i_star']]:.4e}")
        print(f"  Eternal check @N*: ΔX_q/ΔX_cl = {eternal_star['ratio_q_over_c']:.3e}, P_R = {eternal_star['P_R']:.3e}")
        print(f"  Max along trajectory: ΔX_q/ΔX_cl = {max_ratio:.3e} at N={res['N'][i_max_ratio]:.2f}")
        print(f"  Eternal inflation region present? {'YES' if has_eternal_region else 'NO'}")

    print("\n" + "=" * 80)
    print("THEORY BAND: PLATEAU vs AXION PREDICTIONS")
    print("=" * 80)

    print(f"\n{'Observable':<20} {'Plateau':>12} {'Axion':>12} {'Linear':>12} {'Planck 2018':>18}")
    print("-" * 80)

    obs_names = {
        'n_s': ('n_s', '0.9649±0.0042'),
        'r': ('r', '< 0.036'),
        'epsilon': ('ε', '—'),
        'eta': ('η', '—'),
    }

    for key, (label, planck) in obs_names.items():
        vals = []
        for name in ['Plateau', 'Axion', 'Linear']:
            vals.append(f"{results[name]['sr_star'][key]:.4e}" if name in results else "N/A")
        print(f"{label:<20} {vals[0]:>12} {vals[1]:>12} {vals[2]:>12} {planck:>18}")

    vx_report_path = (
        Path(__file__).resolve().parent.parent
        / "43_VX_FROM_LTOTAL"
        / "vx_from_ltotal_report.json"
    )
    if vx_report_path.exists():
        try:
            vx_report = json.loads(vx_report_path.read_text(encoding="utf-8"))
            print("\n" + "=" * 80)
            print("V_X FROM L_TOTAL CANDIDATE STATUS")
            print("=" * 80)
            print(
                f"admissible candidates: {vx_report.get('candidate_count_admissible')} / "
                f"{vx_report.get('candidate_count_total')}"
            )
            print(f"uniqueness pass: {vx_report.get('uniqueness_pass')}")
            print(f"certificate: {vx_report.get('non_uniqueness_certificate')}")
        except Exception:
            print(f"\n[warning] Could not parse {vx_report_path}")
    else:
        print(f"\n[info] V_X report not found at {vx_report_path}; run 43_VX_FROM_LTOTAL/01_vx_from_ltotal.py")

    print("\n" + "=" * 80)
    print("END OF COUPLED ODE SYSTEM")
    print("=" * 80)


if __name__ == "__main__":
    main()
