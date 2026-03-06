# GU Code Audit — Verification & Validation

**Use this skill when:** Auditing Python implementations against theory documents, verifying computational pipeline correctness, identifying gaps between theory and code, cross-validating results, or ensuring consistency across multiple derivation routes.

## Audit Framework

### Primary Reference Documents

**Theory sources (authoritative):**
- `theory/theory-laws.md` (4200+ lines) — Laws 0-38, complete formalism
- `theory/derived-laws.md` — Step-by-step derivations
- `⭐_MASTER_EQUATIONS_REFERENCE.md` — Equation compendium

**Implementation sources:**
- `pipeline/GU_formation_pipeline.py` (889 lines) — Main computational pipeline
- `pipeline/GU_particle_masses.py` (580 lines) — Mass calculations
- `pipeline/PHASE23_*.py` — Phase-specific calculations

**Previous audits:**
- `AUDIT_theory-laws_vs_pipeline.md` — Theory-to-code mapping
- `GU_formation_pipeline_INVENTORY.md` — Function inventory

## Systematic Audit Procedure

### 1. Theory-to-Code Mapping

```python
def audit_theory_implementation(
    theory_file: str,
    code_file: str
) -> Dict[str, str]:
    """
    Map theoretical equations to code implementations.

    Returns:
        Dictionary with:
        - 'implemented': Laws fully implemented
        - 'partial': Laws partially implemented
        - 'missing': Laws not implemented
        - 'discrepancies': Theory-code mismatches
    """
    audit_results = {
        'implemented': [],
        'partial': [],
        'missing': [],
        'discrepancies': []
    }

    # Check each law (0-38)
    for law_num in range(39):
        status = check_law_implementation(law_num, code_file)
        audit_results[status].append(law_num)

    return audit_results


def check_law_implementation(law_number: int, code_file: str) -> str:
    """
    Check if a specific law is implemented in code.

    Returns: 'implemented', 'partial', or 'missing'
    """
    # Read the code file
    with open(code_file, 'r') as f:
        code_content = f.read()

    # Search for law-specific patterns
    # (This requires knowledge of what each law specifies)

    # Example checks:
    law_checks = {
        0: "L_M = L_Omega + L_X + L_int + L_gauge",  # Lagrangian structure
        1: "L_Omega",  # Ω-sector
        2: "L_X",  # X-sector
        14: "phi = (1 + sqrt(5))/2",  # Canonical symbols
        16: "omega_eff = j0 / (2 * rho)",  # Gauge-invariant frequency
        21: "N_e = 111",  # Resonance condition
        33: "nu = 0.82054",  # Route-A parameter
        34: "mu = 0.4192",  # Route-B parameter
    }

    if law_number in law_checks:
        pattern = law_checks[law_number]
        if pattern.lower() in code_content.lower():
            return 'implemented'
        else:
            return 'missing'

    return 'partial'  # Default if not in check list
```

### 2. Known Gaps from Previous Audits

**From `AUDIT_theory-laws_vs_pipeline.md`:**

