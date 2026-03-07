/**
 * ParticleMassCalculator - Dedicated UI for particle mass calculations
 * Shows formula breakdown, comparison with CODATA, and precision metrics
 */

import React, { useState } from 'react';
import { GoldenUniverseCalculator, type CalculationResult } from '../../calculations/goldenUniverseCalculator';
import './ParticleMassCalculator.scss';

type ParticleType = 'electron' | 'muon' | 'tau' | 'proton';

export const ParticleMassCalculatorUI: React.FC = () => {
  const [selectedParticle, setSelectedParticle] = useState<ParticleType>('electron');
  const [result, setResult] = useState<CalculationResult | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [showBreakdown, setShowBreakdown] = useState(true);

  const particles: Array<{ id: ParticleType; name: string; symbol: string }> = [
    { id: 'electron', name: 'Electron', symbol: 'e⁻' },
    { id: 'muon', name: 'Muon', symbol: 'μ⁻' },
    { id: 'tau', name: 'Tau', symbol: 'τ⁻' },
    { id: 'proton', name: 'Proton', symbol: 'p⁺' },
  ];

  const handleCalculate = () => {
    setIsCalculating(true);
    setResult(null);

    // Simulate async calculation with setTimeout
    setTimeout(() => {
      try {
        let calcResult: CalculationResult;

        switch (selectedParticle) {
          case 'electron':
            calcResult = GoldenUniverseCalculator.electron();
            break;
          case 'muon':
            calcResult = GoldenUniverseCalculator.muon();
            break;
          case 'tau':
            calcResult = GoldenUniverseCalculator.tau();
            break;
          case 'proton':
            calcResult = GoldenUniverseCalculator.proton();
            break;
          default:
            calcResult = GoldenUniverseCalculator.electron();
        }

        setResult(calcResult);
      } catch (error) {
        console.error('Calculation failed:', error);
      } finally {
        setIsCalculating(false);
      }
    }, 500); // Small delay to show loading state
  };

  const formatPrecision = (ppm: number): string => {
    const absValue = Math.abs(ppm);
    if (absValue < 1) return `${absValue.toFixed(3)} ppm (excellent)`;
    if (absValue < 10) return `${absValue.toFixed(2)} ppm (very good)`;
    if (absValue < 100) return `${absValue.toFixed(1)} ppm (good)`;
    return `${absValue.toFixed(0)} ppm`;
  };

  const getMatchQuality = (ppm: number): string => {
    const absValue = Math.abs(ppm);
    if (absValue < 1) return 'excellent';
    if (absValue < 10) return 'very-good';
    if (absValue < 100) return 'good';
    return 'fair';
  };

  return (
    <div className="particle-mass-calculator">
      <div className="calculator-header">
        <h2>Particle Mass Calculator</h2>
        <p className="subtitle">
          Calculate particle masses from Golden Universe theory with high precision
        </p>
      </div>

      {/* Particle Selection */}
      <div className="particle-selection">
        {particles.map(particle => (
          <button
            key={particle.id}
            className={`particle-btn ${selectedParticle === particle.id ? 'selected' : ''}`}
            onClick={() => setSelectedParticle(particle.id)}
            disabled={isCalculating}
          >
            <div className="particle-symbol">{particle.symbol}</div>
            <div className="particle-name">{particle.name}</div>
          </button>
        ))}
      </div>

      {/* Calculate Button */}
      <button
        className="calculate-btn"
        onClick={handleCalculate}
        disabled={isCalculating}
      >
        {isCalculating ? 'Calculating...' : `Calculate ${particles.find(p => p.id === selectedParticle)?.name} Mass`}
      </button>

      {/* Results */}
      {result && (
        <div className="results-container">
          {/* Mass Comparison */}
          <div className="result-card mass-comparison">
            <h3>Mass Comparison</h3>
            <div className="comparison-grid">
              <div className="comparison-item">
                <div className="label">Theoretical</div>
                <div className="value">{result.theoretical_MeV.toFixed(8)} MeV/c²</div>
              </div>
              <div className="comparison-item">
                <div className="label">Experimental (CODATA)</div>
                <div className="value">
                  {result.experimental_MeV.toFixed(8)} MeV/c²
                </div>
              </div>
              <div className={`comparison-item precision ${getMatchQuality(result.error_ppm)}`}>
                <div className="label">Error</div>
                <div className="value">
                  {formatPrecision(result.error_ppm)}
                </div>
              </div>
            </div>
          </div>

          {/* Components Information */}
          {result.epoch && (
            <div className="result-card epoch-info">
              <h3>Epoch Parameters</h3>
              <div className="param-grid">
                <div className="param-item">
                  <span className="param-label">Epoch N:</span>
                  <span className="param-value">{result.epoch.N || 'N/A'}</span>
                </div>
                <div className="param-item">
                  <span className="param-label">Resonance k:</span>
                  <span className="param-value">{result.epoch.k_res || 'N/A'}</span>
                </div>
                <div className="param-item">
                  <span className="param-label">Detuning δ:</span>
                  <span className="param-value">
                    {result.epoch.delta ? parseFloat(String(result.epoch.delta)).toFixed(6) : 'N/A'}
                  </span>
                </div>
                <div className="param-item">
                  <span className="param-label">π₁₁₁:</span>
                  <span className="param-value">
                    {result.epoch.pi_n ? parseFloat(String(result.epoch.pi_n)).toFixed(8) : 'N/A'}
                  </span>
                </div>
                <div className="param-item">
                  <span className="param-label">φ₁₁₁:</span>
                  <span className="param-value">
                    {result.epoch.phi_n ? parseFloat(String(result.epoch.phi_n)).toFixed(8) : 'N/A'}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Winding Numbers */}
          {result.winding && (
            <div className="result-card winding-info">
              <h3>Winding Numbers</h3>
              <div className="winding-display">
                <div className="winding-pair">
                  <span className="winding-label">(p, q) =</span>
                  <span className="winding-value">
                    ({result.winding.p}, {result.winding.q})
                  </span>
                </div>
                <div className="winding-length">
                  <span className="winding-label">l_Ω =</span>
                  <span className="winding-value">
                    {parseFloat(String(result.winding.l_Omega)).toFixed(6)}
                  </span>
                </div>
                <div className="winding-constraint">
                  Constraint: |p| + |q| = {Math.abs(result.winding.p) + Math.abs(result.winding.q)}
                </div>
              </div>
            </div>
          )}

          {/* Coupling Breakdown */}
          {result.coupling && showBreakdown && (
            <div className="result-card coupling-breakdown">
              <h3>
                Coupling C_e Formula Breakdown
                <button
                  className="toggle-btn"
                  onClick={() => setShowBreakdown(!showBreakdown)}
                >
                  {showBreakdown ? '▼' : '▶'}
                </button>
              </h3>

              {showBreakdown && (
                <>
                  <div className="formula-display">
                    <code>C_e(ν) = |δ|·K(ν) + η_μ·(ν/2) - (λ_rec/β)·κ/3</code>
                  </div>

                  <div className="component-list">
                    <div className="component-item">
                      <div className="component-name">Term 1: Detuning Stress</div>
                      <div className="component-formula">|δ|·K(ν)</div>
                      <div className="component-value">
                        {result.coupling.components?.detuning
                          ? parseFloat(String(result.coupling.components.detuning)).toFixed(10)
                          : 'N/A'}
                      </div>
                    </div>

                    <div className="component-item">
                      <div className="component-name">Term 2: Elliptic Minimizer</div>
                      <div className="component-formula">η_μ·(ν/2)</div>
                      <div className="component-value">
                        {result.coupling.components?.elliptic
                          ? parseFloat(String(result.coupling.components.elliptic)).toFixed(10)
                          : 'N/A'}
                      </div>
                    </div>

                    <div className="component-item memory">
                      <div className="component-name">Term 3: Memory Binding</div>
                      <div className="component-formula">-(λ_rec/β)·κ/3</div>
                      <div className="component-value">
                        {result.coupling.components?.memory
                          ? parseFloat(String(result.coupling.components.memory)).toFixed(10)
                          : 'N/A'}
                      </div>
                    </div>

                    <div className="component-item total">
                      <div className="component-name">Total C_e</div>
                      <div className="component-formula"></div>
                      <div className="component-value">
                        {parseFloat(String(result.coupling.C_value)).toFixed(10)}
                      </div>
                    </div>
                  </div>

                  <div className="param-grid">
                    <div className="param-item">
                      <span className="param-label">Optimal ν:</span>
                      <span className="param-value">
                        {parseFloat(String(result.coupling.nu_optimal)).toFixed(8)}
                      </span>
                    </div>
                    <div className="param-item">
                      <span className="param-label">λ_rec/β:</span>
                      <span className="param-value">
                        {result.coupling.components
                          ? '0.51097951...'
                          : 'N/A'}
                      </span>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}

          {/* Final Formula */}
          <div className="result-card final-formula">
            <h3>Complete Formula</h3>
            <div className="formula-box">
              <code>
                m<sub>{selectedParticle.substring(0, 1)}</sub> = M<sub>P</sub> ·
                (2π₁₁₁/φ₁₁₁<sup>111</sup>) · C<sub>e</sub>(ν)
              </code>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
