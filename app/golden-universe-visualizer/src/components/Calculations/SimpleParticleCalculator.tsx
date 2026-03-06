/**
 * Simple Particle Mass Calculator with working calculations
 */

import React, { useState } from 'react';
import { GoldenUniverseCalculator, type CalculationResult } from '../../calculations/goldenUniverseCalculator';
import './ParticleMassCalculator.scss';

type ParticleType = 'electron' | 'muon' | 'tau' | 'proton' | 'neutron';

export const SimpleParticleCalculator: React.FC = () => {
  const [selectedParticle, setSelectedParticle] = useState<ParticleType>('electron');
  const [result, setResult] = useState<CalculationResult | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);

  const particles: Array<{ id: ParticleType; name: string; symbol: string }> = [
    { id: 'electron', name: 'Electron', symbol: 'e⁻' },
    { id: 'muon', name: 'Muon', symbol: 'μ⁻' },
    { id: 'tau', name: 'Tau', symbol: 'τ⁻' },
    { id: 'proton', name: 'Proton', symbol: 'p⁺' },
    { id: 'neutron', name: 'Neutron', symbol: 'n⁰' },
  ];

  const handleCalculate = () => {
    setIsCalculating(true);

    // Simulate async with small delay for UX
    setTimeout(() => {
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
        case 'neutron':
          calcResult = GoldenUniverseCalculator.neutron();
          break;
        default:
          calcResult = GoldenUniverseCalculator.electron();
      }

      setResult(calcResult);
      setIsCalculating(false);
    }, 300);
  };

  const formatError = (ppm: number): string => {
    const abs = Math.abs(ppm);
    if (abs < 1) return `${abs.toFixed(3)} ppm`;
    if (abs < 10) return `${abs.toFixed(2)} ppm`;
    if (abs < 100) return `${abs.toFixed(1)} ppm`;
    return `${abs.toFixed(0)} ppm`;
  };

  const getErrorClass = (ppm: number): string => {
    const abs = Math.abs(ppm);
    if (abs < 1) return 'excellent';
    if (abs < 10) return 'very-good';
    if (abs < 100) return 'good';
    return 'fair';
  };

  return (
    <div className="particle-mass-calculator">
      <div className="calculator-header">
        <h2>Particle Mass Calculator</h2>
        <p className="subtitle">
          Real-time Golden Universe Theory calculations with high precision
        </p>
      </div>

      {/* Particle Selection */}
      <div className="particle-selection">
        {particles.map(particle => (
          <button
            key={particle.id}
            className={`particle-btn ${selectedParticle === particle.id ? 'selected' : ''}`}
            onClick={() => {
              setSelectedParticle(particle.id);
              setResult(null);
            }}
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
        {isCalculating ? (
          <>Calculating...</>
        ) : (
          <>Calculate {particles.find(p => p.id === selectedParticle)?.name} Mass</>
        )}
      </button>

      {/* Results */}
      {result && (
        <div className="results-container">
          {/* Mass Comparison */}
          <div className="result-card mass-comparison">
            <h3>Mass Calculation Results</h3>
            <div className="comparison-grid">
              <div className="comparison-item">
                <div className="label">Theoretical (GU)</div>
                <div className="value">{result.theoretical_MeV.toFixed(8)} MeV/c²</div>
              </div>
              <div className="comparison-item">
                <div className="label">Experimental (CODATA)</div>
                <div className="value">{result.experimental_MeV.toFixed(8)} MeV/c²</div>
              </div>
              <div className={`comparison-item precision ${getErrorClass(result.error_ppm)}`}>
                <div className="label">Precision</div>
                <div className="value">{formatError(result.error_ppm)}</div>
              </div>
            </div>
          </div>

          {/* Formula Display */}
          <div className="result-card final-formula">
            <h3>Formula Used</h3>
            <div className="formula-box">
              <code>{result.formula}</code>
            </div>
          </div>

          {/* Component Details */}
          {result.components && (
            <div className="result-card">
              <h3>Calculation Components</h3>
              <div className="param-grid">
                {Object.entries(result.components).map(([key, value]) => {
                  // Skip complex objects
                  if (typeof value === 'object') return null;

                  // Format key for display
                  const displayKey = key.replace(/_/g, ' ').replace(/([A-Z])/g, ' $1').trim();
                  const capitalizedKey = displayKey.charAt(0).toUpperCase() + displayKey.slice(1);

                  // Format value based on type
                  let displayValue: string;
                  if (typeof value === 'number') {
                    displayValue = value > 1000 ? value.toFixed(0) :
                                  value > 1 ? value.toFixed(3) :
                                  value.toFixed(6);
                  } else {
                    displayValue = String(value);
                  }

                  return (
                    <div key={key} className="param-item">
                      <span className="param-label">{capitalizedKey}:</span>
                      <span className="param-value">{displayValue}</span>
                    </div>
                  );
                }).filter(Boolean)}
              </div>
            </div>
          )}

          {/* Key Constants */}
          <div className="result-card">
            <h3>Fundamental Constants Used</h3>
            <div className="param-grid">
              <div className="param-item">
                <span className="param-label">φ (Golden Ratio):</span>
                <span className="param-value">1.618033988...</span>
              </div>
              <div className="param-item">
                <span className="param-label">π (Pi):</span>
                <span className="param-value">3.141592653...</span>
              </div>
              <div className="param-item">
                <span className="param-label">e (Euler's):</span>
                <span className="param-value">2.718281828...</span>
              </div>
              <div className="param-item">
                <span className="param-label">α (Fine Structure):</span>
                <span className="param-value">1/137.036</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="info-box" style={{ marginTop: '2rem', padding: '1rem', background: 'var(--bg-subtle)', borderRadius: '8px' }}>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', margin: 0 }}>
          <strong>Note:</strong> These calculations use the Golden Universe Theory framework,
          deriving particle masses from three fundamental constants (π, φ, e) with remarkable precision.
          The electron mass calculation achieves 23 ppm accuracy, demonstrating the theory's predictive power.
        </p>
      </div>
    </div>
  );
};

export default SimpleParticleCalculator;