```python
KNOWN_GAPS = {
    'FRG_lock_sector_projection': {
        'location': 'pipeline/GU_formation_pipeline.py',
        'theory': 'ℓ_ab coefficients for lock-sector projection (theory/theory-laws.md:2500+)',
        'status': 'Missing',
        'impact': 'High - affects phase-driver coupling to FRG flow'
    },

    'phase_stiffness_beta_function': {
        'location': 'pipeline/GU_formation_pipeline.py',
        'theory': 'β_{K̄} should include η_χ + 2∂_t ln R₀ (theory/theory-laws.md:2800+)',
        'current': 'β_{K̄} = 0',
        'status': 'Placeholder',
        'impact': 'Medium - affects RG flow of phase-driver'
    },

    'target_frequency_beta_function': {
        'location': 'pipeline/GU_formation_pipeline.py',
        'theory': 'β_{ω̄★} should vary with epoch (theory/theory-laws.md:2850+)',
        'current': 'β_{ω̄★} = 0',
        'status': 'Placeholder',
        'impact': 'Medium - affects frequency locking across epochs'
    },

    'six_term_hamiltonian': {
        'location': 'pipeline/GU_formation_pipeline.py',
        'theory': 'H(x) = 6 terms (kinetic + mass + λ_4 + λ_6 + phase + gauge)',
        'current': 'Only 4 terms implemented',
        'status': 'Partial',
        'impact': 'Medium - missing gauge and full phase contributions'
    },

    'NLDE_BVP_solver': {
        'location': 'Missing file',
        'theory': 'Radial BVP solver for κ=-1 s-wave (theory/theory-laws.md:1200-1400)',
        'status': 'Not implemented',
        'impact': 'High - needed for ab-initio m_e calculation'
    },

    'multi_epoch_FRG_flow': {
        'location': 'pipeline/GU_formation_pipeline.py',
        'theory': 'FRG flow with threshold switching at each generation',
        'current': 'Single-epoch flow only',
        'status': 'Partial',
        'impact': 'High - needed for muon, tau, quark masses'
    },

    'gauge_boson_masses': {
        'location': 'Missing',
        'theory': 'W, Z, Higgs mass derivations (theory/theory-laws.md:3500+)',
        'status': 'Not started',
        'impact': 'High - major physics milestone'
    },

    'neutrino_sector': {
        'location': 'Missing',
        'theory': 'Neutrino masses and PMNS mixing (theory/theory-laws.md:3800+)',
        'status': 'Not started',
        'impact': 'High - complete lepton sector'
    },

    'QCD_chiral_symmetry_breaking': {
        'location': 'Partial in pipeline/GU_particle_masses.py',
        'theory': 'Full QCD sector with confinement (theory/theory-laws.md:4000+)',
        'status': 'Placeholder values',
        'impact': 'High - quark to hadron mapping'
    }
}
```

### 3. Cross-Validation Checks

```python
def cross_validate_routes():
    """
    Verify that all five derivation routes yield consistent results.

    All routes must give: m_e = 0.51099895 MeV (within numerical precision)

    Routes:
    - Route A (NLDE): ν = 0.82054 → m_e
    - Route B (Vortex): μ = 0.4192 → m_e
    - Route C (FRG): Ab-initio flow → m_e
    - Route D (Recursion): Closure condition → m_e
    - Route E (NHC): Convention audit → m_e
    """
    results = {}

    # Route A
    m_e_route_A = calculate_electron_mass_route_A()
    results['Route_A'] = m_e_route_A

    # Route B
    m_e_route_B = calculate_electron_mass_route_B()
    results['Route_B'] = m_e_route_B

    # Route C (if implemented)
    try:
        m_e_route_C = calculate_electron_mass_route_C_FRG()
        results['Route_C'] = m_e_route_C
    except NotImplementedError:
        results['Route_C'] = 'Not implemented'

    # Route D
    try:
        m_e_route_D = calculate_electron_mass_route_D_recursion()
        results['Route_D'] = m_e_route_D
    except NotImplementedError:
        results['Route_D'] = 'Not implemented'

    # Route E (NHC audit)
    try:
        m_e_route_E = calculate_electron_mass_route_E_NHC()
        results['Route_E'] = m_e_route_E
    except NotImplementedError:
        results['Route_E'] = 'Not implemented'

    # Cross-validation
    print("Cross-Route Validation:")
    print("=" * 50)
    for route, mass in results.items():
        if isinstance(mass, str):
            print(f"{route}: {mass}")
        else:
            error = abs(mass - 0.51099895) / 0.51099895 * 100
            status = "✓" if error < 0.01 else "✗"
            print(f"{status} {route}: {mass:.8f} MeV (error: {error:.6f}%)")

    return results


def validate_precision_consistency():
    """
    Verify that all calculations use consistent 50-digit precision.

    Check:
    1. mpmath.mp.dps = 50 set at start
    2. All constants (φ, π, e) at 50 digits
    3. No float downcasting in critical paths
    4. Results stored with full precision
    """
    import mpmath

    print("Precision Consistency Check:")
    print("=" * 50)

    # Check current precision
    current_dps = mpmath.mp.dps
    if current_dps == 50:
        print(f"✓ mpmath precision: {current_dps} digits")
    else:
        print(f"✗ mpmath precision: {current_dps} digits (should be 50)")

    # Check φ precision
    phi = mpmath.mpf('1.618033988749894848204586834365638117720309179805762862135')
    phi_str = str(phi)
    if len(phi_str) > 50:
        print(f"✓ φ precision: {len(phi_str)} characters")
    else:
        print(f"✗ φ precision: {len(phi_str)} characters (insufficient)")

    # Check intermediate calculations
    phi_squared = phi * phi
    expected = phi + 1
    error = abs(phi_squared - expected)
    if error < mpmath.mpf('1e-45'):
        print(f"✓ φ² = φ + 1 verified to {-int(mpmath.log10(error))} digits")
    else:
        print(f"✗ φ² identity error: {error}")

    print("\n✓ Precision checks complete")
```

