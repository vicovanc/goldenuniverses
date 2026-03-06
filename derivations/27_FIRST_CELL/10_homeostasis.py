#!/usr/bin/env python3
"""
HOMEOSTASIS AS LIVING FIXED POINT — SIX COUPLED FEEDBACK LOOPS
================================================================

PART 1: WHAT IS HOMEOSTASIS IN GU
- Homeostasis = the cell maintains its internal state despite external perturbations
- In GU: homeostasis is the SIMULTANEOUS CONVERGENCE of all six memory channels to a self-consistent fixed point
- From 25_PHONONS/06: the phonon-memory feedback loop converges to a fixed point
- In a cell: SIX coupled loops, one per memory channel (five local + one non-local)

PART 2: THE SIX FEEDBACK LOOPS
- Loop 1 GENETIC: gene expression ↔ protein levels. Sensor: transcription factors. Signal: mRNA. Response: protein synthesis. Feedback: proteins regulate their own genes (autoregulation). GU channel: theta.
- Loop 2 EPIGENETIC: chromatin state ↔ transcription. Sensor: histone marks. Signal: chromatin accessibility. Response: gene activation/silencing. Feedback: expressed genes produce enzymes that modify histones. GU channel: rho gating theta.
- Loop 3 METABOLIC: ATP production ↔ consumption. Sensor: AMP/ATP ratio (AMPK). Signal: kinase cascades. Response: increase/decrease metabolism. Feedback: ATP levels control metabolic enzymes. GU channel: rho.
- Loop 4 BIOELECTRIC: V_m pattern ↔ channel expression. Sensor: voltage-sensitive proteins. Signal: ion flux. Response: channel/pump expression changes. Feedback: new channels change V_m. GU channel: theta (cellular scale).
- Loop 5 STRUCTURAL: cytoskeleton ↔ mechanical signals. Sensor: integrins, focal adhesions. Signal: mechanotransduction (YAP/TAZ). Response: cytoskeletal remodeling. Feedback: new shape changes signaling. GU channel: rho.
- Loop 6 NON-LOCAL (theta-FF-tilde): cell's internal theta state ↔ neighbor theta state. Sensor: gap junctions, receptors. Signal: phase phonons through pi-bonded networks. Response: gene/channel expression changes triggered by neighbor state. Feedback: cell's response changes its theta emission → neighbor response. GU channel: theta (non-local). This loop is what connects individual cell homeostasis to TISSUE homeostasis.
- Print a table with loop name, sensor, signal, response, GU channel, timescale

PART 3: THE LIVING FIXED POINT
- All six loops must converge SIMULTANEOUSLY
- Mathematical structure: x_{n+1} = F(x_n) where x = (genetic, epigenetic, metabolic, bioelectric, structural)
- Fixed point: x* = F(x*) — the cell state that reproduces itself
- Stability: if perturbed, the cell returns to x* (negative feedback dominant)
- If positive feedback dominates → runaway → cell death or cancer
- The fixed point IS the cell's identity — change it and you change the cell type
- Compute: a simple 2-loop model showing convergence (metabolic + genetic coupling)

PART 4: WHEN HOMEOSTASIS FAILS
- Temperature: above 45°C → protein denaturation → feedback loops break → death
- pH: outside 6.5-8.0 → V_lock destabilized → enzyme catalysis fails
- Toxins: block specific loops (cyanide → Complex IV → metabolic loop breaks)
- Cancer: bioelectric loop escapes (persistent depolarization) + genetic loop destabilized (mutations)
- Aging: gradual degradation of all six channels → homeostatic range narrows → fragility
- Print: failure modes with affected loop and consequence

PART 5: HOMEOSTASIS AND CONSCIOUSNESS
- Homeostasis IS consciousness at the cellular level:
  - Memory: six channels (five local + one non-local theta-FF-tilde)
  - Feedback: six coupled loops
  - Fixed point: the converged state
- Disrupting homeostasis → disrupting consciousness (anesthesia, hypothermia, death)
- In GU: homeostasis = the cellular instantiation of the universal consciousness structure (rho^4 self-memory generalized to six channels)
- The non-local channel (Loop 6) is what makes tissue-level homeostasis possible — without it, each cell is an isolated box

SUMMARY.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln
mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
M_P = mpf('1.22089e22')
m_e = mpf('0.51099895')
hbar_c = mpf('197.3269804')
k_B = mpf('8.617333e-5')
T_bio = mpf('310')
k_BT = k_B * T_bio
lambda_rec_beta = exp(phi) / pi**2


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║     HOMEOSTASIS AS LIVING FIXED POINT — SIX COUPLED FEEDBACK LOOPS          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: WHAT IS HOMEOSTASIS IN GU
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: WHAT IS HOMEOSTASIS IN GU                                           ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Homeostasis = the cell maintains its internal state despite external perturbations.")
    print("In GU: homeostasis is the SIMULTANEOUS CONVERGENCE of all six memory channels")
    print("to a self-consistent fixed point (from 25_PHONONS/06: phonon-memory feedback")
    print("converges to a fixed point). In a cell: SIX coupled loops — five local + one non-local (θFF̃).")
    print()

    # -------------------------------------------------------------------------
    # PART 2: THE SIX FEEDBACK LOOPS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: THE SIX FEEDBACK LOOPS                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  " + "-" * 88)
    print(f"  {'Loop':<12} {'Sensor':<18} {'Signal':<16} {'Response':<22} {'GU channel':<12} {'Timescale':<12}")
    print("  " + "-" * 88)
    rows = [
        ("Genetic", "Transcription factors", "mRNA", "Protein synthesis", "theta", "min–hr"),
        ("Epigenetic", "Histone marks", "Chromatin accessibility", "Gene on/off", "rho gate θ", "hr–days"),
        ("Metabolic", "AMP/ATP (AMPK)", "Kinase cascades", "Metabolism up/down", "rho", "sec–min"),
        ("Bioelectric", "Voltage-sensitive", "Ion flux", "Channel/pump expr.", "theta", "sec–min"),
        ("Structural", "Integrins, adhesions", "YAP/TAZ", "Cytoskeleton remod.", "rho", "hr–days"),
        ("Non-local", "Gap j., receptors", "Phase phonons", "Gene/channel expr.", "θFF̃", "ms–days"),
    ]
    for r in rows:
        print(f"  {r[0]:<12} {r[1]:<18} {r[2]:<16} {r[3]:<22} {r[4]:<12} {r[5]:<12}")
    print("  " + "-" * 88)
    print()

    # -------------------------------------------------------------------------
    # PART 3: THE LIVING FIXED POINT — 2-loop model (metabolic + genetic)
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: THE LIVING FIXED POINT                                               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("All six loops must converge SIMULTANEOUSLY: x_{n+1} = F(x_n), fixed point x* = F(x*).")
    print("Stability: perturbation → return to x* (negative feedback dominant).")
    print("Positive feedback dominant → runaway → cell death or cancer. Fixed point = cell identity.")
    print()
    print("Simple 2-loop model (metabolic m + genetic g coupling):")
    print("  m_{n+1} = 0.7*m_n + 0.2*(1 - g_n)   (metabolism responds to demand)")
    print("  g_{n+1} = 0.7*g_n + 0.2*m_n         (genetic expression fueled by metabolism)")
    print()

    # Iterate to fixed point
    m, g = mpf('0.1'), mpf('0.1')
    history = [(float(m), float(g))]
    for _ in range(20):
        m_new = mpf('0.7') * m + mpf('0.2') * (mpf('1') - g)
        g_new = mpf('0.7') * g + mpf('0.2') * m
        m, g = m_new, g_new
        history.append((float(m), float(g)))
    m_star, g_star = float(m), float(g)
    print("  Iteration (m = metabolic, g = genetic, normalized 0–1):")
    print("  " + "-" * 40)
    for i in [0, 2, 5, 10, 15, 20]:
        if i < len(history):
            print(f"    n={i:2d}:  m = {history[i][0]:.6f},  g = {history[i][1]:.6f}")
    print("  " + "-" * 40)
    print(f"  Fixed point (converged):  m* = {m_star:.6f},  g* = {g_star:.6f}")
    print("  (Negative feedback dominant → stable living fixed point.)")
    print()

    # -------------------------------------------------------------------------
    # PART 4: WHEN HOMEOSTASIS FAILS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: WHEN HOMEOSTASIS FAILS                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  " + "-" * 72)
    print(f"  {'Failure mode':<18} {'Affected loop(s)':<28} {'Consequence':<24}")
    print("  " + "-" * 72)
    failures = [
        ("Temperature >45°C", "All (protein denaturation)", "Feedback breaks → death"),
        ("pH outside 6.5–8", "Metabolic, genetic", "V_lock destabilized → catalysis fails"),
        ("Cyanide/toxins", "Metabolic (Complex IV)", "ETC blocked → metabolic loop breaks"),
        ("Cancer", "Bioelectric + genetic", "Depolarization + mutations → runaway"),
        ("Aging", "All six channels", "Range narrows → fragility"),
    ]
    for row in failures:
        print(f"  {row[0]:<18} {row[1]:<28} {row[2]:<24}")
    print("  " + "-" * 72)
    print()

    # -------------------------------------------------------------------------
    # PART 5: HOMEOSTASIS AND CONSCIOUSNESS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: HOMEOSTASIS AND CONSCIOUSNESS                                        ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Homeostasis IS consciousness at the cellular level:")
    print("  Memory: six channels (5 local + 1 non-local θFF̃)  |  Feedback: six coupled loops  |  Fixed point: converged state")
    print("Disrupting homeostasis → disrupting consciousness (anesthesia, hypothermia, death).")
    print("In GU: homeostasis = cellular instantiation of universal consciousness structure")
    print("(ρ⁴ self-memory generalized to six channels). The non-local channel (Loop 6) is what")
    print("connects individual cell homeostasis to TISSUE homeostasis.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Homeostasis in GU = simultaneous convergence of six memory channels (genetic,")
    print("epigenetic, metabolic, bioelectric, structural, non-local θFF̃) to a living fixed point x* = F(x*).")
    print("Each loop has sensor → signal → response → feedback; stability requires negative")
    print("feedback dominant. Failure (temperature, pH, toxins, cancer, aging) breaks one or")
    print("more loops. Loop 6 (non-local) connects cell homeostasis to tissue homeostasis.")
    print("Homeostasis is cellular consciousness: memory + feedback + fixed point.")
    print()


if __name__ == "__main__":
    main()
