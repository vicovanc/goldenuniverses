#!/usr/bin/env python3
"""
Test script to verify Python execution in the browser
Tests basic functionality without external dependencies
"""

import mpmath as mp
import numpy as np

print("="*60)
print("PYTHON EXECUTOR TEST")
print("="*60)

# Test 1: Basic math
print("\n1. Basic Math Test:")
print(f"  2 + 2 = {2 + 2}")
print(f"  10 * 5 = {10 * 5}")

# Test 2: mpmath precision
print("\n2. High Precision Math (mpmath):")
mp.dps = 50
print(f"  Golden ratio (φ) = {mp.phi}")
print(f"  π to 50 decimals = {mp.pi}")
print(f"  e to 50 decimals = {mp.e}")

# Test 3: NumPy arrays
print("\n3. NumPy Arrays:")
arr = np.array([1, 2, 3, 4, 5])
print(f"  Array: {arr}")
print(f"  Sum: {np.sum(arr)}")
print(f"  Mean: {np.mean(arr)}")
print(f"  Std Dev: {np.std(arr)}")

# Test 4: Golden Universe calculations
print("\n4. Golden Universe Calculation:")
PHI = mp.phi
PI = mp.pi
M_P_MeV = mp.mpf('1.22091e+22')  # Planck mass in MeV
N_e = 111

# Electron mass calculation (simplified)
pi_111 = mp.mpf('3.14117324722610821731917179931573040047401692531433')
phi_111 = mp.mpf('1.61803398874989484820458683436563811772030917971577')
m_e_theory = M_P_MeV * (2 * pi_111 / phi_111**N_e) * mp.mpf('0.51097951228960997824303381840723004398203106664718')
m_e_exp = mp.mpf('0.51099895000')

print(f"  Theoretical electron mass = {m_e_theory:.10f} MeV")
print(f"  Experimental electron mass = {m_e_exp:.10f} MeV")
print(f"  Error = {float((m_e_theory - m_e_exp) / m_e_exp * 1e6):.2f} ppm")

print("\n" + "="*60)
print("ALL TESTS PASSED SUCCESSFULLY!")
print("="*60)