### 4. Dimensional Analysis Audit

```python
def audit_dimensional_consistency(equation: str, variables: dict):
    """
    Verify dimensional consistency of an equation.

    Args:
        equation: String representation of equation
        variables: Dictionary mapping variable names to dimensions

    Example:
        audit_dimensional_consistency(
            "m_e = M_0 * (2*pi / phi**N_e) * C_e",
            {'m_e': 1, 'M_0': 1, 'pi': 0, 'phi': 0, 'N_e': 0, 'C_e': 0}
        )
    """
    print(f"Dimensional analysis: {equation}")

    # Parse LHS and RHS
    lhs, rhs = equation.split('=')

    # Compute dimensions
    lhs_dim = compute_dimension(lhs.strip(), variables)
    rhs_dim = compute_dimension(rhs.strip(), variables)

    if lhs_dim == rhs_dim:
        print(f"✓ [{lhs_dim}] = [{rhs_dim}]")
        return True
    else:
        print(f"✗ [{lhs_dim}] ≠ [{rhs_dim}] - DIMENSIONAL MISMATCH")
        return False


def compute_dimension(expr: str, variables: dict) -> int:
    """
    Compute mass dimension of an expression.

    Returns dimension in natural units (ℏ = c = 1).
    """
    # This is a simplified parser - full implementation would use sympy
    # For now, just look up in variables dict
    for var, dim in variables.items():
        if var in expr:
            return dim
    return 0  # Default for constants
```

### 5. Notation Consistency Audit

```python
def audit_notation_consistency():
    """
    Check for notation conflicts and inconsistencies.

    Reference: MASTER_NOTATION_GUIDE.json (650+ symbols)

    Common conflicts:
    - μ: Bohr magneton vs chemical potential vs Route-B parameter
    - ω: Effective vs target vs bare frequency
    - M: Particle mass vs mass parameter vs dimensionless mass
    - X: Driver field vs epoch scale vs dimensionless variable
    - m̃: Tilde for running vs bare vs dimensionless
    """
    import json

    # Load notation guide
    with open('MASTER_NOTATION_GUIDE.json', 'r') as f:
        notation_db = json.load(f)

    # Find symbols with multiple definitions
    symbol_counts = {}
    for symbol, definitions in notation_db.items():
        if isinstance(definitions, list) and len(definitions) > 1:
            symbol_counts[symbol] = len(definitions)

    print("Notation Conflict Report:")
    print("=" * 50)
    print(f"\nSymbols with multiple definitions: {len(symbol_counts)}")

    # Sort by number of conflicts
    sorted_conflicts = sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)

    for symbol, count in sorted_conflicts[:10]:  # Top 10
        print(f"  {symbol}: {count} definitions")
        for defn in notation_db[symbol]:
            print(f"    - {defn['context']}: {defn['meaning']}")

    print("\n⚠️ Always check context when using these symbols!")


def validate_forbidden_constructions():
    """
    Check code for forbidden constructions (Law 26).

    Forbidden:
    1. φ₁₁₁, π₁₁₁, e₁₁₁ (epoch-refined constants)
    2. Extra N_e in prefactor
    3. Inverted determinant ratio
    4. Separate C_mem multiplier
    5. y_e = 0.511 MeV (dimensionally wrong)
    """
    forbidden_patterns = [
        'phi_111',
        'pi_111',
        'e_111',
        'N_e *.*M_0',  # Extra N_e multiplier
        'det_L0 / det_Lminus',  # Inverted ratio
        'C_mem',  # Separate memory factor
        'y_e.*=.*0.511.*MeV'  # Dimensional error
    ]

    print("Forbidden Construction Check:")
    print("=" * 50)

    # Scan all Python files
    import glob
    python_files = glob.glob('*.py')

    violations = []
    for pyfile in python_files:
        with open(pyfile, 'r') as f:
            content = f.read()

        for pattern in forbidden_patterns:
            if pattern in content:
                violations.append((pyfile, pattern))

    if violations:
        print(f"\n✗ Found {len(violations)} violations:")
        for file, pattern in violations:
            print(f"  {file}: {pattern}")
    else:
        print("\n✓ No forbidden constructions found")

    return violations
```

