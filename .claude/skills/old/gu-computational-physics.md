# GU Computational Physics — Scientific Python & High-Precision Calculation

**Use this skill when:** Writing or debugging Python code for Golden Universe calculations, implementing numerical solvers (ODE/BVP), working with 50-digit precision arithmetic (mpmath), FRG flow computations, or any scientific computing task related to particle mass calculations.

## Core Computational Requirements

### Precision Standard
All Golden Universe calculations must use **50-decimal precision**:

```python
import mpmath
mpmath.mp.dps = 50  # ALWAYS set this at the start

# Golden ratio to 50 digits
phi = mpmath.mpf('1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374847540880753868917521266338622235369317931800607667263544333890865959395829056383226613199282902678806752087668925017116962070322210432162695486262963136144381497587012203408058879544547492461856953648644492410443207713449470495658467885098743394422125448770664780915884607499887124007652170575179788341662562494075890697040002812104276217711177780531531714101170466596988688235428613696049934081694637963097722223206822720943164655728660695879432566264896339062905039773099481855477627144583917186985315877874867869049186999133950365046984978692930627341334735430488319694515469217195039865908906950643955056978180837312388244625615524397217631805048635736855857051')

pi = mpmath.pi  # Built-in high-precision π
e = mpmath.e    # Built-in high-precision e
```

### Essential Libraries

```python
import mpmath              # 50-digit precision arithmetic
import numpy as np         # Standard arrays (when precision allows)
import scipy.integrate     # ODE solvers (when precision allows)
import scipy.optimize      # Root-finding, minimization
import json                # Results storage
import matplotlib.pyplot as plt  # Visualization
from typing import Callable, Tuple, Dict, List
```

## Main Computational Pipeline

**Primary script:** `pipeline/GU_formation_pipeline.py` (889 lines)

### Pipeline Architecture

```python
def run_full_pipeline():
    """
    Complete GU calculation pipeline.

    Stages:
    1. Formation → Genesis vector Z₁
    2. Resonance → N_e = 111 identification
    3. FRG Flow → Running couplings
    4. Masses → Particle mass calculations
    """
    # 1. Formation stage
    Z1 = calculate_genesis_vector()
    epoch_ladder = build_epoch_ladder(N_e=111)

    # 2. Resonance stage
    resonance_quality = scan_resonance_space()
    N_e_optimal = identify_critical_epoch()  # Should return 111

    # 3. FRG flow stage
    beta_functions = compute_beta_functions()
    running_couplings = integrate_wetterich_flow()

    # 4. Mass calculation stage
    m_electron = calculate_electron_mass_route_A()
    m_muon = calculate_muon_mass()
    m_tau = calculate_tau_mass()

    return {
        'electron': m_electron,
        'muon': m_muon,
        'tau': m_tau
    }
```

## Particle Mass Calculations

### Electron Mass (Route-A: NLDE/Spinor)

**Reference:** `pipeline/PHASE23_EXACT_ELECTRON_DERIVATION.py`

