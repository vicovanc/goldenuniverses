#!/usr/bin/env python3
"""
CRITICAL INVESTIGATION: What are the missing "..." terms?
Document line 4057 has ellipsis - what's being left out?
Document line 4883 shows C_e = 1.0500... but I calculated 1.0479
Difference = 0.0021 ≈ 0.2% - EXACTLY the remaining error!
"""

from mpmath import mp, mpf, sqrt, exp, sin, cos, pi as mp_pi, e as mp_e
from mpmath import ellipk, ellipe, gamma as mp_gamma

mp.dps = 50

print("="*90)
print("INVESTIGATION: WHAT'S MISSING IN C_e FORMULA?")
print("="*90)

# ============================================================================
# KNOWN VALUES
# ============================================================================

phi = (1 + sqrt(5)) / 2
N_e = 111
pi_111 = N_e * sin(mp_pi / N_e)
phi_111 = phi

delta_e = N_e / (phi**2) - 42
l_Omega = mpf('374.50')
lambda_rec_over_beta = exp(phi) / (mp_pi ** 2)

# From document line 4883
C_e_CODATA_exact = mpf('1.05000578983624877150669308103856260378515168153948')

print(f"\n### TARGET FROM CODATA (Line 4883):")
print(f"C_e (CODATA) = {C_e_CODATA_exact}")

# ============================================================================
# DOCUMENT'S ν VALUE (Line 4777)
# ============================================================================

nu_doc = mpf('0.91168369826717185782055908941114031156937694954229')
K_nu_doc = ellipk(nu_doc)
E_nu_doc = ellipe(nu_doc)

print(f"\n### DOCUMENT'S ν VALUE (Line 4777):")
print(f"ν_★ = {nu_doc}")
print(f"K(ν_★) = {K_nu_doc}")
print(f"Document says: K(ν_★) = 2.63603836122485977...")
print(f"Match: {'✅' if abs(K_nu_doc - mpf('2.63603836122485977')) < 1e-10 else '❌'}")

# ============================================================================
# MY PHASE 23 CALCULATION (3 TERMS)
# ============================================================================

print(f"\n### MY PHASE 23 CALCULATION (3 TERMS):")
print("-"*90)

# My ν value
nu_my = mpf('0.91174133696844241547505598521378678857606336851817')
K_nu_my = ellipk(nu_my)

term1_my = abs(delta_e) * K_nu_my
eta_mu_my = (2 * K_nu_my / l_Omega) ** 2
term2_my = eta_mu_my * (nu_my / 2)
kappa_my = 2 * sqrt(nu_my) * K_nu_my / l_Omega
term3_my = lambda_rec_over_beta * kappa_my / 3

C_e_my = term1_my + term2_my - term3_my

print(f"ν (my value) = {nu_my}")
print(f"Term 1 (detuning): {term1_my}")
print(f"Term 2 (elliptic): {term2_my}")
print(f"Term 3 (memory):   {term3_my}")
print(f"C_e (3-term) = {C_e_my}")

# ============================================================================
# DOCUMENT'S CALCULATION WITH THEIR ν
# ============================================================================

print(f"\n### DOCUMENT'S CALCULATION (Line 4795-4797):")
print("-"*90)

term1_doc = abs(delta_e) * K_nu_doc
eta_mu_doc = (2 * K_nu_doc / l_Omega) ** 2  
term2_doc = eta_mu_doc * (nu_doc / 2)

C_e_nonmem_doc = term1_doc + term2_doc

print(f"Term 1 (detuning): {term1_doc}")
print(f"Term 2 (elliptic): {term2_doc}")
print(f"C_e (non-memory) = {C_e_nonmem_doc}")
print(f"Document says: C_e (non-mem) = 1.05009617392456884...")
print(f"Match: {'✅' if abs(C_e_nonmem_doc - mpf('1.05009617392456884')) < 1e-10 else '❌'}")

# Memory term from document (line 4805-4806)
lambda_rec_beta_req = mpf('0.02016750845891262524634518845582062000394879710713')
kappa_doc = 2 * sqrt(nu_doc) * K_nu_doc / l_Omega
term3_doc = lambda_rec_beta_req * kappa_doc / 3

print(f"\nTerm 3 (memory with doc's λ_rec/β):")
print(f"λ_rec/β (required) = {lambda_rec_beta_req}")
print(f"λ_rec/β (I used)   = {lambda_rec_over_beta}")
print(f"Ratio: {float(lambda_rec_beta_req / lambda_rec_over_beta)}")

