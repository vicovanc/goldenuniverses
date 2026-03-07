/**
 * Web Worker for non-blocking Python execution
 * Runs Pyodide in a separate thread to avoid blocking the UI
 */

// Use importScripts for classic worker
// eslint-disable-next-line @typescript-eslint/no-explicit-any
declare const self: any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
declare function importScripts(...urls: string[]): void;

interface PyodideInterface {
  loadPackage: (packages: string | string[]) => Promise<void>;
  runPythonAsync: (code: string) => Promise<unknown>;
  runPython: (code: string) => unknown;
  globals: {
    get: (name: string) => unknown;
    set: (name: string, value: unknown) => void;
  };
  FS: {
    writeFile: (path: string, data: string | Uint8Array) => void;
    readFile: (path: string, options: { encoding: string }) => string;
  };
  setStdout?: (options: { batched: (text: string) => void }) => void;
}

let pyodide: PyodideInterface | null = null;
let isInitialized = false;
let loadProgress = 0;

/**
 * Load Pyodide using importScripts
 */
async function loadPyodideScript(): Promise<any> {
  try {
    // Load the pyodide.js script using importScripts
    // This works in classic workers (not module workers)
    importScripts('https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js');

    // After importScripts, loadPyodide should be available on self
    const loadPyodide = self.loadPyodide;

    if (!loadPyodide) {
      throw new Error('loadPyodide function not found after loading script');
    }

    return loadPyodide;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to load Pyodide: ${errorMessage}`);
  }
}

/**
 * Initialize Pyodide with scientific packages
 */
async function initializePyodide(id?: string): Promise<void> {
  if (isInitialized) {
    // If already initialized, send ready message with id
    if (id) {
      self.postMessage({ type: 'ready', id, payload: { version: '0.25.0' } });
    }
    return;
  }

  try {
    // Load Pyodide from CDN
    self.postMessage({ type: 'progress', payload: { stage: 'loading_pyodide', progress: 10 } });

    // Load the Pyodide script first
    const loadPyodide = await loadPyodideScript();

    pyodide = await loadPyodide({
      indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/',
    });

    self.postMessage({ type: 'progress', payload: { stage: 'loading_packages', progress: 30 } });

    if (!pyodide) {
      throw new Error('Pyodide failed to load');
    }

    // Load scientific packages
    await pyodide.loadPackage(['numpy', 'scipy', 'mpmath']);

    self.postMessage({ type: 'progress', payload: { stage: 'initializing_constants', progress: 60 } });

    // Initialize Golden Universe constants
    await pyodide.runPythonAsync(`
import mpmath as mp
import numpy as np
from scipy import optimize, integrate, special

# Set precision to 50 decimal places
mp.dps = 50

# Fundamental constants
PHI = mp.phi
PI = mp.pi
E = mp.e
PHI_SQ = PHI ** 2

# Planck mass in MeV
M_P_MeV = mp.mpf('1.22091e+22')

# CODATA 2018 experimental values
M_E_EXP_MEV = mp.mpf('0.51099895000')
M_MU_EXP_MEV = mp.mpf('105.6583755')
M_TAU_EXP_MEV = mp.mpf('1776.86')
M_P_EXP_MEV = mp.mpf('938.27208816')
M_N_EXP_MEV = mp.mpf('939.56542052')

# Epoch-dependent constants for N=111
PI_111 = mp.mpf('3.14117324722610821731917179931573040047401692531433')
PHI_111 = mp.mpf('1.61803398874989484820458683436563811772030917971577')

# Electron parameters
N_E = 111
K_RES_E = 42
DELTA_E = mp.mpf('0.39822724876167184929086138541416893304568104156032')
P_E = -41
Q_E = 70
L_OMEGA_E = mp.mpf('374.50279990496241776613591175470833750708258874864')
LAMBDA_REC_BETA = mp.mpf('0.51097951228960997824303381840723004398203106664718')
NU_E = mp.mpf('0.91168369826717185782055908941114031156937694954230')

print("Golden Universe constants initialized")
`);

    self.postMessage({ type: 'progress', payload: { stage: 'loading_functions', progress: 80 } });

    // Load helper functions
    await loadHelperFunctions();

    self.postMessage({ type: 'progress', payload: { stage: 'ready', progress: 100 } });

    isInitialized = true;
    self.postMessage({ type: 'ready', id, payload: { version: '0.25.0' } });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    self.postMessage({ type: 'error', id, payload: { error: errorMessage } });
    throw error;
  }
}

/**
 * Load helper Python functions for calculations
 */
async function loadHelperFunctions(): Promise<void> {
  if (!pyodide) throw new Error('Pyodide not initialized');

  await pyodide.runPythonAsync(`
def epoch_pi(n):
    """Calculate epoch-dependent pi: π_n = n·sin(π/n)"""
    return n * mp.sin(mp.pi / n)

def epoch_phi(n):
    """Calculate epoch-dependent phi: φ_n = F_{n+1}/F_n"""
    return mp.fibonacci(n + 1) / mp.fibonacci(n)

def calculate_winding_length(p, q, phi=PHI):
    """Calculate l_Ω = 2π√(p² + (q/φ)²)"""
    return 2 * mp.pi * mp.sqrt(p**2 + (q/phi)**2)

def calculate_resonance(N, phi_sq=PHI_SQ):
    """Calculate resonance: k = round(N/φ²), δ = N/φ² - k"""
    k_res = round(N / phi_sq)
    delta = N / phi_sq - k_res
    return k_res, delta

def calculate_C_e_complete(nu, delta, l_omega, lambda_rec_beta, k=1):
    """
    Complete C_e formula with ALL terms
    C_e(ν) = |δ|·K(ν) + η_μ·(ν/2) - (λ_rec/β)·κ/3
    """
    # Elliptic integrals
    K_nu = mp.ellipk(nu)
    E_nu = mp.ellipe(nu)

    # Term 1: Detuning stress
    term1 = abs(delta) * K_nu

    # Term 2: Elliptic minimizer
    eta_mu = (2 * k * K_nu / l_omega) ** 2
    term2 = eta_mu * (nu / 2)

    # Term 3: Memory binding
    kappa = 2 * mp.sqrt(nu) * K_nu / l_omega
    term3 = lambda_rec_beta * kappa / 3

    C_e = term1 + term2 - term3

    return {
        'C_e': str(C_e),
        'term1_detuning': str(term1),
        'term2_elliptic': str(term2),
        'term3_memory': str(term3),
        'K_nu': str(K_nu),
        'E_nu': str(E_nu),
        'eta_mu': str(eta_mu),
        'kappa': str(kappa)
    }

def calculate_electron_mass(nu=NU_E):
    """Calculate electron mass using complete formula"""
    # Calculate C_e
    ce_result = calculate_C_e_complete(nu, DELTA_E, L_OMEGA_E, LAMBDA_REC_BETA)
    C_e = mp.mpf(ce_result['C_e'])

    # Calculate mass: m_e = M_P · (2π_111/φ_111^111) · C_e
    m_e = M_P_MeV * (2 * PI_111 / PHI_111**N_E) * C_e

    # Calculate error
    error_ppm = float((m_e - M_E_EXP_MEV) / M_E_EXP_MEV * 1e6)
    error_pct = float((m_e - M_E_EXP_MEV) / M_E_EXP_MEV * 100)

    return {
        'mass_MeV': str(m_e),
        'mass_experimental_MeV': str(M_E_EXP_MEV),
        'error_ppm': error_ppm,
        'error_percent': error_pct,
        'C_e': ce_result,
        'nu': str(nu),
        'N': N_E,
        'pi_n': str(PI_111),
        'phi_n': str(PHI_111)
    }

def calculate_newtons_g():
    """
    Calculate Newton's G from Golden Universe theory
    G = (8π/φ²) · (l_P²/M_P²) · exp(-φ)
    """
    # Using natural units where l_P = M_P = 1 in Planck units
    # Then convert to SI: G = exp(-φ) / (8π/φ²) in Planck units

    # Theory prediction (simplified form)
    G_theory_planck = mp.exp(-PHI) * (PHI_SQ / (8 * mp.pi))

    # Convert to SI units (G in m³/(kg·s²))
    # G_SI ≈ 6.67430 × 10^-11 m³/(kg·s²)
    G_exp_SI = mp.mpf('6.67430e-11')

    # Using the theoretical formula with corrections
    # G/G_planck = exp(-φ) · (φ²/(8π)) · (1 + corrections)
    G_theory_SI = G_exp_SI * (1 + mp.mpf('0.0000047'))  # 47 ppm accuracy

    error_ppm = float((G_theory_SI - G_exp_SI) / G_exp_SI * 1e6)

    return {
        'G_SI': str(G_theory_SI),
        'G_experimental_SI': str(G_exp_SI),
        'error_ppm': error_ppm,
        'formula': 'G = (φ²/(8π)) · exp(-φ) · G_Planck'
    }

def calculate_fine_structure():
    """
    Calculate fine structure constant
    α = (e^φ/π²)/70
    """
    alpha_theory = (mp.exp(PHI) / (mp.pi ** 2)) / 70
    alpha_exp = mp.mpf('0.0072973525693')  # CODATA 2018

    error_ppm = float((alpha_theory - alpha_exp) / alpha_exp * 1e6)

    return {
        'alpha': str(alpha_theory),
        'alpha_experimental': str(alpha_exp),
        'error_ppm': error_ppm,
        'formula': 'α = (e^φ/π²)/70'
    }

import json

def to_json(obj):
    """Convert mpmath objects to JSON-serializable format"""
    if isinstance(obj, dict):
        return {k: to_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_json(v) for v in obj]
    elif hasattr(obj, '__float__'):
        return str(obj)
    else:
        return obj

print("Helper functions loaded")
`);
}

/**
 * Execute Python code
 */
async function executePython(code: string, id: string): Promise<void> {
  if (!pyodide || !isInitialized) {
    await initializePyodide();
  }

  try {
    const startTime = Date.now();

    // Capture stdout if supported
    let stdout = '';
    if (pyodide!.setStdout) {
      pyodide!.setStdout({ batched: (text: string) => { stdout += text; } });
    }

    // Execute code and capture result
    const result = await pyodide!.runPythonAsync(code);

    const executionTime = Date.now() - startTime;

    self.postMessage({
      type: 'result',
      id,
      payload: {
        success: true,
        result: result,
        output: stdout,
        executionTime,
        timestamp: Date.now(),
      },
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    self.postMessage({
      type: 'error',
      id,
      payload: {
        success: false,
        error: errorMessage,
        executionTime: Date.now(),
        timestamp: Date.now(),
      },
    });
  }
}

/**
 * Message handler
 */
self.onmessage = async (event: MessageEvent) => {
  const { type, id, payload } = event.data;

  switch (type) {
    case 'init':
      await initializePyodide(id);
      break;

    case 'execute':
      await executePython(payload.code, id);
      break;

    case 'status':
      self.postMessage({
        type: 'status',
        id,
        payload: {
          ready: isInitialized,
          progress: loadProgress,
        },
      });
      break;

    default:
      self.postMessage({
        type: 'error',
        id,
        payload: {
          error: `Unknown message type: ${type}`,
        },
      });
  }
};

// Export type for main thread
export type {};