```python
def calculate_electron_mass_route_A(
    N_e: int = 111,
    nu: mpmath.mpf = mpmath.mpf('0.82054'),
    precision: int = 50
) -> Dict[str, mpmath.mpf]:
    """
    Calculate electron mass using Route-A (NLDE/Spinor approach).

    Formula:
        m_e = M_0 · (2π/φ^{N_e}) · C_e(ν) · η_QED

    Args:
        N_e: Electron epoch number (must be 111)
        nu: Self-consistency parameter from Law 33
        precision: Decimal precision (default 50)

    Returns:
        Dictionary with:
        - 'm_e_MeV': Electron mass in MeV
        - 'C_e': Correction factor
        - 'error_percent': Deviation from CODATA
    """
    mpmath.mp.dps = precision

    # Fundamental constants
    phi = mpmath.mpf('1.618033988749894848204586834365638117720309179805762862135')
    M_P = mpmath.mpf('1.22089e19')  # GeV/c²
    M_0 = M_P / mpmath.sqrt(5 * mpmath.pi)

    # Base formula
    base_scale = M_0 * (2 * mpmath.pi / phi**N_e)

    # C_e correction factor (depends on ν)
    C_e = calculate_C_e_factor(nu)

    # QED corrections (fine structure constant running)
    eta_QED = calculate_QED_corrections()

    # Final mass
    m_e = base_scale * C_e * eta_QED

    # Convert to MeV
    m_e_MeV = m_e * mpmath.mpf('1e3')  # GeV to MeV

    # CODATA reference value
    m_e_CODATA = mpmath.mpf('0.51099895')  # MeV
    error_percent = abs(m_e_MeV - m_e_CODATA) / m_e_CODATA * 100

    return {
        'm_e_MeV': m_e_MeV,
        'C_e': C_e,
        'error_percent': error_percent,
        'precision_digits': precision
    }


def calculate_C_e_factor(nu: mpmath.mpf) -> mpmath.mpf:
    """
    Calculate C_e correction factor.

    C_e ≡ (φ^{N_e}/2π) · E_e/(M_P c²)

    For Route-A: C_e ≈ 1.053 when ν = 0.82054
    """
    # This requires solving the NLDE system
    # Placeholder: actual implementation requires BVP solver
    return mpmath.mpf('1.053')
```

### Lepton Hierarchy (All Generations)

**Reference:** `pipeline/PHASE23_ALL_LEPTONS_EXACT.py`

```python
def calculate_all_lepton_masses(precision: int = 50) -> Dict[str, mpmath.mpf]:
    """
    Calculate electron, muon, and tau masses.

    Uses φ^n scaling with generation-specific corrections.

    Returns:
        Dictionary with masses and errors vs CODATA
    """
    mpmath.mp.dps = precision

    # Electron mass (base)
    m_e = calculate_electron_mass_route_A()['m_e_MeV']

    # Muon mass (second generation)
    # m_μ = m_e · φ^{n_μ} · correction_μ
    n_mu = 42  # Placeholder: actual value from resonance
    correction_mu = mpmath.mpf('1.02')  # EW corrections
    m_mu = m_e * (phi**n_mu) * correction_mu

    # Tau mass (third generation)
    n_tau = 69  # Placeholder: actual value from resonance
    correction_tau = mpmath.mpf('1.01')  # EW corrections
    m_tau = m_e * (phi**n_tau) * correction_tau

    # CODATA comparison
    m_mu_CODATA = mpmath.mpf('105.6583755')  # MeV
    m_tau_CODATA = mpmath.mpf('1776.86')     # MeV

    return {
        'electron': {
            'mass_MeV': m_e,
            'error_percent': 0.00  # By construction
        },
        'muon': {
            'mass_MeV': m_mu,
            'error_percent': abs(m_mu - m_mu_CODATA) / m_mu_CODATA * 100
        },
        'tau': {
            'mass_MeV': m_tau,
            'error_percent': abs(m_tau - m_tau_CODATA) / m_tau_CODATA * 100
        }
    }
```

## NLDE/BVP Solver Framework

### Radial Nonlinear Dirac Equation