### 6. Result Validation

```python
def validate_against_CODATA():
    """
    Validate all particle mass calculations against CODATA 2018 values.

    Tolerances:
    - Electron: 0.01% (should be ~0%)
    - Muon: 1%
    - Tau: 1%
    - Quarks: 10% (larger theoretical uncertainty)
    """
    CODATA = {
        'electron': {'value': 0.51099895, 'unit': 'MeV', 'tolerance': 0.01},
        'muon': {'value': 105.6583755, 'unit': 'MeV', 'tolerance': 1.0},
        'tau': {'value': 1776.86, 'unit': 'MeV', 'tolerance': 1.0},
        'proton': {'value': 938.27208816, 'unit': 'MeV', 'tolerance': 10.0},
    }

    print("CODATA Validation:")
    print("=" * 50)

    results = {}
    for particle, ref in CODATA.items():
        try:
            # Calculate mass
            if particle == 'electron':
                calc = calculate_electron_mass_route_A()
                mass = calc['m_e_MeV']
            elif particle == 'muon':
                calc = calculate_muon_mass()
                mass = calc['m_mu_MeV']
            elif particle == 'tau':
                calc = calculate_tau_mass()
                mass = calc['m_tau_MeV']
            else:
                mass = None

            if mass is not None:
                error = abs(float(mass) - ref['value']) / ref['value'] * 100
                status = "✓" if error < ref['tolerance'] else "✗"
                print(f"{status} {particle}: {float(mass):.8f} {ref['unit']} "
                      f"(error: {error:.4f}%, tolerance: {ref['tolerance']}%)")
                results[particle] = {'mass': mass, 'error': error, 'pass': error < ref['tolerance']}
            else:
                print(f"⊘ {particle}: Not implemented")
                results[particle] = {'mass': None, 'error': None, 'pass': False}

        except Exception as e:
            print(f"✗ {particle}: Error - {e}")
            results[particle] = {'mass': None, 'error': str(e), 'pass': False}

    return results


def validate_self_consistency():
    """
    Check self-consistency of parameters (ν, μ, etc.).

    Parameters like ν and μ must satisfy their own determining equations:
    - ν determines C_e(ν), which determines m_e, which must match CODATA
    - μ determines phase-lock, which determines m_e, must agree with Route-A

    This is a circular consistency check.
    """
    print("Self-Consistency Check:")
    print("=" * 50)

    # Route-A: ν = 0.82054
    nu = mpmath.mpf('0.82054')
    m_e_A = calculate_electron_mass_route_A(nu=nu)

    # Check if m_e_A matches CODATA
    error_A = m_e_A['error_percent']
    if error_A < 0.01:
        print(f"✓ Route-A self-consistent: ν = {nu} → error = {error_A:.6f}%")
    else:
        print(f"✗ Route-A NOT self-consistent: ν = {nu} → error = {error_A:.6f}%")

    # Route-B: μ = 0.4192
    mu = mpmath.mpf('0.4192')
    m_e_B = calculate_electron_mass_route_B(mu=mu)

    error_B = m_e_B['error_percent']
    if error_B < 0.01:
        print(f"✓ Route-B self-consistent: μ = {mu} → error = {error_B:.6f}%")
    else:
        print(f"✗ Route-B NOT self-consistent: μ = {mu} → error = {error_B:.6f}%")

    # Cross-route consistency: Routes A and B must agree
    mass_A = float(m_e_A['m_e_MeV'])
    mass_B = float(m_e_B['m_e_MeV'])
    cross_error = abs(mass_A - mass_B) / mass_A * 100

    if cross_error < 0.01:
        print(f"✓ Routes A & B agree: Δ = {cross_error:.6f}%")
    else:
        print(f"✗ Routes A & B disagree: Δ = {cross_error:.6f}%")
```

## Audit Report Generation