print(f"\nTerm 3 = {term3_doc}")
print(f"Document says: Λ_mem = 0.00027115226496...")

C_e_doc_3term = C_e_nonmem_doc - term3_doc
print(f"\nC_e (3-term with doc ν) = {C_e_doc_3term}")

# ============================================================================
# THE MYSTERY: WHAT'S IN THE "..."?
# ============================================================================

print(f"\n### THE MISSING TERMS IN '...'")
print("-"*90)

print(f"\nDocument formula (line 4055-4057):")
print("""
C_e(ν,k) = |δk|·K(ν) 
         + [(2πk/L)²·(K(ν)/π)² + E(ν)/K(ν) - (1-ν)]·(8m + ν/2)
         - (λ_rec/β)·κ·(1/√π)·[Γ(a+1/2)/Γ(a)]²·Γ(2a)/Γ(2a+1/2)
         + ...  ← WHAT'S HERE?
""")

print(f"\nLine 4059 says ellipsis contains:")
print("  1. Gauge self-energy term")
print("  2. Higher-order local corrections")

# ============================================================================
# ANALYZE THE SECOND TERM DIFFERENCES
# ============================================================================

print(f"\n### ANALYZING SECOND TERM")
print("-"*90)

print(f"\nDocument's second term has MORE than just η_μ·(ν/2):")
print(f"Full: [(2πk/L)²·(K/π)² + E(ν)/K(ν) - (1-ν)]·(8m + ν/2)")
print(f"My simplified: η_μ·(ν/2)")

print(f"\nLet me calculate the FULL second term:")

# Full second term calculation
K_nu = K_nu_doc
E_nu = E_nu_doc
k = 1
m = 0  # Ground sector

# First part of bracket
part1 = (2 * mp_pi * k / l_Omega)**2 * (K_nu / mp_pi)**2
part2 = E_nu / K_nu
part3 = -(1 - nu_doc)

bracket_full = part1 + part2 + part3

# Second part
second_part = 8*m + nu_doc/2

term2_full = bracket_full * second_part

print(f"\nBracket parts:")
print(f"  (2πk/L)²·(K/π)² = {part1}")
print(f"  E(ν)/K(ν)       = {part2}")
print(f"  -(1-ν)          = {part3}")
print(f"  Bracket total   = {bracket_full}")

print(f"\n(8m + ν/2) = {second_part}")
print(f"\nFull Term 2 = {term2_full}")
print(f"My Term 2   = {term2_doc}")
print(f"Difference  = {term2_full - term2_doc}")

# ============================================================================
# RECALCULATE WITH FULL FORMULA
# ============================================================================

print(f"\n### RECALCULATE C_e WITH FULL SECOND TERM")
print("-"*90)

C_e_with_full_term2 = term1_doc + term2_full - term3_doc

print(f"C_e (with full term 2) = {C_e_with_full_term2}")
print(f"C_e (CODATA target)    = {C_e_CODATA_exact}")
print(f"Difference             = {C_e_with_full_term2 - C_e_CODATA_exact}")
print(f"Still missing          = {float((C_e_CODATA_exact - C_e_with_full_term2) * 100)} %")

# ============================================================================
# CONCLUSIONS
# ============================================================================

print(f"\n{'='*90}")
print("CONCLUSIONS")
print("="*90)

print(f"\n1. ❌ I used SIMPLIFIED term 2: just η_μ·(ν/2)")
print(f"   Should use FULL: [(2πk/L)²·(K/π)² + E(ν)/K(ν) - (1-ν)]·(8m + ν/2)")

print(f"\n2. ❌ Document shows λ_rec/β = {float(lambda_rec_beta_req)}")
print(f"   I used: λ_rec/β = e^φ/π² = {float(lambda_rec_over_beta)}")
print(f"   These are DIFFERENT by factor {float(lambda_rec_over_beta / lambda_rec_beta_req):.3f}!")

print(f"\n3. ⚠️ The '...' contains:")
print(f"   - Gauge self-energy term E_gauge")
print(f"   - Higher-order corrections")
print(f"   - These likely account for the remaining ~0.2%")

print(f"\n4. 🎯 Document achieves EXACT match (0.00%) by:")
print(f"   - Using correct ν = 0.91168...")
print(f"   - Using full second term formula")
print(f"   - Solving for required λ_rec/β")
print(f"   - Including gauge term (not shown)")

print(f"\n✅ NEXT: Implement COMPLETE formula with all terms!")