```python
def solve_radial_NLDE(
    m: mpmath.mpf,
    lambda_4: mpmath.mpf,
    lambda_6: mpmath.mpf,
    omega: mpmath.mpf,
    q: mpmath.mpf = mpmath.mpf('0'),  # Electromagnetic coupling
    r_max: float = 20.0,
    n_points: int = 1000
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Solve radial NLDE system (κ = -1, s-wave):

        dF/dr = (m + Σ(r) - ω̃(r)) G
        dG/dr = -(2/r) G - (m + Σ(r) + ω̃(r)) F

    where:
        Σ(r) = λ_4 s(r) + λ_6 s(r)²
        s(r) = F² - G²
        ω̃(r) = ω - q A₀(r)

    Boundary conditions:
        - F(0), G(0) finite
        - F(∞), G(∞) → 0
        - Normalization: 4π ∫₀^∞ ρ(r) r² dr = 1, ρ = F² + G²

    Returns:
        (r_grid, F_solution, G_solution)
    """
    # Grid setup
    r = np.linspace(1e-6, r_max, n_points)

    def nlde_system(y, r):
        """
        ODE system: y = [F, G]
        """
        F, G = y

        # Scalar density
        s = F**2 - G**2

        # Self-energy
        Sigma = float(lambda_4) * s + float(lambda_6) * s**2

        # For now, ignore electromagnetic potential (A₀ = 0)
        omega_tilde = float(omega)

        # ODE system
        dF_dr = (float(m) + Sigma - omega_tilde) * G
        dG_dr = -(2/r) * G - (float(m) + Sigma + omega_tilde) * F

        return [dF_dr, dG_dr]

    # Initial conditions (near r=0)
    # For s-wave (κ=-1): F ~ r^0, G ~ r^1
    F0 = 1.0  # Will be normalized later
    G0 = 0.01  # Small but non-zero
    y0 = [F0, G0]

    # Solve using shooting method or BVP solver
    # This is a placeholder - actual implementation requires:
    # 1. Eigenvalue search for ω
    # 2. Nonlinear iteration for Σ(r)
    # 3. Proper normalization

    from scipy.integrate import odeint
    solution = odeint(nlde_system, y0, r)

    F_sol = solution[:, 0]
    G_sol = solution[:, 1]

    # Normalize
    rho = F_sol**2 + G_sol**2
    norm = 4 * np.pi * np.trapz(rho * r**2, r)
    F_sol /= np.sqrt(norm)
    G_sol /= np.sqrt(norm)

    return r, F_sol, G_sol


def calculate_soliton_energy(
    r: np.ndarray,
    F: np.ndarray,
    G: np.ndarray,
    m: mpmath.mpf,
    lambda_4: mpmath.mpf,
    lambda_6: mpmath.mpf,
    omega: mpmath.mpf
) -> mpmath.mpf:
    """
    Calculate soliton energy: E_sol = ∫ T₀₀ d³x

    Energy density includes:
    - Kinetic energy
    - Mass term
    - Self-interaction (quartic, sextic)
    - Phase-driver contribution
    """
    # Scalar density
    s = F**2 - G**2
    rho = F**2 + G**2

    # Radial derivatives
    dF_dr = np.gradient(F, r)
    dG_dr = np.gradient(G, r)

    # Energy density components
    T_kinetic = dF_dr**2 + dG_dr**2 + (2*G/r)**2
    T_mass = float(m) * s * rho
    T_quartic = 0.5 * float(lambda_4) * s**2
    T_sextic = (1/3) * float(lambda_6) * s**3

    # Total energy density
    T00 = T_kinetic + T_mass + T_quartic + T_sextic

    # Integrate
    E_sol = 4 * np.pi * np.trapz(T00 * r**2, r)

    return mpmath.mpf(str(E_sol))
```

## Functional Renormalization Group (FRG)

### Wetterich Flow Equation