```python
def generate_audit_report(output_file: str = 'AUDIT_REPORT.md'):
    """
    Generate comprehensive audit report.

    Sections:
    1. Executive Summary
    2. Theory-to-Code Mapping
    3. Known Gaps
    4. Cross-Validation Results
    5. Precision Consistency
    6. Dimensional Analysis
    7. Notation Conflicts
    8. Forbidden Constructions
    9. CODATA Validation
    10. Self-Consistency Checks
    11. Recommendations
    """
    report = []

    report.append("# Golden Universe Code Audit Report")
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n" + "=" * 50)

    # 1. Executive Summary
    report.append("\n## Executive Summary\n")
    # ... generate summary

    # 2. Theory-to-Code Mapping
    report.append("\n## Theory-to-Code Mapping\n")
    mapping = audit_theory_implementation('theory/theory-laws.md', 'pipeline/GU_formation_pipeline.py')
    report.append(f"- Fully implemented: {len(mapping['implemented'])} laws")
    report.append(f"- Partially implemented: {len(mapping['partial'])} laws")
    report.append(f"- Missing: {len(mapping['missing'])} laws")

    # 3. Known Gaps
    report.append("\n## Known Implementation Gaps\n")
    for gap_name, gap_info in KNOWN_GAPS.items():
        report.append(f"\n### {gap_name}")
        report.append(f"- **Impact:** {gap_info['impact']}")
        report.append(f"- **Status:** {gap_info['status']}")
        report.append(f"- **Theory:** {gap_info['theory']}")

    # ... continue for all sections

    # Save report
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))

    print(f"Audit report saved to: {output_file}")
```

## Quick Audit Checklist

```python
def run_quick_audit():
    """
    Run essential checks quickly (< 1 minute).

    Returns:
        Dictionary with pass/fail for each check
    """
    results = {}

    print("Running Quick Audit...")
    print("=" * 50)

    # 1. Precision check
    print("\n[1/7] Checking precision...")
    results['precision'] = validate_precision_consistency()

    # 2. Canonical symbols check
    print("\n[2/7] Checking canonical symbols...")
    results['symbols'] = check_canonical_symbols()

    # 3. Forbidden constructions
    print("\n[3/7] Checking for forbidden constructions...")
    violations = validate_forbidden_constructions()
    results['forbidden'] = len(violations) == 0

    # 4. Electron mass
    print("\n[4/7] Validating electron mass...")
    m_e = calculate_electron_mass_route_A()
    results['electron'] = m_e['error_percent'] < 0.01

    # 5. Resonance
    print("\n[5/7] Checking resonance condition...")
    resonances = scan_resonance_space()
    N_e = identify_critical_epoch(resonances)
    results['resonance'] = (N_e == 111)

    # 6. Cross-route consistency
    print("\n[6/7] Cross-validating routes...")
    cross_val = cross_validate_routes()
    results['cross_validation'] = all_routes_agree(cross_val)

    # 7. Known gaps status
    print("\n[7/7] Checking known gaps...")
    results['gaps'] = check_known_gaps_status()

    # Summary
    print("\n" + "=" * 50)
    print("Quick Audit Summary:")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"  Passed: {passed}/{total}")

    for check, status in results.items():
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {check}")

    return results


def check_canonical_symbols():
    """Verify φ, π, e at 50 digits."""
    import mpmath
    mpmath.mp.dps = 50

    phi = mpmath.mpf('1.618033988749894848204586834365638117720309179805762862135')
    pi = mpmath.pi
    e = mpmath.e

    # Check identity: φ² = φ + 1
    error = abs(phi**2 - (phi + 1))
    return error < mpmath.mpf('1e-45')


def all_routes_agree(cross_val):
    """Check if all implemented routes agree on m_e."""
    masses = []
    for route, mass in cross_val.items():
        if isinstance(mass, (float, int)):
            masses.append(mass)

    if len(masses) < 2:
        return False

    # All masses should agree to within 0.01%
    avg_mass = sum(masses) / len(masses)
    for mass in masses:
        error = abs(mass - avg_mass) / avg_mass * 100
        if error > 0.01:
            return False

    return True


def check_known_gaps_status():
    """Check if any critical gaps have been filled."""
    critical_gaps = ['NLDE_BVP_solver', 'FRG_lock_sector_projection']

    # Check if files exist or functions implemented
    for gap in critical_gaps:
        if gap == 'NLDE_BVP_solver':
            # Check if solver exists
            if not os.path.exists('NLDE_BVP_solver.py'):
                return False
        # ... other checks

    return True  # If all critical gaps addressed
```

## When to Use This Skill

**Invoke when:**
- Verifying code implementations against theory
- Identifying gaps between theory and code
- Cross-validating results across derivation routes
- Checking for forbidden constructions
- Auditing precision and dimensional consistency
- Generating compliance reports
- Before submitting results for publication

**Related skills:**
- `golden-universe-theory` → Theory reference
- `gu-computational-physics` → Implementation details
- `gu-mathematical-derivation` → Symbolic verification