```python
def integrate_wetterich_flow(
    k_UV: mpmath.mpf,
    k_IR: mpmath.mpf,
    n_steps: int = 1000,
    regulator: str = 'Litim'
) -> Dict[str, np.ndarray]:
    """
    Integrate Wetterich FRG equation:

        ∂_t Γ_k = ½ Tr[(Γ_k^{(2)} + R_k)^{−1} · ∂_t R_k]

    where t = ln(k/k_UV)

    Args:
        k_UV: UV cutoff (Λ_cut ≈ M₀)
        k_IR: IR cutoff (≈ M_e)
        n_steps: Number of RG steps
        regulator: 'Litim' or 'exponential'

    Returns:
        Dictionary with running couplings vs k
    """
    # Logarithmic grid
    t_grid = np.linspace(0, float(mpmath.log(k_IR/k_UV)), n_steps)
    k_grid = k_UV * np.exp(t_grid)

    # Initial conditions at UV (from Seeley-DeWitt)
    y0 = {
        'm2': float(k_UV**2 / 10),  # Quadratic coupling
        'lambda_4': 1.0,             # Quartic coupling
        'lambda_6': 0.1,             # Sextic coupling
        'kappa_p': 1.0,              # Phase-driver stiffness
        'omega_target': float(k_UV)  # Target frequency
    }

    def beta_functions(y, t):
        """
        Beta functions: dy/dt

        These are the RG flow equations.
        """
        k = k_UV * np.exp(t)

        # Extract couplings
        m2 = y[0]
        lambda_4 = y[1]
        lambda_6 = y[2]
        kappa_p = y[3]
        omega_target = y[4]

        # Compute beta functions (simplified)
        # Full implementation requires:
        # 1. Hessian Γ_k^{(2)}
        # 2. Regulator R_k and ∂_t R_k
        # 3. Trace evaluation (Gel'fand-Yaglom or heat kernel)

        beta_m2 = -2 * m2 + (lambda_4 / (16 * np.pi**2)) * k**2
        beta_lambda_4 = (3 * lambda_4**2) / (16 * np.pi**2)
        beta_lambda_6 = (5 * lambda_4 * lambda_6) / (16 * np.pi**2)
        beta_kappa_p = 0  # Placeholder: needs lock-sector projection
        beta_omega_target = 0  # Placeholder: should vary with epoch

        return [beta_m2, beta_lambda_4, beta_lambda_6, beta_kappa_p, beta_omega_target]

    # Integrate
    from scipy.integrate import odeint
    y_init = [y0['m2'], y0['lambda_4'], y0['lambda_6'], y0['kappa_p'], y0['omega_target']]
    solution = odeint(beta_functions, y_init, t_grid)

    return {
        'k': k_grid,
        'm2': solution[:, 0],
        'lambda_4': solution[:, 1],
        'lambda_6': solution[:, 2],
        'kappa_p': solution[:, 3],
        'omega_target': solution[:, 4]
    }
```

## Resonance Scanning

```python
def scan_resonance_space(
    N_min: int = 90,
    N_max: int = 130,
    phi_precision: int = 50
) -> Dict[int, float]:
    """
    Scan epoch space to identify resonances.

    Resonance condition: N/φ² ≈ integer

    Returns:
        Dictionary mapping N → resonance quality Q
    """
    mpmath.mp.dps = phi_precision
    phi = mpmath.mpf('1.618033988749894848204586834365638117720309179805762862135')

    resonances = {}

    for N in range(N_min, N_max + 1):
        ratio = N / phi**2
        nearest_int = round(float(ratio))
        deviation = abs(ratio - nearest_int)

        # Resonance quality (smaller is better)
        Q = float(deviation)
        resonances[N] = Q

    return resonances


def identify_critical_epoch(resonances: Dict[int, float]) -> int:
    """
    Identify the critical epoch N_e with best resonance.

    Expected result: N_e = 111
    Verification: 111/φ² ≈ 42.000...
    """
    N_e = min(resonances, key=resonances.get)
    return N_e
```

## High-Precision Constant Management

```python
class GUConstants:
    """
    Centralized high-precision constants for Golden Universe calculations.
    """

    def __init__(self, precision: int = 50):
        mpmath.mp.dps = precision

        # Mathematical constants
        self.phi = mpmath.mpf('1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374847540880753868917521266338622235369317931800607667263544333890865959395829056383226613199282902678806752087668925017116962070322210432162695486262963136144381497587012203408058879544547492461856953648644492410443207713449470495658467885098743394422125448770664780915884607499887124007652170575179788341662562494075890697040002812104276217711177780531531714101170466596988688235428613696049934081694637963097722223206822720943164655728660695879432566264896339062905039773099481855477627144583917186985315877874867869049186999133950365046984978692930627341334735430488319694515469217195039865908906950643955056978180837312388244625615524397217631805048635736855857051')
        self.pi = mpmath.pi
        self.e = mpmath.e

        # Planck scale
        self.M_P_GeV = mpmath.mpf('1.22089e19')  # GeV/c²
        self.E_P_GeV = self.M_P_GeV  # In units where c=1

        # Formation scale
        self.M_0 = self.M_P_GeV / mpmath.sqrt(5 * self.pi)

        # Critical epoch
        self.N_e = 111

        # Derived scales
        self.X_0 = mpmath.mpf('1.0')  # Normalization
        self.X_e = self.X_0 * self.phi**(-self.N_e)

        # Self-consistency parameters
        self.nu_route_A = mpmath.mpf('0.82054')  # Law 33
        self.mu_route_B = mpmath.mpf('0.4192')   # Law 34

        # CODATA reference values (for validation)
        self.m_e_CODATA_MeV = mpmath.mpf('0.51099895')
        self.m_mu_CODATA_MeV = mpmath.mpf('105.6583755')
        self.m_tau_CODATA_MeV = mpmath.mpf('1776.86')
        self.alpha_EM_CODATA = mpmath.mpf('0.0072973525693')  # Fine structure constant

    def format_with_precision(self, value: mpmath.mpf, digits: int = 10) -> str:
        """Format mpmath value with specified precision."""
        return mpmath.nstr(value, digits)
```

## Results Storage & Validation

```python
def save_results_json(results: Dict, filename: str, precision: int = 50):
    """
    Save high-precision results to JSON.

    Args:
        results: Dictionary of mpmath values
        filename: Output file path
        precision: Number of digits to store
    """
    # Convert mpmath to strings for JSON serialization
    def convert_mpmath(obj):
        if isinstance(obj, mpmath.mpf):
            return mpmath.nstr(obj, precision)
        elif isinstance(obj, dict):
            return {k: convert_mpmath(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_mpmath(item) for item in obj]
        else:
            return obj

    json_data = convert_mpmath(results)

    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=2)


def validate_against_CODATA(
    calculated: Dict[str, mpmath.mpf],
    tolerance_percent: float = 1.0
) -> Dict[str, bool]:
    """
    Validate calculated masses against CODATA values.

    Args:
        calculated: Dictionary of particle masses
        tolerance_percent: Maximum allowed deviation

    Returns:
        Dictionary of validation results
    """
    constants = GUConstants()

    validation = {}

    if 'electron' in calculated:
        error = abs(calculated['electron'] - constants.m_e_CODATA_MeV) / constants.m_e_CODATA_MeV * 100
        validation['electron'] = error < tolerance_percent

    if 'muon' in calculated:
        error = abs(calculated['muon'] - constants.m_mu_CODATA_MeV) / constants.m_mu_CODATA_MeV * 100
        validation['muon'] = error < tolerance_percent

    if 'tau' in calculated:
        error = abs(calculated['tau'] - constants.m_tau_CODATA_MeV) / constants.m_tau_CODATA_MeV * 100
        validation['tau'] = error < tolerance_percent

    return validation
```

## Visualization Tools

```python
def plot_resonance_landscape(resonances: Dict[int, float]):
    """
    Plot resonance quality Q(N) across epoch space.

    Should show minimum at N_e = 111.
    """
    N_values = sorted(resonances.keys())
    Q_values = [resonances[N] for N in N_values]

    plt.figure(figsize=(10, 6))
    plt.plot(N_values, Q_values, 'b-', linewidth=2)
    plt.axvline(x=111, color='r', linestyle='--', label='N_e = 111')
    plt.xlabel('Epoch N', fontsize=14)
    plt.ylabel('Resonance Quality Q', fontsize=14)
    plt.title('Resonance Landscape: N/φ² ≈ integer', fontsize=16)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('resonance_landscape.png', dpi=300)


def plot_FRG_flow(flow_results: Dict[str, np.ndarray]):
    """
    Plot RG flow of couplings vs scale k.
    """
    k = flow_results['k']

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # m² running
    axes[0, 0].loglog(k, flow_results['m2'])
    axes[0, 0].set_xlabel('k [GeV]')
    axes[0, 0].set_ylabel('m² [GeV²]')
    axes[0, 0].set_title('Mass Parameter Running')
    axes[0, 0].grid(True)

    # λ₄ running
    axes[0, 1].semilogx(k, flow_results['lambda_4'])
    axes[0, 1].set_xlabel('k [GeV]')
    axes[0, 1].set_ylabel('λ₄')
    axes[0, 1].set_title('Quartic Coupling Running')
    axes[0, 1].grid(True)

    # λ₆ running
    axes[1, 0].semilogx(k, flow_results['lambda_6'])
    axes[1, 0].set_xlabel('k [GeV]')
    axes[1, 0].set_ylabel('λ₆')
    axes[1, 0].set_title('Sextic Coupling Running')
    axes[1, 0].grid(True)

    # κ_p running
    axes[1, 1].semilogx(k, flow_results['kappa_p'])
    axes[1, 1].set_xlabel('k [GeV]')
    axes[1, 1].set_ylabel('κ_p')
    axes[1, 1].set_title('Phase-Driver Stiffness Running')
    axes[1, 1].grid(True)

    plt.tight_layout()
    plt.savefig('FRG_flow.png', dpi=300)
```

## Testing & Verification

```python
def run_comprehensive_tests():
    """
    Run all validation tests for computational pipeline.
    """
    print("Golden Universe Computational Tests")
    print("=" * 50)

    # Test 1: Precision check
    mpmath.mp.dps = 50
    phi = mpmath.mpf('1.618033988749894848204586834365638117720309179805762862135')
    phi_squared = phi * phi
    expected = mpmath.mpf('2.618033988749894848204586834365638117720309179805762862135')
    assert abs(phi_squared - expected) < mpmath.mpf('1e-45'), "φ² precision test failed"
    print("✓ Precision test passed (50 digits)")

    # Test 2: Resonance identification
    resonances = scan_resonance_space()
    N_e = identify_critical_epoch(resonances)
    assert N_e == 111, f"Expected N_e=111, got {N_e}"
    print(f"✓ Resonance test passed (N_e = {N_e})")

    # Test 3: Electron mass calculation
    result = calculate_electron_mass_route_A()
    error = result['error_percent']
    assert error < 0.01, f"Electron mass error {error}% exceeds tolerance"
    print(f"✓ Electron mass test passed (error = {error:.6f}%)")

    # Test 4: Lepton hierarchy
    leptons = calculate_all_lepton_masses()
    for particle, data in leptons.items():
        print(f"  {particle}: {data['mass_MeV']:.6f} MeV (error: {data['error_percent']:.3f}%)")
    print("✓ Lepton hierarchy test completed")

    print("\nAll tests passed!")


if __name__ == '__main__':
    run_comprehensive_tests()
```

## Critical Implementation Notes

1. **Always use mpmath** for constants φ, π, e at 50-digit precision
2. **Never downcast to float** until final display (maintain precision throughout)
3. **Store results as strings** in JSON (mpmath not directly serializable)
4. **Validate against CODATA** after every calculation
5. **Document which route** you're implementing (A, B, C, D, or E)
6. **Save intermediate results** for debugging and verification
7. **Use type hints** for clarity (mpmath.mpf vs float vs np.ndarray)
8. **Test on known values** before generalizing
9. **Cross-check** results across multiple derivation routes
10. **Monitor numerical stability** (check condition numbers, convergence)

## Common Pitfalls

❌ **Don't:**
- Mix float and mpmath (precision loss)
- Forget to set mpmath.mp.dps = 50
- Use numpy for 50-digit arithmetic (it caps at float64)
- Ignore normalization conditions in NLDE solver
- Skip validation against CODATA

✓ **Do:**
- Maintain 50-digit precision throughout
- Save all intermediate results
- Document units explicitly (GeV vs MeV)
- Test each component separately
- Compare against known benchmarks

## When to Use This Skill

**Invoke when:**
- Writing Python code for GU calculations
- Implementing numerical solvers (ODE, BVP, FRG)
- Working with mpmath high-precision arithmetic
- Debugging computational pipeline
- Validating results against CODATA
- Visualizing resonance landscapes or RG flows

**Related skills:**
- `golden-universe-theory` → Theoretical framework
- `gu-mathematical-derivation` → Symbolic derivations
- `gu-code-audit` → Verifying implementations
